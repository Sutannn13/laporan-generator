# /// script
# requires-python = ">=3.10"
# dependencies = ["python-docx"]
# ///
"""
Unified SINTA 1-6 Journal Catalog (16,617 Journals) & GARUDA Reference MCP Server + CLI.
Provides:
1. Local O(1) lookup and search across 16,617 SINTA 1-6 accredited Indonesian journals
   (snapshot 2026-11-15 + Scopus/Garuda/H5 metrics, zero HTTP 403 risk).
2. Live article search via Garba Rujukan Digital (https://garuda.kemdiktisaintek.go.id)
   automatically cross-referenced against the SINTA 1-6 catalog.
3. End-to-end R1-R4 reference discovery (Garuda + Crossref API, 2022-2026 recency window,
   SINTA 1-6 verification, and Mendeley .txt/.docx dossier export).
4. Dual execution mode: STDIO Model Context Protocol server (--mcp) and standalone CLI.
"""
import argparse
from datetime import datetime
import gzip
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT_DIR = os.path.dirname(_THIS_DIR)
for _cand in (_THIS_DIR, _PARENT_DIR):
    if _cand not in sys.path:
        sys.path.insert(0, _cand)

GARUDA_BASE_URL = "https://garuda.kemdiktisaintek.go.id"
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", re.IGNORECASE)
ISSN_TOKEN_RE = re.compile(r"^\d{4}-?\d{3}[\dXx]$")
YEAR_PAREN_RE = re.compile(r"\((19\d\d|20\d\d)\)")
YEAR_ANY_RE = re.compile(r"\b(19\d\d|20\d\d)\b")
VOL_SUFFIX_RE = re.compile(
    r"\s+(?:vol(?:ume)?\.?\s*\d+|no\.?\s*\d+|edisi\s+|issue\s+\d+|\(\d{4}\)).*$",
    re.IGNORECASE,
)

_CATALOG_STATE = None


def norm_issn(val):
    """Normalize a strict ISSN token (XXXX-XXXX or XXXXXXXX) into XXXX-XXXX uppercase format."""
    raw = str(val or "").strip()
    if not ISSN_TOKEN_RE.match(raw):
        return ""
    s = raw.replace("-", "").upper()
    return f"{s[:4]}-{s[4:8]}"


def norm_title(val):
    """Normalize journal title for fuzzy/exact matching."""
    s = html.unescape(str(val or "")).lower().strip()
    s = VOL_SUFFIX_RE.sub("", s)
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _find_catalog_path():
    candidates = [
        os.path.join(_PARENT_DIR, "presets", "sinta-catalog.json.gz"),
        os.path.join(_THIS_DIR, "presets", "sinta-catalog.json.gz"),
        os.path.join(_PARENT_DIR, ".agents", "skills", "laporan-generator", "presets", "sinta-catalog.json.gz"),
        os.path.join(
            os.path.expanduser("~"),
            ".gemini",
            "config",
            "skills",
            "laporan-generator",
            "presets",
            "sinta-catalog.json.gz",
        ),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("sinta-catalog.json.gz not found in presets/ or skill bundle.")


def load_sinta_catalog():
    """Load and index 16,617 SINTA 1-6 journals in memory (singleton)."""
    global _CATALOG_STATE
    if _CATALOG_STATE is not None:
        return _CATALOG_STATE

    cat_path = _find_catalog_path()
    with gzip.open(cat_path, "rt", encoding="utf-8") as gz:
        raw = json.load(gz)

    journals = raw.get("journals", [])
    by_issn = {}
    by_title = {}
    by_short = {}
    by_doi_prefix = {}
    by_id = {}

    for j in journals:
        jid = str(j.get("id") or "").strip()
        if jid:
            by_id[jid] = j
        for k in ("p_issn", "e_issn", "alt_issn"):
            ni = norm_issn(j.get(k))
            if ni:
                by_issn[ni] = j
        nt = norm_title(j.get("title"))
        if nt:
            by_title[nt] = j
            # Also index title without parenthetical suffix e.g. "Jurnal X (Journal of X)"
            raw_t = str(j.get("title") or "")
            if "(" in raw_t:
                base_nt = norm_title(raw_t.split("(", 1)[0])
                if len(base_nt) >= 5 and base_nt not in by_title:
                    by_title[base_nt] = j
        sh = str(j.get("short_name") or "").strip().lower()
        if sh:
            by_short[sh] = j
        dp = str(j.get("doi_prefix") or "").strip().lower()
        if dp:
            by_doi_prefix[dp] = j

    _CATALOG_STATE = {
        "as_of": raw.get("as_of", "2026-11-15"),
        "total": len(journals),
        "path": cat_path,
        "journals": journals,
        "by_issn": by_issn,
        "by_title": by_title,
        "by_short": by_short,
        "by_doi_prefix": by_doi_prefix,
        "by_id": by_id,
    }
    return _CATALOG_STATE


def format_journal_entry(j):
    """Format a catalog journal entry with canonical R3 verification label."""
    if not j:
        return None
    rank = int(j.get("rank") or 0)
    return {
        "id": j.get("id", ""),
        "title": j.get("title", ""),
        "short_name": j.get("short_name", ""),
        "sinta_rank": rank,
        "sinta_verified": rank in (1, 2, 3, 4, 5, 6),
        "r3_label": (
            f"[Peringkat: SINTA {rank} - Terverifikasi]"
            if rank in (1, 2, 3, 4, 5, 6)
            else "[Level SINTA: tidak terverifikasi]"
        ),
        "p_issn": j.get("p_issn", ""),
        "e_issn": j.get("e_issn", ""),
        "doi_prefix": j.get("doi_prefix", ""),
        "affiliation": j.get("affiliation", ""),
        "subject": j.get("subject", ""),
        "sinta_url": j.get("sinta_url", ""),
        "website_url": j.get("website_url", ""),
        "scopus_indexed": bool(j.get("scopus")),
        "garuda_indexed": bool(j.get("garuda")),
        "h5_index": j.get("h5", ""),
        "impact": j.get("impact", ""),
    }


def match_sinta_journal(issn="", title="", doi="", sinta_id=""):
    """Match a journal against the 16,617 SINTA 1-6 catalog by ID, ISSN, DOI prefix, or title."""
    state = load_sinta_catalog()

    if sinta_id:
        sid = str(sinta_id).strip()
        if sid in state["by_id"]:
            return format_journal_entry(state["by_id"][sid])

    if issn:
        for part in re.split(r"[,;\s/|]+", str(issn)):
            ni = norm_issn(part)
            if ni and ni in state["by_issn"]:
                return format_journal_entry(state["by_issn"][ni])

    if doi:
        d_clean = str(doi).lower().replace("https://doi.org/", "").strip()
        for dp, j in state["by_doi_prefix"].items():
            if d_clean.startswith(dp.lower()):
                return format_journal_entry(j)

    if title:
        raw_t = str(title).strip()
        sh_cand = raw_t.lower()
        if sh_cand in state["by_short"]:
            return format_journal_entry(state["by_short"][sh_cand])

        nt = norm_title(raw_t)
        if nt in state["by_title"]:
            return format_journal_entry(state["by_title"][nt])

        # Strip parenthetical or colon subtitle if present
        for sep in ("(", ":"):
            if sep in raw_t:
                sub_nt = norm_title(raw_t.split(sep, 1)[0])
                if len(sub_nt) >= 5 and sub_nt in state["by_title"]:
                    return format_journal_entry(state["by_title"][sub_nt])

    return None


def _parse_rank_filter(sinta_rank):
    if sinta_rank is None or sinta_rank == "":
        return set()
    ranks = set()
    for token in re.split(r"[,;\s]+", str(sinta_rank).upper()):
        t = token.replace("SINTA", "").replace("S", "").strip()
        if t.isdigit() and int(t) in (1, 2, 3, 4, 5, 6):
            ranks.add(int(t))
    return ranks


def sinta_search_journals(
    query="",
    sinta_rank="",
    subject="",
    affiliation="",
    scopus_only=False,
    garuda_only=False,
    limit=20,
):
    """Search across 16,617 SINTA 1-6 journals with rank, subject, and institution filters."""
    state = load_sinta_catalog()
    ranks = _parse_rank_filter(sinta_rank)
    q_norm = norm_title(query) if query else ""
    q_tokens = [tok for tok in q_norm.split() if tok]
    q_issn = norm_issn(query) if query else ""
    subj_q = str(subject or "").strip().lower()
    aff_q = str(affiliation or "").strip().lower()
    lim = max(1, min(int(limit or 20), 100))

    scored = []
    for j in state["journals"]:
        r = int(j.get("rank") or 0)
        if ranks and r not in ranks:
            continue
        if scopus_only and not j.get("scopus"):
            continue
        if garuda_only and not j.get("garuda"):
            continue
        if subj_q and subj_q not in str(j.get("subject") or "").lower():
            continue
        if aff_q and aff_q not in str(j.get("affiliation") or "").lower():
            continue

        score = 0
        if q_tokens or q_issn:
            if q_issn and q_issn in (j.get("p_issn"), j.get("e_issn"), j.get("alt_issn")):
                score = 1000
            else:
                title_low = str(j.get("title") or "").lower()
                short_low = str(j.get("short_name") or "").lower()
                haystack = f"{title_low} {short_low} {j.get('affiliation', '').lower()} {j.get('subject', '').lower()}"
                if not all(tok in haystack for tok in q_tokens):
                    continue
                if q_norm == short_low:
                    score = 900
                elif q_norm == norm_title(title_low):
                    score = 850
                elif title_low.startswith(q_norm):
                    score = 700
                elif all(tok in title_low for tok in q_tokens):
                    score = 500
                else:
                    score = 250

        # Prioritize better SINTA rank and higher H5-index
        h5_val = int(j["h5"]) if str(j.get("h5") or "").isdigit() else 0
        scored.append((score, -r, h5_val, j))

    scored.sort(key=lambda item: (item[0], item[1], item[2]), reverse=True)
    results = [format_journal_entry(item[3]) for item in scored[:lim]]
    return {
        "as_of": state["as_of"],
        "total_catalog_journals": state["total"],
        "total_matches": len(scored),
        "returned": len(results),
        "filters": {
            "query": query,
            "sinta_rank": sorted(ranks) if ranks else "all (S1-S6)",
            "subject": subject,
            "affiliation": affiliation,
            "scopus_only": bool(scopus_only),
            "garuda_only": bool(garuda_only),
        },
        "results": results,
    }


def sinta_lookup_journal(identifier):
    """Look up a single journal by ISSN, DOI, SINTA ID, or journal name."""
    ident = str(identifier or "").strip()
    if not ident:
        return {"found": False, "verified": False, "r3_label": "[Level SINTA: tidak terverifikasi]"}

    matched = (
        match_sinta_journal(issn=ident)
        or match_sinta_journal(doi=ident)
        or match_sinta_journal(sinta_id=ident)
        or match_sinta_journal(title=ident)
    )
    if matched:
        return {"found": True, "verified": True, "journal": matched}

    # Fallback partial search
    search_res = sinta_search_journals(query=ident, limit=5)
    return {
        "found": False,
        "verified": False,
        "r3_label": "[Level SINTA: tidak terverifikasi]",
        "candidates": search_res.get("results", []),
    }


def sinta_stats_summary(subject=""):
    """Return summary counts of SINTA 1-6 journals across accreditation levels."""
    state = load_sinta_catalog()
    subj_q = str(subject or "").strip().lower()
    by_rank = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    scopus_count = 0
    garuda_count = 0
    total = 0

    for j in state["journals"]:
        if subj_q and subj_q not in str(j.get("subject") or "").lower():
            continue
        r = int(j.get("rank") or 0)
        if r in by_rank:
            by_rank[r] += 1
            total += 1
        if j.get("scopus"):
            scopus_count += 1
        if j.get("garuda"):
            garuda_count += 1

    return {
        "as_of": state["as_of"],
        "subject_filter": subject or "all",
        "total_journals": total,
        "by_sinta_rank": {f"SINTA_{k}": v for k, v in sorted(by_rank.items())},
        "scopus_indexed_count": scopus_count,
        "garuda_indexed_count": garuda_count,
    }


def _strip_tags(raw_html):
    text = re.sub(r"<[^>]+>", " ", str(raw_html or ""))
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def _extract_year(text):
    m = YEAR_PAREN_RE.search(str(text or ""))
    if m:
        return int(m.group(1))
    m2 = YEAR_ANY_RE.search(str(text or ""))
    return int(m2.group(1)) if m2 else None


def _parse_garuda_html(raw_html):
    """Parse GARUDA search results HTML using stdlib regex (no bs4/lxml dependency)."""
    total_m = re.search(r"Found\s+([\d,.]+)\s+documents", raw_html, re.IGNORECASE)
    total_docs = int(re.sub(r"[^\d]", "", total_m.group(1))) if total_m else None

    articles = []
    blocks = re.split(r'<div\s+class=["\'][^"\']*article-item[^"\']*["\'][^>]*>', raw_html)[1:]
    for block in blocks:
        t_m = re.search(
            r'<a[^>]+class=["\'][^"\']*title-article[^"\']*["\'][^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
            block,
            re.S | re.I,
        )
        if not t_m:
            t_m = re.search(
                r'<a[^>]+href=["\']([^"\']*?/documents/detail/\d+[^"\']*)["\'][^>]*>(.*?)</a>',
                block,
                re.S | re.I,
            )
        if not t_m:
            continue

        href, raw_title = t_m.group(1), t_m.group(2)
        detail_url = urllib.parse.urljoin(GARUDA_BASE_URL, href.strip())
        id_m = re.search(r"/documents/detail/(\d+)", detail_url)
        garuda_id = id_m.group(1) if id_m else ""
        title = _strip_tags(raw_title)

        authors = [
            _strip_tags(a_txt)
            for a_txt in re.findall(
                r'<a[^>]+class=["\'][^"\']*author-article[^"\']*["\'][^>]*>(.*?)</a>',
                block,
                re.S | re.I,
            )
            if _strip_tags(a_txt)
        ]

        subtitles = [
            _strip_tags(s_txt)
            for s_txt in re.findall(
                r'<xmp[^>]+class=["\'][^"\']*subtitle-article[^"\']*["\'][^>]*>(.*?)</xmp>',
                block,
                re.S | re.I,
            )
        ]
        journal_raw = subtitles[0] if len(subtitles) > 0 else ""
        publisher = subtitles[1] if len(subtitles) > 1 else ""

        abs_m = re.search(
            r'<xmp[^>]+class=["\'][^"\']*abstract-article[^"\']*["\'][^>]*>(.*?)</xmp>',
            block,
            re.S | re.I,
        )
        abstract = _strip_tags(abs_m.group(1)) if abs_m else ""

        doi = ""
        download_original = ""
        full_pdf = ""
        original_source = ""
        for a_href, a_inner in re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', block, re.S | re.I):
            a_text = _strip_tags(a_inner)
            h_clean = html.unescape(a_href).strip()
            if "doi.org/" in h_clean or a_text.upper().startswith("DOI"):
                dm = DOI_RE.search(h_clean) or DOI_RE.search(a_text)
                if dm and not doi:
                    doi = dm.group(0).rstrip(".,;)")
            elif "Download Original" in a_text:
                download_original = h_clean
            elif "Full PDF" in a_text:
                full_pdf = h_clean
            elif "Original Source" in a_text:
                original_source = h_clean

        year = _extract_year(journal_raw) or 0
        clean_journal_name = VOL_SUFFIX_RE.sub("", journal_raw).strip(" ,;-:")
        sinta_info = match_sinta_journal(title=clean_journal_name, doi=doi)
        sinta_rank = sinta_info["sinta_rank"] if sinta_info else None
        sinta_verified = bool(sinta_info and sinta_info.get("sinta_verified"))
        issn_str = ""
        if sinta_info:
            issn_parts = [x for x in (sinta_info.get("p_issn"), sinta_info.get("e_issn")) if x]
            issn_str = ", ".join(issn_parts)

        vol_m = re.search(r"Vol(?:ume)?\.?\s*(\d+)", journal_raw, re.I)
        no_m = re.search(r"No\.?\s*(\d+)", journal_raw, re.I)
        vol_str = vol_m.group(1) if vol_m else ""
        no_str = no_m.group(1) if no_m else ""
        doi_url = f"https://doi.org/{doi}" if doi else ""
        pdf_url = download_original or full_pdf or ""

        auth_str = ", ".join(authors[:3]) + (", et al." if len(authors) > 3 else "") if authors else "Anonim"
        apa_str = (
            f"{auth_str} ({year or '-'}). {title}. {clean_journal_name or journal_raw}"
            f"{f', {vol_str}({no_str})' if vol_str and no_str else (f', {vol_str}' if vol_str else '')}."
            f"{f' {doi_url}' if doi_url else f' {detail_url}'}"
        )
        ieee_str = (
            f'{auth_str}, "{title}," {clean_journal_name or journal_raw}'
            f'{f", vol. {vol_str}" if vol_str else ""}'
            f'{f", no. {no_str}" if no_str else ""}, {year or "-"}'
            f'{f", doi: {doi}." if doi else "."}'
        )

        articles.append(
            {
                "source": "garuda",
                "garuda_id": garuda_id,
                "title": title,
                "authors": authors,
                "year": year,
                "journal": clean_journal_name or journal_raw,
                "journal_raw": journal_raw,
                "publisher": publisher,
                "volume": vol_str,
                "issue": no_str,
                "page": "",
                "issn": issn_str,
                "doi": doi,
                "doi_url": doi_url,
                "pdf_url": pdf_url,
                "detail_url": detail_url,
                "original_source": original_source,
                "sinta_rank": sinta_rank,
                "sinta_verified": sinta_verified,
                "r3_label": (
                    f"[Peringkat: SINTA {sinta_rank} - Terverifikasi]"
                    if sinta_verified
                    else "[Level SINTA: tidak terverifikasi]"
                ),
                "apa": apa_str,
                "ieee": ieee_str,
                "abstract": abstract,
                "relevance": (
                    f"Artikel Garuda terindeks SINTA {sinta_rank} ({clean_journal_name})."
                    if sinta_verified
                    else "Artikel Garba Rujukan Digital (Garuda Kemdiktisaintek)."
                ),
            }
        )

    return {"total_documents": total_docs, "articles": articles}


def garuda_search_articles(
    query,
    search_field="",
    publisher="",
    sinta_rank="",
    year_from=2022,
    year_to=None,
    pdf_only=True,
    limit=15,
    max_pages=2,
):
    """Search Indonesian articles on Garba Rujukan Digital (GARUDA) and enrich with SINTA 1-6 ranks."""
    q_str = str(query or "").strip()
    if len(q_str) < 3:
        raise ValueError("GARUDA query must be at least 3 characters.")

    ranks = _parse_rank_filter(sinta_rank)
    lim = max(1, min(int(limit or 15), 50))
    pages = max(1, min(int(max_pages or 2), 5))
    collected = []
    total_docs = None

    for page in range(1, pages + 1):
        params = {"q": q_str, "page": page}
        if search_field in ("title", "abstract", "author", "doi"):
            params["select"] = search_field
        if publisher:
            params["pub"] = publisher
        if pdf_only:
            params["pdf"] = 1
        if year_from:
            params["from"] = int(year_from)
            if not year_to:
                params["to"] = datetime.now().year
        if year_to:
            params["to"] = int(year_to)

        url = f"{GARUDA_BASE_URL}/documents?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; SintaGarudaMCP/1.0)",
                "Accept": "text/html,application/xhtml+xml",
            },
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw_html = resp.read().decode("utf-8", errors="ignore")

        parsed = _parse_garuda_html(raw_html)
        if total_docs is None:
            total_docs = parsed["total_documents"]

        page_items = parsed["articles"]
        if not page_items:
            break

        for art in page_items:
            if year_from and art.get("year") and int(art["year"]) < int(year_from):
                continue
            if ranks and art.get("sinta_rank") not in ranks:
                continue
            collected.append(art)
            if len(collected) >= lim:
                break

        if len(collected) >= lim:
            break

    return {
        "query": q_str,
        "source": "GARUDA + SINTA 1-6 Local Catalog",
        "total_garuda_matches": total_docs,
        "returned": len(collected),
        "results": collected,
    }


def sinta_find_verified_references(
    query,
    target_sinta=None,
    min_year=2022,
    limit=15,
    source="both",
    check_live=False,
    txt_out="",
    docx_out="",
    no_et_al=False,
    target_doc="",
    title="",
):
    """
    Find R1-R4 compliant candidate references from GARUDA and/or Crossref,
    enrich with verified SINTA 1-6 accreditation from the 16,617 journal catalog,
    and optionally write standalone .txt and .docx Mendeley dossiers.
    """
    try:
        from scripts.verify_sinta_refs import (
            build_dossier_docx,
            export_refs_txt,
            is_within_recency_window,
            query_crossref,
            verify_url_status,
        )
    except ImportError:
        from verify_sinta_refs import (
            build_dossier_docx,
            export_refs_txt,
            is_within_recency_window,
            query_crossref,
            verify_url_status,
        )

    q_clean = str(query or "").strip()
    if not q_clean:
        raise ValueError("Reference search query must not be empty.")

    src_mode = str(source or "both").strip().lower()
    if src_mode not in ("both", "garuda", "crossref"):
        raise ValueError(f"Invalid source {source!r}: must be 'both', 'garuda', or 'crossref'.")

    cur_year = datetime.now().year
    lim = max(1, min(int(limit or 15), 50))
    candidates = []
    seen_keys = set()
    source_errors = {}
    attempted_sources = 0

    if src_mode in ("both", "garuda"):
        attempted_sources += 1
        try:
            g_res = garuda_search_articles(
                query=q_clean,
                year_from=min_year,
                year_to=cur_year,
                pdf_only=True,
                limit=lim,
                max_pages=2,
            )
            for item in g_res.get("results", []):
                yr = int(item.get("year") or 0)
                if not (min_year <= yr <= cur_year and is_within_recency_window(yr, current_year=cur_year)):
                    continue
                key = (item.get("doi") or item.get("title") or "").lower().strip()
                if key and key not in seen_keys:
                    seen_keys.add(key)
                    candidates.append(item)
        except Exception as exc:
            source_errors["garuda"] = str(exc)

    if src_mode in ("both", "crossref"):
        attempted_sources += 1
        try:
            c_rows = query_crossref(q_clean, min_year=min_year, rows=lim * 2)
            for item in c_rows:
                yr = int(item.get("year") or 0)
                if not (min_year <= yr <= cur_year and is_within_recency_window(yr, current_year=cur_year)):
                    continue
                s_info = match_sinta_journal(
                    issn=item.get("issn", ""),
                    title=item.get("journal", ""),
                    doi=item.get("doi", ""),
                )
                if s_info and s_info.get("sinta_verified"):
                    item["sinta_rank"] = s_info["sinta_rank"]
                    item["sinta_verified"] = True
                    item["r3_label"] = s_info["r3_label"]
                    item["relevance"] = (
                        f"Artikel Crossref terindeks SINTA {s_info['sinta_rank']} ({s_info['title']})."
                    )
                else:
                    item["r3_label"] = "[Level SINTA: tidak terverifikasi]"
                key = (item.get("doi") or item.get("title") or "").lower().strip()
                if key and key not in seen_keys:
                    seen_keys.add(key)
                    candidates.append(item)
        except Exception as exc:
            source_errors["crossref"] = str(exc)

    if attempted_sources > 0 and len(source_errors) == attempted_sources and not candidates:
        err_summary = "; ".join(f"{k}: {v}" for k, v in source_errors.items())
        raise RuntimeError(f"All reference sources failed ({err_summary})")

    target_r = int(target_sinta) if str(target_sinta or "").isdigit() else None

    def _rank_priority(ref):
        verified = 1 if ref.get("sinta_verified") else 0
        r = ref.get("sinta_rank")
        exact_target = 1 if (target_r and r == target_r) else 0
        has_doi = 1 if ref.get("doi_url") else 0
        has_pdf = 1 if ref.get("pdf_url") else 0
        return (exact_target, verified, has_doi, has_pdf, int(ref.get("year") or 0))

    candidates.sort(key=_rank_priority, reverse=True)
    if check_live:
        selected = []
        for r in candidates:
            doi_ok = True
            if r.get("doi_url"):
                r["doi_http"] = verify_url_status(r["doi_url"], expect_pdf=False)
                doi_ok = bool(r["doi_http"].get("ok"))
            if r.get("pdf_url"):
                r["pdf_http"] = verify_url_status(r["pdf_url"], expect_pdf=True)
                if not r["pdf_http"].get("ok"):
                    r["pdf_url"] = ""
            if doi_ok:
                selected.append(r)
            if len(selected) >= lim:
                break
    else:
        selected = candidates[:lim]

    saved_txt = ""
    saved_docx = ""
    if txt_out:
        saved_txt = export_refs_txt(
            selected,
            txt_out,
            target_doc=target_doc,
            manuscript_title=title,
            min_year=min_year,
            no_et_al=no_et_al,
        )
    if docx_out:
        saved_docx = build_dossier_docx(selected, docx_out, target_doc=target_doc)

    return {
        "query": q_clean,
        "target_sinta": target_r,
        "min_year": min_year,
        "returned": len(selected),
        "verified_sinta_count": sum(1 for r in selected if r.get("sinta_verified")),
        "exact_target_sinta_count": sum(1 for r in selected if target_r and r.get("sinta_rank") == target_r),
        "source_errors": source_errors,
        "txt_out": saved_txt,
        "docx_out": saved_docx,
        "references": selected,
    }


MCP_TOOLS = [
    {
        "name": "sinta_search_journals",
        "description": (
            "Search the local catalog of 16,617 Indonesian SINTA 1-6 accredited journals "
            "(snapshot 2026-11-15) by keyword, SINTA rank (1-6 / S1-S6), subject area, "
            "affiliation/university, Scopus status, or Garuda status."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Journal name, abbreviation (e.g. JKI, JTIIK), ISSN, or keyword"},
                "sinta_rank": {"type": "string", "description": "SINTA accreditation level filter: '1'..'6', 'S1'..'S6', or '2,3,4'"},
                "subject": {"type": "string", "description": "Subject area filter (e.g. Engineering, Education, Science, Social)"},
                "affiliation": {"type": "string", "description": "Publisher or university name filter (e.g. Bina Sarana Informatika, Brawijaya)"},
                "scopus_only": {"type": "boolean", "description": "Only return Scopus-indexed SINTA journals"},
                "garuda_only": {"type": "boolean", "description": "Only return Garuda-indexed SINTA journals"},
                "limit": {"type": "integer", "description": "Max results to return (default 20, max 100)"},
            },
        },
    },
    {
        "name": "sinta_lookup_journal",
        "description": (
            "Verify exact SINTA 1-6 accreditation status of a journal by P-ISSN, E-ISSN, "
            "DOI prefix, SINTA ID, or journal title. Returns verified R3 label."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "identifier": {"type": "string", "description": "ISSN (e.g. 2579-633X), journal title, short name, or DOI"},
            },
            "required": ["identifier"],
        },
    },
    {
        "name": "sinta_stats_summary",
        "description": "Get total breakdown of SINTA 1 to SINTA 6 journals in Indonesia ( optionally filtered by subject ).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "subject": {"type": "string", "description": "Optional subject filter"},
            },
        },
    },
    {
        "name": "garuda_search_articles",
        "description": (
            "Search Indonesian journal articles live from Garba Rujukan Digital (GARUDA Kemdiktisaintek) "
            "and automatically match each article's journal against the 16,617 SINTA 1-6 catalog."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search keywords (min 3 chars)"},
                "search_field": {"type": "string", "description": "Optional field: 'title', 'abstract', 'author', or 'doi'"},
                "publisher": {"type": "string", "description": "Optional publisher filter"},
                "sinta_rank": {"type": "string", "description": "Optional SINTA rank filter ('1'..'6' or '3,4')"},
                "year_from": {"type": "integer", "description": "Minimum publication year (default 2022 for 5-year R3 window)"},
                "year_to": {"type": "integer", "description": "Maximum publication year"},
                "pdf_only": {"type": "boolean", "description": "Only return articles with direct PDF links (default true)"},
                "limit": {"type": "integer", "description": "Maximum results (default 15)"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "sinta_find_verified_references",
        "description": (
            "Find R1-R4 compliant candidate references (2022-2026) combining GARUDA + Crossref API "
            "with automatic SINTA 1-6 rank verification and optional Mendeley .txt / .docx dossier export."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Research topic or keywords"},
                "target_sinta": {"type": "integer", "description": "Target SINTA rank (1-6) to prioritize matching-tier journals"},
                "min_year": {"type": "integer", "description": "Minimum publication year (default 2022)"},
                "limit": {"type": "integer", "description": "Number of references to return (default 15, use 25 for SINTA 1)"},
                "source": {"type": "string", "description": "'both' (default), 'garuda', or 'crossref'"},
                "check_live": {"type": "boolean", "description": "Verify live HTTP 200 status for DOI and PDF links"},
                "txt_out": {"type": "string", "description": "Optional output path for standalone R3 .txt candidate file"},
                "docx_out": {"type": "string", "description": "Optional output path for standalone Word .docx reference dossier"},
                "no_et_al": {"type": "boolean", "description": "Write all author names in full without 'et al.' (UBSI 2026 Skripsi rule)"},
                "target_doc": {"type": "string", "description": "Target manuscript filename for dossier header"},
                "title": {"type": "string", "description": "Manuscript title for dossier header"},
            },
            "required": ["query"],
        },
    },
]


def handle_mcp_request(msg):
    """Process a single JSON-RPC 2.0 MCP message and return response dict (or None for notifications)."""
    if not isinstance(msg, dict) or not isinstance(msg.get("method"), str):
        return {
            "jsonrpc": "2.0",
            "id": msg.get("id") if isinstance(msg, dict) else None,
            "error": {"code": -32600, "message": "Invalid Request"},
        }

    method = msg.get("method", "")
    req_id = msg.get("id")
    params = msg.get("params") if isinstance(msg.get("params"), dict) else {}

    if "id" not in msg or req_id is None:
        return None

    if method == "initialize":
        client_proto = params.get("protocolVersion") or "2024-11-05"
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": client_proto,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "sinta-garuda", "version": "1.0.0"},
            },
        }

    if method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": MCP_TOOLS}}

    if method == "tools/call":
        t_name = params.get("name", "")
        t_args = params.get("arguments") or {}
        try:
            if t_name == "sinta_search_journals":
                out = sinta_search_journals(**t_args)
            elif t_name == "sinta_lookup_journal":
                out = sinta_lookup_journal(**t_args)
            elif t_name == "sinta_stats_summary":
                out = sinta_stats_summary(**t_args)
            elif t_name == "garuda_search_articles":
                out = garuda_search_articles(**t_args)
            elif t_name == "sinta_find_verified_references":
                out = sinta_find_verified_references(**t_args)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Unknown tool: {t_name}"},
                }
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(out, indent=2, ensure_ascii=False)}],
                    "isError": False,
                },
            }
        except Exception as exc:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({"error": str(exc)}, ensure_ascii=False)}],
                    "isError": True,
                },
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


def serve_mcp_stdio():
    """Run STDIO MCP server supporting both line-delimited JSON-RPC and Content-Length framing."""
    stdin = sys.stdin.buffer
    stdout = sys.stdout.buffer

    while True:
        first_line = stdin.readline()
        if not first_line:
            break
        stripped = first_line.strip()
        if not stripped:
            continue

        use_content_length = False
        if stripped.lower().startswith(b"content-length:"):
            use_content_length = True
            try:
                length = int(stripped.split(b":", 1)[1].strip())
            except ValueError:
                continue
            if length <= 0 or length > 10_485_760:
                continue
            while True:
                hdr = stdin.readline()
                if not hdr or hdr in (b"\r\n", b"\n"):
                    break
            body = stdin.read(length)
            raw_json = body.decode("utf-8", errors="replace")
        else:
            raw_json = stripped.decode("utf-8", errors="replace")

        try:
            msg = json.loads(raw_json)
            resp = handle_mcp_request(msg)
        except Exception:
            resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"},
            }
        if resp is not None:
            payload = json.dumps(resp, ensure_ascii=False).encode("utf-8")
            if use_content_length:
                stdout.write(f"Content-Length: {len(payload)}\r\n\r\n".encode("ascii") + payload)
            else:
                stdout.write(payload + b"\n")
            stdout.flush()


def main():
    if hasattr(sys.stdout, "reconfigure") and "--mcp" not in sys.argv:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="SINTA 1-6 Journal Catalog (16,617 Journals) & GARUDA Reference MCP Server + CLI"
    )
    parser.add_argument("--mcp", action="store_true", help="Run as STDIO Model Context Protocol (MCP) server")
    parser.add_argument("--search-journals", help="Search SINTA 1-6 journals by keyword/title/ISSN")
    parser.add_argument("--lookup", help="Lookup exact SINTA 1-6 status by ISSN, DOI, or journal name")
    parser.add_argument("--stats", action="store_true", help="Show SINTA 1-6 catalog statistics")
    parser.add_argument("--search-garuda", help="Search articles on Garba Rujukan Digital (GARUDA)")
    parser.add_argument("--find-refs", help="Find R1-R4 verified candidate references (GARUDA + Crossref)")
    parser.add_argument("--sinta", default="", help="Filter by SINTA rank (1..6 or e.g. '3,4')")
    parser.add_argument("--subject", default="", help="Filter by subject area")
    parser.add_argument("--affiliation", default="", help="Filter by institution/publisher")
    parser.add_argument("--scopus-only", action="store_true", help="Only Scopus-indexed SINTA journals")
    parser.add_argument("--min-year", type=int, default=2022, help="Minimum publication year (default: 2022)")
    parser.add_argument("--limit", type=int, default=15, help="Maximum results to return")
    parser.add_argument("--source", default="both", choices=["both", "garuda", "crossref"], help="Reference source")
    parser.add_argument("--check-live", action="store_true", help="Verify HTTP 200 status of DOI & PDF links")
    parser.add_argument("--txt-out", default="", help="Export candidate references to R3 .txt file")
    parser.add_argument("--docx-out", default="", help="Export candidate references to Word .docx dossier")
    parser.add_argument("--no-et-al", action="store_true", help="Write all author names without 'et al.'")
    args = parser.parse_args()

    if args.mcp:
        serve_mcp_stdio()
        return

    if args.stats:
        print(json.dumps(sinta_stats_summary(subject=args.subject), indent=2, ensure_ascii=False))
    elif args.lookup:
        print(json.dumps(sinta_lookup_journal(args.lookup), indent=2, ensure_ascii=False))
    elif args.search_journals is not None:
        print(
            json.dumps(
                sinta_search_journals(
                    query=args.search_journals,
                    sinta_rank=args.sinta,
                    subject=args.subject,
                    affiliation=args.affiliation,
                    scopus_only=args.scopus_only,
                    limit=args.limit,
                ),
                indent=2,
                ensure_ascii=False,
            )
        )
    elif args.search_garuda:
        print(
            json.dumps(
                garuda_search_articles(
                    query=args.search_garuda,
                    sinta_rank=args.sinta,
                    year_from=args.min_year,
                    limit=args.limit,
                ),
                indent=2,
                ensure_ascii=False,
            )
        )
    elif args.find_refs:
        target_s = int(args.sinta) if str(args.sinta).isdigit() else None
        print(
            json.dumps(
                sinta_find_verified_references(
                    query=args.find_refs,
                    target_sinta=target_s,
                    min_year=args.min_year,
                    limit=args.limit,
                    source=args.source,
                    check_live=args.check_live,
                    txt_out=args.txt_out,
                    docx_out=args.docx_out,
                    no_et_al=args.no_et_al,
                ),
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
