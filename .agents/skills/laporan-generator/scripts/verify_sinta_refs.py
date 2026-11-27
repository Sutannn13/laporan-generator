# /// script
# requires-python = ">=3.10"
# dependencies = ["python-docx"]
# ///
"""
Verifikator Referensi Ilmiah SINTA & Builder Dosir Mendeley (.txt & .docx).
Menegakkan 4 syarat R3:
1. Terbitan maksimal 5 tahun terakhir (default 2022-2026)
2. Crossref DOI aktif (HTTP 200)
3. Direct PDF Download link aktif (HTTP 200 + application/pdf / header %PDF-)
4. Label peringkat SINTA jujur (tidak pernah mengarang peringkat jika belum terverifikasi)
"""
import argparse
from datetime import datetime
import ipaddress
import json
import os
import re
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Cm, Pt, RGBColor

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT_DIR = os.path.dirname(_THIS_DIR)
for _cand_dir in (_THIS_DIR, _PARENT_DIR):
    if _cand_dir not in sys.path:
        sys.path.insert(0, _cand_dir)

try:
    from scripts.docx_io import atomic_save_docx
except ImportError:
    from docx_io import atomic_save_docx

DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", re.IGNORECASE)


def extract_doi(raw_text):
    """Extract canonical DOI string from a DOI or doi.org URL."""
    if not raw_text:
        return None
    m = DOI_RE.search(str(raw_text).strip())
    return m.group(0).rstrip(".,;)") if m else None


def is_within_recency_window(year, current_year=None, window_years=5):
    """Return True if publication year is within last `window_years` (e.g., 2022-2026 for window=5 in 2026)."""
    if year is None:
        return False
    try:
        yr = int(year)
    except (TypeError, ValueError):
        return False
    ref_yr = current_year or datetime.now().year
    min_yr = ref_yr - (window_years - 1)
    return min_yr <= yr <= ref_yr


def format_sinta_label(sinta_rank=None, verified=False):
    """Enforce honest SINTA ranking tags without guessing."""
    if verified and sinta_rank in {1, 2, 3, 4, 5, 6, "1", "2", "3", "4", "5", "6"}:
        return f"[Peringkat: SINTA {sinta_rank} - Terverifikasi]"
    return "[Level SINTA: tidak terverifikasi]"


def _validate_public_http_url(url):
    """Validate URL is HTTP(S) and resolves strictly to public unicast IP addresses (SSRF guard)."""
    parsed = urllib.parse.urlparse(str(url or "").strip())
    if parsed.scheme.lower() not in ("http", "https") or not parsed.netloc or not parsed.hostname:
        return None, f"Blocked non-HTTP(S) URL scheme: {parsed.scheme!r}"

    host = parsed.hostname.strip().lower().rstrip(".")
    if host in ("localhost", "localhost.localdomain") or host.endswith(".local") or host.endswith(".internal"):
        return None, f"Blocked local/internal hostname: {host!r}"

    def _is_forbidden_ip(ip_obj):
        return (
            ip_obj.is_private
            or ip_obj.is_loopback
            or ip_obj.is_link_local
            or ip_obj.is_multicast
            or ip_obj.is_reserved
            or ip_obj.is_unspecified
        )

    try:
        literal_ip = ipaddress.ip_address(host)
    except ValueError:
        literal_ip = None

    if literal_ip is not None:
        if _is_forbidden_ip(literal_ip):
            return None, f"Blocked private/loopback/reserved IP address: {host}"
        return parsed.geturl(), None

    port = parsed.port or (443 if parsed.scheme.lower() == "https" else 80)
    try:
        infos = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except OSError as exc:
        return None, f"DNS resolution failed for {host}: {exc}"

    if not infos:
        return None, f"No DNS records resolved for {host}"

    for _, _, _, _, sockaddr in infos:
        resolved_ip = ipaddress.ip_address(sockaddr[0])
        if _is_forbidden_ip(resolved_ip):
            return None, f"Blocked hostname resolving to non-public IP: {host} -> {resolved_ip}"

    return parsed.geturl(), None


class _SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Re-validate every HTTP redirect target against the public-IP SSRF guard."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        resolved_next = urllib.parse.urljoin(req.full_url, newurl)
        safe_url, err = _validate_public_http_url(resolved_next)
        if err:
            raise urllib.error.URLError(err)
        return super().redirect_request(req, fp, code, msg, headers, safe_url)


def verify_url_status(url, expect_pdf=False, timeout=12):
    """Verify live HTTP 200 status and optional PDF Content-Type / %PDF- magic header."""
    safe_url, err = _validate_public_http_url(url)
    if err:
        return {"ok": False, "status": 0, "content_type": "", "error": err}
    req = urllib.request.Request(
        safe_url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; SintaRefVerifier/1.0)",
            "Accept": "application/pdf,*/*;q=0.8" if expect_pdf else "*/*",
        },
    )
    opener = urllib.request.build_opener(_SafeRedirectHandler())
    try:
        with opener.open(req, timeout=timeout) as resp:
            status = getattr(resp, "status", 200)
            ctype = (resp.headers.get("Content-Type") or "").lower()
            head = resp.read(16) if expect_pdf else b""
            if status != 200:
                return {"ok": False, "status": status, "content_type": ctype, "final_url": resp.geturl()}
            if expect_pdf:
                is_pdf = ("pdf" in ctype) or head.startswith(b"%PDF-")
                return {"ok": is_pdf, "status": status, "content_type": ctype, "final_url": resp.geturl()}
            return {"ok": True, "status": status, "content_type": ctype, "final_url": resp.geturl()}
    except urllib.error.HTTPError as e:
        return {"ok": False, "status": e.code, "content_type": "", "error": str(e)}
    except Exception as e:
        return {"ok": False, "status": 0, "content_type": "", "error": str(e)}


def _format_authors_apa(authors, no_et_al=False):
    if not authors:
        return "Anonim"
    if len(authors) == 1:
        return authors[0]
    if no_et_al or len(authors) <= 3:
        return ", ".join(authors[:-1]) + ", & " + authors[-1]
    return f"{authors[0]} et al."


def _format_authors_ieee(authors, no_et_al=False):
    if not authors:
        return "Anonim"
    if len(authors) == 1:
        return authors[0]
    if no_et_al or len(authors) <= 3:
        return ", ".join(authors[:-1]) + ", and " + authors[-1]
    return f"{authors[0]} et al."


def query_crossref(query, min_year=2022, rows=10, timeout=15):
    """Fetch real journal articles matching query and min_year from Crossref API."""
    q_enc = urllib.parse.quote(query)
    url = (
        f"https://api.crossref.org/works?query={q_enc}"
        f"&filter=from-pub-date:{min_year}-01-01,type:journal-article&rows={rows}"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "SintaRefVerifier/1.0 (mailto:research@example.org)"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read().decode("utf-8"))

    results = []
    for item in payload.get("message", {}).get("items", []):
        doi = item.get("DOI")
        title = (item.get("title") or [""])[0].strip()
        date_parts = (
            item.get("published-print", {}).get("date-parts")
            or item.get("published-online", {}).get("date-parts")
            or item.get("published", {}).get("date-parts")
            or [[0]]
        )
        year = date_parts[0][0] if date_parts and date_parts[0] else 0
        raw_authors = []
        for a in item.get("author", []):
            fam = a.get("family", "").strip()
            giv = a.get("given", "").strip()
            if fam:
                initials = " ".join(f"{w[0]}." for w in giv.split() if w)
                raw_authors.append(f"{fam}, {initials}".strip(", "))
        journal = (item.get("container-title") or [""])[0].strip()
        vol = str(item.get("volume", "")).strip()
        issue = str(item.get("issue", "")).strip()
        page = str(item.get("page", "")).strip()
        issns = item.get("ISSN") or []
        if not doi or not title or not year:
            continue

        doi_url = f"https://doi.org/{doi}"
        issn_joined = ", ".join(issns)
        sinta_rank = None
        sinta_verified = False
        relevance_txt = "Kandidat hasil penelusuran Crossref (perlu verifikasi SINTA Kemdiktisaintek & URL PDF)."
        try:
            try:
                from scripts.sinta_garuda_mcp import match_sinta_journal
            except ImportError:
                from sinta_garuda_mcp import match_sinta_journal
            s_info = match_sinta_journal(issn=issn_joined, title=journal, doi=doi)
            if s_info and s_info.get("sinta_verified"):
                sinta_rank = s_info["sinta_rank"]
                sinta_verified = True
                relevance_txt = f"Artikel Crossref terindeks SINTA {sinta_rank} ({s_info['title']})."
        except Exception:
            pass

        apa_str = (
            f"{_format_authors_apa(raw_authors)} ({year}). {title}. {journal}"
            f"{f', {vol}({issue})' if vol and issue else (f', {vol}' if vol else '')}"
            f"{f', {page}' if page else ''}. {doi_url}"
        )
        ieee_str = (
            f'{_format_authors_ieee(raw_authors)}, "{title}," {journal}'
            f'{f", vol. {vol}" if vol else ""}'
            f'{f", no. {issue}" if issue else ""}'
            f'{f", pp. {page}" if page else ""}, {year}, doi: {doi}.'
        )
        results.append(
            {
                "doi": doi,
                "doi_url": doi_url,
                "title": title,
                "year": year,
                "authors": raw_authors,
                "journal": journal,
                "volume": vol,
                "issue": issue,
                "page": page,
                "issn": issn_joined,
                "pdf_url": "",
                "sinta_rank": sinta_rank,
                "sinta_verified": sinta_verified,
                "apa": apa_str,
                "ieee": ieee_str,
                "relevance": relevance_txt,
            }
        )
    return results


def export_refs_txt(refs, output_txt, target_doc="", manuscript_title="", min_year=2022, no_et_al=False):
    """Write structured R3 candidate reference dossier to a standalone .txt file."""
    lines = [
        f"KANDIDAT REFERENSI ILMIAH TERVERIFIKASI (TERBITAN >= {min_year} | CROSSREF DOI)",
        f"Naskah Target : {target_doc or '-'}",
        f"Judul Naskah  : {manuscript_title or '-'}",
        f"Tanggal Riset : {datetime.now().strftime('%Y-%m-%d')}",
        f"Total Entri   : {len(refs)}",
        "=" * 80,
        "",
    ]
    for idx, r in enumerate(refs, start=1):
        label = format_sinta_label(r.get("sinta_rank"), bool(r.get("sinta_verified")))
        raw_auth = r.get("authors", [])
        auth_disp = _format_authors_apa(raw_auth, no_et_al=no_et_al) if isinstance(raw_auth, list) else str(raw_auth or "-")
        vol = str(r.get("volume") or "").strip()
        if vol == "-":
            vol = ""
        issue = str(r.get("issue") or "").strip()
        if issue == "-":
            issue = ""
        page = str(r.get("page") or "").strip()
        if page == "-":
            page = ""
        if no_et_al and isinstance(raw_auth, list) and len(raw_auth) > 3:
            vol_issue_str = f", {vol}({issue})" if (vol and issue) else (f", {vol}" if vol else "")
            page_str = f", {page}" if page else ""
            apa_val = (
                f"{auth_disp} ({r.get('year', '-')}). {r.get('title', '-')}. "
                f"{r.get('journal', '-')}{vol_issue_str}{page_str}. {r.get('doi_url', '')}"
            ).strip()
            ieee_auth = _format_authors_ieee(raw_auth, no_et_al=True)
            doi_clean = r.get("doi") or extract_doi(r.get("doi_url", "")) or "-"
            ieee_val = (
                f'{ieee_auth}, "{r.get("title", "-")}," {r.get("journal", "-")}'
                f'{f", vol. {vol}" if vol else ""}'
                f'{f", no. {issue}" if issue else ""}'
                f'{f", pp. {page}" if page else ""}, {r.get("year", "-")}, doi: {doi_clean}.'
            )
        else:
            apa_val = r.get("apa", "-")
            ieee_val = r.get("ieee", "-")
        lines.extend(
            [
                f"[{idx}] {auth_disp} ({r.get('year', '-')}) {label}",
                f"Judul Artikel : {r.get('title', '-')}",
                f"Nama Jurnal   : {r.get('journal', '-')}",
                f"ISSN          : {r.get('issn', '-')}",
                f"Volume/No/Hal : Vol. {r.get('volume', '-')}, No. {r.get('issue', '-')}, hlm. {r.get('page', '-')}",
                f"DOI Aktif     : {r.get('doi_url', '-')}",
                f"Download PDF  : {r.get('pdf_url') or '[Belum diverifikasi URL PDF langsung]'}",
                f"Relevansi     : {r.get('relevance', '-')}",
                f"Format APA 7  : {apa_val}",
                f"Format IEEE   : [{idx}] {ieee_val}",
                "",
            ]
        )

    out_dir = os.path.dirname(os.path.abspath(output_txt))
    os.makedirs(out_dir, exist_ok=True)
    with open(output_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).replace("\u2014", ","))
    return os.path.abspath(output_txt)


def _add_hyperlink(paragraph, text, url, font_name="Times New Roman", size_pt=9.5, color_hex="1D4ED8"):
    part = paragraph.part
    r_id = part.relate_to(
        url,
        docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK,
        is_external=True,
    )
    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)
    new_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    rFonts = OxmlElement("w:rFonts")
    rFonts.set(qn("w:ascii"), font_name)
    rFonts.set(qn("w:hAnsi"), font_name)
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(int(size_pt * 2)))
    color = OxmlElement("w:color")
    color.set(qn("w:val"), color_hex)
    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    rPr.extend([rFonts, sz, color, u])
    t = OxmlElement("w:t")
    t.text = text
    new_run.extend([rPr, t])
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def build_dossier_docx(refs, output_docx, title="DOSIR KANDIDAT REFERENSI ILMIAH TERVERIFIKASI", target_doc=""):
    """Build a standalone Mendeley-ready Word (.docx) dossier with clickable DOI & PDF links."""
    doc = docx.Document()
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sec.left_margin = Cm(2.5)
    sec.right_margin = Cm(2.5)

    def add_line(txt, size_pt=10.5, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=4):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if txt:
            r = p.add_run(str(txt).replace("\u2014", ","))
            r.font.name = "Times New Roman"
            r.font.size = Pt(size_pt)
            r.bold = bold
            r.italic = italic
        return p

    add_line(title.upper(), size_pt=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    add_line(
        f"Naskah Target: {target_doc or '-'} | Total Referensi: {len(refs)} | Format Siap Mendeley (APA 7 & IEEE)",
        size_pt=9.5,
        italic=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=10,
    )

    tbl = doc.add_table(rows=len(refs) + 1, cols=4)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["No", "Penulis & Tahun", "Nama Jurnal & Status SINTA", "DOI & Akses"]
    widths = [Cm(1.0), Cm(4.2), Cm(6.3), Cm(4.5)]
    for c_i, h_txt in enumerate(headers):
        cell = tbl.rows[0].cells[c_i]
        cell.width = widths[c_i]
        tcPr = cell._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="1E3A8A"/>'))
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_txt)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.0)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    for idx, item in enumerate(refs, start=1):
        row = tbl.rows[idx]
        lbl = format_sinta_label(item.get("sinta_rank"), bool(item.get("sinta_verified")))
        auth = _format_authors_apa(item.get("authors", [])) if isinstance(item.get("authors"), list) else str(item.get("authors", "-"))
        vals = [
            str(idx),
            f"{auth} ({item.get('year', '-')})",
            f"{item.get('journal', '-')} {lbl}",
            item.get("doi_url", "-"),
        ]
        for c_i, val in enumerate(vals):
            cell = row.cells[c_i]
            cell.width = widths[c_i]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val.replace("\u2014", ","))
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.5)

    add_line("", space_after=6)
    for idx, item in enumerate(refs, start=1):
        lbl = format_sinta_label(item.get("sinta_rank"), bool(item.get("sinta_verified")))
        add_line(f"[{idx}] {item.get('title', '-')} {lbl}", size_pt=10.5, bold=True, space_after=2)
        add_line(f"Jurnal: {item.get('journal', '-')} | Tahun: {item.get('year', '-')} | ISSN: {item.get('issn', '-')}", size_pt=9.5, space_after=2)
        p_links = add_line("", size_pt=9.5, space_after=2)
        r_lbl = p_links.add_run("DOI: ")
        r_lbl.font.name = "Times New Roman"
        r_lbl.font.size = Pt(9.5)
        if item.get("doi_url", "").startswith("http"):
            _add_hyperlink(p_links, item["doi_url"], item["doi_url"], size_pt=9.5)
        if item.get("pdf_url", "").startswith("http"):
            r_sep = p_links.add_run("  |  Download PDF: ")
            r_sep.font.name = "Times New Roman"
            r_sep.font.size = Pt(9.5)
            _add_hyperlink(p_links, item["pdf_url"], item["pdf_url"], size_pt=9.5, color_hex="15803D")
        add_line(f"Format APA 7: {item.get('apa', '-')}", size_pt=9.5, space_after=1)
        add_line(f"Format IEEE: [{idx}] {item.get('ieee', '-')}", size_pt=9.5, space_after=8)

    return atomic_save_docx(doc, output_docx, backup=False)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(
        description="Pencari & Verifikator Referensi Ilmiah Crossref + Direct PDF + Builder Dosir Mendeley (.txt & .docx)"
    )
    parser.add_argument("-q", "--query", help="Kata kunci penelusuran Crossref/Garuda")
    parser.add_argument("--from-json", help="Baca daftar kandidat referensi JSON yang sudah dikurasi")
    parser.add_argument("--source", default="crossref", choices=["crossref", "garuda", "both"], help="Sumber penelusuran (default: crossref)")
    parser.add_argument("--sinta", default="", help="Prioritaskan atau filter peringkat SINTA target (1..6)")
    parser.add_argument("--min-year", type=int, default=2022, help="Tahun terbit minimal (default: 2022 = 5 tahun terakhir)")
    parser.add_argument("--rows", type=int, default=15, help="Jumlah maksimum hasil (default: 15)")
    parser.add_argument("--check-live", action="store_true", help="Uji HTTP 200 URL DOI dan PDF langsung")
    parser.add_argument("--txt-out", help="Simpan dosir kandidat referensi ke file .txt (R3)")
    parser.add_argument("--docx-out", help="Simpan dosir kandidat referensi ke file Word .docx terpisah")
    parser.add_argument("--no-et-al", action="store_true", help="Tulis lengkap semua nama penulis tanpa 'et al.' (wajib Daftar Pustaka TA/Skripsi UBSI 2026 Poin 2.12)")
    parser.add_argument("--target-doc", default="", help="Nama file naskah target untuk header dosir")
    parser.add_argument("--title", default="", help="Judul penelitian untuk header dosir")
    args = parser.parse_args()

    refs = []
    target_s = int(args.sinta) if str(args.sinta).isdigit() else None
    if args.from_json:
        with open(args.from_json, "r", encoding="utf-8") as f:
            refs = json.load(f)
        try:
            try:
                from scripts.sinta_garuda_mcp import match_sinta_journal
            except ImportError:
                from sinta_garuda_mcp import match_sinta_journal
            for r in refs:
                if not r.get("sinta_verified"):
                    s_info = match_sinta_journal(
                        issn=r.get("issn", ""),
                        title=r.get("journal", ""),
                        doi=r.get("doi") or r.get("doi_url", ""),
                    )
                    if s_info and s_info.get("sinta_verified"):
                        r["sinta_rank"] = s_info["sinta_rank"]
                        r["sinta_verified"] = True
        except Exception:
            pass
    elif args.query:
        if args.source in ("garuda", "both") or target_s is not None:
            try:
                from scripts.sinta_garuda_mcp import sinta_find_verified_references
            except ImportError:
                from sinta_garuda_mcp import sinta_find_verified_references
            found = sinta_find_verified_references(
                query=args.query,
                target_sinta=target_s,
                min_year=args.min_year,
                limit=args.rows,
                source=args.source,
                check_live=False,
            )
            refs = found.get("references", [])
        else:
            refs = query_crossref(args.query, min_year=args.min_year, rows=args.rows)
    else:
        parser.error("Berikan --query atau --from-json.")

    cur_year = datetime.now().year
    filtered_refs = []
    for r in refs:
        try:
            yr = int(r.get("year") or 0)
        except (TypeError, ValueError):
            yr = 0
        if args.min_year <= yr <= cur_year and is_within_recency_window(yr, current_year=cur_year, window_years=5):
            filtered_refs.append(r)
    refs = filtered_refs

    if args.check_live:
        for r in refs:
            if r.get("doi_url"):
                r["doi_http"] = verify_url_status(r["doi_url"], expect_pdf=False)
            if r.get("pdf_url"):
                r["pdf_http"] = verify_url_status(r["pdf_url"], expect_pdf=True)

    if args.txt_out:
        path_txt = export_refs_txt(refs, args.txt_out, target_doc=args.target_doc, manuscript_title=args.title, min_year=args.min_year, no_et_al=args.no_et_al)
        print(f"[BERHASIL] Dosir .txt tersimpan: {path_txt}")
    if args.docx_out:
        path_docx = build_dossier_docx(refs, args.docx_out, target_doc=args.target_doc)
        print(f"[BERHASIL] Dosir Word .docx tersimpan: {path_docx}")
    if not args.txt_out and not args.docx_out:
        print(json.dumps(refs, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
