#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["python-docx"]
# ///
"""
scripts/challenge_text_and_math.py
Empirical Adversarial Verification Suite for IT Audit Project Report (.docx).
Evaluates text fidelity, structure, mathematical consistency, CCCE completeness,
sampling figures, placeholder absence, page geometry, typography, and embedded assets.
"""

import argparse
import os
import re
import sys
import docx

DEFAULT_TARGET_DOCX = os.path.join(
    "website", "public", "downloads", "04_Sampel_Laporan_Audit_TI_COBIT2019.docx"
)


def _parse_roster(roster_arg):
    if not roster_arg:
        return [("Penulis Contoh", "00000001")]
    pairs = []
    for item in roster_arg.split(","):
        item = item.strip()
        if ":" in item:
            name, nim = item.split(":", 1)
            pairs.append((name.strip(), nim.strip()))
        elif item:
            pairs.append((item, ""))
    return pairs or [("Penulis Contoh", "00000001")]


def _find_table_by_keywords(doc, required_keywords):
    for tbl in doc.tables:
        if not tbl.rows:
            continue
        txt = " ".join(c.text for r in tbl.rows[:2] for c in r.cells)
        if all(kw.lower() in txt.lower() for kw in required_keywords):
            return tbl
    for tbl in doc.tables:
        txt = " ".join(c.text for r in tbl.rows for c in r.cells)
        if all(kw.lower() in txt.lower() for kw in required_keywords):
            return tbl
    return None


def run_challenge(
    target_docx=None,
    roster_str="Penulis Contoh:00000001",
    domains_str="",
    min_words=5000,
    min_paragraphs=250,
):
    target_path = target_docx or DEFAULT_TARGET_DOCX
    print("=" * 75)
    print("CHALLENGER 1: EMPIRICAL TEXT & MATHEMATICAL ADVERSARIAL VERIFICATION")
    print("=" * 75)

    findings = []
    passed_tests = 0
    total_tests = 0

    def assert_test(condition, test_name, detail="", is_critical=True):
        nonlocal passed_tests, total_tests
        total_tests += 1
        if condition:
            passed_tests += 1
            print(f" [PASS] Test {total_tests:02d}: {test_name}")
            return True
        status = "CRITICAL FAIL" if is_critical else "WARNING/OBSERVATION"
        print(f"![{status}] Test {total_tests:02d}: {test_name} -> {detail}")
        findings.append((test_name, detail, is_critical))
        return False

    file_exists = os.path.exists(target_path)
    file_size = os.path.getsize(target_path) if file_exists else 0
    assert_test(
        file_exists and file_size > 500_000,
        "Document File Existence and Plausible Size (>500 KB)",
        f"File exists: {file_exists}, size: {file_size:,} bytes",
    )

    if not file_exists:
        print("CRITICAL: Cannot open target document.")
        return False, findings, "REJECT"

    doc = docx.Document(target_path)

    geometry_ok = True
    for s in doc.sections:
        if round(s.page_width.cm, 1) != 21.0 or round(s.page_height.cm, 1) != 29.7:
            geometry_ok = False
            break
        if (
            round(s.left_margin.cm, 1) != 4.0
            or round(s.top_margin.cm, 1) != 3.0
            or round(s.right_margin.cm, 1) != 2.5
            or round(s.bottom_margin.cm, 1) != 2.5
        ):
            geometry_ok = False
            break

    assert_test(
        geometry_ok and len(doc.sections) >= 8,
        "Institutional Geometry: >=8 Sections with A4 (21x29.7cm) & Margins (4-3-2.5-2.5cm)",
        f"Sections count: {len(doc.sections)}, geometry conformant: {geometry_ok}",
    )

    images = [rel.target_ref for rel in doc.part.rels.values() if "image" in rel.target_ref]
    assert_test(
        len(images) >= 6,
        "Embedded Graphic Assets Count >= 6 (UBSI Logo + 5 Technical Diagrams)",
        f"Found {len(images)} images in document media package.",
    )

    fonts = set()
    for p in doc.paragraphs:
        for r in p.runs:
            if r.font.name:
                fonts.add(r.font.name)
    assert_test(
        fonts == {"Times New Roman"},
        "Typography Strictness: 100% Times New Roman across all styled runs",
        f"Detected font families: {fonts}",
    )

    all_text = [p.text for p in doc.paragraphs]
    for t in doc.tables:
        for r in t.rows:
            for c in r.cells:
                all_text.append(c.text)

    full_corpus = " ".join(all_text)
    words = re.findall(r"\b\w+\b", full_corpus)
    word_count = len(words)
    paragraph_count = len(doc.paragraphs)

    assert_test(
        word_count >= min_words,
        f"Word Count Threshold (>={min_words:,} words)",
        f"Actual word count: {word_count:,} words",
    )
    assert_test(
        paragraph_count >= min_paragraphs,
        f"Paragraph Count Threshold (>={min_paragraphs} paragraphs)",
        f"Actual paragraphs: {paragraph_count}",
    )

    expected_bab_titles = [
        ("BAB I", "PENDAHULUAN"),
        ("BAB II", "LANDASAN TEORI"),
        ("BAB III", "GAMBARAN UMUM"),
        ("BAB IV", "PEMBAHASAN"),
        ("BAB V", "KESIMPULAN"),
    ]
    p_texts = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    joined_p = "\n".join(p_texts)
    for b_num, b_title in expected_bab_titles:
        found = (b_num in joined_p) and (b_title in joined_p)
        assert_test(found, f"Major Chapter Presence: '{b_num} {b_title}'", f"Chapter '{b_num} {b_title}' not found.")

    front_matter_sections = ["KATA PENGANTAR", "DAFTAR ISI", "DAFTAR TABEL", "DAFTAR GAMBAR"]
    for fm in front_matter_sections:
        found = any(fm in pt.upper() for pt in p_texts)
        assert_test(found, f"Front Matter Presence: '{fm}'", f"Section '{fm}' not found.")

    for app in ["Lampiran L-A", "Lampiran L-B", "Lampiran L-C", "Lampiran L-D", "Lampiran L-E"]:
        found = any(app.lower() in pt.lower() for pt in p_texts)
        assert_test(found, f"Appendix Presence: '{app}'", f"Appendix '{app}' not found.")

    team_roster = _parse_roster(roster_str)
    for name, nim in team_roster:
        found = (name in full_corpus) and (not nim or nim in full_corpus)
        assert_test(found, f"Author/Auditor Identity: {name} ({nim})", f"Identity {name} ({nim}) not found in document.")

    if domains_str:
        active_domains = [d.strip().upper() for d in domains_str.split(",") if d.strip()]
    elif "APO12" in full_corpus and any("APO12" in pt and "Temuan" in pt for pt in p_texts):
        active_domains = ["APO12", "APO13", "BAI06", "DSS05", "MEA03"]
    else:
        active_domains = ["APO13", "BAI06", "DSS01", "DSS05", "MEA03"]

    for domain in active_domains:
        domain_found = any(domain in pt and "Temuan" in pt for pt in p_texts)
        assert_test(domain_found, f"CCCE Finding Presence for Domain {domain}", f"Finding for {domain} not identified.")

    ccce_elements = [
        "Kondisi Nyata (Condition)",
        "Kriteria Standar (Criteria)",
        "Akar Penyebab (Cause)",
        "Akibat / Dampak Risiko (Effect)",
        "Rekomendasi Tindakan",
    ]
    for elem in ccce_elements:
        count = sum(1 for pt in p_texts if elem in pt)
        assert_test(count == 5, f"CCCE Element '{elem}' Count == 5", f"Found {count} occurrences (expected 5).")

    # Dynamic lookup for Risk Matrix table
    risk_table = _find_table_by_keywords(doc, ["Kemungkinan", "Dampak", "Skor"])
    if risk_table is None:
        risk_table = _find_table_by_keywords(doc, ["Likelihood", "Impact"])
    risk_math_ok = risk_table is not None
    checked_risk_rows = 0
    if risk_table is not None:
        hdr_cells = [c.text.strip().lower() for c in risk_table.rows[0].cells]
        col_l = next((idx for idx, h in enumerate(hdr_cells) if "kemungkinan" in h or "likelihood" in h), None)
        col_i = next((idx for idx, h in enumerate(hdr_cells) if "dampak" in h or "impact" in h), None)
        col_s = next((idx for idx, h in enumerate(hdr_cells) if "skor" in h or "score" in h), None)
        for row in risk_table.rows[1:]:
            row_txt = " ".join(c.text.strip() for c in row.cells)
            matched_dom = next((d for d in active_domains if d in row_txt), None)
            if not matched_dom:
                continue
            if col_l is not None and col_i is not None and col_s is not None:
                m_l = re.search(r"\d+", row.cells[col_l].text.strip())
                m_i = re.search(r"\d+", row.cells[col_i].text.strip())
                m_s = re.search(r"\d+", row.cells[col_s].text.strip())
                if m_l and m_i and m_s:
                    l_val, i_val, s_val = int(m_l.group()), int(m_i.group()), int(m_s.group())
                    checked_risk_rows += 1
                    if l_val * i_val != s_val:
                        risk_math_ok = False
                        findings.append((f"Risk Math {matched_dom}", f"Got {l_val}x{i_val}={s_val}", True))
            else:
                risk_math_ok = False

    assert_test(
        risk_math_ok and checked_risk_rows == len(active_domains),
        f"Risk Matrix Math: Score = Likelihood x Impact ({checked_risk_rows} domains)",
        "Discrepancy or missing rows in risk matrix table.",
    )

    # Dynamic lookup for Capability Gap table
    gap_table = _find_table_by_keywords(doc, ["Saat Ini", "Target", "Gap"])
    if gap_table is None:
        gap_table = _find_table_by_keywords(doc, ["Current", "Target", "Gap"])

    gap_math_ok = gap_table is not None
    current_levels = []
    target_levels = []
    gaps = []
    if gap_table is not None:
        gap_hdrs = [c.text.strip().lower() for c in gap_table.rows[0].cells]
        col_cur = next((idx for idx, h in enumerate(gap_hdrs) if "saat ini" in h or "current" in h), 1)
        col_tgt = next((idx for idx, h in enumerate(gap_hdrs) if "target" in h), 2)
        col_gap = next((idx for idx, h in enumerate(gap_hdrs) if "gap" in h or "kesenjangan" in h), 3)
        for row in gap_table.rows[1:]:
            dom_raw = row.cells[0].text.strip()
            matched_dom = next((d for d in active_domains if d in dom_raw), None)
            if not matched_dom:
                continue
            c_m = re.search(r"\d+(?:[.,]\d+)?", row.cells[col_cur].text)
            t_m = re.search(r"\d+(?:[.,]\d+)?", row.cells[col_tgt].text)
            g_m = re.search(r"\d+(?:[.,]\d+)?", row.cells[col_gap].text)
            if c_m and t_m and g_m:
                c_val = float(c_m.group(0).replace(",", "."))
                t_val = float(t_m.group(0).replace(",", "."))
                g_val = float(g_m.group(0).replace(",", "."))
                current_levels.append(c_val)
                target_levels.append(t_val)
                gaps.append(g_val)
                if round(t_val - c_val, 2) != round(g_val, 2):
                    gap_math_ok = False
                    findings.append((f"Gap Math {matched_dom}", f"Got {c_val}->{t_val} (gap {g_val})", True))

    avg_c = sum(current_levels) / len(current_levels) if current_levels else 0.0
    avg_t = sum(target_levels) / len(target_levels) if target_levels else 0.0
    avg_g = sum(gaps) / len(gaps) if gaps else 0.0

    assert_test(
        gap_math_ok and len(current_levels) == len(active_domains),
        "Per-Domain Capability Level & Gap Calculation",
        "Domain gap math mismatch.",
    )

    if gap_table is not None:
        summary_row_txt = " ".join(c.text.strip().replace(",", ".") for c in gap_table.rows[-1].cells)
        c_ok = (f"{avg_c:.1f}" in summary_row_txt) or (f"{avg_c:.2f}" in summary_row_txt)
        t_ok = (f"{avg_t:.1f}" in summary_row_txt) or (f"{avg_t:.2f}" in summary_row_txt)
        g_ok = (f"{avg_g:.1f}" in summary_row_txt) or (f"{avg_g:.2f}" in summary_row_txt)
        assert_test(
            c_ok and t_ok and g_ok,
            f"Summary Row in Gap Table reflects averages ({avg_c:.2f}, {avg_t:.2f}, {avg_g:.2f})",
            f"Summary row text: {summary_row_txt}",
        )

    placeholder_pattern = re.compile(
        r"\b(TODO|TBD|LOREM IPSUM|INSERT)\b|\[(TODO|TBD|LOREM IPSUM|INSERT|ISI DATA NYATA).*?\]",
        re.IGNORECASE,
    )
    found_placeholders = []
    for i, p in enumerate(doc.paragraphs):
        if placeholder_pattern.search(p.text):
            found_placeholders.append((f"P{i}", p.text[:80]))
    for t_idx, t in enumerate(doc.tables):
        for r_idx, r in enumerate(t.rows):
            for c_idx, c in enumerate(r.cells):
                if placeholder_pattern.search(c.text):
                    found_placeholders.append((f"T{t_idx}R{r_idx}C{c_idx}", c.text[:80]))

    assert_test(
        len(found_placeholders) == 0,
        "Zero Unresolved Placeholders in Paragraphs and Tables",
        f"Found {len(found_placeholders)} placeholders: {found_placeholders}",
    )

    # Dynamic lookup for Appendix L-B checklist tables and quantitative summary table
    summary_table = _find_table_by_keywords(doc, ["Domain", "Sesuai", "Tidak Sesuai"])
    if summary_table is None:
        summary_table = _find_table_by_keywords(doc, ["Sesuai", "Tidak Sesuai"])
    checklist_map = {}
    for tbl in doc.tables:
        if not tbl.rows:
            continue
        hdr_txt = " ".join(c.text for c in tbl.rows[0].cells).lower()
        if "pertanyaan" in hdr_txt and ("catatan" in hdr_txt or "status" in hdr_txt):
            for d in active_domains:
                if d not in checklist_map:
                    checklist_map[d] = tbl
                    break

    print("\n--- DETAILED CHECKLIST CROSS-EXAMINATION ---")
    tally_mismatch = False
    if summary_table is not None and len(checklist_map) == len(active_domains):
        sum_hdrs = [c.text.strip().lower() for c in summary_table.rows[0].cells]
        col_tot = next((idx for idx, h in enumerate(sum_hdrs) if "total" in h or "jumlah" in h), 1)
        col_ses = next((idx for idx, h in enumerate(sum_hdrs) if h.startswith("sesuai") or "sesuai (" in h), 2)
        col_ts = next((idx for idx, h in enumerate(sum_hdrs) if "tidak sesuai" in h), 3)
        summary_rows_by_dom = {}
        for row in summary_table.rows[1:]:
            r_txt = " ".join(c.text.strip() for c in row.cells[:2])
            dom = next((d for d in active_domains if d in r_txt), None)
            if dom:
                m_tot = re.search(r"\d+", row.cells[col_tot].text)
                m_ses = re.search(r"\d+", row.cells[col_ses].text)
                m_ts = re.search(r"\d+", row.cells[col_ts].text)
                if m_tot and m_ses and m_ts:
                    summary_rows_by_dom[dom] = [int(m_tot.group()), int(m_ses.group()), int(m_ts.group())]

        for d in active_domains:
            tbl = checklist_map[d]
            chk_hdrs = [c.text.strip().lower() for c in tbl.rows[0].cells]
            col_status = next((idx for idx, h in enumerate(chk_hdrs) if "status" in h), 3)
            actual_total = len(tbl.rows) - 1
            actual_s = sum(
                1
                for r in tbl.rows[1:]
                if ("Sesuai" in r.cells[col_status].text and "Tidak" not in r.cells[col_status].text)
            )
            actual_t = sum(1 for r in tbl.rows[1:] if "Tidak Sesuai" in r.cells[col_status].text)
            sum_vals = summary_rows_by_dom.get(d)
            if sum_vals != [actual_total, actual_s, actual_t]:
                tally_mismatch = True
            print(
                f" * {d}: Summary={sum_vals} vs Appendix (Total={actual_total}, Sesuai={actual_s}, Tidak Sesuai={actual_t})"
            )
    else:
        tally_mismatch = True

    assert_test(
        not tally_mismatch,
        "Checklist Summary Table strictly matches Appendix L-B.1-5 item-for-item",
        f"Checklist tables found: {len(checklist_map)}, tally mismatch: {tally_mismatch}",
    )

    print("\n" + "=" * 75)
    critical_fails = [f for f in findings if f[2]]
    warnings = [f for f in findings if not f[2]]
    print(
        f"CHALLENGER 1 SUMMARY: {passed_tests}/{total_tests} Tests Passed | Critical: {len(critical_fails)} | Warnings: {len(warnings)}"
    )
    print("=" * 75)
    for t_name, err, crit in findings:
        tag = "CRITICAL" if crit else "NON-BLOCKING WARNING"
        print(f" - [{tag}] {t_name}: {err}")

    verdict = "APPROVE" if len(critical_fails) == 0 else "REJECT"
    print(f"\nFINAL VERDICT: {verdict}")
    return (verdict == "APPROVE", findings, verdict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Empirical Text & Mathematical Audit Report Verifier (.docx)")
    parser.add_argument("-t", "--target", default=DEFAULT_TARGET_DOCX, help="Path ke dokumen Laporan Audit .docx target")
    parser.add_argument(
        "--roster",
        default="Penulis Contoh:00000001",
        help="Daftar anggota tim format 'Nama:NIM,Nama2:NIM2' (default: Penulis Contoh:00000001)",
    )
    parser.add_argument("--domains", default="", help="Daftar 5 domain COBIT 2019 dipisahkan koma")
    parser.add_argument("--min-words", type=int, default=5000, help="Batas minimum jumlah kata")
    parser.add_argument("--min-paragraphs", type=int, default=250, help="Batas minimum jumlah paragraf")
    args = parser.parse_args()
    success, findings, verdict = run_challenge(
        target_docx=args.target,
        roster_str=args.roster,
        domains_str=args.domains,
        min_words=args.min_words,
        min_paragraphs=args.min_paragraphs,
    )
    sys.exit(0 if success else 1)
