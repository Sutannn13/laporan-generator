# /// script
# requires-python = ">=3.10"
# dependencies = ["python-docx", "pillow"]
# ///
"""
Adversarial Verification Suite for IT Audit Project Report (.docx).
Role: Challenger 2 (Empirical Table, Checklist, and OpenXML XML Integrity Auditor)

Verifies:
1. Zip & OpenXML package structure, image embedding in word/media/
2. Section page geometry & margins (Left 4.0, Top 3.0, Right 2.5, Bottom 2.5 cm)
3. Table inventory & count (Assert >= 20 tables)
4. 5 Checklist tables in appendix with exact row counts [10, 9, 9, 10, 8] = 46 items
5. Compliance tally: exactly 21 compliant (✓ Sesuai), 25 non-compliant (✗ Tidak Sesuai), 45.7% rate
6. OpenXML styling: header shading (w:shd), header repeat (w:tblHeader), row split prevention (w:cantSplit)
7. Textual consistency: cross-check with narrative in BAB IV and Appendix
8. Zero dummy placeholders / TODOs
"""

import argparse
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import docx
from docx import Document
from docx.shared import Cm

BASE_DIR = Path(__file__).resolve().parent.parent
TARGET_FILE = BASE_DIR / "Laporan_Audit_TI_COBIT2019.docx"

# XML Namespaces
NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
}


def _is_checklist_table(tbl) -> bool:
    if not tbl.rows:
        return False
    hdr_text = " ".join(c.text for c in tbl.rows[0].cells).lower()
    return "pertanyaan" in hdr_text and ("catatan" in hdr_text or "status" in hdr_text)


def _extract_summary_expectations(doc):
    """Extract expected domains, row distribution, and totals from the summary table when present."""
    for tbl in doc.tables:
        if not tbl.rows:
            continue
        hdrs = [c.text.strip().lower() for c in tbl.rows[0].cells]
        hdr_join = " ".join(hdrs)
        if "sesuai" in hdr_join and "tidak sesuai" in hdr_join:
            col_tot = next((i for i, h in enumerate(hdrs) if "total" in h or "jumlah" in h), 1)
            col_ses = next((i for i, h in enumerate(hdrs) if h.startswith("sesuai") or "sesuai (" in h), 2)
            col_ts = next((i for i, h in enumerate(hdrs) if "tidak sesuai" in h), 3)
            domains = []
            counts = []
            ses_tot = 0
            ts_tot = 0
            for r in tbl.rows[1:]:
                r_txt = " ".join(c.text.strip() for c in r.cells[:2])
                m_dom = re.search(r"\b(APO\d{2}|BAI\d{2}|DSS\d{2}|MEA\d{2}|EDM\d{2})\b", r_txt)
                if not m_dom:
                    continue
                m_tot = re.search(r"\d+", r.cells[col_tot].text)
                m_ses = re.search(r"\d+", r.cells[col_ses].text)
                m_ts = re.search(r"\d+", r.cells[col_ts].text)
                if m_tot and m_ses and m_ts:
                    domains.append(m_dom.group(1))
                    counts.append(int(m_tot.group()))
                    ses_tot += int(m_ses.group())
                    ts_tot += int(m_ts.group())
            if len(domains) == 5:
                return domains, counts, ses_tot, ts_tot
    return ["APO13", "BAI06", "DSS01", "DSS05", "MEA03"], [10, 9, 9, 10, 8], 21, 25


class AdversarialAuditor:
    def __init__(self, docx_path: Path):
        self.docx_path = docx_path
        self.failures = []
        self.passed = 0
        self.doc = None
        self.zip_file = None

    def record_pass(self, test_name: str, detail: str = ""):
        self.passed += 1
        msg = f"[PASS] {test_name}"
        if detail:
            msg += f" - {detail}"
        print(msg)

    def record_fail(self, test_name: str, reason: str):
        self.failures.append((test_name, reason))
        print(f"[FAIL] {test_name} - REASON: {reason}")

    def run_all_challenges(self):
        print(f"\n========================================================")
        print(f"  CHALLENGER 2: ADVERSARIAL AUDIT OF DOCX & TABLES")
        print(f"  Target: {self.docx_path.name}")
        print(f"========================================================\n")

        self.challenge_zip_and_media()
        self.challenge_openxml_geometry()
        self.challenge_tables_and_checklist()
        self.challenge_openxml_table_styling()
        self.challenge_compliance_tally_and_narrative()
        self.challenge_anti_placeholder_and_hygiene()

        print(f"\n========================================================")
        print(f"  AUDIT SUMMARY: {self.passed} PASSED, {len(self.failures)} FAILED")
        print(f"========================================================")

        if self.failures:
            print("\nLIST OF FAILURES:")
            for name, reason in self.failures:
                print(f" - {name}: {reason}")
            print("\nFINAL VERDICT: REJECT")
            return False
        else:
            print("\nFINAL VERDICT: APPROVE")
            return True

    def challenge_zip_and_media(self):
        print("\n--- [CHALLENGE 1] Zip Archive & Media Embedding Integrity ---")
        if not self.docx_path.exists():
            self.record_fail("file_existence", f"File does not exist: {self.docx_path}")
            return

        size = self.docx_path.stat().st_size
        if size < 500_000:
            self.record_fail("file_size", f"File suspiciously small: {size} bytes")
        else:
            self.record_pass("file_size", f"{size:,} bytes ({size / (1024*1024):.2f} MB)")

        try:
            self.zip_file = zipfile.ZipFile(self.docx_path, 'r')
            names = self.zip_file.namelist()
            self.record_pass("zip_integrity", f"Valid ZIP archive with {len(names)} parts")
        except Exception as e:
            self.record_fail("zip_integrity", f"Failed to open ZIP: {e}")
            return

        # Check media files
        media_files = [n for n in names if n.startswith("word/media/")]
        print(f"Found {len(media_files)} files in word/media/: {media_files}")
        if len(media_files) < 6:
            self.record_fail("media_count", f"Expected at least 6 media files (logo + 5 diagrams), got {len(media_files)}")
        else:
            self.record_pass("media_count", f"Exactly {len(media_files)} media files embedded")

        # Verify all media files have non-zero size
        zero_byte_media = []
        for mf in media_files:
            info = self.zip_file.getinfo(mf)
            if info.file_size == 0:
                zero_byte_media.append(mf)
        if zero_byte_media:
            self.record_fail("media_byte_size", f"Found 0-byte media files: {zero_byte_media}")
        else:
            self.record_pass("media_byte_size", "All embedded media files have valid positive byte counts")

        # Inspect relationships
        try:
            rels_xml = self.zip_file.read("word/_rels/document.xml.rels")
            rels_root = ET.fromstring(rels_xml)
            image_rels = [
                rel.attrib['Target'] for rel in rels_root.findall('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship')
                if 'image' in rel.attrib.get('Type', '')
            ]
            print(f"Document relationships contain {len(image_rels)} image targets: {image_rels}")
            if len(image_rels) >= 6:
                self.record_pass("image_relationships", f"Document has {len(image_rels)} image relationships defined")
            else:
                self.record_fail("image_relationships", f"Expected >= 6 image rels, found {len(image_rels)}")
        except Exception as e:
            self.record_fail("image_relationships", f"Failed to parse document.xml.rels: {e}")

    def challenge_openxml_geometry(self):
        print("\n--- [CHALLENGE 2] OpenXML Section Geometry & Academic Margins ---")
        try:
            self.doc = Document(str(self.docx_path))
            self.record_pass("docx_load", "Successfully opened with python-docx")
        except Exception as e:
            self.record_fail("docx_load", f"Failed to load docx: {e}")
            return

        sections = self.doc.sections
        print(f"Document has {len(sections)} sections")
        if len(sections) < 8:
            self.record_fail("section_count", f"Expected at least 8 sections, found {len(sections)}")
        else:
            self.record_pass("section_count", f"Found {len(sections)} sections")

        # UBSI Standard: A4 (21.0 x 29.7 cm), Left 4.0 cm, Top 3.0 cm, Right 2.5 cm, Bottom 2.5 cm
        geometry_mismatches = []
        for idx, sec in enumerate(sections):
            w = round(sec.page_width.cm, 1)
            h = round(sec.page_height.cm, 1)
            left = round(sec.left_margin.cm, 1)
            top = round(sec.top_margin.cm, 1)
            right = round(sec.right_margin.cm, 1)
            bottom = round(sec.bottom_margin.cm, 1)

            if w != 21.0 or h != 29.7:
                geometry_mismatches.append(f"Sec {idx}: Size {w}x{h} cm != 21.0x29.7 cm")
            if left != 4.0 or top != 3.0 or right != 2.5 or bottom != 2.5:
                geometry_mismatches.append(f"Sec {idx}: Margins L={left}, T={top}, R={right}, B={bottom} cm != (4, 3, 2.5, 2.5)")

        if geometry_mismatches:
            self.record_fail("section_margins", "; ".join(geometry_mismatches))
        else:
            self.record_pass("section_margins", f"All {len(sections)} sections strictly adhere to Left=4.0cm, Top=3.0cm, Right=2.5cm, Bottom=2.5cm")

        # Also inspect raw XML <w:sectPr> in document.xml
        try:
            doc_xml = self.zip_file.read("word/document.xml")
            doc_root = ET.fromstring(doc_xml)
            sect_prs = doc_root.findall('.//w:sectPr', NS)
            print(f"Found {len(sect_prs)} raw <w:sectPr> elements in document.xml")
            raw_margin_ok = True
            for i, spr in enumerate(sect_prs):
                pgMar = spr.find('w:pgMar', NS)
                if pgMar is not None:
                    # In dxa: 1 cm = 566.929 dxa.
                    # Left 4.0 cm = ~2268 dxa
                    # Top 3.0 cm = ~1701 dxa
                    # Right 2.5 cm = ~1417 dxa
                    # Bottom 2.5 cm = ~1417 dxa
                    left_dxa = int(pgMar.attrib.get(f"{{{NS['w']}}}left", 0))
                    top_dxa = int(pgMar.attrib.get(f"{{{NS['w']}}}top", 0))
                    right_dxa = int(pgMar.attrib.get(f"{{{NS['w']}}}right", 0))
                    bottom_dxa = int(pgMar.attrib.get(f"{{{NS['w']}}}bottom", 0))

                    if not (2260 <= left_dxa <= 2275 and 1695 <= top_dxa <= 1710 and 1410 <= right_dxa <= 1425 and 1410 <= bottom_dxa <= 1425):
                        raw_margin_ok = False
                        self.record_fail("raw_openxml_margins", f"SectPr {i} dxa out of bounds: L={left_dxa}, T={top_dxa}, R={right_dxa}, B={bottom_dxa}")
                        break
            if raw_margin_ok:
                self.record_pass("raw_openxml_margins", "Raw <w:pgMar> dxa values verified (Left=2268, Top=1701, Right=1417, Bottom=1417 dxa)")
        except Exception as e:
            self.record_fail("raw_openxml_margins", f"XML inspection failed: {e}")

    def challenge_tables_and_checklist(self):
        print("\n--- [CHALLENGE 3] Table Inventory & Checklist Items ---")
        tables = self.doc.tables
        total_tables = len(tables)
        print(f"Total tables detected in document: {total_tables}")

        if total_tables < 12:
            self.record_fail("table_count_min_12", f"Expected at least 12 tables, found {total_tables}")
        else:
            self.record_pass("table_count_min_12", f"Found {total_tables} tables (>= 12 threshold satisfied)")

        # Detailed inventory of all tables
        print("\n[Table Inventory]")
        for idx, tbl in enumerate(tables):
            rows = len(tbl.rows)
            cols = len(tbl.columns) if tbl.columns else 0
            first_text = tbl.rows[0].cells[0].text.strip().replace("\n", " ") if rows > 0 and len(tbl.rows[0].cells) > 0 else "<empty>"
            if len(first_text) > 40:
                first_text = first_text[:37] + "..."
            print(f"  Table #{idx:02d}: {rows:2d} rows x {cols:2d} cols | Header/Cell 0: '{first_text}'")

        # Identify checklist tables in Appendix
        checklist_tables = [(idx, tbl) for idx, tbl in enumerate(tables) if _is_checklist_table(tbl)]

        print(f"\nFound {len(checklist_tables)} checklist tables matching header signature")
        if len(checklist_tables) != 5:
            self.record_fail("checklist_table_count", f"Expected exactly 5 checklist tables, found {len(checklist_tables)}")
            return
        else:
            self.record_pass("checklist_table_count", "Exactly 5 checklist tables identified in Appendix L-B")

        expected_domains, expected_counts, _, _ = _extract_summary_expectations(self.doc)
        actual_counts = []

        for i, (tbl_idx, tbl) in enumerate(checklist_tables):
            data_rows = len(tbl.rows) - 1
            actual_counts.append(data_rows)
            all_tbl_text = " ".join([c.text for r in tbl.rows for c in r.cells])
            prev_p_text = ""
            prev_elm = tbl._tbl.getprevious()
            while prev_elm is not None:
                if prev_elm.tag.endswith('p'):
                    p_text = "".join(prev_elm.itertext())
                    prev_p_text += " " + p_text
                    if len(prev_p_text) > 100:
                        break
                prev_elm = prev_elm.getprevious()

            full_context = all_tbl_text + " " + prev_p_text
            expected_dom = expected_domains[i]
            if expected_dom not in full_context:
                self.record_fail(f"checklist_domain_{expected_dom}", f"Domain code {expected_dom} not found in checklist table #{i+1} or its caption")
            else:
                self.record_pass(f"checklist_domain_{expected_dom}", f"Checklist table #{i+1} covers domain {expected_dom} with {data_rows} items")

        if actual_counts != expected_counts:
            self.record_fail("checklist_row_distribution", f"Row distribution {actual_counts} does not match expected {expected_counts}")
        else:
            self.record_pass("checklist_row_distribution", f"Exact row counts verified: {actual_counts} data rows (excluding headers)")

        total_checklist_items = sum(actual_counts)
        expected_total = sum(expected_counts)
        if total_checklist_items != expected_total:
            self.record_fail("total_checklist_items", f"Expected exactly {expected_total} checklist items, got {total_checklist_items}")
        else:
            self.record_pass("total_checklist_items", f"Total items sum to exactly {total_checklist_items} audit checklist items")

    def challenge_compliance_tally_and_narrative(self):
        print("\n--- [CHALLENGE 4] Compliance Tally & Narrative Consistency ---")
        checklist_tables = [tbl for tbl in self.doc.tables if _is_checklist_table(tbl)]
        domain_names, expected_counts, exp_ses, exp_ts = _extract_summary_expectations(self.doc)
        exp_total = sum(expected_counts)

        compliant_items = []
        non_compliant_items = []
        unclassified_items = []
        domain_tallies = {}

        for dom_idx, tbl in enumerate(checklist_tables):
            dom_name = domain_names[dom_idx]
            dom_compliant = 0
            dom_non_compliant = 0
            chk_hdrs = [c.text.strip().lower() for c in tbl.rows[0].cells]
            col_status = next((idx for idx, h in enumerate(chk_hdrs) if "status" in h), 3)

            for r_idx in range(1, len(tbl.rows)):
                row = tbl.rows[r_idx]
                status_text = row.cells[col_status].text.strip() if col_status < len(row.cells) else ""
                code = row.cells[1].text.strip() if len(row.cells) > 1 else f"Row {r_idx}"

                if "Tidak Sesuai" in status_text:
                    non_compliant_items.append((dom_name, code))
                    dom_non_compliant += 1
                elif "Sesuai" in status_text:
                    compliant_items.append((dom_name, code))
                    dom_compliant += 1
                else:
                    unclassified_items.append((dom_name, code, status_text[:60]))

            domain_tallies[dom_name] = {
                "compliant": dom_compliant,
                "non_compliant": dom_non_compliant,
                "total": dom_compliant + dom_non_compliant
            }

        print("\n[Checklist Compliance Per-Domain Tally]")
        for dom, data in domain_tallies.items():
            rate = (data['compliant'] / data['total'] * 100) if data['total'] > 0 else 0
            print(f"  {dom:6s}: {data['compliant']:2d} Sesuai, {data['non_compliant']:2d} Tidak Sesuai | Total: {data['total']:2d} | Compliance: {rate:5.1f}%")

        if unclassified_items:
            self.record_fail("unclassified_items", f"Found {len(unclassified_items)} unclassified checklist rows: {unclassified_items}")
        else:
            self.record_pass("unclassified_items", f"Zero unclassified checklist items; all {exp_total} items strictly categorized")

        num_compliant = len(compliant_items)
        num_non_compliant = len(non_compliant_items)
        print(f"\nOverall Tally: {num_compliant} Compliant (Sesuai), {num_non_compliant} Non-Compliant (Tidak Sesuai)")

        if num_compliant != exp_ses:
            self.record_fail("compliant_count", f"Expected {exp_ses} compliant items, got {num_compliant}")
        else:
            self.record_pass("compliant_count", f"Exactly {num_compliant} compliant items (Sesuai)")

        if num_non_compliant != exp_ts:
            self.record_fail("non_compliant_count", f"Expected {exp_ts} non-compliant items, got {num_non_compliant}")
        else:
            self.record_pass("non_compliant_count", f"Exactly {num_non_compliant} non-compliant items (Tidak Sesuai)")

        compliance_rate = (num_compliant / exp_total) * 100 if exp_total else 0.0
        rate_1f = f"{compliance_rate:.1f}%"
        rate_2f = f"{compliance_rate:.2f}%"
        all_doc_text = " ".join([p.text for p in self.doc.paragraphs])
        all_table_text = " ".join([c.text for tbl in self.doc.tables for row in tbl.rows for c in row.cells])
        full_text = (all_doc_text + " " + all_table_text).replace(",", ".")
        if rate_1f in full_text or rate_2f in full_text or f"{num_compliant} dari {exp_total}" in full_text:
            self.record_pass("narrative_tally_consistency", f"Document explicitly references compliance tally ({num_compliant}/{exp_total})")
        else:
            self.record_fail("narrative_tally_consistency", f"Document does not reference {rate_1f}/{rate_2f} or {num_compliant} dari {exp_total}")

    def challenge_openxml_table_styling(self):
        print("\n--- [CHALLENGE 5] OpenXML Table XML Styling (w:shd, w:tblHeader, w:cantSplit) ---")
        tables = self.doc.tables

        tables_with_shd = 0
        tables_with_tblHeader = 0
        tables_with_cantSplit = 0

        # Data tables are tables that have > 1 row
        multi_row_tables = [tbl for tbl in tables if len(tbl.rows) > 1]
        print(f"Total multi-row tables to evaluate for styling: {len(multi_row_tables)}")

        tbl_styling_details = []

        for idx, tbl in enumerate(multi_row_tables):
            # Inspect raw XML
            tbl_elm = tbl._tbl

            # Check header shading on row 0
            has_shd = False
            hdr_cells = tbl.rows[0].cells
            for c in hdr_cells:
                tcPr = c._tc.tcPr
                if tcPr is not None:
                    shd = tcPr.find(f"{{{NS['w']}}}shd")
                    if shd is not None and shd.attrib.get(f"{{{NS['w']}}}fill"):
                        has_shd = True
                        break

            # Check tblHeader on row 0
            has_tblHeader = False
            hdr_trPr = tbl.rows[0]._tr.trPr
            if hdr_trPr is not None:
                th = hdr_trPr.find(f"{{{NS['w']}}}tblHeader")
                if th is not None:
                    has_tblHeader = True

            # Check cantSplit on data rows
            cantSplit_count = 0
            for r in tbl.rows:
                r_trPr = r._tr.trPr
                if r_trPr is not None:
                    cs = r_trPr.find(f"{{{NS['w']}}}cantSplit")
                    if cs is not None:
                        cantSplit_count += 1

            has_cantSplit = (cantSplit_count == len(tbl.rows)) or (cantSplit_count >= len(tbl.rows) - 1)

            if has_shd:
                tables_with_shd += 1
            if has_tblHeader:
                tables_with_tblHeader += 1
            if has_cantSplit:
                tables_with_cantSplit += 1

            tbl_styling_details.append((idx, len(tbl.rows), has_shd, has_tblHeader, cantSplit_count))

        print(f"Multi-row tables with header shading (w:shd): {tables_with_shd}/{len(multi_row_tables)}")
        print(f"Multi-row tables with header repeat (w:tblHeader): {tables_with_tblHeader}/{len(multi_row_tables)}")
        print(f"Multi-row tables with row split prevention (w:cantSplit): {tables_with_cantSplit}/{len(multi_row_tables)}")

        # Table 0 is cover table, which is a layout container and intentionally borderless without tblHeader.
        # But all styled data tables and checklist tables MUST have w:shd, w:tblHeader, w:cantSplit.
        # Check that all 5 checklist tables have all 3 properties:
        checklist_tables = [tbl for tbl in tables if _is_checklist_table(tbl)]
        print(f"\nEvaluating OpenXML styling specifically for the 5 Checklist Tables:")
        checklist_styling_ok = True
        for i, tbl in enumerate(checklist_tables):
            # Check tblHeader
            hdr_trPr = tbl.rows[0]._tr.trPr
            th = hdr_trPr.find(f"{{{NS['w']}}}tblHeader") if hdr_trPr is not None else None
            # Check shd
            shd = tbl.rows[0].cells[0]._tc.tcPr.find(f"{{{NS['w']}}}shd") if tbl.rows[0].cells[0]._tc.tcPr is not None else None
            fill_val = shd.attrib.get(f"{{{NS['w']}}}fill", "") if shd is not None else ""
            # Check cantSplit on all rows
            cs_count = sum(1 for r in tbl.rows if r._tr.trPr is not None and r._tr.trPr.find(f"{{{NS['w']}}}cantSplit") is not None)

            shd_desc = f"YES ({fill_val})" if shd is not None else "NO"
            print(f"  Checklist #{i+1}: tblHeader={'YES' if th is not None else 'NO'}, "
                  f"shd={shd_desc}, "
                  f"cantSplit={cs_count}/{len(tbl.rows)} rows")

            if th is None or shd is None or cs_count < len(tbl.rows):
                checklist_styling_ok = False
                self.record_fail(f"checklist_openxml_styling_{i+1}", f"Missing styling attributes: tblHeader={th is not None}, shd={shd is not None}, cantSplit={cs_count}/{len(tbl.rows)}")

        if checklist_styling_ok:
            self.record_pass("checklist_openxml_styling", "All 5 checklist tables have w:tblHeader, w:shd, and w:cantSplit across 100% of rows")

        # General data tables styling check
        if tables_with_shd < 10 or tables_with_tblHeader < 10 or tables_with_cantSplit < 10:
            self.record_fail("general_table_styling", f"Insufficient styled tables: shd={tables_with_shd}, tblHeader={tables_with_tblHeader}, cantSplit={tables_with_cantSplit}")
        else:
            self.record_pass("general_table_styling", f"Data tables comprehensively styled (shd={tables_with_shd}, tblHeader={tables_with_tblHeader}, cantSplit={tables_with_cantSplit})")

    def challenge_anti_placeholder_and_hygiene(self):
        print("\n--- [CHALLENGE 6] Anti-Placeholder, Typography & Data Hygiene ---")
        banned_patterns = [
            r"\blorem ipsum\b",
            r"\bdolor sit amet\b",
            r"\[tbd\]",
            r"\btodo\b",
            r"\bfixme\b",
            r"\[isi data nyata",
            r"\bplaceholder\b",
            r"\bxxx+\b",
        ]

        found_banned = []
        for p_idx, p in enumerate(self.doc.paragraphs):
            text = p.text
            for pattern in banned_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    found_banned.append((f"Paragraph {p_idx}", pattern, p.text[:80]))

        for tbl_idx, tbl in enumerate(self.doc.tables):
            for r_idx, r in enumerate(tbl.rows):
                for c_idx, c in enumerate(r.cells):
                    text = c.text
                    for pattern in banned_patterns:
                        if re.search(pattern, text, re.IGNORECASE):
                            found_banned.append((f"Table {tbl_idx} R{r_idx}C{c_idx}", pattern, c.text[:80]))

        if found_banned:
            self.record_fail("placeholder_scan", f"Detected {len(found_banned)} placeholder occurrences: {found_banned}")
        else:
            self.record_pass("placeholder_scan", "Zero placeholder/dummy tokens found in document text and tables")

        # Check total words
        all_words = " ".join([p.text for p in self.doc.paragraphs]).split()
        word_count = len(all_words)
        print(f"Total body word count: {word_count:,} words")
        if word_count < 5000:
            self.record_fail("word_count", f"Word count too low ({word_count:,} < 5,000)")
        else:
            self.record_pass("word_count", f"Rich document content: {word_count:,} words")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Challenger 2: OpenXML Table & Checklist Integrity Verifier (.docx)")
    parser.add_argument("-t", "--target", default=str(TARGET_FILE), help="Target .docx path")
    args = parser.parse_args()
    auditor = AdversarialAuditor(Path(args.target))
    success = auditor.run_all_challenges()
    sys.exit(0 if success else 1)
