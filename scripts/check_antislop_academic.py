# /// script
# requires-python = ">=3.10"
# dependencies = ["python-docx"]
# ///
"""
Academic Anti-Slop, Anti-AI-Detector (Burstiness), and R1 Mendeley Compliance Linter.
Integrates GitHub antislop + antislop-copywriting rules (R-02, R-16, R-36)
for Indonesian & English academic manuscripts (.docx, .txt, .md).
"""
import argparse
import json
import math
import os
import re
import sys

REF_HEADINGS = {"DAFTAR PUSTAKA", "REFERENSI", "REFERENCES", "BIBLIOGRAPHY"}
POST_REF_HEADINGS = {"LAMPIRAN", "APPENDICES", "APPENDIX", "BIODATA", "DAFTAR RIWAYAT HIDUP", "RIWAYAT HIDUP"}

BANNED_CLICHE_PATTERNS = [
    ("ID_ERA_KLISE", r"\bdi era (?:digital|teknologi|globalisasi|transformasi|revolusi industri)[^\.,;\n]{0,45}(?:berkembang pesat|dewasa ini|saat ini)\b"),
    ("ID_DIPUNGKIRI", r"\btidak dapat dipungkiri\b"),
    ("ID_PERAN_KRUSIAL", r"\bmemainkan peran (?:yang )?(?:krusial|vital|sentral|penting)\b"),
    ("ID_KOMPREHENSIF_DOBEL", r"\bsecara komprehensif dan menyeluruh\b"),
    ("EN_LANDSCAPE", r"\bin today'?s rapidly evolving[^\.,;\n]{0,35}landscape\b"),
    ("EN_DELVE", r"\bdelve(?:s|d|ing)? into\b"),
    ("EN_TESTAMENT", r"\b(?:a )?testament to\b"),
    ("EN_PIVOTAL", r"\bpivotal (?:moment|role)\b"),
    ("EN_BUZZWORD", r"\b(?:game-changer|cutting-edge|seamless(?:ly)?|next-generation)\b"),
    ("EN_FILLER", r"\bit is important to note that\b"),
    ("EN_OPTIMISM", r"\bthe future looks bright\b"),
]

NEG_PARALLEL_RE = re.compile(
    r"\b(?:bukan hanya [^\.\n]{2,90}\bmelainkan juga\b|"
    r"tidak semata-mata [^\.\n]{2,90}\btetapi\b|"
    r"not only [^\.\n]{2,90}\bbut also\b|"
    r"it(?:'s| is) not just [^\.\n]{2,90}\bit(?:'s| is)\b)",
    re.IGNORECASE,
)

INANIMATE_HUMAN_RE = re.compile(
    r"\b(?:tabel\s+\d+|gambar\s+\d+|data|grafik|dashboard|sistem ini)\s+"
    r"(?:mengatakan|memahami|percaya|memutuskan sendiri|berbicara|understands|believes|wants|cares)\b",
    re.IGNORECASE,
)

DEBUG_BANNER_RE = re.compile(r"\|\s*Peringkat:\s*SINTA|Layout:\s*[12]\s*Kolom", re.IGNORECASE)
URL_DOI_RE = re.compile(r"https?://\S+", re.IGNORECASE)
REF_LINE_RE = re.compile(r"^\s*\[\d+\]\s+|https?://doi\.org/10\.", re.IGNORECASE)


def extract_document_segments(path):
    """Extract body prose paragraphs, table strings, and bibliography paragraphs."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Berkas tidak ditemukan: {path}")
    ext = os.path.splitext(path)[1].lower()
    table_texts = []
    if ext == ".docx":
        import docx
        doc = docx.Document(path)
        raw_paras = [p.text.strip() for p in doc.paragraphs if p.text and p.text.strip()]
        for tbl in doc.tables:
            for row in tbl.rows:
                for cell in row.cells:
                    txt = cell.text.strip()
                    if txt:
                        table_texts.append(txt)
    else:
        with open(path, "r", encoding="utf-8") as f:
            raw_paras = [line.strip() for line in f if line.strip()]

    body_paras = []
    ref_paras = []
    in_refs = False
    toc_line_re = re.compile(r"(?:\t|\.{2,}|\u2026+)\s*(?:[ivxlcdm]+|\d+)\s*$", re.IGNORECASE)
    chapter_reset_re = re.compile(
        r"^(?:BAB\s+[IVXLCDM]+\b|(?:1\.|I\.)\s*(?:PENDAHULUAN|INTRODUCTION)\b|ABSTRAK\b|ABSTRACT\b)",
        re.IGNORECASE,
    )
    for text in raw_paras:
        if toc_line_re.search(text):
            body_paras.append(text)
            continue
        cleaned_head = re.sub(r"^[\d\.\s]+", "", text).strip().upper()
        if cleaned_head in REF_HEADINGS and len(text) <= 45:
            in_refs = True
            continue
        if in_refs and (
            (cleaned_head in POST_REF_HEADINGS and len(text) <= 45)
            or chapter_reset_re.match(text.strip())
        ):
            if chapter_reset_re.match(text.strip()) and ref_paras:
                body_paras.extend(ref_paras)
                ref_paras = []
            in_refs = False
            body_paras.append(text)
            continue
        if in_refs:
            if text.startswith("[REFERENSI DIKELOLA") or text.startswith("[MASUKKAN REFERENSI"):
                continue
            ref_paras.append(text)
        else:
            body_paras.append(text)
    return body_paras, table_texts, ref_paras


def compute_burstiness(body_paras):
    """Compute sentence-length distribution stats on prose body paragraphs."""
    lengths = []
    for para in body_paras:
        if len(para.split()) < 18:
            continue
        # Strip inline URLs/DOIs & numbered brackets before splitting prose sentences
        cleaned = URL_DOI_RE.sub("", para)
        cleaned = re.sub(r"\[\d+(?:,\s*\d+)*\]", "", cleaned)
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", cleaned) if s.strip()]
        for sent in sentences:
            words = re.findall(r"\b[\w-]+\b", sent)
            if len(words) >= 4:
                lengths.append(len(words))

    if len(lengths) < 3:
        return {"sentence_count": len(lengths), "mean_words": 0.0, "std_words": 0.0, "min_words": 0, "max_words": 0}

    mean_w = sum(lengths) / len(lengths)
    var_w = sum((x - mean_w) ** 2 for x in lengths) / len(lengths)
    return {
        "sentence_count": len(lengths),
        "mean_words": round(mean_w, 2),
        "std_words": round(math.sqrt(var_w), 2),
        "min_words": min(lengths),
        "max_words": max(lengths),
    }


def audit_manuscript(path, min_std=5.5, mendeley_mode=False):
    """Run antislop-copywriting, Burstiness, and R1 compliance checks on a file."""
    body_paras, table_texts, ref_paras = extract_document_segments(path)
    all_text = "\n".join(body_paras + table_texts + ref_paras)
    body_text = "\n".join(body_paras + table_texts)

    em_dash_count = all_text.count("\u2014")
    spaced_hyphen_count = len(re.findall(r"\s--\s", body_text))
    debug_banner_hits = DEBUG_BANNER_RE.findall(body_text)

    cliche_hits = []
    for code, pat in BANNED_CLICHE_PATTERNS:
        matches = re.findall(pat, body_text, flags=re.IGNORECASE)
        if matches:
            cliche_hits.append({"rule": code, "count": len(matches), "samples": matches[:3]})

    neg_parallel_hits = NEG_PARALLEL_RE.findall(body_text)
    inanimate_hits = INANIMATE_HUMAN_RE.findall(body_text)
    isi_data_placeholders = re.findall(r"\[ISI DATA NYATA:[^\]]*\]", body_text)
    burstiness = compute_burstiness(body_paras)

    ref_entries_count = sum(1 for r in ref_paras if len(r.split()) >= 4 or REF_LINE_RE.search(r))
    critical_issues = []
    warnings = []

    if em_dash_count > 0:
        critical_issues.append(f"R-02: Ditemukan {em_dash_count} karakter em dash (\\u2014).")
    if spaced_hyphen_count > 0:
        warnings.append(f"R-02: Ditemukan {spaced_hyphen_count} tanda pisah ganda ' -- ' di narasi.")
    if debug_banner_hits:
        critical_issues.append(f"AI Debug Banner terlarang di badan dokumen: {debug_banner_hits}")
    if cliche_hits:
        critical_issues.append(f"R-16/R-36 Antislop Copywriting: Ditemukan frasa klise AI: {cliche_hits}")
    if inanimate_hits:
        warnings.append(f"R-02 Inanimate Human Verb terdeteksi: {inanimate_hits}")
    if len(neg_parallel_hits) > 1:
        warnings.append(f"R-36 Negative Parallelism berulang ({len(neg_parallel_hits)}x).")
    if mendeley_mode and ref_entries_count > 0:
        critical_issues.append(
            f"R1 Pelanggaran Mendeley: Ditemukan {ref_entries_count} entri di bawah heading REFERENSI/DAFTAR PUSTAKA di .docx."
        )
    if burstiness["sentence_count"] >= 6 and burstiness["std_words"] < min_std:
        warnings.append(
            f"Burstiness rendah (std={burstiness['std_words']} < {min_std} kata/kalimat): variasikan kalimat pendek & kompleks."
        )

    passed = len(critical_issues) == 0
    return {
        "file": os.path.abspath(path),
        "passed": passed,
        "em_dash_count": em_dash_count,
        "cliche_hits": cliche_hits,
        "negative_parallelism_count": len(neg_parallel_hits),
        "inanimate_human_verb_hits": inanimate_hits,
        "debug_banner_hits": debug_banner_hits,
        "r1_ref_entries_in_docx": ref_entries_count,
        "isi_data_placeholders": len(isi_data_placeholders),
        "burstiness": burstiness,
        "critical_issues": critical_issues,
        "warnings": warnings,
    }


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Linter Anti-Slop, Anti-AI-Detector (Burstiness), & Kepatuhan R1 Mendeley")
    parser.add_argument("-i", "--input", required=True, help="Path berkas .docx, .txt, atau .md")
    parser.add_argument("--mendeley-mode", action="store_true", help="Wajibkan 0 entri daftar pustaka di dalam .docx (Aturan R1)")
    parser.add_argument("--min-std", type=float, default=5.5, help="Ambang minimum simpangan baku panjang kalimat (default: 5.5)")
    parser.add_argument("--strict", action="store_true", help="Jadikan warning burstiness/parallelism juga menggagalkan exit code")
    parser.add_argument("--json", action="store_true", help="Tampilkan output JSON lengkap")
    args = parser.parse_args()

    result = audit_manuscript(args.input, min_std=args.min_std, mendeley_mode=args.mendeley_mode)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        status = "PASS" if result["passed"] else "FAIL"
        b = result["burstiness"]
        print(f"[{status}] {result['file']}")
        print(f"  Em dash: {result['em_dash_count']} | Clichés: {len(result['cliche_hits'])} | R1 ref entries in docx: {result['r1_ref_entries_in_docx']}")
        print(f"  Burstiness: sentences={b['sentence_count']}, mean={b['mean_words']} words, std={b['std_words']} (range {b['min_words']}-{b['max_words']})")
        for issue in result["critical_issues"]:
            print(f"  [CRITICAL] {issue}")
        for warn in result["warnings"]:
            print(f"  [WARN] {warn}")

    has_fail = not result["passed"] or (args.strict and len(result["warnings"]) > 0)
    sys.exit(1 if has_fail else 0)


if __name__ == "__main__":
    main()
