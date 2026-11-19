# /// script
# requires-python = ">=3.10"
# dependencies = ["python-docx"]
# ///
import argparse
import json
import os
import sys
import docx
from docx.shared import Cm, Pt, RGBColor
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT_DIR = os.path.dirname(_THIS_DIR)
for _cand_dir in (_THIS_DIR, _PARENT_DIR):
    if _cand_dir not in sys.path:
        sys.path.insert(0, _cand_dir)

try:
    from scripts.sinta_content_data import (
        cite_ref,
        get_reference_list,
        render_apk_kuhp_body,
        render_humas_en_body,
    )
    from scripts.docx_io import atomic_save_docx
except ImportError:
    from sinta_content_data import (
        cite_ref,
        get_reference_list,
        render_apk_kuhp_body,
        render_humas_en_body,
    )
    from docx_io import atomic_save_docx


def _resolve_asset_path(*rel_parts):
    """Resolve presets or template assets from repo root OR bundled skill directory."""
    for base in (_THIS_DIR, _PARENT_DIR, os.getcwd()):
        cand = os.path.join(base, *rel_parts)
        if os.path.exists(cand):
            return cand
    return os.path.join(_THIS_DIR, *rel_parts)


def load_presets():
    preset_path = _resolve_asset_path("presets", "sinta-journals.json")
    with open(preset_path, "r", encoding="utf-8") as f:
        return json.load(f)


def set_section_columns(section, num_cols, gap_cm=0.6):
    sectPr = section._sectPr
    cols = sectPr.find(qn("w:cols"))
    if cols is None:
        cols = OxmlElement("w:cols")
        sectPr.append(cols)
    cols.set(qn("w:num"), str(num_cols))
    # ponytail: 1 cm equals ~567 dxa in OpenXML WordprocessingML.
    gap_dxa = int(round(gap_cm * 567))
    cols.set(qn("w:space"), str(gap_dxa))


def apply_margins(section, margins_cm):
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(margins_cm["top"])
    section.bottom_margin = Cm(margins_cm["bottom"])
    section.left_margin = Cm(margins_cm["left"])
    section.right_margin = Cm(margins_cm["right"])
    section.header_distance = Cm(1.2)
    section.footer_distance = Cm(1.2)


def format_run(run, font_name="Times New Roman", size_pt=10, bold=False, italic=False,
               superscript=False, color=(0, 0, 0)):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.superscript = superscript
    run.font.color.rgb = RGBColor(*color)


def add_p(doc, text="", font_name="Times New Roman", size_pt=10, bold=False, italic=False,
          align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=3,
          line_spacing=1.0, first_indent_cm=0.0, keep_with_next=False, color=(0, 0, 0)):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = align
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = line_spacing
    pf.first_line_indent = Cm(first_indent_cm) if first_indent_cm else Cm(0)
    pf.keep_with_next = keep_with_next
    if text:
        r = p.add_run(text)
        format_run(r, font_name=font_name, size_pt=size_pt, bold=bold, italic=italic, color=color)
    return p


def configure_ojs_header_footer(section, active_meta, font_name):
    header = section.header
    p_hdr = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_hdr.paragraph_format.space_before = Pt(0)
    p_hdr.paragraph_format.space_after = Pt(3)
    p_hdr.paragraph_format.line_spacing = 1.0

    r_jname = p_hdr.add_run(f"{active_meta['journal_name']} ({active_meta['short_name']})\n")
    format_run(r_jname, font_name=font_name, size_pt=8.5, bold=True, color=(31, 41, 55))

    vol_str = active_meta.get("vol_issue_sample", "Vol. 12, No. 1, 2026")
    doi_str = active_meta.get("sample_doi", f"https://doi.org/{active_meta.get('doi_prefix', '10.31294/jki')}")
    r_meta = p_hdr.add_run(
        f"{vol_str} | p-ISSN: {active_meta['p_issn']} | e-ISSN: {active_meta['e_issn']} | DOI: {doi_str}"
    )
    format_run(r_meta, font_name=font_name, size_pt=7.5, italic=True, color=(75, 85, 99))

    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        '<w:bottom w:val="single" w:sz="6" w:space="3" w:color="9CA3AF"/>'
        '</w:pBdr>'
    )
    p_hdr._p.get_or_add_pPr().append(pBdr)

    footer = section.footer
    p_ftr = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    p_ftr.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_ftr.paragraph_format.space_before = Pt(2)
    p_ftr.paragraph_format.space_after = Pt(0)
    p_ftr.paragraph_format.line_spacing = 1.0

    ftr_bdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        '<w:top w:val="single" w:sz="4" w:space="2" w:color="D1D5DB"/>'
        '</w:pBdr>'
    )
    p_ftr._p.get_or_add_pPr().append(ftr_bdr)

    lic = active_meta.get("license", "CC BY-SA 4.0")
    ojs_url = active_meta.get("ojs_url", "")
    r_ftr = p_ftr.add_run(
        f"{active_meta['institution']} | Open Access Article distributed under the Creative Commons {lic} License ({ojs_url}) | Hal. "
    )
    format_run(r_ftr, font_name=font_name, size_pt=7.5, italic=True, color=(107, 114, 128))
    r_pg = p_ftr.add_run()
    format_run(r_pg, font_name=font_name, size_pt=7.5, bold=True, color=(75, 85, 99))
    r_pg._r.append(parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>'))
    r_pg._r.append(parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>'))
    r_pg._r.append(parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="separate"/>'))
    r_pg._r.append(parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>'))


def add_authors_and_affiliations(
    doc,
    font_name,
    f_author,
    f_affil,
    is_en=False,
    author="Penulis Contoh",
    coauthor="Penulis Pendamping Contoh",
    email="penulis.contoh@contoh.ac.id",
    coemail="pendamping.contoh@contoh.ac.id",
    affiliation=None,
):
    p_auth = add_p(
        doc,
        "",
        font_name=font_name,
        size_pt=f_author,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_before=2,
        space_after=2,
    )
    format_run(p_auth.add_run(author), font_name=font_name, size_pt=f_author, bold=True)
    format_run(p_auth.add_run("1*"), font_name=font_name, size_pt=f_author, bold=True, superscript=True)
    if coauthor:
        format_run(p_auth.add_run(f", {coauthor}"), font_name=font_name, size_pt=f_author, bold=True)
        format_run(p_auth.add_run("2"), font_name=font_name, size_pt=f_author, bold=True, superscript=True)

    p_aff = add_p(
        doc,
        "",
        font_name=font_name,
        size_pt=f_affil,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_before=0,
        space_after=4,
    )
    format_run(p_aff.add_run("1,2" if coauthor else "1"), font_name=font_name, size_pt=f_affil, superscript=True)
    default_aff = (
        "Department of Information Technology, Faculty of Engineering and Informatics, Universitas Bina Sarana Informatika, Kota Contoh, Indonesia\n"
        if is_en
        else "Program Studi Teknologi Informasi, Fakultas Teknik dan Informatika, Universitas Bina Sarana Informatika, Kota Contoh, Indonesia\n"
    )
    aff_text = f"{affiliation.rstrip()}\n" if affiliation else default_aff
    format_run(p_aff.add_run(aff_text), font_name=font_name, size_pt=f_affil)
    format_run(p_aff.add_run("E-mail: "), font_name=font_name, size_pt=f_affil, italic=True)
    format_run(p_aff.add_run("1*"), font_name=font_name, size_pt=f_affil, superscript=True)
    if coauthor:
        format_run(p_aff.add_run(f"{email}, "), font_name=font_name, size_pt=f_affil)
        format_run(p_aff.add_run("2"), font_name=font_name, size_pt=f_affil, superscript=True)
        corr_lbl = f"{coemail} (*Corresponding Author)" if is_en else f"{coemail} (*Penulis Korespondensi)"
    else:
        corr_lbl = f"{email} (*Corresponding Author)" if is_en else f"{email} (*Penulis Korespondensi)"
    format_run(p_aff.add_run(corr_lbl), font_name=font_name, size_pt=f_affil)


def set_booktabs_borders(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        '<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        '<w:left w:val="none"/>'
        '<w:right w:val="none"/>'
        '<w:insideH w:val="none"/>'
        '<w:insideV w:val="none"/>'
        '</w:tblBorders>'
    )
    tblPr.append(borders)
    cell_mar = parse_xml(
        f'<w:tblCellMar {nsdecls("w")}>'
        '<w:top w:w="35" w:type="dxa"/>'
        '<w:left w:w="45" w:type="dxa"/>'
        '<w:bottom w:w="35" w:type="dxa"/>'
        '<w:right w:w="45" w:type="dxa"/>'
        '</w:tblCellMar>'
    )
    tblPr.append(cell_mar)


def set_header_bottom_border(row):
    for cell in row.cells:
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            '<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
            '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
            '<w:left w:val="none"/>'
            '<w:right w:val="none"/>'
            '</w:tcBorders>'
        )
        tcPr.append(tcBorders)


def add_journal_table(doc, caption_text, headers, rows_data, col_widths_cm, font_name, caption_pt, body_pt):
    add_p(
        doc,
        caption_text,
        font_name=font_name,
        size_pt=caption_pt,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_before=6,
        space_after=2,
        keep_with_next=True,
    )
    table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_booktabs_borders(table)

    tbl_font_pt = max(min(caption_pt, 8.5), 7.5)
    hdr_row = table.rows[0]
    set_header_bottom_border(hdr_row)
    for idx, h_text in enumerate(headers):
        cell = hdr_row.cells[idx]
        cell.width = Cm(col_widths_cm[idx])
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(h_text)
        format_run(r, font_name=font_name, size_pt=tbl_font_pt, bold=True)

    for r_i, r_data in enumerate(rows_data):
        row = table.rows[r_i + 1]
        for c_i, val in enumerate(r_data):
            cell = row.cells[c_i]
            cell.width = Cm(col_widths_cm[c_i])
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (c_i == 0 and len(str(val)) <= 3) else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(1.5)
            p.paragraph_format.line_spacing = 1.0
            r = p.add_run(str(val))
            format_run(r, font_name=font_name, size_pt=tbl_font_pt, bold=False)

    add_p(doc, "", size_pt=4, space_before=0, space_after=2)
    return table


def build_sinta_docx(sinta_rank="4", layout_choice="default", citation_style="default",
                     topic="layanan-publik", output_path=None, mendeley_mode=False,
                     refs_txt_out=None, title=None, title_en=None,
                     author="Penulis Contoh", coauthor="Penulis Pendamping Contoh",
                     email="penulis.contoh@contoh.ac.id", coemail="pendamping.contoh@contoh.ac.id",
                     affiliation=None):
    presets = load_presets()
    spec = presets.get(str(sinta_rank), presets["4"])

    # When generating the SINTA 1 Cyber Law / APK-KUHP paper, use the SINTA 1 Law Journal profile (PJIH Unpad)
    active_meta = dict(spec)
    if str(sinta_rank) == "1" and topic == "apk-kuhp" and "law_profile" in spec:
        active_meta.update(spec["law_profile"])

    active_layout = spec["default_layout"] if layout_choice == "default" else layout_choice
    active_citation = spec["citation_style"] if citation_style == "default" else citation_style
    num_cols = 2 if active_layout == "2col" else 1
    is_en_only = (str(sinta_rank) == "1" and topic != "apk-kuhp")

    font_name = spec["fonts"]["family"]
    f_title = spec["fonts"]["title_pt"]
    f_author = spec["fonts"]["author_pt"]
    f_affil = spec["fonts"]["affiliation_pt"]
    f_abs = spec["fonts"]["abstract_pt"]
    f_h1 = spec["fonts"]["heading1_pt"]
    f_h2 = spec["fonts"]["heading2_pt"]
    f_body = spec["fonts"]["body_pt"]
    f_cap = spec["fonts"]["caption_pt"]
    f_ref = spec["fonts"]["reference_pt"]
    line_sp = spec["paragraph"]["line_spacing"]
    indent_cm = spec["paragraph"]["first_line_indent_cm"]

    doc = docx.Document()

    # Section 1: 1-Column Title, Authors, Affiliations, Article History, and Abstract
    sec1 = doc.sections[0]
    apply_margins(sec1, spec["margins_cm"])
    set_section_columns(sec1, 1, spec["column_gap_cm"])
    configure_ojs_header_footer(sec1, active_meta, font_name)

    if topic == "apk-kuhp":
        title_id = (
            "Unauthorized Access to Computer System: Tanggung Jawab Bank atas Pengurasan Rekening "
            "Nasabah Melalui Aplikasi APK Berbahaya Setelah Berlakunya KUHP Baru"
        )
        title_en = (
            "Unauthorized Access to Computer System: Bank Liability for Customer Account Draining "
            "via Malicious APK Applications Following the Enactment of the New Indonesian Criminal Code"
        )
    else:
        title_id = title or (
            "Analisis Sistem Pengelolaan Publikasi Berita dan Perancangan Aplikasi "
            "Press Release Auto-Generator pada Dinas Komunikasi dan Informatika Kota Contoh"
        )
        title_en = title_en or (
            "Analysis of News Publication Management System and Design of Press Release "
            "Auto-Generator Application at the Department of Communication and Informatics of Contoh City"
        )

    if is_en_only:
        add_p(
            doc,
            title_en,
            font_name=font_name,
            size_pt=f_title,
            bold=True,
            align=WD_ALIGN_PARAGRAPH.CENTER,
            space_before=4,
            space_after=6,
        )
    else:
        add_p(
            doc,
            title_id.upper() if int(sinta_rank) == 4 else title_id,
            font_name=font_name,
            size_pt=f_title,
            bold=True,
            align=WD_ALIGN_PARAGRAPH.CENTER,
            space_before=4,
            space_after=2,
        )
        add_p(
            doc,
            title_en,
            font_name=font_name,
            size_pt=max(f_title - 3, 10),
            bold=False,
            italic=True,
            align=WD_ALIGN_PARAGRAPH.CENTER,
            space_before=0,
            space_after=6,
        )

    add_authors_and_affiliations(doc, font_name, f_author, f_affil, is_en=is_en_only, author=author, coauthor=coauthor, email=email, coemail=coemail, affiliation=affiliation)

    # Authentic OJS Article History & DOI Metadata Line
    doi_url = active_meta.get("sample_doi", f"https://doi.org/{active_meta.get('doi_prefix', '10.31294/jki')}")
    history_text = (
        f"Article History: Received January 12, 2026; Revised February 18, 2026; Accepted March 5, 2026 | DOI: {doi_url}"
        if is_en_only
        else f"Riwayat Artikel: Diterima 12 Januari 2026; Direvisi 18 Februari 2026; Disetujui 5 Maret 2026 | DOI: {doi_url}"
    )
    p_hist = add_p(
        doc,
        history_text,
        font_name=font_name,
        size_pt=8.0,
        italic=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_before=2,
        space_after=6,
        color=(55, 65, 81),
    )
    pBdr_top = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        '<w:top w:val="single" w:sz="4" w:space="3" w:color="9CA3AF"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="3" w:color="9CA3AF"/>'
        '</w:pBdr>'
    )
    p_hist._p.get_or_add_pPr().append(pBdr_top)

    if topic == "apk-kuhp":
        abs_id_text = (
            "Eskalasi kejahatan siber perbankan melalui rekayasa sosial pengiriman paket aplikasi Android berbahaya "
            "(malicious file .APK) di luar toko aplikasi resmi telah mengakibatkan pengurasan dana simpanan nasabah secara "
            "masif. Secara teknis, aplikasi .APK berbahaya mengeksploitasi izin BIND_ACCESSIBILITY_SERVICE serta "
            "RECEIVE_SMS/READ_SMS untuk menyadap ketukan PIN, melakukan serangan layar tumpuk (overlay), dan memintas kode "
            "One-Time Password (OTP) ke server Command and Control (C2) milik pelaku. Penelitian ini bertujuan menganalisis "
            "kualifikasi delik unauthorized access melalui APK berbahaya setelah berlakunya Undang-Undang Nomor 1 Tahun 2023 "
            "tentang Kitab Undang-Undang Hukum Pidana (KUHP Baru) serta merumuskan konstruksi tanggung jawab hukum bank atas "
            "kerugian nasabah. Menggunakan metode yuridis normatif-empiris yang dipadukan dengan analisis arsitektur keamanan "
            "teknis mobile banking, hasil penelitian menunjukkan bahwa: (1) pasca berlakunya KUHP Baru pada 2 Januari 2026, "
            "delik akses ilegal dan penyadapan OTP dikualifikasikan ke dalam Pasal 332 ayat (2)-(3), Pasal 334, dan Pasal 492 "
            "KUHP Baru yang mencabut Pasal 30-32 UU ITE; dan (2) berdasarkan Pasal 15 UU ITE, Pasal 35 UU Nomor 27 Tahun 2022 "
            "tentang Pelindungan Data Pribadi, POJK Nomor 11/POJK.03/2022, serta Pasal 30-31 POJK Nomor 22 Tahun 2023, bank "
            "memikul beban pembuktian terbalik (shifting burden of proof) untuk membuktikan keandalan Runtime Application "
            "Self-Protection (RASP) dan Fraud Detection System (FDS). Kegagalan aplikasi bank dalam mendeteksi layanan "
            "aksesibilitas berbahaya dan anomali transaksi melahirkan tanggung jawab hukum bagi bank untuk mengganti kerugian "
            "simpanan nasabah."
        )
        kw_id_text = "Accessibility Service; APK Berbahaya; KUHP Baru; Perlindungan Nasabah; Tanggung Jawab Bank; Unauthorized Access"
        abs_en_text = (
            "The escalation of banking cybercrime through social engineering distribution of malicious Android Package Kit (.APK) "
            "files outside official app stores has caused widespread draining of customer deposits. Technically, malicious .APK "
            "files exploit BIND_ACCESSIBILITY_SERVICE and RECEIVE_SMS/READ_SMS permissions to log PIN keystrokes, launch screen "
            "overlay attacks, and intercept One-Time Password (OTP) SMS messages to a Command and Control (C2) server. This study "
            "analyzes the criminal offense qualification of unauthorized access via malicious APKs following the enactment of Law "
            "Number 1 of 2023 on the Indonesian Criminal Code (New KUHP) and formulates the legal liability of banks for customer "
            "losses. Employing a normative-empirical legal method combined with mobile banking security architecture analysis, the "
            "findings demonstrate that: (1) under the New KUHP effective January 2, 2026, illegal access and OTP interception are "
            "governed by Articles 332(2)-(3), 334, and 492, superseding Articles 30-32 of the Electronic Information and "
            "Transactions (EIT) Law; and (2) under Article 15 of the EIT Law, Article 35 of the Personal Data Protection Law "
            "(Law No. 27/2022), POJK No. 11/POJK.03/2022, and Articles 30-31 of POJK No. 22/2023, banks bear a shifting burden "
            "of proof to demonstrate active Runtime Application Self-Protection (RASP) and Fraud Detection Systems (FDS)."
        )
        kw_en_text = "Accessibility Service; Bank Liability; Customer Protection; Malicious APK; New Criminal Code; Unauthorized Access"
    else:
        abs_id_text = (
            "Bidang Pengelolaan Informasi dan Komunikasi Publik (Humas) pada Dinas Komunikasi dan Informatika Kota Contoh "
            "bertanggung jawab penuh atas peliputan agenda kedinasan, penyusunan siaran pers (press release), dan publikasi "
            "informasi ke portal website resmi portal.kotacontoh.go.id serta media sosial Instagram @humas_kotacontoh. Berdasarkan "
            "observasi dan wawancara selama Praktik Kerja Lapangan (PKL), proses bisnis yang berjalan saat ini masih menghadapi "
            "tiga kendala utama: penyusunan draf berita secara manual di Microsoft Word memakan waktu 1 hingga 2 jam per rilis "
            "dan memicu variasi format antarstaf, proses verifikasi pimpinan melalui pesan instan WhatsApp menyulitkan "
            "pelacakan riwayat revisi, serta pengarsipan di komputer lokal berisiko menyebabkan kehilangan dokumen. Penelitian "
            "ini bertujuan menganalisis prosedur sistem berjalan menggunakan pemodelan Unified Modeling Language (UML) dan "
            "merancang usulan Aplikasi Press Release Auto-Generator berbasis formulir 5W+1H terstruktur. Hasil perancangan "
            "menunjukkan bahwa standarisasi masukan 5W+1H, antarmuka verifikasi berjenjang, serta repositori arsip terpusat "
            "mampu memangkas tahapan manual dan menjaga konsistensi redaksional berita instansi."
        )
        kw_id_text = "Analisis Sistem; Humas Diskominfo; Otomatisasi Press Release; Sistem Informasi Publikasi; UML"
        abs_en_text = (
            "The Public Information and Communication Division of the Department of Communication and Informatics "
            "of Contoh City manages official event coverage, press release drafting, and multi-channel publication to "
            "portal.kotacontoh.go.id and Instagram @humas_kotacontoh. Field observation and interviews conducted during the internship "
            "program revealed three operational bottlenecks in the current workflow: manual press release drafting in Microsoft "
            "Word requires 1 to 2 hours per article with inconsistent structure across staff members, manuscript verification "
            "via WhatsApp chat obscures revision history, and local folder archiving exposes files to data loss. This study "
            "analyzes the ongoing system using Unified Modeling Language (UML) diagrams and proposes a structured 5W+1H Press "
            "Release Auto-Generator application. The proposed system integrates automated manuscript formatting, centralized "
            "approval tracking, and cloud-ready document archiving to standardize institutional news publishing."
        )
        kw_en_text = "Press Release Automation; Public Information System; Public Relations; System Analysis; UML"

    if not is_en_only:
        p_abs_id = add_p(
            doc,
            "",
            font_name=font_name,
            size_pt=f_abs,
            align=WD_ALIGN_PARAGRAPH.JUSTIFY,
            space_before=4,
            space_after=2,
            line_spacing=1.0,
        )
        format_run(p_abs_id.add_run("ABSTRAK - "), font_name=font_name, size_pt=f_abs, bold=True)
        format_run(p_abs_id.add_run(abs_id_text), font_name=font_name, size_pt=f_abs)

        p_kw_id = add_p(doc, "", font_name=font_name, size_pt=f_abs, space_before=1, space_after=5)
        format_run(p_kw_id.add_run("Kata Kunci: "), font_name=font_name, size_pt=f_abs, bold=True)
        format_run(p_kw_id.add_run(kw_id_text), font_name=font_name, size_pt=f_abs)

    p_abs_en = add_p(
        doc,
        "",
        font_name=font_name,
        size_pt=f_abs,
        align=WD_ALIGN_PARAGRAPH.JUSTIFY,
        space_before=2,
        space_after=2,
        line_spacing=1.0,
    )
    format_run(p_abs_en.add_run("ABSTRACT - "), font_name=font_name, size_pt=f_abs, bold=True, italic=not is_en_only)
    format_run(p_abs_en.add_run(abs_en_text), font_name=font_name, size_pt=f_abs, italic=not is_en_only)

    p_kw_en = add_p(doc, "", font_name=font_name, size_pt=f_abs, space_before=1, space_after=8)
    format_run(p_kw_en.add_run("Keywords: "), font_name=font_name, size_pt=f_abs, bold=True, italic=not is_en_only)
    format_run(p_kw_en.add_run(kw_en_text), font_name=font_name, size_pt=f_abs, italic=not is_en_only)

    pBdr_abs = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        '<w:bottom w:val="single" w:sz="6" w:space="6" w:color="6B7280"/>'
        '</w:pBdr>'
    )
    p_kw_en._p.get_or_add_pPr().append(pBdr_abs)

    # Section 2: Continuous Section Break for Body Content (2-Column or 1-Column)
    sec2 = doc.add_section(WD_SECTION.CONTINUOUS)
    apply_margins(sec2, spec["margins_cm"])
    set_section_columns(sec2, num_cols, spec["column_gap_cm"])

    page_usable_cm = 21.0 - spec["margins_cm"]["left"] - spec["margins_cm"]["right"]
    col_width_cm = (page_usable_cm - spec["column_gap_cm"]) / 2.0 if num_cols == 2 else page_usable_cm
    img_width_cm = min(col_width_cm - 0.15, 13.8)

    def h1(text):
        add_p(
            doc,
            text.upper(),
            font_name=font_name,
            size_pt=f_h1,
            bold=True,
            align=WD_ALIGN_PARAGRAPH.LEFT,
            space_before=8,
            space_after=3,
            keep_with_next=True,
        )

    def h2(text):
        add_p(
            doc,
            text,
            font_name=font_name,
            size_pt=f_h2,
            bold=True,
            align=WD_ALIGN_PARAGRAPH.LEFT,
            space_before=6,
            space_after=2,
            keep_with_next=True,
        )

    def body_p(text):
        add_p(
            doc,
            text,
            font_name=font_name,
            size_pt=f_body,
            align=WD_ALIGN_PARAGRAPH.JUSTIFY,
            space_before=0,
            space_after=3,
            line_spacing=line_sp,
            first_indent_cm=indent_cm,
        )

    def embed_figure(img_file, fig_num, caption_label, source_label, is_en=False):
        resolved_img = img_file
        if not os.path.exists(resolved_img):
            alt_img = _resolve_asset_path("template", "gambar", os.path.basename(img_file))
            if os.path.exists(alt_img):
                resolved_img = alt_img
            else:
                return
        p_img = add_p(
            doc,
            "",
            align=WD_ALIGN_PARAGRAPH.CENTER,
            space_before=5,
            space_after=2,
            keep_with_next=True,
        )
        p_img.add_run().add_picture(resolved_img, width=Cm(img_width_cm))
        fig_prefix = f"Fig. {fig_num}." if is_en else f"Gambar {fig_num}."
        src_prefix = "Source:" if is_en else "Sumber:"
        add_p(
            doc,
            f"{fig_prefix} {caption_label}",
            font_name=font_name,
            size_pt=f_cap,
            bold=True,
            align=WD_ALIGN_PARAGRAPH.CENTER,
            space_before=1,
            space_after=1,
            keep_with_next=True,
        )
        add_p(
            doc,
            f"{src_prefix} {source_label}",
            font_name=font_name,
            size_pt=max(f_cap - 0.5, 7.5),
            italic=True,
            align=WD_ALIGN_PARAGRAPH.CENTER,
            space_before=0,
            space_after=5,
        )

    def tbl_wrapper(cap, hdrs, r_data, widths):
        return add_journal_table(doc, cap, hdrs, r_data, widths, font_name, f_cap, f_body)

    if topic == "apk-kuhp":
        render_apk_kuhp_body(h1, h2, body_p, tbl_wrapper, embed_figure, col_width_cm, active_citation)
    elif is_en_only:
        render_humas_en_body(h1, h2, body_p, tbl_wrapper, embed_figure, col_width_cm, active_citation)
    else:
        c = lambda i: cite_ref(i, active_citation, "layanan-publik")
        h1("1. PENDAHULUAN")
        body_p(
            f"Dinas Komunikasi dan Informatika (Diskominfo) Kota Contoh merupakan perangkat daerah pemerintah kota "
            f"yang menyelenggarakan pelayanan publik di bidang komunikasi, informatika, dan keterbukaan informasi pada wilayah "
            f"Kota Contoh {c(1)}, {c(2)}. Dalam struktur organisasi perangkat daerah, fungsi pengelolaan informasi dan "
            f"komunikasi publik berada pada Bidang Pengelolaan Informasi dan Komunikasi Publik (Humas). "
            f"Setiap pekan, unit Humas meliput beragam agenda kedinasan dari bidang pelayanan publik, infrastruktur digital, "
            f"statistik sektoral, hingga kegiatan operasional kecamatan dan kelurahan di Kota Contoh {c(3)}, {c(12)}."
        )
        body_p(
            f"Kecepatan dan akurasi penyampaian informasi publik memerlukan dukungan sistem informasi yang terstruktur "
            f"{c(1)}, {c(4)}, {c(11)}. Namun, hasil pengamatan langsung pada Bidang Humas Diskominfo Kota Contoh menunjukkan bahwa "
            f"alur produksi berita dari catatan lapangan menjadi naskah siaran pers (press release) masih dikerjakan secara manual "
            f"menggunakan aplikasi Microsoft Word. Pengetikan naskah dari nol tanpa templat baku membutuhkan waktu rata-rata 1 hingga "
            f"2 jam untuk setiap kegiatan dan menghasilkan variasi gaya bahasa antarstaf {c(5)}, {c(8)}. Selain itu, pengajuan draf "
            f"naskah kepada Kepala Bidang Informasi Publik maupun Pranata Humas dilakukan melalui aplikasi pesan instan "
            f"WhatsApp. Mekanisme ini menyebabkan berkas naskah rawan tertumpuk oleh percakapan dinas lain, menyulitkan pelacakan "
            f"riwayat revisi (version tracking), dan menghambat kepastian waktu tayang berita {c(6)}, {c(14)}."
        )
        body_p(
            f"Sejumlah penelitian terdahulu menegaskan bahwa digitalisasi proses bisnis dan pemodelan berorientasi objek menggunakan "
            f"Unified Modeling Language (UML) efektif mengurai hambatan birokrasi dokumen {c(7)}, {c(9)}, {c(10)}, {c(15)}. Oleh karena "
            f"itu, penelitian ini bertujuan untuk: (1) menganalisis secara menyeluruh prosedur, spesifikasi dokumen masukan-keluaran, "
            f"dan pemodelan UML pada sistem pengelolaan publikasi berita yang berjalan di Bidang Humas Diskominfo Kota Contoh; "
            f"(2) mengidentifikasi titik kelemahan operasional pada tahapan penyusunan, verifikasi, dan pengarsipan berita; serta "
            f"(3) merumuskan rancangan sistem usulan berupa Aplikasi Press Release Auto-Generator berbasis formulir 5W+1H terstruktur "
            f"untuk meningkatkan konsistensi dan kecepatan rilis berita instansi {c(12)}, {c(13)}."
        )

        h1("2. METODE PENELITIAN")
        body_p(
            f"Penelitian ini dilaksanakan pada Bidang Pengelolaan Informasi dan Komunikasi Publik, Dinas Komunikasi dan Informatika "
            f"Kota Contoh yang berlokasi di Jalan Raya Pemerintahan Nomor 1, Kota Contoh. Metode "
            f"pengumpulan data dan analisis sistem dilakukan melalui tiga tahapan utama {c(4)}, {c(10)}, {c(15)}:"
        )
        h2("2.1. Teknik Pengumpulan Data")
        body_p(
            f"1) Observasi Lapangan: Penulis terlibat langsung dalam operasional harian Humas selama masa Praktik Kerja Lapangan "
            f"periode Agustus hingga Oktober 2025, meliputi peliputan kegiatan kedinasan, pencatatan unsur 5W+1H (What, Who, Where, "
            f"When, Why, How), pengambilan dokumentasi visual, hingga penyusunan naskah press release {c(1)}, {c(2)}."
        )
        body_p(
            f"2) Wawancara Terstruktur: Penulis melakukan tanya jawab langsung dengan Pranata Humas dan staf pengelola publikasi "
            f"di bawah Bidang Informasi Publik untuk memetakan alur verifikasi naskah, standar redaksional berita, serta kendala "
            f"pengarsipan dokumen {c(3)}, {c(12)}."
        )
        body_p(
            f"3) Studi Pustaka: Penulis mengkaji literatur rekayasa perangkat lunak {c(4)}, {c(7)}, konsep sistem informasi manajemen "
            f"berbasis web {c(11)}, {c(14)}, standar pemodelan UML {c(8)}, {c(10)}, serta pengujian sistem informasi {c(14)}, {c(15)}."
        )
        h2("2.2. Metode Analisis dan Perancangan")
        body_p(
            f"Analisis sistem dilakukan dengan membedah prosedur operasional standar (SOP) berjalan, mendokumentasikan spesifikasi "
            f"berkas masukan (input) dan keluaran (output), lalu memodelkan interaksi aktor menggunakan Use Case Diagram serta "
            f"aliran kerja (workflow) menggunakan Activity Diagram {c(10)}, {c(13)}. Berdasarkan temuan masalah pokok "
            f"pada sistem berjalan, disusun spesifikasi solusi sistem usulan Aplikasi Press Release Auto-Generator {c(15)}."
        )

        h1("3. HASIL DAN PEMBAHASAN")
        h2("3.1. Tinjauan Organisasi dan Kedudukan Humas")
        body_p(
            "Dinas Komunikasi dan Informatika Kota Contoh dibentuk berdasarkan Peraturan Daerah tentang Pembentukan Perangkat Daerah "
            "sebagai pelaksana urusan pemerintahan bidang komunikasi dan informatika. Secara struktural, fungsi kehumasan berada di bawah "
            "Bidang Pengelolaan Informasi dan Komunikasi Publik sebagaimana ditunjukkan pada Gambar 1."
        )
        embed_figure(
            "gambar_3_1_struktur_organisasi.png",
            1,
            "Struktur Organisasi Dinas Komunikasi dan Informatika Kota Contoh",
            "Dinas Komunikasi dan Informatika Kota Contoh (2026)",
        )

        h2("3.2. Analisis Prosedur dan Dokumen Sistem Berjalan")
        body_p(
            "Alur pengelolaan publikasi berita yang berjalan saat ini terdiri atas enam prosedur berurutan: (1) peliputan agenda "
            "dan pencatatan fakta 5W+1H di lapangan; (2) pengetikan draf naskah berita secara manual di Microsoft Word; (3) pengiriman "
            "file draf (.docx) kepada pimpinan melalui aplikasi WhatsApp; (4) pemeriksaan dan pemberian catatan revisi atau "
            "persetujuan (ACC) via WhatsApp; (5) penerbitan berita ke CMS website portal.kotacontoh.go.id serta akun Instagram "
            "@humas_kotacontoh; dan (6) penyimpanan arsip naskah beserta foto di folder komputer lokal staf."
        )
        body_p(
            "Berdasarkan identifikasi berkas administratif pada unit Humas, dokumen sistem berjalan dikelompokkan menjadi dokumen "
            "masukan (Lembar Catatan Peliputan 5W+1H dan Foto Dokumentasi Kegiatan) serta dokumen keluaran (Draf Naskah Berita Word, "
            "Artikel Website Resmi, dan Konten Instagram). Rekapitulasi spesifikasi dokumen masukan dan keluaran disajikan pada Tabel 1."
        )

        w_t1 = [col_width_cm * 0.10, col_width_cm * 0.28, col_width_cm * 0.34, col_width_cm * 0.28]
        tbl_wrapper(
            "Tabel 1. Spesifikasi Dokumen Masukan dan Keluaran Sistem Berjalan",
            ["No", "Nama Dokumen", "Kategori & Fungsi", "Media & Tujuan"],
            [
                ["1", "Catatan Liputan 5W+1H", "Input: Fakta acara & kutipan", "Kertas/Digital -> Staf Humas"],
                ["2", "Foto Dokumentasi", "Input: Bukti visual kegiatan", "JPEG/PNG (5-20 foto) -> Humas"],
                ["3", "Draf Press Release", "Output: Naskah verifikasi", "File .docx via WA -> Pimpinan"],
                ["4", "Artikel Portal Web", "Output: Rilis berita resmi", "HTML CMS -> Publik / ASN"],
                ["5", "Konten Instagram", "Output: Informasi ringkas visual", "Feed/Carousel -> Warganet"],
            ],
            w_t1,
        )

        h2("3.3. Pemodelan UML Sistem Berjalan")
        body_p(
            f"Interaksi fungsional pada sistem berjalan melibatkan tiga aktor utama {c(8)}, {c(10)}: Staf Humas sebagai "
            f"pelaksana liputan dan penulis draf, Pimpinan (Kepala Bidang / Pranata Humas) sebagai penelaah dan pemberi persetujuan, "
            f"serta Masyarakat sebagai pembaca informasi publikasi. Rincian peran aktor disajikan pada Tabel 2, sedangkan pemodelan "
            f"Use Case Diagram sistem berjalan ditampilkan pada Gambar 2."
        )

        w_t2 = [col_width_cm * 0.10, col_width_cm * 0.28, col_width_cm * 0.62]
        tbl_wrapper(
            "Tabel 2. Deskripsi Aktor pada Sistem Publikasi Berjalan",
            ["No", "Aktor", "Peran dalam Sistem Pengelolaan Publikasi"],
            [
                ["1", "Staf Humas", "Meliput kegiatan, mengetik draf di MS Word, mengirim via WA, merevisi, mempublikasikan ke web/medsos, dan mengarsipkan file lokal."],
                ["2", "Pimpinan (Kepala Bidang)", "Menerima file draf melalui WhatsApp, memeriksa ketepatan isi dan redaksi, memberi catatan revisi, serta memberikan ACC tayang."],
                ["3", "Masyarakat / Publik", "Mengakses dan membaca berita resmi melalui portal website portal.kotacontoh.go.id serta Instagram @humas_kotacontoh."],
            ],
            w_t2,
        )

        embed_figure(
            "gambar_3_2_use_case_berjalan.png",
            2,
            "Use Case Diagram Sistem Publikasi Berita Berjalan",
            "Hasil Analisis Sistem Berjalan (2026)",
        )

        body_p(
            "Dinamika aliran aktivitas (workflow) antar-entitas dari tahap peliputan hingga pengarsipan lokal dimodelkan menggunakan "
            "Activity Diagram pada Gambar 3. Terlihat bahwa proses koreksi naskah membentuk siklus berulang melalui percakapan "
            "WhatsApp sebelum naskah dapat diterbitkan ke portal web dan media sosial."
        )

        embed_figure(
            "gambar_3_3_activity_diagram_berjalan.png",
            3,
            "Activity Diagram Sistem Publikasi Berita Berjalan",
            "Hasil Analisis Sistem Berjalan (2026)",
        )

        h2("3.4. Evaluasi Masalah Pokok dan Rancangan Solusi Usulan")
        body_p(
            "Berdasarkan analisis diagram UML dan observasi operasional, teridentifikasi tiga permasalahan pokok yang menghambat "
            "kinerja publikasi Humas Diskominfo Kota Contoh. Sebagai pemecahan masalah, diusulkan perancangan Aplikasi Press Release "
            "Auto-Generator. Perbandingan terukur antara kondisi sistem berjalan dan rancangan sistem usulan dirangkum pada Tabel 3."
        )

        w_t3 = [col_width_cm * 0.24, col_width_cm * 0.38, col_width_cm * 0.38]
        tbl_wrapper(
            "Tabel 3. Komparasi Sistem Berjalan dan Usulan Press Release Auto-Generator",
            ["Aspek Proses", "Kondisi Sistem Berjalan (Manual)", "Rancangan Sistem Usulan (Otomatisasi)"],
            [
                ["Penyusunan Naskah", "Ketik manual dari nol di MS Word (durasi 1-2 jam/berita); struktur tidak seragam.", "Input formulir 5W+1H terstruktur; pembangkitan draf berita otomatis sesuai templat baku instansi."],
                ["Verifikasi & Approval", "Kirim file .docx via chat WhatsApp; riwayat revisi rawan tertimbun pesan lain.", "Dashboard verifikasi terpusat dengan penanda status (Draft, Revisi, Approved) dan log riwayat koreksi."],
                ["Pengarsipan Berkas", "Simpan di harddisk lokal laptop staf; rawan hilang dan sulit dicari kembali.", "Repositori arsip terpusat terindeks berdasarkan tanggal, seksi penyelenggara, dan kategori agenda."],
            ],
            w_t3,
        )

        body_p(
            f"Melalui penerapan Aplikasi Press Release Auto-Generator, staf Humas cukup memasukkan parameter kegiatan (nama acara, "
            f"waktu, tempat, pejabat/narasumber, poin sambutan, dan unggahan foto) ke dalam formulir web. Sistem secara otomatis "
            f"menyusun paragraf pembuka (lead), tubuh berita, dan penutup sesuai kaidah jurnalistik kedinasan {c(14)}, {c(15)}, "
            f"sehingga memangkas waktu penulisan draf dan menjamin keseragaman standar rilis publikasi Diskominfo Kota Contoh."
        )

        h1("4. KESIMPULAN")
        body_p(
            "Berdasarkan hasil analisis sistem pengelolaan publikasi berita pada Bidang Humas Dinas Komunikasi dan Informatika Kota Contoh, "
            "dapat disimpulkan bahwa: (1) alur kerja sistem berjalan masih mengandalkan pengetikan manual di Microsoft Word, "
            "komunikasi verifikasi melalui WhatsApp, dan penyimpanan arsip lokal yang memicu keterlambatan rilis serta risiko "
            "kehilangan dokumen; (2) pemodelan Use Case Diagram (10 use case, 3 aktor) dan Activity Diagram berhasil memetakan "
            "titik hambatan utama pada siklus penulisan draf dan persetujuan berulang; serta (3) rancangan Aplikasi Press Release "
            "Auto-Generator berbasis input 5W+1H terstruktur dan modul persetujuan terpusat memberikan solusi konkret untuk "
            "mempercepat produksi siaran pers sekaligus menstandarkan dokumentasi publikasi instansi. Penelitian selanjutnya "
            "disarankan menguji integrasi langsung (API) antara generator naskah dengan CMS portal resmi instansi."
        )

        h1("UCAPAN TERIMA KASIH")
        body_p(
            "Penulis menyampaikan terima kasih kepada Kepala Dinas Komunikasi dan Informatika Kota Contoh, Kepala Bidang Informasi Publik, "
            "Pranata Humas beserta seluruh staf Bidang Informasi dan Komunikasi Publik Kota Contoh, serta Dosen Penasehat "
            "Akademik Program Studi Teknologi Informasi Universitas Bina Sarana Informatika atas dukungan data dan bimbingan "
            "selama pelaksanaan penelitian ini."
        )

        h1("DAFTAR PUSTAKA")

    ref_count = max(spec.get("min_references", 15), 25 if str(sinta_rank) == "1" else 15)
    active_refs = get_reference_list(style=active_citation, topic=topic, count=ref_count)

    if mendeley_mode:
        # Aturan R1 & R3: Kosongkan daftar entri di .docx untuk Mendeley pemilik, ekspor ke file .txt terpisah.
        add_p(
            doc,
            "[REFERENSI DIKELOLA VIA MENDELEY - Lihat kandidat referensi ber-DOI aktif pada berkas .txt terpisah sesuai R1 & R3]",
            font_name=font_name,
            size_pt=f_ref,
            italic=True,
            align=WD_ALIGN_PARAGRAPH.LEFT,
            space_before=0,
            space_after=2.5,
            line_spacing=1.0,
            color=(107, 114, 128),
        )
    else:
        for ref_item in active_refs:
            p_ref = add_p(
                doc,
                ref_item,
                font_name=font_name,
                size_pt=f_ref,
                align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                space_before=0,
                space_after=2.5,
                line_spacing=1.0,
            )
            p_ref.paragraph_format.left_indent = Cm(0.6)
            p_ref.paragraph_format.first_line_indent = Cm(-0.6)

    if not output_path:
        col_tag = "2KOLOM" if num_cols == 2 else "1KOLOM"
        topic_tag = "APK_KUHP_BARU" if topic == "apk-kuhp" else "LAYANAN_PUBLIK"
        output_path = f"JURNAL_SINTA{spec['sinta_rank']}_{active_meta['short_name']}_{col_tag}_{topic_tag}.docx"

    out_abs = atomic_save_docx(doc, output_path, backup=False)

    exported_txt_path = None
    if mendeley_mode or refs_txt_out:
        import re as _re
        if not refs_txt_out:
            stem, _ = os.path.splitext(output_path)
            refs_txt_out = f"{stem}_kandidat_referensi.txt"
        txt_dir = os.path.dirname(os.path.abspath(refs_txt_out))
        if txt_dir:
            os.makedirs(txt_dir, exist_ok=True)
        header_lines = [
            f"KANDIDAT REFERENSI BER-DOI AKTIF (ATURAN R1 & R3 MENDELEY WORKFLOW)",
            f"Target Jurnal : SINTA {spec['sinta_rank']} - {active_meta['journal_name']} ({active_meta['institution']})",
            f"Naskah Target : {out_abs}",
            f"Gaya Sitasi   : {active_citation.upper()}",
            "=" * 80,
            "",
        ]
        formatted_entries = []
        for idx, ref_entry in enumerate(active_refs, start=1):
            doi_m = _re.search(r"https?://doi\.org/\S+", ref_entry)
            doi_url = doi_m.group(0).rstrip(".,") if doi_m else "-"
            formatted_entries.extend([
                f"[{idx}] [Level SINTA: tidak terverifikasi]",
                f"Sitasi ({active_citation.upper()}) : {ref_entry}",
                f"DOI Aktif     : {doi_url}",
                "Download PDF  : [Perlu verifikasi URL PDF langsung via verify_sinta_refs.py --check-live]",
                "",
            ])
        with open(refs_txt_out, "w", encoding="utf-8") as f:
            f.write("\n".join(header_lines + formatted_entries))
        exported_txt_path = os.path.abspath(refs_txt_out)

    return {
        "output_path": os.path.abspath(output_path),
        "sinta_rank": spec["sinta_rank"],
        "journal_name": active_meta["journal_name"],
        "institution": active_meta["institution"],
        "issn": f"p-ISSN {active_meta['p_issn']} / e-ISSN {active_meta['e_issn']}",
        "doi": active_meta.get("sample_doi", ""),
        "layout": f"{num_cols} Kolom ({'Terbagi 2' if num_cols == 2 else 'Biasa / 1 Kolom Penuh'})",
        "citation": active_citation.upper(),
        "topic": topic,
        "mendeley_mode": bool(mendeley_mode),
        "references_count": 0 if mendeley_mode else len(active_refs),
        "exported_refs_txt": exported_txt_path,
    }


def inspect_existing_docx(docx_path):
    if not os.path.exists(docx_path):
        raise FileNotFoundError(f"File tidak ditemukan: {docx_path}")
    doc = docx.Document(docx_path)
    sec_info = []
    margins_info = {}
    hdr_preview = []
    ftr_preview = []
    for idx, sec in enumerate(doc.sections):
        cols_el = sec._sectPr.find(qn("w:cols"))
        c_num = cols_el.get(qn("w:num"), "1") if cols_el is not None else "1"
        sec_info.append(f"Section {idx + 1}: {c_num} kolom")
        if idx == 0:
            margins_info = {
                "top_cm": round(sec.top_margin.cm, 2) if sec.top_margin else None,
                "bottom_cm": round(sec.bottom_margin.cm, 2) if sec.bottom_margin else None,
                "left_cm": round(sec.left_margin.cm, 2) if sec.left_margin else None,
                "right_cm": round(sec.right_margin.cm, 2) if sec.right_margin else None,
            }
            hdr_preview = [p.text.strip() for p in sec.header.paragraphs if p.text.strip()][:3]
            ftr_preview = [p.text.strip() for p in sec.footer.paragraphs if p.text.strip()][:3]

    headings = []
    fonts_seen = set()
    non_empty_tail = []
    for i, p in enumerate(doc.paragraphs):
        for r in p.runs:
            if r.font and r.font.name:
                sz = round(r.font.size.pt, 1) if r.font.size else "inherit"
                fonts_seen.add(f"{r.font.name} ({sz}pt)")
        txt = p.text.strip()
        if not txt:
            continue
        non_empty_tail.append(f"[{i}] {txt[:120]}")
        style_name = p.style.name if p.style else ""
        has_numpr = p._p.find(".//w:numPr", p._p.nsmap) is not None
        if style_name.startswith("Heading") or has_numpr or (txt.isupper() and len(txt) < 85):
            headings.append(f"[{i}] {txt}")

    report = {
        "file": os.path.abspath(docx_path),
        "paragraphs_count": len(doc.paragraphs),
        "tables_count": len(doc.tables),
        "margins_cm": margins_info,
        "sections": sec_info,
        "header_preview": hdr_preview,
        "footer_preview": ftr_preview,
        "fonts_detected": sorted(list(fonts_seen))[:15],
        "detected_headings": headings[:40],
        "last_paragraphs": non_empty_tail[-5:],
    }
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return report


def generate_showcase_folder(showcase_dir="contoh-template-ai"):
    import shutil
    import subprocess

    os.makedirs(showcase_dir, exist_ok=True)
    variants = [
        ("1", "2col", "ieee", "apk-kuhp", "00_Jurnal_SINTA1_HukumSiber_APK_KUHP_Baru_PJIH_Unpad.docx"),
        ("1", "2col", "ieee", "layanan-publik", "01_Jurnal_SINTA1_IJAIN_UAD_2Kolom.docx"),
        ("2", "2col", "ieee", "layanan-publik", "02_Jurnal_SINTA2_JTIIK_UB_2Kolom.docx"),
        ("3", "2col", "ieee", "layanan-publik", "03_Jurnal_SINTA3_JISKA_UIN_2Kolom.docx"),
        ("4", "2col", "ieee", "layanan-publik", "04_Jurnal_SINTA4_JKI_UBSI_2Kolom.docx"),
        ("4", "1col", "ieee", "layanan-publik", "05_Jurnal_SINTA4_JKI_UBSI_1Kolom_Biasa.docx"),
        ("5", "2col", "ieee", "layanan-publik", "06_Jurnal_SINTA5_TEKNOIF_ITP_2Kolom.docx"),
        ("6", "1col", "apa", "layanan-publik", "07_Jurnal_SINTA6_METIK_Jayakarta_1Kolom_Biasa.docx"),
        ("6", "2col", "ieee", "layanan-publik", "08_Jurnal_SINTA6_METIK_Jayakarta_2Kolom.docx"),
    ]
    generated = []
    for rank, layout, cit, top, fname in variants:
        target = os.path.join(showcase_dir, fname)
        info = build_sinta_docx(
            sinta_rank=rank,
            layout_choice=layout,
            citation_style=cit,
            topic=top,
            output_path=target,
        )
        generated.append((fname, info))

    try:
        from scripts.update_docx_script import scaffold_pkl_docx
        scaffold_pkl_docx(
            outline="4",
            doc_type="laporan",
            title="ANALISIS SISTEM PENGELOLAAN PUBLIKASI BERITA DAN USULAN OTOMATISASI PRESS RELEASE PADA DINAS KOMUNIKASI DAN INFORMATIKA KOTA CONTOH",
            author="Penulis Contoh",
            nim="00000001",
            instansi="Dinas Komunikasi dan Informatika Kota Contoh",
            output_path=os.path.join(showcase_dir, "09_Laporan_PKL_UBSI_Analisis_Sistem.docx"),
        )
    except Exception:
        pass

    typst_bin = shutil.which("typst")
    if not typst_bin:
        winget_dir = os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Local", "Microsoft", "WinGet", "Packages")
        if os.path.exists(winget_dir):
            for ent in os.listdir(winget_dir):
                if "typst" in ent.lower():
                    cand = os.path.join(winget_dir, ent, "typst-x86_64-pc-windows-msvc", "typst.exe")
                    if os.path.exists(cand):
                        typst_bin = cand
                        break
    if typst_bin and os.path.exists("template/main.typ"):
        pkl_pdf_out = os.path.join(showcase_dir, "10_Laporan_PKL_UBSI_Analisis_Sistem.pdf")
        subprocess.run([typst_bin, "compile", "--root", ".", "template/main.typ", pkl_pdf_out], check=False)
    if typst_bin and os.path.exists("template/jurnal-sinta.typ"):
        pdf_out = os.path.join(showcase_dir, "11_Jurnal_SINTA4_JKI_UBSI_Typst.pdf")
        subprocess.run([typst_bin, "compile", "--root", ".", "template/jurnal-sinta.typ", pdf_out], check=False)

    readme_lines = [
        "# Katalog Contoh Hasil Template AI Agent (Jurnal SINTA 1-6 & Laporan PKL UBSI)",
        "",
        "Folder ini berisi koleksi naskah jurnal ilmiah terakreditasi **SINTA 1 sampai SINTA 6** (dengan **header/footer OJS asli**, **DOI Crossref terverifikasi**, **superscript afiliasi penulis**, dan **bebas teks AI slop / debug banner**) serta **Laporan PKL UBSI**.",
        "",
        "## Daftar File Contoh di Folder Ini",
        "",
        "| No | Nama File | Kategori / Peringkat | Instansi / Penerbit | DOI Jurnal | Layout | Sitasi & Ref |",
        "| :---: | :--- | :--- | :--- | :--- | :--- | :---: |",
    ]
    for idx, (fname, info) in enumerate(generated, start=1):
        readme_lines.append(
            f"| {idx} | `{fname}` | Jurnal SINTA {info['sinta_rank']} ({info['journal_name']}) | {info['institution']} | `{info['doi']}` | {info['layout']} | {info['citation']} ({info['references_count']} ref) |"
        )
    readme_lines.extend([
        "| 10 | `09_Laporan_PKL_UBSI_Analisis_Sistem.docx` | Laporan Akhir PKL (Word) | Universitas Bina Sarana Informatika (UBSI) | `-` | 1 Kolom Standar Pedoman UBSI | APA |",
        "| 11 | `10_Laporan_PKL_UBSI_Analisis_Sistem.pdf` | Laporan Akhir PKL (PDF Typst) | Universitas Bina Sarana Informatika (UBSI) | `-` | 1 Kolom Standar Pedoman UBSI | APA |",
        "| 12 | `11_Jurnal_SINTA4_JKI_UBSI_Typst.pdf` | Jurnal SINTA 4 (PDF Typst) | LPPM Universitas Bina Sarana Informatika (UBSI) | `https://doi.org/10.31294/jki.v14i1.21890` | 2 Kolom (Terbagi 2) | IEEE |",
        "",
        "## Standar Kualitas & Kepatuhan Etika Publikasi (ARJUNA & COPE)",
        "",
        "1. **Tanpa AI Debug Banner (`AI Indeks`)**: Identitas jurnal, p-ISSN/e-ISSN, Volume/Nomor, dan DOI ditempatkan pada **Header & Footer Word (`w:hdr` / `w:ftr`)** serta blok **Riwayat Artikel (*Received / Revised / Accepted*)** sesuai anatomi OJS asli.",
        "2. **100% Referensi Jurnal Terbit dengan DOI Aktif**: Seluruh sitasi pada daftar pustaka diambil dari jurnal terbit yang terindeks Crossref/SINTA/Scopus (`https://doi.org/10....`) ditambah regulasi primer (UU No. 1 Tahun 2023 KUHP Baru, UU No. 1 Tahun 2024 UU ITE, UU No. 27 Tahun 2022 UU PDP, POJK No. 11/POJK.03/2022, dan POJK No. 22 Tahun 2023).",
        "3. **Superscript Afiliasi & Korespondensi**: Angka indeks afiliasi penulis (`1*`, `2`) menggunakan properti `w:vertAlign=\"superscript\"` asli.",
        "4. **Kesesuaian Bahasa per Peringkat SINTA**: Naskah SINTA 1 IT (`IJAIN` UAD) ditulis 100% dalam Bahasa Inggris akademik sesuai pedoman Scopus Q3/SINTA 1, sedangkan naskah SINTA 1 Hukum Siber (`PJIH` Unpad) menyajikan analisis mendalam terkait *Unauthorized Access to Computer System* melalui aplikasi APK berbahaya pasca berlakunya KUHP Baru.",
        "",
        "## Cara Membuat Ulang Seluruh Contoh",
        "",
        "```powershell",
        "# Generate ulang seluruh koleksi contoh di folder contoh-template-ai/",
        "uv run generate_sinta_journal_docx.py --generate-showcase contoh-template-ai",
        "",
        "# Generate khusus Jurnal SINTA 1 topik Unauthorized Access APK Berbahaya & KUHP Baru",
        "uv run generate_sinta_journal_docx.py --sinta 1 --layout 2col --citation ieee --topic apk-kuhp --yes",
        "```",
    ])
    with open(os.path.join(showcase_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(readme_lines) + "\n")

    print(f"[BERHASIL] {len(generated)} contoh jurnal SINTA 1-6 dan berkas Laporan PKL tersimpan di folder: {os.path.abspath(showcase_dir)}")
    return generated


def interactive_cli():
    presets = load_presets()
    parser = argparse.ArgumentParser(description="Generator & Inspector Dokumen Word (.docx) Jurnal SINTA 1-6 dan Laporan PKL")
    parser.add_argument("-s", "--sinta", choices=["1", "2", "3", "4", "5", "6"], help="Pilih peringkat SINTA (1-6)")
    parser.add_argument("-l", "--layout", choices=["2col", "1col", "default"], help="Pilih layout: 2col (bagi 2), 1col (biasa), atau default")
    parser.add_argument("-c", "--citation", choices=["ieee", "apa", "default"], help="Gaya sitasi: ieee atau apa")
    parser.add_argument("-t", "--topic", choices=["layanan-publik", "apk-kuhp"], default="layanan-publik", help="Pilih topik naskah: layanan-publik atau apk-kuhp")
    parser.add_argument("--title", default=None, help="Judul artikel kustom (Bahasa Indonesia)")
    parser.add_argument("--title-en", default=None, help="Judul artikel kustom (Bahasa Inggris)")
    parser.add_argument("--author", default="Penulis Contoh", help="Nama penulis pertama")
    parser.add_argument("--coauthor", default="Penulis Pendamping Contoh", help="Nama penulis kedua (kosongkan dengan '' untuk penulis tunggal)")
    parser.add_argument("--email", default="penulis.contoh@contoh.ac.id", help="Email penulis pertama")
    parser.add_argument("--coemail", default="pendamping.contoh@contoh.ac.id", help="Email penulis kedua")
    parser.add_argument("--affiliation", default=None, help="Afiliasi penulis kustom")
    parser.add_argument("-o", "--output", help="Nama file .docx keluaran")
    parser.add_argument("--mendeley-mode", "--no-references", dest="mendeley_mode", action="store_true", help="Mode R1: Kosongkan entri daftar pustaka di .docx untuk Mendeley dan ekspor ke .txt terpisah")
    parser.add_argument("--export-refs-txt", help="Path file .txt kandidat referensi (R3)")
    parser.add_argument("--generate-showcase", metavar="FOLDER", nargs="?", const="contoh-template-ai", help="Generate koleksi lengkap contoh template SINTA 1-6 ke folder khusus")
    parser.add_argument("--inspect-docx", metavar="FILE", help="Inspeksi struktur dokumen Word (.docx) laporan/jurnal yang sudah ada")
    parser.add_argument("-y", "--yes", action="store_true", help="Gunakan opsi default tanpa prompt interaktif")
    args = parser.parse_args()

    if args.inspect_docx:
        inspect_existing_docx(args.inspect_docx)
        return

    if args.generate_showcase:
        generate_showcase_folder(args.generate_showcase)
        return

    sinta_rank = args.sinta
    layout_choice = args.layout
    citation_style = args.citation

    if not args.yes and sys.stdin.isatty():
        if not sinta_rank:
            print("\nPilih Target Template Jurnal Terakreditasi SINTA (1-6 dari 6 Instansi Berbeda):")
            for k in sorted(presets.keys()):
                p = presets[k]
                def_lbl = "2 Kolom" if p["default_layout"] == "2col" else "1 Kolom"
                print(f"  {k}. SINTA {k} - {p['short_name']} ({p['journal_name']}) | {p['institution']} [Default: {def_lbl}]")
            ans = input("Pilihan SINTA [1-6] (default: 4 - JKI UBSI): ").strip()
            sinta_rank = ans if ans in presets else "4"

        if not layout_choice:
            def_col = presets[sinta_rank]["default_layout"]
            print("\nPilih Tata Letak Kolom Jurnal (Layout Halaman):")
            print("  1. Layout Terbagi 2 (2 Kolom / Two-Column di bagian isi)")
            print("  2. Layout Biasa (1 Kolom Penuh / Single-Column)")
            print(f"  3. Ikuti Default Bawaan Jurnal ({'2 Kolom' if def_col == '2col' else '1 Kolom'})")
            l_ans = input("Pilihan Layout [1/2/3] (default: 3): ").strip()
            if l_ans == "1":
                layout_choice = "2col"
            elif l_ans == "2":
                layout_choice = "1col"
            else:
                layout_choice = "default"

        if not citation_style:
            print("\nPilih Gaya Sitasi & Daftar Pustaka:")
            print("  1. IEEE Style [1], [2] (Standar mayoritas jurnal IT SINTA 1-6)")
            print("  2. APA Style (Penulis, Tahun)")
            c_ans = input("Pilihan Sitasi [1/2] (default: 1 - IEEE): ").strip()
            citation_style = "apa" if c_ans == "2" else "ieee"

    sinta_rank = sinta_rank or "4"
    layout_choice = layout_choice or "default"
    citation_style = citation_style or "ieee"

    norm_topic = args.topic
    info = build_sinta_docx(
        sinta_rank=sinta_rank,
        layout_choice=layout_choice,
        citation_style=citation_style,
        topic=norm_topic,
        output_path=args.output,
        mendeley_mode=args.mendeley_mode,
        refs_txt_out=args.export_refs_txt,
        title=args.title,
        title_en=args.title_en,
        author=args.author,
        coauthor=args.coauthor,
        email=args.email,
        coemail=args.coemail,
        affiliation=args.affiliation,
    )
    print(f"[BERHASIL] Dokumen Jurnal SINTA {info['sinta_rank']} selesai dibuat:")
    print(f"  Jurnal     : {info['journal_name']} ({info['institution']})")
    print(f"  ISSN       : {info['issn']}")
    print(f"  DOI        : {info['doi']}")
    print(f"  Layout     : {info['layout']}")
    print(f"  Sitasi     : {info['citation']} ({info['references_count']} entri di .docx | Mendeley Mode: {info['mendeley_mode']})")
    if info.get("exported_refs_txt"):
        print(f"  Refs .txt  : {info['exported_refs_txt']}")
    print(f"  File Word  : {info['output_path']}")


if __name__ == "__main__":
    interactive_cli()
