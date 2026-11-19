# /// script
# requires-python = ">=3.10"
# dependencies = ["python-docx"]
# ///
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET
import docx

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from generate_sinta_journal_docx import (
    generate_showcase_folder,
    inspect_existing_docx,
    load_presets,
)
from scripts.sinta_content_data import REFS_APK_KUHP, REFS_HUMAS
from scripts.check_antislop_academic import audit_manuscript
from scripts.verify_sinta_refs import (
    _format_authors_apa,
    build_dossier_docx,
    export_refs_txt,
    extract_doi,
    format_sinta_label,
    is_within_recency_window,
    verify_url_status,
)


def verify_sinta_system():
    # Clean up any temporary crossref json files from workspace root if present
    for tmp_json in ["crossref_verified.json", "crossref_more.json"]:
        if os.path.exists(tmp_json):
            os.remove(tmp_json)

    presets = load_presets()
    assert len(presets) == 6, f"Expected 6 SINTA presets, got {len(presets)}"

    institutions = set()
    doi_prefixes = set()
    for rank in ["1", "2", "3", "4", "5", "6"]:
        assert rank in presets, f"Missing SINTA {rank}"
        p = presets[rank]
        institutions.add(p["institution"])
        doi_prefixes.add(p["doi_prefix"])
        assert p["p_issn"] and p["e_issn"], f"Missing ISSN for SINTA {rank}"
        assert p["sample_doi"].startswith("https://doi.org/10."), f"Invalid DOI for SINTA {rank}"

    assert len(institutions) == 6, "All 6 SINTA journals must come from 6 different institutions"
    assert len(doi_prefixes) == 6, "All 6 SINTA journals must have 6 distinct Crossref DOI prefixes"

    # Generate and verify showcase folder
    showcase_dir = "contoh-template-ai"
    generated = generate_showcase_folder(showcase_dir)
    assert len(generated) == 9, f"Expected 9 SINTA showcase variants, got {len(generated)}"
    assert os.path.exists(os.path.join(showcase_dir, "README.md")), "Missing README.md in showcase folder"
    assert os.path.exists(os.path.join(showcase_dir, "11_Jurnal_SINTA4_JKI_UBSI_Typst.pdf")), "Missing Typst SINTA 4 PDF in showcase folder"
    assert os.path.exists(os.path.join(showcase_dir, "00_Jurnal_SINTA1_HukumSiber_APK_KUHP_Baru_PJIH_Unpad.docx")), "Missing SINTA 1 APK & KUHP Baru manuscript"

    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    # Audit every generated SINTA docx in showcase_dir
    for fname, info in generated:
        fpath = os.path.join(showcase_dir, fname)
        assert os.path.exists(fpath), f"Missing generated file: {fpath}"

        with zipfile.ZipFile(fpath, "r") as zf:
            namelist = zf.namelist()
            assert "word/header1.xml" in namelist, f"Missing OJS Word header in {fname}"
            assert "word/footer1.xml" in namelist, f"Missing OJS Word footer in {fname}"

            hdr_xml = zf.read("word/header1.xml").decode("utf-8")
            assert "https://doi.org/10." in hdr_xml, f"Missing DOI in Word header of {fname}"
            assert "ISSN" in hdr_xml, f"Missing ISSN in Word header of {fname}"

            doc_bytes = zf.read("word/document.xml")
            doc_str = doc_bytes.decode("utf-8")
            root_el = ET.fromstring(doc_bytes)

            # 1. Verify zero "AI indeks" debug banner in body
            assert "| Peringkat: SINTA" not in doc_str, f"Found forbidden AI debug banner in {fname}"
            assert "Layout: 2 Kolom" not in doc_str and "Layout: 1 Kolom" not in doc_str, f"Found layout debug text in body of {fname}"

            # 2. Verify real OpenXML superscript exists for author affiliations
            superscripts = root_el.findall(".//w:vertAlign[@w:val='superscript']", ns)
            assert len(superscripts) >= 4, f"Expected >= 4 superscript runs in {fname}, got {len(superscripts)}"

        # 3. Verify references & zero em-dashes via python-docx
        d = docx.Document(fpath)
        full_text = "\n".join(p.text for p in d.paragraphs)
        assert "\u2014" not in full_text, f"Forbidden em dash found in {fname}"

        doi_occurrences = full_text.count("https://doi.org/10.")
        min_expected_dois = 22 if str(info["sinta_rank"]) == "1" else 14
        assert doi_occurrences >= min_expected_dois, (
            f"Expected >= {min_expected_dois} live Crossref DOIs in {fname}, got {doi_occurrences}"
        )

    # Specific audit for SINTA 1 APK & KUHP Baru manuscript
    apk_docx = os.path.join(showcase_dir, "00_Jurnal_SINTA1_HukumSiber_APK_KUHP_Baru_PJIH_Unpad.docx")
    d_apk = docx.Document(apk_docx)
    apk_text = "\n".join(p.text for p in d_apk.paragraphs)
    for required_term in [
        "Unauthorized Access to Computer System",
        "Tanggung Jawab Bank atas Pengurasan Rekening Nasabah Melalui Aplikasi APK Berbahaya Setelah Berlakunya KUHP Baru",
        "BIND_ACCESSIBILITY_SERVICE",
        "Pasal 332",
        "Pasal 334",
        "POJK Nomor 22 Tahun 2023",
        "Runtime Application Self-Protection",
    ]:
        assert required_term in apk_text, f"Missing required legal/technical term '{required_term}' in SINTA 1 APK paper"
    assert len(d_apk.tables) == 3, f"Expected 3 analytical tables in SINTA 1 APK paper, got {len(d_apk.tables)}"

    # Specific audit for SINTA 1 IJAIN English manuscript
    ijain_docx = os.path.join(showcase_dir, "01_Jurnal_SINTA1_IJAIN_UAD_2Kolom.docx")
    d_ijain = docx.Document(ijain_docx)
    ijain_text = "\n".join(p.text for p in d_ijain.paragraphs)
    assert "1. INTRODUCTION" in ijain_text and "REFERENCES" in ijain_text, "SINTA 1 IJAIN must use full English headings"

    # Verify 2-column and 1-column XML structure on SINTA 4 showcase files
    docx_2col = os.path.join(showcase_dir, "04_Jurnal_SINTA4_JKI_UBSI_2Kolom.docx")
    docx_1col = os.path.join(showcase_dir, "05_Jurnal_SINTA4_JKI_UBSI_1Kolom_Biasa.docx")

    with zipfile.ZipFile(docx_2col, "r") as zf:
        root_2 = ET.fromstring(zf.read("word/document.xml"))
        media_files = [n for n in zf.namelist() if n.startswith("word/media/")]
        assert len(media_files) == 3, f"Expected 3 embedded diagrams, got {len(media_files)}"
    cols_2 = [c.attrib.get(f"{{{ns['w']}}}num") for c in root_2.findall(".//w:sectPr/w:cols", ns)]
    assert cols_2 == ["1", "2"], f"Expected ['1', '2'] columns in 2col file, got {cols_2}"

    with zipfile.ZipFile(docx_1col, "r") as zf:
        root_1 = ET.fromstring(zf.read("word/document.xml"))
    cols_1 = [c.attrib.get(f"{{{ns['w']}}}num") for c in root_1.findall(".//w:sectPr/w:cols", ns)]
    assert cols_1 == ["1", "1"], f"Expected ['1', '1'] columns in 1col file, got {cols_1}"

    inspected = inspect_existing_docx(docx_2col)
    assert inspected["tables_count"] == 3, f"Expected 3 tables in SINTA journal, got {inspected['tables_count']}"

    # 4. Verify strict 5-year recency window (2022-2026) in sinta_content_data.py
    for dataset_name, dataset in (("REFS_APK_KUHP", REFS_APK_KUHP), ("REFS_HUMAS", REFS_HUMAS)):
        for entry in dataset:
            yr_m = re.search(r"\b(19\d\d|20\d\d)\b", entry["apa_cite"])
            assert yr_m, f"Missing year in {dataset_name} id={entry['id']}"
            yr = int(yr_m.group(1))
            assert is_within_recency_window(yr, current_year=2026, window_years=5), (
                f"{dataset_name} id={entry['id']} year={yr} violates 5-year recency (2022-2026)"
            )

    # 5. Verify all showcase manuscripts and bundled examples pass antislop + Burstiness
    for fname, _ in generated:
        res = audit_manuscript(os.path.join(showcase_dir, fname), min_std=5.5, mendeley_mode=False)
        assert res["passed"], f"Antislop failed on showcase {fname}: {res['critical_issues']}"
        assert not res["warnings"], f"Antislop warnings on showcase {fname}: {res['warnings']}"

    examples_dir = os.path.join(".agents", "skills", "laporan-generator", "examples")
    for ex_name in os.listdir(examples_dir):
        if ex_name.endswith(".docx"):
            res = audit_manuscript(os.path.join(examples_dir, ex_name), min_std=5.5, mendeley_mode=False)
            assert res["passed"], f"Antislop failed on bundled example {ex_name}: {res['critical_issues']}"

    # 6. Verify failure-mode & happy-path checks in check_antislop_academic & verify_sinta_refs
    assert extract_doi("https://doi.org/10.31294/jki.v14i1.21890") == "10.31294/jki.v14i1.21890"
    assert is_within_recency_window(2022, current_year=2026, window_years=5)
    assert not is_within_recency_window(2021, current_year=2026, window_years=5)
    assert format_sinta_label(4, verified=False) == "[Level SINTA: tidak terverifikasi]"
    assert format_sinta_label(4, verified=True) == "[Peringkat: SINTA 4 - Terverifikasi]"

    # Verify multi-agent installer (Antigravity, KiloCode, OpenCode, Freebuff, Claude, Roo, Cline, Cursor, Windsurf)
    from scripts.install_agent_skills import install_all, check_status
    installed = install_all()
    assert len(installed) >= 40, f"Expected >= 40 multi-agent bundle/adapter files installed, got {len(installed)}"
    statuses = check_status()
    assert all(s["status"] == "INSTALLED" for s in statuses), f"Some agent adapters failed to install: {statuses}"

    # 7. Isolated out-of-repo execution test using ONLY bundled global skill scripts & Mendeley mode R1/R3
    with tempfile.TemporaryDirectory() as tmp_iso:
        sloppy_txt = os.path.join(tmp_iso, "sloppy.txt")
        with open(sloppy_txt, "w", encoding="utf-8") as f:
            f.write(
                "Di era digital yang berkembang pesat saat ini \u2014 bukan hanya itu, melainkan juga ini. "
                "Bukan hanya sistem ini cepat, melainkan juga murah.\n\n"
                "DAFTAR PUSTAKA\n"
                "[1] Palsu et al., 2024.\n"
            )
        slop_res = audit_manuscript(sloppy_txt, mendeley_mode=True)
        assert not slop_res["passed"], "Expected failure on em-dash + cliche + R1 violation"
        assert slop_res["em_dash_count"] == 1
        assert len(slop_res["cliche_hits"]) >= 1
        assert slop_res["r1_ref_entries_in_docx"] == 1

        uniform_txt = os.path.join(tmp_iso, "uniform.txt")
        with open(uniform_txt, "w", encoding="utf-8") as f:
            sent = "Sistem informasi publik daerah mencatat seluruh agenda kegiatan harian bagian humas instansi. "
            f.write(" ".join([sent] * 7))
        uni_res = audit_manuscript(uniform_txt, min_std=5.5)
        assert any("Burstiness rendah" in w for w in uni_res["warnings"]), f"Expected low burstiness warning, got {uni_res}"

        global_scripts_dir = os.path.join(os.path.expanduser("~"), ".gemini", "config", "skills", "laporan-generator", "scripts")
        out_mendeley = os.path.join(tmp_iso, "Naskah_Mandiri_JKI.docx")
        cp_jki = subprocess.run(
            [
                sys.executable,
                os.path.join(global_scripts_dir, "generate_sinta_journal_docx.py"),
                "--sinta", "4", "--layout", "2col", "--citation", "ieee",
                "--mendeley-mode", "--output", out_mendeley, "--yes",
            ],
            cwd=tmp_iso,
            capture_output=True,
            text=True,
        )
        assert cp_jki.returncode == 0, f"Isolated bundled JKI failed:\n{cp_jki.stdout}\n{cp_jki.stderr}"
        assert os.path.exists(out_mendeley), "Bundled JKI did not create output .docx"
        r1_audit = audit_manuscript(out_mendeley, min_std=5.5, mendeley_mode=True)
        assert r1_audit["passed"] and r1_audit["r1_ref_entries_in_docx"] == 0, f"R1 check failed: {r1_audit}"
        exported_txt = os.path.join(tmp_iso, "Naskah_Mandiri_JKI_kandidat_referensi.txt")
        assert os.path.exists(exported_txt), "Expected R3 exported .txt from --mendeley-mode"
        with open(exported_txt, "r", encoding="utf-8") as ef:
            assert "[Level SINTA: tidak terverifikasi]" in ef.read()
        with zipfile.ZipFile(out_mendeley, "r") as z_jki:
            assert "PAGE" in z_jki.read("word/footer1.xml").decode("utf-8"), "Expected PAGE field in SINTA footer"

        out_pkl = os.path.join(tmp_iso, "PKL_Mandiri.docx")
        cp_pkl = subprocess.run(
            [
                sys.executable,
                os.path.join(global_scripts_dir, "update_docx_script.py"),
                "--scaffold", "--type", "laporan", "--outline", "4",
                "--title", "ANALISIS SISTEM MANDIRI", "--author", "Penulis Contoh",
                "--nim", "00000001", "--output", out_pkl,
            ],
            cwd=tmp_iso,
            capture_output=True,
            text=True,
        )
        assert cp_pkl.returncode == 0, f"Isolated bundled PKL scaffold failed:\n{cp_pkl.stdout}\n{cp_pkl.stderr}"
        d_pkl = docx.Document(out_pkl)
        pkl_txt = "\n".join(p.text for p in d_pkl.paragraphs)
        for req_pkl in ("PERSETUJUAN", "DAFTAR SIMBOL", "BAB I PENDAHULUAN", "SURAT KETERANGAN PKL", "NILAI PRAKTIK KERJA LAPANGAN", "LEMBAR KUESIONER"):
            assert req_pkl in pkl_txt, f"Missing '{req_pkl}' in PKL scaffold"
        assert len(d_pkl.sections) == 7, f"Expected 7 sections in PKL Outline 4 scaffold, got {len(d_pkl.sections)}"
        assert d_pkl.sections[1]._sectPr.find(".//w:pgNumType", ns).attrib.get(f"{{{ns['w']}}}fmt") == "lowerRoman"
        assert d_pkl.sections[2]._sectPr.find(".//w:pgNumType", ns).attrib.get(f"{{{ns['w']}}}fmt") == "decimal"
        assert d_pkl.sections[2].different_first_page_header_footer is True
        with zipfile.ZipFile(out_pkl, "r") as z_pkl:
            pkl_hf = "\n".join(z_pkl.read(n).decode("utf-8", "ignore") for n in z_pkl.namelist() if n.startswith(("word/header", "word/footer")) and n.endswith(".xml"))
            assert "PAGE" in pkl_hf, "Expected PAGE field in PKL scaffold headers/footers"
            pkl_ext = ET.fromstring(z_pkl.read("word/document.xml")).find(".//{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent")
            assert pkl_ext is not None and round(int(pkl_ext.attrib["cx"]) / 360000.0, 1) == 4.0, "Expected 4.0 cm PKL cover logo"

        out_skripsi = os.path.join(tmp_iso, "Skripsi_UBSI_156.docx")
        cp_skr = subprocess.run(
            [
                sys.executable,
                os.path.join(global_scripts_dir, "update_docx_script.py"),
                "--scaffold", "--type", "skripsi", "--outline", "156",
                "--title", "RANCANG BANGUN SISTEM AKADEMIK", "--author", "Penulis Contoh",
                "--nim", "00000002", "--output", out_skripsi,
            ],
            cwd=tmp_iso,
            capture_output=True,
            text=True,
        )
        assert cp_skr.returncode == 0, f"Skripsi scaffold failed:\n{cp_skr.stdout}\n{cp_skr.stderr}"
        d_skr = docx.Document(out_skripsi)
        skr_txt = "\n".join(p.text for p in d_skr.paragraphs)
        for req_part in ("SKRIPSI", "SURAT PERNYATAAN KEASLIAN SKRIPSI", "PERSETUJUAN PUBLIKASI", "ABSTRAK", "ABSTRACT", "BAB I PENDAHULUAN", "BAB V PENUTUP", "DAFTAR PUSTAKA"):
            assert req_part in skr_txt, f"Missing '{req_part}' in Skripsi scaffold"
        assert "Surat Keterangan PKL" not in skr_txt, "PKL lampiran text leaked into Skripsi scaffold"
        assert round(d_skr.sections[0].left_margin.cm, 1) == 4.0 and round(d_skr.sections[0].right_margin.cm, 1) == 2.5
        assert len(d_skr.sections) == 8, f"Expected 8 sections in Skripsi Outline 156 scaffold, got {len(d_skr.sections)}"
        assert d_skr.sections[1]._sectPr.find(".//w:pgNumType", ns).attrib.get(f"{{{ns['w']}}}fmt") == "lowerRoman"
        assert d_skr.sections[2]._sectPr.find(".//w:pgNumType", ns).attrib.get(f"{{{ns['w']}}}fmt") == "decimal"
        assert d_skr.sections[2].different_first_page_header_footer is True
        with zipfile.ZipFile(out_skripsi, "r") as z_skr:
            skr_hdrs = {n: z_skr.read(n).decode("utf-8", "ignore") for n in z_skr.namelist() if n.startswith(("word/header", "word/footer")) and n.endswith(".xml")}
            all_skr_hf = "\n".join(skr_hdrs.values())
            assert "PAGE" in all_skr_hf, "Expected PAGE field in Skripsi scaffold headers/footers"
            assert 'behindDoc="1"' in all_skr_hf and "UBSI Watermark 10x10cm" in all_skr_hf, "Expected 10x10 cm behind-text watermark in Skripsi non-cover headers"
            assert "UBSI Watermark 10x10cm" not in skr_hdrs.get("word/header1.xml", ""), "Cover header must not contain watermark"
            skr_ext = ET.fromstring(z_skr.read("word/document.xml")).find(".//{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}extent")
            assert skr_ext is not None and round(int(skr_ext.attrib["cx"]) / 360000.0, 1) == 5.0, "Expected 5.0 cm Skripsi cover logo"

        # Verify SSRF scheme guard & UBSI full author formatting (--no-et-al) & LAMPIRAN em-dash check
        bad_url_res = verify_url_status("file:///C:/Windows/win.ini")
        assert not bad_url_res["ok"] and "HTTP(S)" in bad_url_res.get("error", "")
        assert "et al." not in _format_authors_apa(["A", "B", "C", "D"], no_et_al=True)
        lampiran_txt = os.path.join(tmp_iso, "lampiran.txt")
        with open(lampiran_txt, "w", encoding="utf-8") as f:
            f.write("DAFTAR PUSTAKA\n\nLAMPIRAN\nTeks lampiran mengandung em dash \u2014 wajib terdeteksi.\n")
        assert not audit_manuscript(lampiran_txt)["passed"], "Expected LAMPIRAN em-dash to fail after DAFTAR PUSTAKA"

        # Verify TOC line with DAFTAR PUSTAKA does not flip in_refs before BAB I
        toc_txt = os.path.join(tmp_iso, "toc_check.txt")
        with open(toc_txt, "w", encoding="utf-8") as f:
            f.write(
                "DAFTAR ISI\nDAFTAR PUSTAKA\t15\nBAB I PENDAHULUAN\n"
                "Paragraf ini sangat pendek. Paragraf kedua menjelaskan arsitektur perangkat lunak pemerintahan secara rinci dan terstruktur berdasarkan hasil pengamatan lapangan yang memadai.\n"
                "DAFTAR PUSTAKA\n[REFERENSI DIKELOLA VIA MENDELEY]\n"
            )
        toc_res = audit_manuscript(toc_txt, min_std=1.0, mendeley_mode=True)
        assert toc_res["passed"] and toc_res["r1_ref_entries_in_docx"] == 0, f"TOC DAFTAR PUSTAKA false positive: {toc_res}"

        # Verify --no-et-al preserves volume(issue), page in APA and full authors in IEEE
        four_author_ref = [{
            "authors": ["Satu, A.", "Dua, B.", "Tiga, C.", "Empat, D."],
            "year": 2024,
            "sinta_rank": 4,
            "sinta_verified": True,
            "title": "Uji Empat Penulis",
            "journal": "Jurnal Uji",
            "issn": "2579-633X",
            "volume": "12",
            "issue": "2",
            "page": "10-20",
            "doi": "10.31294/jki.v12i2.99999",
            "doi_url": "https://doi.org/10.31294/jki.v12i2.99999",
            "pdf_url": "https://ejournal.bsi.ac.id/test.pdf",
            "apa": "Satu, A. et al. (2024). Uji Empat Penulis. Jurnal Uji, 12(2), 10-20. https://doi.org/10.31294/jki.v12i2.99999",
            "ieee": 'Satu, A. et al., "Uji Empat Penulis," Jurnal Uji, vol. 12, no. 2, pp. 10-20, 2024, doi: 10.31294/jki.v12i2.99999.',
            "relevance": "Uji no-et-al.",
        }]
        no_etal_txt = export_refs_txt(four_author_ref, os.path.join(tmp_iso, "no_etal.txt"), no_et_al=True)
        no_etal_body = open(no_etal_txt, "r", encoding="utf-8").read()
        assert "et al." not in no_etal_body, f"Found et al. in no_et_al output: {no_etal_body}"
        assert "12(2), 10-20" in no_etal_body, f"Missing vol(issue), page in no_et_al APA: {no_etal_body}"
        assert "Empat, D." in no_etal_body.split("Format IEEE")[1], "Missing 4th author in Format IEEE"

        # Verify shared atomic_save_docx persistence boundary (.bak backup & PermissionError lock handling) + IDE recommendations
        from unittest.mock import patch
        from scripts.docx_io import atomic_save_docx
        assert os.path.exists(os.path.join(global_scripts_dir, "docx_io.py"))
        assert os.path.exists(os.path.join(os.path.expanduser("~"), ".gemini", "config", "skills", "jurnal-sinta", "scripts", "docx_io.py"))
        with open(".vscode/extensions.json", "r", encoding="utf-8") as ext_f:
            import json as _json
            ext_cfg = _json.load(ext_f)
        for rec_id in ("cweijan.vscode-office", "tomoki1207.pdf", "myriad-dreamin.tinymist"):
            assert rec_id in ext_cfg.get("recommendations", []), f"Missing IDE recommendation: {rec_id}"

        atomic_save_docx(d_skr, out_skripsi, backup=True)
        assert os.path.exists(out_skripsi + ".bak"), "Expected .bak backup on in-place atomic_save_docx(backup=True)"
        with patch("scripts.docx_io.os.replace", side_effect=PermissionError("locked by Word")):
            try:
                atomic_save_docx(d_skr, out_skripsi, backup=False)
                raise AssertionError("Expected PermissionError when target is locked")
            except PermissionError as lock_exc:
                assert "[TERKUNCI]" in str(lock_exc)
                assert os.path.exists(out_skripsi + ".tmp.docx"), "Expected staged .tmp.docx preserved on lock error"

        # Verify global humanizer-id UBSI 2026 preset + pre-filter + no BRN-002 collision
        global_hum_dir = os.path.join(os.path.expanduser("~"), ".gemini", "config", "skills", "humanizer-id")
        assert os.path.exists(os.path.join(global_hum_dir, "data", "pedoman-kampus-ubsi.json"))
        sys.path.insert(0, global_hum_dir)
        from humanizer_id.engine import _read_text_file_safely, audit_text, load_data
        k_dict, g_dict, c_dict = load_data("ubsi")
        sample_id = (
            "Penulis Contoh1*, Penulis Pendamping Contoh2\n"
            "ABSTRACT - This study evaluates coverage and system design.\n"
            "Keywords: cache, backend\n"
            "Tinjauan Pustaka membahas Landasan Teori serta Hasil dan Pembahasan penelitian.\n"
            "Data2 mahasiswa yg terdaftar di https://contoh.blogspot.com, dll.\n"
        )
        hum_res = audit_text(sample_id, k_dict, g_dict, c_dict, preset="akademik")
        hum_ids = {r["id"] for r in hum_res}
        assert not any(rid.startswith("BRN-") for rid in hum_ids), f"BRN false positive under akademik preset: {hum_ids}"
        assert "KAMPUS-UBSI-02" in hum_ids and "KAMPUS-UBSI-03" in hum_ids and "KAMPUS-UBSI-04" in hum_ids
        assert not any(r["baris"] in (1, 2, 3) for r in hum_res), f"Metadata/ABSTRACT pre-filter failed: {hum_res}"
        fp_res = audit_text(
            "Puji syukur ke hadirat Tuhan Yang Maha Esa atas terselesaikannya laporan (Putri & Afrilia, 2023).",
            k_dict, g_dict, c_dict, preset="akademik",
        )
        fp_ids = {r["id"] for r in fp_res}
        assert "EYD-023" not in fp_ids and "JRN-007" not in fp_ids, f"False positive in humanizer-id: {fp_res}"
        try:
            _read_text_file_safely(out_skripsi)
            raise AssertionError("Expected binary .docx rejection in humanizer-id")
        except ValueError:
            pass

        sample_ref = [{
            "authors": ["Hasanudin, T. A."],
            "year": 2026,
            "sinta_rank": 5,
            "sinta_verified": True,
            "title": "Contoh Pengujian Dosir Mendeley",
            "journal": "Indonesia of Journal Business Law",
            "issn": "2809-8439",
            "volume": "5",
            "issue": "1",
            "page": "99-115",
            "doi_url": "https://doi.org/10.47709/ijbl.v5i1.7476",
            "pdf_url": "https://jurnal.itscience.org/index.php/ijbl/article/download/7476/5496",
            "apa": "Hasanudin, T. A. (2026). Contoh.",
            "ieee": 'T. A. Hasanudin, "Contoh," 2026.',
            "relevance": "Uji dosir.",
        }]
        txt_dosir = export_refs_txt(sample_ref, os.path.join(tmp_iso, "dosir.txt"), target_doc="JURNAL.docx")
        docx_dosir = build_dossier_docx(sample_ref, os.path.join(tmp_iso, "dosir.docx"), target_doc="JURNAL.docx")
        assert os.path.exists(txt_dosir) and os.path.exists(docx_dosir)
        assert audit_manuscript(docx_dosir)["passed"]

        # Verify SINTA 1-6 16,617 journal catalog + MCP JSON-RPC handler (happy-path & failure-mode)
        from scripts.sinta_garuda_mcp import (
            handle_mcp_request,
            norm_issn,
            sinta_find_verified_references,
            sinta_lookup_journal,
            sinta_search_journals,
            sinta_stats_summary,
        )
        assert os.path.exists(os.path.join(global_scripts_dir, "sinta_garuda_mcp.py"))
        assert os.path.exists(os.path.join(os.path.dirname(global_scripts_dir), "presets", "sinta-catalog.json.gz"))
        assert norm_issn("2579-633X") == "2579-633X" and norm_issn("2579633x") == "2579-633X"
        assert norm_issn("Jurnal Vol 2024 1234") == "", "Expected non-ISSN string with 8 digits to be rejected"
        stats = sinta_stats_summary()
        assert stats["total_journals"] >= 16600, f"Expected >= 16600 SINTA journals, got {stats['total_journals']}"
        jki_lookup = sinta_lookup_journal("2579-633X")
        assert jki_lookup["verified"] and jki_lookup["journal"]["sinta_rank"] == 4
        vol_lookup = sinta_lookup_journal("Jurnal Khatulistiwa Informatika Vol. 12 No. 1 (2025)")
        assert vol_lookup["verified"] and vol_lookup["journal"]["sinta_rank"] == 4
        unknown_lookup = sinta_lookup_journal("0000-0000")
        assert not unknown_lookup["verified"] and unknown_lookup["r3_label"] == "[Level SINTA: tidak terverifikasi]"
        srch_s4 = sinta_search_journals(query="informatika", sinta_rank="4", limit=5)
        assert srch_s4["returned"] == 5 and all(x["sinta_rank"] == 4 for x in srch_s4["results"])
        mcp_init = handle_mcp_request({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
        assert mcp_init["result"]["serverInfo"]["name"] == "sinta-garuda"
        mcp_tools = handle_mcp_request({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        assert len(mcp_tools["result"]["tools"]) == 5
        mcp_err = handle_mcp_request({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "invalid_tool"}})
        assert mcp_err["error"]["code"] == -32601
        mcp_bad_req = handle_mcp_request({"jsonrpc": "2.0", "id": 4})
        assert mcp_bad_req["error"]["code"] == -32600
        try:
            sinta_find_verified_references("ab", source="garuda")
            raise AssertionError("Expected RuntimeError when GARUDA fails on <3 char query")
        except RuntimeError as rte:
            assert "garuda:" in str(rte)

    # Verify skill, rule, and multi-agent command files exist and have no forbidden em-dashes
    skill_paths = [
        ".agents/skills/laporan-generator/SKILL.md",
        ".agents/skills/laporan-generator/resources/matriks-metodologi-ilmiah.md",
        ".agents/skills/laporan-generator/resources/antislop-akademik-id.md",
        ".agents/skills/jurnal-sinta/SKILL.md",
        ".agents/skills/mode-ilmiah/SKILL.md",
        ".agents/rules/sinta-journal-prompt.md",
        ".kilocode/workflows/laporan-generator.md",
        ".kilocode/workflows/jurnal-sinta.md",
        ".opencode/commands/laporan-generator.md",
        ".opencode/commands/jurnal-sinta.md",
        ".freebuff/commands/laporan-generator.md",
        ".freebuff/commands/jurnal-sinta.md",
        ".claude/commands/laporan-generator.md",
        ".claude/commands/jurnal-sinta.md",
        "AGENTS.md",
    ]
    for sp in skill_paths:
        assert os.path.exists(sp), f"Missing agent customization file: {sp}"
        with open(sp, "r", encoding="utf-8") as f:
            txt = f.read()
        assert "\u2014" not in txt, f"Forbidden em dash found in {sp}"

    print("PASS: All 6 SINTA presets, 9 SINTA showcase manuscripts, 2022-2026 refs, antislop/Burstiness linter, isolated global bundle execution (Mendeley R1/R3 + PKL), and multi-agent skills verified.")


if __name__ == "__main__":
    verify_sinta_system()
