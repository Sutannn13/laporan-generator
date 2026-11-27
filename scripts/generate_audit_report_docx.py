# /// script
# requires-python = ">=3.10"
# dependencies = ["python-docx", "pillow"]
# ///
"""
Generator Dokumen Laporan Proyek Audit Teknologi Informasi
Audit Tata Kelola Portal Akademik Perguruan Tinggi Contoh Menggunakan Framework COBIT 2019
(Studi pada Proses APO13, BAI06, DSS01, DSS05, dan MEA03)
Penulis Contoh (NIM 00000001)
Universitas Bina Sarana Informatika - 2026

Kepatuhan Standar Tata Naskah UBSI:
- Kertas: A4 (21.0 x 29.7 cm)
- Margin: Kiri 4.0 cm, Atas 3.0 cm, Kanan 2.5 cm, Bawah 2.5 cm
- Tipografi: Times New Roman 12 pt, Spasi 2.0 (Bab Pokok), Spasi 1.5 (Awal), Justified, Indent 1.2 cm
- Heading 1: 14 pt Bold Centered Uppercase
- Heading 2: 12 pt Bold Left-aligned
- Heading 3: 12 pt Bold Left-aligned
- Tabel: 9.5-10 pt, Spasi 1.0, Header Abu-abu (#E5E7EB), Border Halus, Keterangan 2 baris di atas
- Gambar: Centered, Keterangan 2 baris di bawah, Sumber di bawah
- Penomoran: Romawi kecil (ii, iii, ...) tengah bawah di bagian awal; Arab (1, 2, ...) di bab isi
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import docx
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

# --- PATH CONFIGURATION ---
BASE_DIR = Path(__file__).resolve().parent.parent
for _cand in (str(Path(__file__).resolve().parent), str(BASE_DIR)):
    if _cand not in sys.path:
        sys.path.insert(0, _cand)
try:
    from scripts.docx_io import atomic_save_docx
except ImportError:
    from docx_io import atomic_save_docx
import argparse

DEFAULT_OUTPUT_FILE = BASE_DIR / "Laporan_Audit_TI_COBIT2019_Contoh.docx"
LOGO_PATH = BASE_DIR / "template" / "gambar" / "logo-ubsi.png"
GAMBAR_DIR = BASE_DIR / "template" / "gambar"
REQUIRED_AUDIT_DIAGRAMS = (
    "diagram_organisasi_upt_tik.png",
    "diagram_arsitektur_siakad.png",
    "diagram_risk_matrix.png",
    "diagram_radar_capability.png",
    "diagram_roadmap_perbaikan.png",
)


def _find_diagram_file(filename, search_dirs):
    for d in search_dirs:
        if not d:
            continue
        cand = Path(d) / filename
        if cand.exists():
            return cand
    return GAMBAR_DIR / filename


def _prepare_audit_diagrams(diagrams_dir=None, auto_diagrams=True):
    """Resolve the 5 audit PNGs from user dir / repo template, auto-rendering into a temp dir if pruned in zero-clone skill bundles."""
    search_dirs = []
    if diagrams_dir:
        search_dirs.append(Path(diagrams_dir))
    search_dirs.extend([
        Path.cwd() / "audit_diagrams",
        Path.cwd() / "template" / "gambar",
        Path.cwd(),
        GAMBAR_DIR,
    ])
    missing = [fn for fn in REQUIRED_AUDIT_DIAGRAMS if not _find_diagram_file(fn, search_dirs).exists()]
    if not missing or not auto_diagrams:
        return search_dirs, None

    diag_script = Path(__file__).resolve().parent / "generate_audit_diagrams.py"
    if not diag_script.exists():
        return search_dirs, None

    tmp_obj = None
    if diagrams_dir:
        target_dir = Path(diagrams_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
    else:
        tmp_obj = tempfile.TemporaryDirectory(prefix="lg_audit_diagrams_")
        target_dir = Path(tmp_obj.name)

    uv_bin = shutil.which("uv")
    cmd = (
        [uv_bin, "run", str(diag_script), "--output-dir", str(target_dir)]
        if uv_bin
        else [sys.executable, str(diag_script), "--output-dir", str(target_dir)]
    )
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        print(f"Warning: Auto-generation of audit diagrams failed (rc={res.returncode}): {res.stderr.strip()}")
    return [target_dir, *search_dirs], tmp_obj



# ==========================================
# OPENXML FORMATTING HELPER FUNCTIONS
# ==========================================

def set_cell_background(cell, fill_hex):
    """Set background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    """Set inner padding of a table cell in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def set_table_borders(table, color="D1D5DB", sz="4", val="single"):
    """Set elegant, clean table borders."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def format_run(run, font_name="Times New Roman", size_pt=12, bold=False, italic=False, color_rgb=(0, 0, 0)):
    """Apply typography formatting to a text run."""
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)
    # Ensure eastAsia font attribute does not override Times New Roman
    rPr = run._r.get_or_add_rPr()
    rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" w:hAnsi="{font_name}" w:cs="{font_name}"/>')
    rPr.append(rFonts)


def format_paragraph(p, space_after=0, space_before=0, line_spacing=2.0,
                     align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent=Cm(1.2),
                     keep_with_next=False, page_break_before=False):
    """Format paragraph according to UBSI academic pedoman."""
    pPr = p.paragraph_format
    pPr.space_after = Pt(space_after)
    pPr.space_before = Pt(space_before)
    pPr.line_spacing = line_spacing
    pPr.alignment = align
    if first_line_indent is not None:
        pPr.first_line_indent = first_line_indent
    else:
        pPr.first_line_indent = Cm(0)
    if keep_with_next:
        pPr.keep_with_next = True
    if page_break_before:
        pPr.page_break_before = True


def add_page_number_field(run):
    """Add a dynamic Word PAGE field code to a run."""
    fldChar1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
    instrText = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>')
    fldChar2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="separate"/>')
    fldChar3 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)


def setup_ubsi_geometry(section):
    """Apply standard UBSI A4 margins and geometry to a section."""
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(4.0)
    section.top_margin = Cm(3.0)
    section.right_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.header_distance = Cm(1.2)
    section.footer_distance = Cm(1.2)


def set_section_numbering(section, fmt="decimal", start=None):
    """Set section page numbering format and start value."""
    sectPr = section._sectPr
    pgNumType = sectPr.find(qn("w:pgNumType"))
    if pgNumType is None:
        pgNumType = parse_xml(f'<w:pgNumType {nsdecls("w")}/>')
        sectPr.append(pgNumType)
    pgNumType.set(qn("w:fmt"), fmt)
    if start is not None:
        pgNumType.set(qn("w:start"), str(start))
    elif qn("w:start") in pgNumType.attrib:
        del pgNumType.attrib[qn("w:start")]


def setup_chapter_section(section, start_number=None):
    """
    Configure a chapter section (BAB I-V, Lampiran) according to UBSI pagination rules:
    - Geometry: standard A4 margins (Left 4.0, Top 3.0, Right 2.5, Bottom 2.5 cm)
    - Unlinked headers and footers (breaks relationship with previous sections)
    - Different first page: True
    - First page footer: unlinked, centered single page number (decimal)
    - First page header: unlinked, empty
    - Subsequent pages header: unlinked, right-aligned single page number (decimal)
    - Subsequent pages footer: unlinked, empty
    """
    setup_ubsi_geometry(section)
    section.header.is_linked_to_previous = False
    section.footer.is_linked_to_previous = False
    set_section_numbering(section, fmt="decimal", start=start_number)
    section.different_first_page_header_footer = True
    section.first_page_footer.is_linked_to_previous = False
    section.first_page_header.is_linked_to_previous = False

    # First page footer (centered page number)
    p_first_ftr = section.first_page_footer.paragraphs[0]
    p_first_ftr.text = ""
    p_first_ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ff = p_first_ftr.add_run()
    format_run(r_ff, size_pt=12)
    add_page_number_field(r_ff)

    # First page header empty
    section.first_page_header.paragraphs[0].text = ""

    # Subsequent pages header (right-aligned page number)
    p_hdr = section.header.paragraphs[0]
    p_hdr.text = ""
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_h = p_hdr.add_run()
    format_run(r_h, size_pt=12)
    add_page_number_field(r_h)

    # Subsequent pages footer empty
    section.footer.paragraphs[0].text = ""


# ==========================================
# CONTENT BUILDER HELPER FUNCTIONS
# ==========================================

def add_heading_bab(doc, bab_str, title_str):
    """
    Standard UBSI Chapter Title (Level 1):
    BAB I
    PENDAHULUAN
    14 pt Bold Centered Uppercase.
    """
    p1 = doc.add_paragraph()
    format_paragraph(p1, space_before=0, space_after=4, line_spacing=1.0,
                     align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None, keep_with_next=True)
    r1 = p1.add_run(bab_str)
    format_run(r1, size_pt=14, bold=True)

    p2 = doc.add_paragraph()
    format_paragraph(p2, space_before=0, space_after=24, line_spacing=1.0,
                     align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None, keep_with_next=True)
    r2 = p2.add_run(title_str.upper())
    format_run(r2, size_pt=14, bold=True)


def add_heading_2(doc, title_str):
    """
    Sub-bab (Level 2): 12 pt Bold Left-aligned at margin.
    Example: 1.1. Latar Belakang
    """
    p = doc.add_paragraph()
    format_paragraph(p, space_before=16, space_after=6, line_spacing=1.5,
                     align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=None, keep_with_next=True)
    r = p.add_run(title_str)
    format_run(r, size_pt=12, bold=True)
    return p


def add_heading_3(doc, title_str):
    """
    Sub-sub-bab (Level 3): 12 pt Bold Left-aligned at margin.
    Example: 1.1.1. Ketergantungan Institusi
    """
    p = doc.add_paragraph()
    format_paragraph(p, space_before=12, space_after=4, line_spacing=1.5,
                     align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=None, keep_with_next=True)
    r = p.add_run(title_str)
    format_run(r, size_pt=12, bold=True)
    return p


def add_body_p(doc, text, space_after=0, space_before=0, line_spacing=2.0,
               first_line_indent=Cm(1.2), bold=False, italic=False,
               align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    """Standard UBSI body paragraph."""
    p = doc.add_paragraph()
    format_paragraph(p, space_after=space_after, space_before=space_before,
                     line_spacing=line_spacing, align=align,
                     first_line_indent=first_line_indent)
    r = p.add_run(text)
    format_run(r, size_pt=12, bold=bold, italic=italic)
    return p


def add_list_item(doc, num_str, text, level=1):
    """Add a structured hierarchical list item (1.2 cm indent)."""
    p = doc.add_paragraph()
    indent = Cm(1.2 * level)
    format_paragraph(p, space_after=2, space_before=1, line_spacing=2.0,
                     align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent=Cm(-0.6))
    p.paragraph_format.left_indent = indent
    r_num = p.add_run(num_str + " ")
    format_run(r_num, size_pt=12, bold=True)
    r_text = p.add_run(text)
    format_run(r_text, size_pt=12, bold=False)
    return p


def add_table_caption(doc, tabel_label, tabel_title):
    """
    Table caption according to UBSI standard (2 lines centered ABOVE table):
    Tabel IV.1.
    Matriks Penilaian Risiko (Risk Register) Portal Akademik Perguruan Tinggi Contoh
    """
    p1 = doc.add_paragraph()
    format_paragraph(p1, space_before=12, space_after=2, line_spacing=1.0,
                     align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None, keep_with_next=True)
    r1 = p1.add_run(tabel_label)
    format_run(r1, size_pt=10, bold=True)

    p2 = doc.add_paragraph()
    format_paragraph(p2, space_before=0, space_after=6, line_spacing=1.0,
                     align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None, keep_with_next=True)
    r2 = p2.add_run(tabel_title)
    format_run(r2, size_pt=10, bold=True)


def add_table_source(doc, source_text="Sumber: Hasil Olah Data Audit, 2026"):
    """Table source note below table."""
    p = doc.add_paragraph()
    format_paragraph(p, space_before=3, space_after=14, line_spacing=1.0,
                     align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=None)
    r = p.add_run(source_text)
    format_run(r, size_pt=9.5, italic=True)


def add_figure_caption(doc, figure_label, figure_title, source_text=None):
    """
    Figure caption according to UBSI standard (2 lines centered BELOW figure):
    Gambar III.1.
    Arsitektur Logis dan Fisik Portal Akademik Perguruan Tinggi Contoh
    """
    p1 = doc.add_paragraph()
    format_paragraph(p1, space_before=6, space_after=2, line_spacing=1.0,
                     align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None, keep_with_next=True)
    r1 = p1.add_run(figure_label)
    format_run(r1, size_pt=10, bold=True)

    p2 = doc.add_paragraph()
    format_paragraph(p2, space_before=0, space_after=2, line_spacing=1.0,
                     align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None, keep_with_next=True)
    r2 = p2.add_run(figure_title)
    format_run(r2, size_pt=10, bold=True)

    if source_text:
        p3 = doc.add_paragraph()
        format_paragraph(p3, space_before=2, space_after=14, line_spacing=1.0,
                         align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None)
        r3 = p3.add_run(source_text)
        format_run(r3, size_pt=9.5, italic=True)


def add_evidence_box(doc, box_title, items):
    """
    Add a styled callout box for gathered evidence (Bukti yang dikumpulkan).
    Shaded box with clean border and bullet points.
    """
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, "F1F5F9")  # Slate 100
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    set_table_borders(table, color="94A3B8", sz="6", val="single")

    p_title = cell.paragraphs[0]
    format_paragraph(p_title, space_before=2, space_after=4, line_spacing=1.1,
                     align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=None, keep_with_next=True)
    r_title = p_title.add_run(f"[BUKTI AUDIT] {box_title}")
    format_run(r_title, size_pt=10.5, bold=True, color_rgb=(15, 23, 42))

    for item in items:
        p_item = cell.add_paragraph()
        format_paragraph(p_item, space_before=1, space_after=2, line_spacing=1.1,
                         align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=None)
        r_bullet = p_item.add_run("• ")
        format_run(r_bullet, size_pt=9.5, bold=True, color_rgb=(30, 41, 59))
        r_text = p_item.add_run(item)
        format_run(r_text, size_pt=9.5, bold=False, color_rgb=(51, 65, 85))

    # Add space after table
    p_spacer = doc.add_paragraph()
    format_paragraph(p_spacer, space_before=0, space_after=8, line_spacing=1.0,
                     first_line_indent=None)


def add_styled_table(doc, headers, data, col_widths=None, align_center_cols=None):
    """
    Render a standard UBSI data table:
    - 9.5 pt font size
    - Single line spacing (1.0)
    - Shaded header (#E5E7EB)
    - Thin borders (#D1D5DB)
    - cantSplit on rows & tblHeader on first row
    """
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color="D1D5DB", sz="4", val="single")

    # Header Row
    hdr_row = table.rows[0]
    trPr = hdr_row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    for i, title in enumerate(headers):
        cell = hdr_row.cells[i]
        cell.text = title
        set_cell_background(cell, "E5E7EB")
        set_cell_margins(cell, top=120, bottom=120, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        for r in p.runs:
            format_run(r, size_pt=9.5, bold=True)

    # Data Rows
    for r_idx, row_data in enumerate(data):
        row = table.rows[r_idx + 1]
        row_trPr = row._tr.get_or_add_trPr()
        row_trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        bg_color = "FFFFFF" if r_idx % 2 == 0 else "F9FAFB"
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.text = str(val)
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=90, bottom=90, left=120, right=120)
            p = cell.paragraphs[0]
            if align_center_cols and c_idx in align_center_cols:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif c_idx == 0 and len(str(val)) <= 4:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            for r in p.runs:
                format_run(r, size_pt=9.5, bold=False)

    # Set column widths if provided
    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                if idx < len(row.cells):
                    row.cells[idx].width = Cm(width)

    return table


def add_toc_line(doc, title, page_str, bold=False, indent_cm=0.0):
    """
    Render a single Table of Contents entry with right-aligned dot leader at 14.5 cm.
    """
    p = doc.add_paragraph()
    format_paragraph(p, space_before=1.5, space_after=1.5, line_spacing=1.0,
                     align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=None)
    if indent_cm > 0:
        p.paragraph_format.left_indent = Cm(indent_cm)

    # Tab stop at 14.5 cm (8221 dxa)
    p_pPr = p._p.get_or_add_pPr()
    tabs = parse_xml(f'<w:tabs {nsdecls("w")}><w:tab w:val="right" w:leader="dot" w:pos="8221"/></w:tabs>')
    p_pPr.append(tabs)

    r_title = p.add_run(title)
    format_run(r_title, size_pt=11, bold=bold)

    r_tab = p.add_run("\t")
    format_run(r_tab, size_pt=11, bold=bold)

    r_page = p.add_run(str(page_str))
    format_run(r_page, size_pt=11, bold=bold)


# ==========================================
# MAIN DOCUMENT GENERATOR LOGIC
# ==========================================

def build_audit_report(
    output_path=None,
    title="Audit Tata Kelola Keamanan dan Kepatuhan Portal Akademik Perguruan Tinggi Contoh Menggunakan Framework COBIT 2019",
    subtitle="(Studi pada Proses APO13, BAI06, DSS01, DSS05, dan MEA03)",
    author="Penulis Contoh",
    nim="00000001",
    auditee="Portal Akademik Perguruan Tinggi Contoh",
    unit="UPT Teknologi Informasi dan Komunikasi Perguruan Tinggi Contoh",
    city="Kota Contoh",
    year="2026",
    mendeley_mode=True,
    diagrams_dir=None,
    auto_diagrams=True,
):
    diagram_search_dirs, tmp_diag_ctx = _prepare_audit_diagrams(
        diagrams_dir=diagrams_dir,
        auto_diagrams=auto_diagrams,
    )
    try:
        return _build_audit_report_impl(
            output_path=output_path,
            title=title,
            subtitle=subtitle,
            author=author,
            nim=nim,
            auditee=auditee,
            unit=unit,
            city=city,
            year=year,
            mendeley_mode=mendeley_mode,
            diagram_search_dirs=diagram_search_dirs,
        )
    finally:
        if tmp_diag_ctx is not None:
            tmp_diag_ctx.cleanup()


def _build_audit_report_impl(
    output_path=None,
    title="Audit Tata Kelola Keamanan dan Kepatuhan Portal Akademik Perguruan Tinggi Contoh Menggunakan Framework COBIT 2019",
    subtitle="(Studi pada Proses APO13, BAI06, DSS01, DSS05, dan MEA03)",
    author="Penulis Contoh",
    nim="00000001",
    auditee="Portal Akademik Perguruan Tinggi Contoh",
    unit="UPT Teknologi Informasi dan Komunikasi Perguruan Tinggi Contoh",
    city="Kota Contoh",
    year="2026",
    mendeley_mode=True,
    diagram_search_dirs=None,
):
    diagram_search_dirs = diagram_search_dirs or [GAMBAR_DIR]
    target_out = Path(output_path) if output_path else DEFAULT_OUTPUT_FILE
    target_out.parent.mkdir(parents=True, exist_ok=True)
    print(f"Creating document: {target_out}")
    doc = Document()

    # Configure Normal style default to Times New Roman 12 pt
    style_normal = doc.styles["Normal"]
    style_normal.font.name = "Times New Roman"
    style_normal.font.size = Pt(12)
    style_normal.font.color.rgb = RGBColor(0, 0, 0)

    # -------------------------------------------------------------
    # SECTION 1: COVER PAGE
    # -------------------------------------------------------------
    sec_cover = doc.sections[0]
    setup_ubsi_geometry(sec_cover)
    sec_cover.different_first_page_header_footer = True
    # Ensure header & footer are empty for cover
    sec_cover.first_page_header.paragraphs[0].text = ""
    sec_cover.first_page_footer.paragraphs[0].text = ""
    sec_cover.header.paragraphs[0].text = ""
    sec_cover.footer.paragraphs[0].text = ""

    # Cover Title
    p_cov_title = doc.add_paragraph()
    format_paragraph(p_cov_title, space_before=12, space_after=6, line_spacing=1.1,
                     align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None, keep_with_next=True)
    r_cov_title = p_cov_title.add_run("LAPORAN PROYEK AUDIT TEKNOLOGI INFORMASI")
    format_run(r_cov_title, size_pt=14, bold=True)

    # Cover Subtitle
    p_cov_sub = doc.add_paragraph()
    format_paragraph(p_cov_sub, space_before=0, space_after=18, line_spacing=1.15,
                     align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None, keep_with_next=True)
    r_cov_sub = p_cov_sub.add_run(f"{title}\n{subtitle}")
    format_run(r_cov_sub, size_pt=12, bold=True)

    if LOGO_PATH.exists():
        p_cov_logo = doc.add_paragraph()
        format_paragraph(p_cov_logo, space_before=10, space_after=18, line_spacing=1.0,
                         align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None, keep_with_next=True)
        r_cov_logo = p_cov_logo.add_run()
        r_cov_logo.add_picture(str(LOGO_PATH), width=Cm(5.0))
    else:
        print(f"Warning: Logo not found at {LOGO_PATH}")

    p_cov_team = doc.add_paragraph()
    format_paragraph(p_cov_team, space_before=12, space_after=10, line_spacing=1.1,
                     align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None, keep_with_next=True)
    r_cov_team = p_cov_team.add_run(f"Disusun oleh : {author} (NIM: {nim})")
    format_run(r_cov_team, size_pt=13, bold=True)

    team_members = [
        ("1.", author, nim),
    ]

    tbl_team = doc.add_table(rows=len(team_members), cols=3)
    tbl_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (no, nama, nim) in enumerate(team_members):
        row = tbl_team.rows[idx]
        cell_no, cell_nama, cell_nim = row.cells[0], row.cells[1], row.cells[2]

        cell_no.width = Cm(1.0)
        cell_nama.width = Cm(6.5)
        cell_nim.width = Cm(3.5)

        for c, text, align in [(cell_no, no, WD_ALIGN_PARAGRAPH.CENTER),
                               (cell_nama, nama, WD_ALIGN_PARAGRAPH.LEFT),
                               (cell_nim, nim, WD_ALIGN_PARAGRAPH.LEFT)]:
            c.text = text
            p = c.paragraphs[0]
            p.alignment = align
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            for r in p.runs:
                format_run(r, size_pt=11.5, bold=True)

    # Institutional Footer
    p_cov_foot = doc.add_paragraph()
    format_paragraph(p_cov_foot, space_before=36, space_after=0, line_spacing=1.15,
                     align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None)
    r_cov_foot = p_cov_foot.add_run(
        "UNIVERSITAS BINA SARANA INFORMATIKA\n"
        "FAKULTAS TEKNIK DAN INFORMATIKA\n"
        "PROGRAM STUDI TEKNOLOGI INFORMASI\n"
        "2026"
    )
    format_run(r_cov_foot, size_pt=12, bold=True)


    # -------------------------------------------------------------
    # SECTION 2: FRONT MATTER (Kata Pengantar, Daftar Isi, Tabel, Gambar)
    # -------------------------------------------------------------
    sec_front = doc.add_section(WD_SECTION.NEW_PAGE)
    setup_ubsi_geometry(sec_front)
    sec_front.different_first_page_header_footer = False
    sec_front.header.is_linked_to_previous = False
    sec_front.footer.is_linked_to_previous = False
    sec_front.first_page_header.is_linked_to_previous = False
    sec_front.first_page_footer.is_linked_to_previous = False
    set_section_numbering(sec_front, fmt="lowerRoman", start=2)

    # Header for Front Matter: Empty
    sec_front.header.paragraphs[0].text = ""

    # Footer for Front Matter: Centered Roman page number
    p_ftr_front = sec_front.footer.paragraphs[0]
    p_ftr_front.text = ""
    p_ftr_front.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ftr_front = p_ftr_front.add_run()
    format_run(r_ftr_front, size_pt=12)
    add_page_number_field(r_ftr_front)

    # --- KATA PENGANTAR ---
    p_kp_title = doc.add_paragraph()
    format_paragraph(p_kp_title, space_before=12, space_after=24, line_spacing=1.0,
                     align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None, keep_with_next=True)
    r_kp_title = p_kp_title.add_run("KATA PENGANTAR")
    format_run(r_kp_title, size_pt=14, bold=True)

    add_body_p(doc,
               "Puji dan syukur senantiasa dipanjatkan ke hadirat Allah SWT, Tuhan Yang Maha Esa, "
               "karena atas limpahan rahmat, taufik, dan hidayah-Nya, Laporan Proyek Audit Teknologi Informasi "
               "yang berjudul \"Audit Tata Kelola Portal Akademik Perguruan Tinggi Contoh Menggunakan Framework "
               "COBIT 2019 (Studi pada Proses APO13, BAI06, DSS01, DSS05, dan MEA03)\" ini dapat diselesaikan "
               "dengan baik dan tepat pada waktunya.",
               line_spacing=1.5, space_after=6)

    add_body_p(doc,
               "Penyusunan laporan proyek ini merupakan bagian integral dari pemenuhan capaian pembelajaran mata "
               "kuliah Audit Teknologi Informasi pada Program Studi Teknologi Informasi, Fakultas Teknik dan Informatika, "
               "Universitas Bina Sarana Informatika. Laporan ini bertujuan untuk mengevaluasi secara empiris tingkat "
               "kematangan (capability level) tata kelola sistem informasi akademik kampus, memetakan kesenjangan "
               "(gap analysis) terhadap target standar internasional COBIT 2019, serta merumuskan rekomendasi "
               "perbaikan konkret yang komprehensif demi mendukung keandalan operasional, keamanan data akademik, "
               "dan kepatuhan terhadap regulasi nasional pelindungan data pribadi.",
               line_spacing=1.5, space_after=6)

    add_body_p(doc,
               "Keberhasilan penyusunan laporan proyek audit ini tentu tidak terlepas dari bimbingan, arahan, dukungan, "
               "serta kerjasama dari berbagai pihak. Oleh karena itu, pada kesempatan yang berharga ini, perkenankanlah "
               "kami menyampaikan apresiasi dan rasa terima kasih yang setinggi-tingginya kepada:",
               line_spacing=1.5, space_after=4)

    gratitude_list = [
        ("1.", "Rektor Universitas Bina Sarana Informatika, atas kepemimpinan visioner dalam mendorong modernisasi dan keandalan tata kelola teknologi informasi di lingkungan kampus."),
        ("2.", "Dekan Fakultas Teknik dan Informatika Universitas Bina Sarana Informatika, atas fasilitas akademik dan dukungan institusional yang senantiasa diberikan."),
        ("3.", "Ketua Program Studi Teknologi Informasi Universitas Bina Sarana Informatika, yang senantiasa menginspirasi dan mengawal relevansi kurikulum perkuliahan dengan kebutuhan industri."),
        ("4.", "Dosen Pengampu Mata Kuliah Audit Teknologi Informasi, yang telah memberikan bimbingan teknis, wawasan metodologi audit berstandar internasional, serta masukan konstruktif selama pengerjaan proyek ini."),
        ("5.", f"Kepala {unit} beserta jajaran staf teknis, administrator basis data, dan helpdesk yang telah memberikan keterbukaan data observasi, akses wawancara, dan verifikasi dokumen pendukung."),
        ("6.", "Rekan-rekan mahasiswa Kelas 17.7A.01, khususnya seluruh anggota Penulis Contoh yang telah menunjukkan dedikasi, soliditas, kerja keras, dan komitmen tinggi dalam menyelesaikan seluruh tahapan audit."),
    ]
    for num, text in gratitude_list:
        p_g = doc.add_paragraph()
        format_paragraph(p_g, space_before=1, space_after=2, line_spacing=1.5,
                         align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent=Cm(-0.6))
        p_g.paragraph_format.left_indent = Cm(1.2)
        r_num = p_g.add_run(num + " ")
        format_run(r_num, size_pt=12, bold=True)
        r_text = p_g.add_run(text)
        format_run(r_text, size_pt=12, bold=False)

    add_body_p(doc,
               "Penyusun menyadari sepenuhnya bahwa laporan proyek ini masih memiliki keterbatasan. Oleh sebab itu, "
               "segala bentuk kritik, masukan, dan saran yang membangun dari para pembaca sangat kami harapkan "
               "guna penyempurnaan karya ilmiah dan pelaksanaan audit di masa yang akan datang. Semoga laporan ini "
               "dapat memberikan sumbangsih nyata bagi peningkatan tata kelola TI di Perguruan Tinggi Contoh.",
               line_spacing=1.5, space_before=6, space_after=14)

    # Signer Date & Team
    p_kp_sign = doc.add_paragraph()
    format_paragraph(p_kp_sign, space_before=12, space_after=0, line_spacing=1.15,
                     align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent=None)
    r_kp_sign = p_kp_sign.add_run(
        f"{city}, {year}\n\n\n\n"
        f"{author}"
    )
    format_run(r_kp_sign, size_pt=12, bold=True)


    # --- DAFTAR ISI ---
    doc.add_page_break()
    p_toc_title = doc.add_paragraph()
    format_paragraph(p_toc_title, space_before=12, space_after=14, line_spacing=1.0,
                     align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None, keep_with_next=True)
    r_toc_title = p_toc_title.add_run("DAFTAR ISI")
    format_run(r_toc_title, size_pt=14, bold=True)

    # Header label "Halaman" right aligned
    p_toc_lbl = doc.add_paragraph()
    format_paragraph(p_toc_lbl, space_before=0, space_after=6, line_spacing=1.0,
                     align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent=None, keep_with_next=True)
    r_toc_lbl = p_toc_lbl.add_run("Halaman")
    format_run(r_toc_lbl, size_pt=11, bold=True)

    toc_entries = [
        ("HALAMAN JUDUL", "i", True, 0.0),
        ("KATA PENGANTAR", "ii", True, 0.0),
        ("DAFTAR ISI", "iii", True, 0.0),
        ("DAFTAR TABEL", "iv", True, 0.0),
        ("DAFTAR GAMBAR", "v", True, 0.0),
        ("BAB I PENDAHULUAN", "1", True, 0.0),
        ("1.1. Latar Belakang", "1", False, 0.6),
        ("1.2. Rumusan Masalah", "3", False, 0.6),
        ("1.3. Tujuan Proyek", "4", False, 0.6),
        ("1.4. Manfaat Proyek", "4", False, 0.6),
        ("1.5. Ruang Lingkup Proyek", "5", False, 0.6),
        ("BAB II LANDASAN TEORI", "7", True, 0.0),
        ("2.1. Pengertian dan Tujuan Audit Teknologi Informasi", "7", False, 0.6),
        ("2.2. Sistem Informasi Akademik (SIAKAD) dalam Pendidikan Tinggi", "9", False, 0.6),
        ("2.3. Kerangka Kerja COBIT 2019", "11", False, 0.6),
        ("2.4. Teori Pengendalian Internal, Manajemen Risiko, dan Standar Pendukung", "17", False, 0.6),
        ("BAB III GAMBARAN UMUM OBJEK AUDIT", "20", True, 0.0),
        ("3.1. Profil Portal Akademik Perguruan Tinggi Contoh", "20", False, 0.6),
        ("3.2. Struktur Organisasi Pengelola TI (UPT TIK Perguruan Tinggi Contoh)", "22", False, 0.6),
        ("3.3. Infrastruktur dan Arsitektur Sistem", "24", False, 0.6),
        ("3.4. Kebijakan dan Prosedur TI yang Berlaku", "28", False, 0.6),
        ("BAB IV PEMBAHASAN", "30", True, 0.0),
        ("4.1. Teknik Pengumpulan Data", "30", False, 0.6),
        ("4.2. Penilaian Risiko dan Pengendalian", "33", False, 0.6),
        ("4.3. Identifikasi Temuan Audit (Struktur CCCE)", "37", False, 0.6),
        ("4.4. Analisis Kesesuaian Framework (Gap Analysis)", "43", False, 0.6),
        ("4.5. Rekomendasi Perbaikan dan Rencana Tindak Lanjut", "47", False, 0.6),
        ("BAB V KESIMPULAN DAN SARAN", "52", True, 0.0),
        ("5.1. Kesimpulan", "52", False, 0.6),
        ("5.2. Saran", "54", False, 0.6),
        ("LAMPIRAN", "56", True, 0.0),
        ("Lampiran L-A: Ringkasan Artikel Ilmiah Rujukan", "56", False, 0.6),
        ("Lampiran L-B: Instrumen Checklist Audit COBIT 2019 (46 Butir)", "58", False, 0.6),
        ("Lampiran L-C: Matriks Sampling Pengujian Audit", "68", False, 0.6),
        ("Lampiran L-D: Panduan Skoring dan Rubrik Kriteria Kemampuan COBIT 2019", "70", False, 0.6),
        ("Lampiran L-E: Matriks Peta Panas Risiko (Risk Heatmap 5x5)", "72", False, 0.6),
    ]

    for title, pg, is_bold, ind in toc_entries:
        add_toc_line(doc, title, pg, bold=is_bold, indent_cm=ind)


    # --- DAFTAR TABEL ---
    doc.add_page_break()
    p_tot_title = doc.add_paragraph()
    format_paragraph(p_tot_title, space_before=12, space_after=14, line_spacing=1.0,
                     align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None, keep_with_next=True)
    r_tot_title = p_tot_title.add_run("DAFTAR TABEL")
    format_run(r_tot_title, size_pt=14, bold=True)

    p_tot_lbl = doc.add_paragraph()
    format_paragraph(p_tot_lbl, space_before=0, space_after=6, line_spacing=1.0,
                     align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent=None, keep_with_next=True)
    r_tot_lbl = p_tot_lbl.add_run("Halaman")
    format_run(r_tot_lbl, size_pt=11, bold=True)

    table_entries = [
        ("Tabel I.1. Ruang Lingkup Proyek Audit TI Portal Akademik Perguruan Tinggi Contoh", "6"),
        ("Tabel II.1. Pemetaan 5 Proses Fokus COBIT 2019 pada Portal Akademik Perguruan Tinggi Contoh", "13"),
        ("Tabel II.2. Model Tingkat Kapabilitas Proses COBIT 2019 (Level 0–5)", "16"),
        ("Tabel III.1. Inventaris Kebijakan dan Prosedur TI Eksisting Portal Akademik Perguruan Tinggi Contoh", "29"),
        ("Tabel IV.1. Matriks Penilaian Risiko (Risk Register) 5 Domain Fokus", "34"),
        ("Tabel IV.2. Evaluasi Pengendalian Eksisting pada Portal Akademik Perguruan Tinggi Contoh", "36"),
        ("Tabel IV.3. Rekapitulasi Temuan Audit Berstruktur CCCE", "42"),
        ("Tabel IV.4. Rekapitulasi Kuantitatif Checklist Audit COBIT 2019", "44"),
        ("Tabel IV.5. Matriks Analisis Kesenjangan (Gap Analysis) Kapabilitas", "45"),
        ("Tabel IV.6. Matriks Prioritas Rekomendasi Perbaikan Tata Kelola SIAKAD", "50"),
        ("Tabel L-B.1. Checklist Audit APO13 Managed Security (10 Butir)", "58"),
        ("Tabel L-B.2. Checklist Audit BAI06 Managed IT Changes (9 Butir)", "60"),
        ("Tabel L-B.3. Checklist Audit DSS01 Managed Operations (9 Butir)", "62"),
        ("Tabel L-B.4. Checklist Audit DSS05 Managed Security Services (10 Butir)", "64"),
        ("Tabel L-B.5. Checklist Audit MEA03 Managed Compliance External (8 Butir)", "66"),
    ]

    for title, pg in table_entries:
        add_toc_line(doc, title, pg, bold=False, indent_cm=0.0)


    # --- DAFTAR GAMBAR ---
    doc.add_page_break()
    p_tog_title = doc.add_paragraph()
    format_paragraph(p_tog_title, space_before=12, space_after=14, line_spacing=1.0,
                     align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None, keep_with_next=True)
    r_tog_title = p_tog_title.add_run("DAFTAR GAMBAR")
    format_run(r_tog_title, size_pt=14, bold=True)

    p_tog_lbl = doc.add_paragraph()
    format_paragraph(p_tog_lbl, space_before=0, space_after=6, line_spacing=1.0,
                     align=WD_ALIGN_PARAGRAPH.RIGHT, first_line_indent=None, keep_with_next=True)
    r_tog_lbl = p_tog_lbl.add_run("Halaman")
    format_run(r_tog_lbl, size_pt=11, bold=True)

    figure_entries = [
        (f"Gambar III.1. Struktur Organisasi {unit}", "23"),
        ("Gambar III.2. Arsitektur Multi-Tier dan Keamanan Portal Akademik Perguruan Tinggi Contoh", "25"),
        ("Gambar IV.1. Matriks Penilaian Risiko 5x5 (Likelihood vs Impact) Portal Akademik Perguruan Tinggi Contoh", "35"),
        ("Gambar IV.2. Perbandingan Tingkat Kapabilitas Eksisting vs Target COBIT 2019", "46"),
        ("Gambar IV.3. Peta Jalan (Roadmap) Perbaikan Tata Kelola Portal Akademik Perguruan Tinggi Contoh 3 Fase", "49"),
    ]

    for title, pg in figure_entries:
        add_toc_line(doc, title, pg, bold=False, indent_cm=0.0)


    # -------------------------------------------------------------
    # SECTION 3: BAB I PENDAHULUAN
    # -------------------------------------------------------------
    sec_b1 = doc.add_section(WD_SECTION.NEW_PAGE)
    setup_chapter_section(sec_b1, start_number=1)

    add_heading_bab(doc, "BAB I", "PENDAHULUAN")

    add_heading_2(doc, "1.1. Latar Belakang")

    add_body_p(doc,
               "Perkembangan teknologi informasi dalam era revolusi industri 4.0 dan transformasi digital "
               "telah mengubah secara mendasar tata kelola operasional pada perguruan tinggi di Indonesia. "
               "Sistem Informasi Akademik (SIAKAD) kini tidak lagi sekadar berfungsi sebagai piranti pencatat "
               "administrasi kependidikan, melainkan telah berevolusi menjadi tulang punggung operasional "
               "(mission-critical backbone) yang mengintegrasikan seluruh siklus hidup layanan akademik mahasiswa, "
               "mulai dari proses registrasi dan pembayaran perkuliahan, penyusunan Kartu Rencana Studi (KRS), "
               "presensi perkuliahan, pengelolaan Kartu Hasil Studi (KHS), transkrip akademik, proses yudisium, "
               "hingga pelaporan data transaksi semesteran ke Pangkalan Data Pendidikan Tinggi (PDDikti) Kementerian "
               "Pendidikan, Kebudayaan, Riset, dan Teknologi.")

    add_body_p(doc,
               "Pada Perguruan Tinggi Contoh, portal akademik terpadu melayani puluhan ribu mahasiswa aktif "
               "yang tersebar di berbagai kampus dan program studi. Tingginya intensitas transaksi digital yang "
               "mencapai puncaknya pada periode kalender akademik tertentu, seperti masa pengisian KRS dan pekan ujian, "
               "menuntut ketersediaan layanan (high availability) yang optimal dan perlindungan data yang sangat kokoh. "
               "Kegagalan atau gangguan operasional pada SIAKAD tidak hanya memicu keluhan massal dari civitas akademika, "
               "tetapi juga berpotensi melumpuhkan proses belajar-mengajar, mengacaukan jadwal pembayaran, dan "
               "menghambat pelaporan kepatuhan perguruan tinggi kepada lembaga regulator eksternal.")

    add_body_p(doc,
               "Di sisi lain, ketergantungan yang masif terhadap sistem elektronik ini secara linier meningkatkan "
               "eksposur terhadap risiko keamanan informasi dan ancaman siber (cyber threats). Portal Akademik Perguruan Tinggi Contoh memproses "
               "dan menyimpan ratusan ribu entitas data pribadi sensitif (Personally Identifiable Information / PII), "
               "seperti Nomor Induk Kependudukan (NIK), tanggal lahir, nama ibu kandung, riwayat keuangan, serta "
               "integritas rekam jejak nilai mahasiswa. Penerbitan Undang-Undang No. 27 Tahun 2022 tentang Pelindungan "
               "Data Pribadi (UU PDP) memberikan mandat hukum yang sangat tegas kepada badan hukum penyelenggara sistem "
               "elektronik untuk menjamin kerahasiaan, integritas, dan ketersediaan data pemrosesan pribadi. "
               "Kegagalan dalam menerapkan tata kelola keamanan yang memadai mengekspos universitas pada ancaman sanksi "
               "administratif yang sangat berat, denda finansial hingga 2 persen dari total pendapatan tahunan, "
               "tuntutan perdata, maupun ancaman pidana.")

    add_body_p(doc,
               "Menghadapi kompleksitas risiko teknologi tersebut, manajemen Perguruan Tinggi Contoh memerlukan "
               "kerangka pengukuran tata kelola teknologi informasi yang komprehensif, terstruktur, dan berbasis "
               "standar internasional. Kerangka kerja COBIT 2019 (Control Objectives for Information and Related "
               "Technologies) yang diterbitkan oleh ISACA (Information Systems Audit and Control Association) dipilih "
               "karena memiliki metodologi yang sangat adaptif, memisahkan secara tegas antara tata kelola (governance) "
               "dan manajemen (management), serta menyediakan model penilaian tingkat kemampuan proses (capability level) "
               "yang terukur dari skala 0 (Incomplete) hingga 5 (Optimizing).")

    add_body_p(doc,
               "Penelitian proyek audit ini secara khusus memfokuskan evaluasi pada lima proses inti COBIT 2019 yang "
               "paling krusial bagi keandalan dan integritas Portal Akademik Perguruan Tinggi Contoh, yaitu: (1) APO13 (Managed Security) untuk "
               "mengevaluasi kerangka kebijakan keamanan informasi dan enkripsi aset data; (2) BAI06 (Managed IT Changes) "
               "untuk mengaudit pengendalian siklus rilis dan perubahan sistem aplikasi; (3) DSS01 (Managed Operations) "
               "untuk menilai keandalan operasional harian, prosedur pencadangan (backup), dan pemantauan sistem; "
               "(4) DSS05 (Managed Security Services) untuk menelaah efektivitas kontrol akses berbasis peran (RBAC), "
               "penanganan insiden, dan proteksi malware; serta (5) MEA03 (Managed Compliance With External Requirements) "
               "guna memastikan keselarasan operasional TI terhadap mandat hukum UU PDP No. 27/2022 dan standar "
               "akreditasi PDDikti Kemendikbudristek.")

    add_heading_2(doc, "1.2. Rumusan Masalah")

    add_body_p(doc,
               "Berdasarkan latar belakang permasalahan yang telah diuraikan, rumusan masalah dalam proyek audit "
               "tata kelola teknologi informasi ini dirumuskan dalam enam pertanyaan pokok sebagai berikut:")

    prob_statements = [
        ("1.", "Bagaimana tingkat kemampuan (capability level) tata kelola keamanan informasi (APO13) yang diterapkan pada Portal Akademik Perguruan Tinggi Contoh saat ini?"),
        ("2.", "Bagaimana efektivitas dan kepatuhan prosedur manajemen perubahan sistem (BAI06) dalam mengawal rilis modul baru pada Portal Akademik Perguruan Tinggi Contoh?"),
        ("3.", "Bagaimana kualitas dan keandalan manajemen operasional TI harian serta prosedur pencadangan dan pemulihan data (DSS01) pada Portal Akademik Perguruan Tinggi Contoh?"),
        ("4.", "Bagaimana efektivitas layanan keamanan, pengelolaan hak akses pengguna (RBAC), dan penegakan akuntabilitas administratif (DSS05) pada Portal Akademik Perguruan Tinggi Contoh?"),
        ("5.", "Bagaimana tingkat kepatuhan tata kelola teknologi informasi Portal Akademik Perguruan Tinggi Contoh terhadap regulasi eksternal (MEA03), khususnya UU PDP No. 27/2022 dan regulasi PDDikti?"),
        ("6.", "Rekomendasi perbaikan dan peta jalan (roadmap) tindak lanjut apa yang perlu dirumuskan untuk menjembatani kesenjangan (gap) antara kondisi kapabilitas saat ini menuju tingkat target yang diharapkan?"),
    ]
    for num, text in prob_statements:
        add_list_item(doc, num, text)

    add_heading_2(doc, "1.3. Tujuan Proyek")

    add_body_p(doc,
               "Sejalan dengan rumusan masalah yang ditetapkan, tujuan pelaksanaan proyek audit tata kelola ini adalah:")

    obj_statements = [
        ("1.", "Menganalisis dan mengukur tingkat kemampuan (capability level) proses APO13 (Managed Security) pada tata kelola Portal Akademik Perguruan Tinggi Contoh."),
        ("2.", "Mengevaluasi efektivitas pengendalian proses BAI06 (Managed IT Changes) dalam meminimalisasi risiko kegagalan sistem saat rilis aplikasi."),
        ("3.", "Menilai keandalan prosedur operasional, penjadwalan pencadangan data, dan mekanisme pemantauan infrastruktur pada proses DSS01 (Managed Operations)."),
        ("4.", "Memeriksa kontrol akses logis, pengelolaan akun pengguna, penonaktifan hak akses, dan proteksi aset pada proses DSS05 (Managed Security Services)."),
        ("5.", "Mengidentifikasi kesesuaian dan kepatuhan sistem terhadap regulasi eksternal pada proses MEA03 (Managed Compliance With External Requirements)."),
        ("6.", "Menyusun analisis kesenjangan (gap analysis) dan merumuskan rekomendasi perbaikan berbasis roadmap tiga fase (Quick Wins, Standarisasi, dan Optimalisasi) bagi UPT TIK Perguruan Tinggi Contoh."),
    ]
    for num, text in obj_statements:
        add_list_item(doc, num, text)

    add_heading_2(doc, "1.4. Manfaat Proyek")

    add_body_p(doc,
               "Pelaksanaan proyek audit teknologi informasi ini diharapkan dapat memberikan kontribusi manfaat "
               "baik secara teoretis maupun praktis, yang diuraikan sebagai berikut:")

    add_body_p(doc,
               "a. Manfaat Teoretis:\n"
               "Laporan proyek ini diharapkan dapat memperkaya literatur dan referensi kajian akademis dalam bidang "
               "audit sistem informasi dan tata kelola teknologi informasi perguruan tinggi, khususnya mengenai "
               "implementasi praktis kerangka kerja COBIT 2019 pada lima proses domain manajemen dan keselarasan dengan "
               "regulasi perlindungan data pribadi di Indonesia.",
               first_line_indent=Cm(1.2), space_after=4)

    add_body_p(doc,
               "b. Manfaat Praktis bagi Perguruan Tinggi Contoh (Objek Simulasi):\n"
               "Memberikan gambaran objektif, transparan, dan terukur mengenai postur kematangan tata kelola Portal Akademik Perguruan Tinggi Contoh, "
               "menyediakan register risiko teknologi terkini, serta memberikan panduan strategis berupa rekomendasi "
               "dan peta jalan perbaikan prioritas bagi pimpinan universitas dan UPT TIK dalam mengambil keputusan investasi "
               "dan penguatan kontrol keamanan TI.",
               first_line_indent=Cm(1.2), space_after=4)

    add_body_p(doc,
               "c. Manfaat Praktis bagi Mahasiswa dan Tim Auditor:\n"
               "Memberikan pengalaman empiris yang nyata dalam menerapkan konsep teoritis audit sistem informasi, "
               "mengasah kompetensi teknik pengumpulan data lapangan (wawancara, observasi, sampling uji kontrol), serta "
               "memahami secara mendalam tata cara penyusunan laporan temuan audit berstandar industri ISACA.",
               first_line_indent=Cm(1.2), space_after=6)

    add_heading_2(doc, "1.5. Ruang Lingkup Proyek")

    add_body_p(doc,
               "Guna menjaga fokus dan ketajaman analisis, batasan dan ruang lingkup pelaksanaan proyek audit "
               "ditetapkan secara tegas sebagaimana dirangkum pada Tabel I.1 berikut:")

    add_table_caption(doc, "Tabel I.1.", "Ruang Lingkup Proyek Audit TI Portal Akademik Perguruan Tinggi Contoh")
    scope_headers = ["Dimensi Lingkup", "Batasan Pelaksanaan Audit", "Keterangan / Justifikasi"]
    scope_data = [
        ["Objek Sistem Audit", "Portal Akademik Perguruan Tinggi Contoh", "Meliputi modul KRS, KHS, nilai, kurikulum, dan integrasi API PDDikti."],
        ["Kerangka Kerja Acuan", "COBIT 2019 (ISACA)", "Fokus pada 5 proses inti: APO13, BAI06, DSS01, DSS05, dan MEA03."],
        ["Periode Data Audit", "Januari s.d. Juni 2026 (Semester Genap)", "Mencakup log sistem, tiket perubahan (CR), dan jadwal pencadangan data."],
        ["Unit Organisasi", f"{unit} & Biro Akademik Contoh", "Pengelola server, basis data, pengembang aplikasi, dan pengguna BAAK."],
        ["Metodologi Audit", "Kualitatif & Kuantitatif (Wawancara, Observasi, Sampling, Review Dokumen)", "Menggunakan checklist audit 46 butir dan uji petik sampel 30 CR & 25 Akun."],
        ["Di Luar Ruang Lingkup (Out of Scope)", "Audit Keuangan Kampus & Modul SDM Penggajian", "Sistem akuntansi, inventaris aset fisik kampus umum di luar ruang server, dan pengembangan modul software baru tidak diaudit."],
    ]
    add_styled_table(doc, scope_headers, scope_data, col_widths=[3.5, 5.0, 6.0], align_center_cols=[0])
    add_table_source(doc, "Sumber: Tim Proyek Audit Penulis Contoh, 2026")

    # Evidence Box BAB I
    add_evidence_box(doc, "Bukti yang Dikumpulkan pada BAB I", [
        "U-1: Surat Konfirmasi dan Otorisasi Skenario Simulasi Proyek Audit TI Kampus Contoh.",
        "U-2: Matriks Penetapan Ruang Lingkup, Batasan Penelitian, dan Jadwal Audit Semester Genap 2026.",
    ])


    # -------------------------------------------------------------
    # SECTION 4: BAB II LANDASAN TEORI
    # -------------------------------------------------------------
    sec_b2 = doc.add_section(WD_SECTION.NEW_PAGE)
    setup_chapter_section(sec_b2)

    add_heading_bab(doc, "BAB II", "LANDASAN TEORI")

    add_heading_2(doc, "2.1. Pengertian dan Tujuan Audit Teknologi Informasi")

    add_body_p(doc,
               "Audit Teknologi Informasi (Information Technology Audit) didefinisikan oleh ISACA (2021) sebagai "
               "proses pengumpulan dan evaluasi bukti-bukti yang sistematis dan independen untuk menentukan apakah "
               "suatu sistem informasi telah dirancang dan dioperasikan secara efektif dalam menjaga integritas aset "
               "informasi, memelihara integritas data, memungkinkan pencapaian tujuan organisasi secara efektif, serta "
               "mengkonsumsi sumber daya secara efisien. Senada dengan definisi tersebut, Harvard University Information "
               "Security Office (2024) menegaskan bahwa audit TI merupakan evaluasi independen atas tata kelola, kontrol, "
               "dan operasional infrastruktur komputasi untuk menjamin kepatuhan terhadap kebijakan internal dan "
               "regulasi perundang-undangan serta memitigasi kerentanan keamanan siber.")

    add_body_p(doc,
               "Dalam pelaksanaan tata kelola teknologi informasi perguruan tinggi, audit TI memiliki tujuh tujuan "
               "strategis utama yang saling berkesinambungan:")

    audit_goals = [
        ("1.", "Evaluasi Efektivitas dan Efisiensi Operasional: Memastikan sistem teknologi informasi dirancang untuk mendukung kelancaran layanan administrasi dan akademik secara optimal tanpa pemborosan sumber daya."),
        ("2.", "Penjaminan Keamanan Informasi dan Pengendalian: Menilai kecukupan mekanisme perlindungan aset komputasi dari ancaman peretasan, intersepsi data, modifikasi ilegal, dan bencana operasional."),
        ("3.", "Penegakan Kepatuhan (Compliance): Memastikan operasional sistem selaras dengan kerangka regulasi eksternal, hukum perlindungan data pribadi, dan standar akreditasi perguruan tinggi."),
        ("4.", "Penguatan Tata Kelola TI (IT Governance): Menjamin keselarasan antara strategi investasi teknologi informasi dengan sasaran strategis jangka panjang institusi pendidikan."),
        ("5.", "Identifikasi dan Penanganan Risiko (Risk Mitigation): Menemukan secara dini potensi titik lemah (vulnerabilities) sistem dan merumuskan rencana mitigasi sebelum dieksploitasi oleh pihak yang tidak bertanggung jawab."),
        ("6.", "Perumusan Rekomendasi Solutif: Menyajikan peta jalan perbaikan yang terukur, realistis, dan berorientasi pada pencapaian efisiensi tata kelola."),
        ("7.", "Peningkatan Kepercayaan Pemangku Kepentingan (Stakeholders Trust): Menumbuhkan kredibilitas dan reputasi institusi di mata mahasiswa, orang tua, dosen, dunia industri, dan pemerintah."),
    ]
    for num, text in audit_goals:
        add_list_item(doc, num, text)

    add_heading_2(doc, "2.2. Sistem Informasi Akademik (SIAKAD) dalam Pendidikan Tinggi")

    add_body_p(doc,
               "Sistem Informasi Akademik (SIAKAD) adalah aplikasi enterprise berskala besar yang mengelola seluruh "
               "alur kerja administratif dan kegiatan belajar-mengajar pada perguruan tinggi. Komponen inti SIAKAD mencakup "
               "modul registrasi mahasiswa, penjadwalan kuliah, pemilihan Kartu Rencana Studi (KRS) daring, pencatatan "
               "presensi harian, penilaian hasil belajar (KHS), penerbitan transkrip nilai akademik, monitoring skripsi/TA, "
               "hingga pemrosesan kelulusan/yudisium. Secara teknis, SIAKAD terhubung melalui Application Programming "
               "Interface (API) dengan subsistem keuangan kampus (host-to-host perbankan) dan sistem pelaporan nasional "
               "PDDikti Feeder.")

    add_body_p(doc,
               "Pengguna SIAKAD terbagi ke dalam lima kategori peran kerja: (1) Mahasiswa sebagai subjek layanan; "
               "(2) Dosen sebagai pendidik yang mengesahkan rencana studi dan menginput nilai perkuliahan; (3) Staf BAAK "
               "(Biro Administrasi Akademik dan Kemahasiswaan) sebagai pengelola master data akademik; (4) Bagian Keuangan "
               "sebagai pengontrol status pelunasan kewajiban biaya kuliah; dan (5) Administrator UPT TIK yang "
               "bertanggung jawab atas ketersediaan server, keamanan basis data, dan integritas aplikasi.")

    add_heading_2(doc, "2.3. Kerangka Kerja COBIT 2019")

    add_body_p(doc,
               "COBIT (Control Objectives for Information and Related Technologies) merupakan kerangka kerja tata kelola "
               "dan manajemen informasi dan teknologi (I&T) terkemuka di dunia yang dirilis oleh ISACA. Kerangka ini telah "
               "berevolusi dari COBIT 4.1 (2007) yang berfokus pada tujuan pengendalian, COBIT 5 (2012) yang "
               "mengintegrasikan prinsip tata kelola enterprise, hingga versi mutakhir COBIT 2019 yang dirancang sangat "
               "modular, fleksibel, serta mengintegrasikan konsep Design Factors untuk menyesuaikan tata kelola sesuai "
               "profil risiko masing-masing organisasi.")

    add_body_p(doc,
               "COBIT 2019 membagi sasaran tata kelola dan manajemen ke dalam 40 proses yang dikelompokkan dalam 5 domain "
               "utama: (1) Evaluate, Direct, and Monitor (EDM) yang merupakan domain tata kelola dewan pimpinan; "
               "(2) Align, Plan, and Organize (APO) untuk perencanaan strategis; (3) Build, Acquire, and Implement (BAI) "
               "untuk pengembangan sistem; (4) Deliver, Service, and Support (DSS) untuk pelaksanaan operasional dan "
               "layanan harian; serta (5) Monitor, Evaluate, and Assess (MEA) untuk pemantauan kinerja dan kepatuhan.")

    add_body_p(doc,
               "Kelima proses fokus yang diaudit dalam laporan proyek ini dijabarkan secara rinci pada Tabel II.1 berikut:")

    add_table_caption(doc, "Tabel II.1.", "Pemetaan 5 Proses Fokus COBIT 2019 pada Portal Akademik Perguruan Tinggi Contoh")
    cobit_headers = ["Kode Domain", "Nama Proses Resmi COBIT 2019", "Tujuan Proses (Process Purpose)", "Fokus Evaluasi pada Objek SIAKAD"]
    cobit_data = [
        ["APO13", "Managed Security",
         "Menjaga dampak dan kejadian insiden keamanan informasi agar tetap berada dalam batas toleransi risiko yang dapat diterima organisasi.",
         "Evaluasi kebijakan keamanan informasi, klasifikasi data akademik (PII), enkripsi basis data at rest/in transit, dan risk assessment berkala."],
        ["BAI06", "Managed IT Changes",
         "Memungkinkan pengiriman perubahan sistem yang cepat dan andal guna merespons kebutuhan organisasi dengan memitigasi risiko disrupsi operasional.",
         "Pengendalian formulir permohonan Change Request (CR), alur persetujuan CAB, pengujian terpisah pada staging environment, dan rollback plan."],
        ["DSS01", "Managed Operations",
         "Mengantarkan layanan operasional TI sesuai rencana demi memenuhi kebutuhan layanan bisnis dan kepuasan pengguna institusi.",
         "Pelaksanaan SOP harian data center, otomatisasi jadwal backup database, pengujian pemulihan (restore drill), dan monitoring ketersediaan (uptime)."],
        ["DSS05", "Managed Security Services",
         "Melindungi aset informasi enterprise untuk mempertahankan tingkat risiko keamanan informasi yang dapat diterima sesuai kebijakan institusi.",
         "Penerapan Role-Based Access Control (RBAC), pencegahan akun administratif bersama, pencabutan akun alumni/staf nonaktif, proteksi malware, dan SOP insiden."],
        ["MEA03", "Managed Compliance With External Requirements",
         "Memastikan organisasi mematuhi seluruh hukum, regulasi, dan perjanjian kontraktual eksternal yang mengikat secara berkelanjutan.",
         "Inventarisasi regulasi eksternal (compliance register), pemenuhan kewajiban UU PDP No. 27/2022 (DPO & notifikasi kebocoran), dan kepatuhan pelaporan PDDikti."],
    ]
    add_styled_table(doc, cobit_headers, cobit_data, col_widths=[2.0, 3.5, 4.5, 4.5], align_center_cols=[0])
    add_table_source(doc, "Sumber: ISACA COBIT 2019 Framework: Governance and Management Objectives")

    add_heading_3(doc, "2.3.1. Model Tingkat Kapabilitas Proses (Capability Levels 0–5)")

    add_body_p(doc,
               "COBIT 2019 mengadopsi model kapabilitas proses yang selaras dengan standar internasional ISO/IEC 15504 "
               "(Software Engineering - Process Assessment). Tingkat kapabilitas proses diukur pada rentang skala 0 "
               "sampai dengan 5 sebagaimana dijelaskan pada Tabel II.2:")

    add_table_caption(doc, "Tabel II.2.", "Model Tingkat Kapabilitas Proses COBIT 2019 (Level 0–5)")
    cap_headers = ["Tingkat (Level)", "Status Kematangan", "Karakteristik Praktik Tata Kelola", "Bukti Pelaksanaan (Artifacts)"]
    cap_data = [
        ["Level 0", "Incomplete", "Proses tidak diterapkan sama sekali atau gagal mencapai tujuan dasarnya secara konsisten.", "Tidak ada dokumen atau bukti pelaksanaan kerja."],
        ["Level 1", "Initial / Ad-hoc", "Proses mencapai tujuan dasarnya melalui sekumpulan aktivitas tidak terstruktur yang bersifat reaktif dan sangat bergantung pada figur individu.", "Catatan kerja sporadis, komunikasi lisan, tidak ada SOP baku tertulis."],
        ["Level 2", "Managed / Repeatable", "Proses telah direncanakan, dipantau, dan disesuaikan pada tingkat unit kerja. Menghasilkan output kerja yang dapat diulang.", "Dokumen SOP unit kerja, log eksekusi, pelaporan berkala namun belum terstandarisasi institusi."],
        ["Level 3", "Defined", "Proses telah distandarisasi, didokumentasikan rapi, disahkan secara formal oleh manajemen puncak universitas, dan dikomunikasikan menyeluruh.", "SK Rektor, dokumen kebijakan institusi, SOP baku terpusat, formulir resmi yang dipatuhi seragam."],
        ["Level 4", "Quantitatively Managed", "Proses dikendalikan secara kuantitatif menggunakan metrik kinerja terukur (KPI/SLA) dan deviasi proses dapat diprediksi secara statistik.", "Dashboard metrik real-time, laporan pemantauan SLA kuantitatif, analisis tren kapasitas."],
        ["Level 5", "Optimizing", "Proses terus disempurnakan secara berkelanjutan (continuous improvement) melalui otomatisasi cerdas, inovasi teknologi, dan evaluasi akar masalah preventif.", "Otomatisasi DevSecOps penuh, AI-driven anomaly detection, audit mandiri preventif berkelanjutan."],
    ]
    add_styled_table(doc, cap_headers, cap_data, col_widths=[1.8, 2.5, 5.2, 5.0], align_center_cols=[0])
    add_table_source(doc, "Sumber: Adaptasi ISACA COBIT 2019 Design and Implementation Guide")

    add_body_p(doc,
               "Pencapaian kapabilitas pada setiap level ditentukan berdasarkan skala pemenuhan ISO/IEC 15504: "
               "(1) N - Not Achieved (0% s.d. 15%); (2) P - Partially Achieved (>15% s.d. 50%); (3) L - Largely Achieved "
               "(>50% s.d. 85%); dan (4) F - Fully Achieved (>85% s.d. 100%). Suatu proses dinyatakan sah naik ke level "
               "berikutnya apabila seluruh aktivitas pada level tersebut dinilai minimal Largely Achieved (L) atau Fully "
               "Achieved (F), serta seluruh level prasyarat di bawahnya telah berstatus Fully Achieved (F).")

    add_heading_2(doc, "2.4. Teori Pengendalian Internal, Manajemen Risiko, dan Standar Pendukung")

    add_body_p(doc,
               "Pengendalian Internal TI mencakup seluruh kebijakan, prosedur, dan instrumen yang dirancang untuk memberikan "
               "keyakinan memadai bahwa tujuan organisasi dapat tercapai dan risiko yang tidak diinginkan dapat dicegah. "
               "Kontrol TI terbagi menjadi: (1) General Controls (ITGC) yang mengendalikan lingkungan komputasi luas "
               "(manajemen perubahan, kontrol akses, backup); dan (2) Application Controls yang tertanam di dalam logika "
               "kode program (validasi input, pemeriksaan otorisasi transaksi KRS). Berdasarkan fungsinya, kontrol "
               "dibedakan atas kontrol preventif (mencegah kesalahan), detektif (menemukan insiden), dan korektif "
               "(memulihkan sistem pasca-insiden).")

    add_body_p(doc,
               "Manajemen Risiko TI merupakan proses terstruktur untuk mengidentifikasi ancaman (threats), menganalisis "
               "kerentanan (vulnerabilities), dan memperkirakan dampak (impact) serta kemungkinan terjadinya (likelihood). "
               "Selain COBIT 2019, analisis dalam laporan ini mengintegrasikan standar pendukung: ISO/IEC 27001 untuk "
               "prinsip kerahasiaan, integritas, dan ketersediaan (CIA Triad); ITIL 4 untuk praktik Change Enablement; "
               "serta UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi yang mewajibkan penerapan enkripsi dan "
               "penunjukan Pejabat Pelindung Data Pribadi (DPO).")

    # Evidence Box BAB II
    add_evidence_box(doc, "Bukti yang Dikumpulkan pada BAB II", [
        "U-3: Repositori Artikel Ilmiah Rujukan Terverifikasi (5 artikel terakreditasi mengenai Audit TI, COBIT 2019, dan SIAKAD).",
        "U-4: Ringkasan Analitis Eksekutif Artikel Rujukan Ilmiah (disajikan pada Lampiran L-A).",
        "U-5: Struktur Sitasi Ilmiah Berstandar APA/IEEE yang Diintegrasikan ke dalam Naskah Laporan.",
    ])


    # -------------------------------------------------------------
    # SECTION 5: BAB III GAMBARAN UMUM OBJEK AUDIT
    # -------------------------------------------------------------
    sec_b3 = doc.add_section(WD_SECTION.NEW_PAGE)
    setup_chapter_section(sec_b3)

    add_heading_bab(doc, "BAB III", "GAMBARAN UMUM OBJEK AUDIT")

    add_heading_2(doc, "3.1. Profil Portal Akademik Perguruan Tinggi Contoh")

    add_body_p(doc,
               "Perguruan Tinggi Contoh merupakan institusi pendidikan tinggi yang mengimplementasikan sistem informasi akademik dalam skenario simulasi terkontrol untuk "
               "menguji kerangka kerja tata kelola audit TI berbasis COBIT 2019 pada lingkungan akademik perguruan tinggi "
               "secara komprehensif. Dalam skenario simulasi ini, Perguruan Tinggi Contoh mengoperasikan Portal Akademik "
               "terpadu yang dapat diakses melalui portal web daring (`portal-mhs.contoh.ac.id` untuk mahasiswa, `portal-dosen.contoh.ac.id` "
               "untuk tenaga pendidik) serta aplikasi seluler akademik. Sistem simulasi ini memodelkan layanan bagi lebih dari 10.000 mahasiswa "
               "aktif dan ratusan dosen di seluruh fakultas.")

    add_body_p(doc,
               "Portal Akademik Perguruan Tinggi Contoh memfasilitasi transaksi akademik yang sangat padat, mencakup proses pengisian rencana studi (KRS) "
               "pada awal semester, presensi kehadiran perkuliahan dengan integrasi kode QR, ujian daring (CBT), penilaian "
               "dan penerbitan KHS, hingga pelaporan berkala ke PDDikti Kemendikbudristek. Sasaran strategis universitas "
               "menuntut SIAKAD dapat diakses tanpa hambatan 24 jam sehari, 7 hari seminggu, dengan jaminan integritas "
               "transkrip nilai yang bebas dari manipulasi serta perlindungan mutlak atas kerahasiaan data pribadi civitas.")

    add_heading_2(doc, "3.2. Struktur Organisasi Pengelola TI (UPT TIK Perguruan Tinggi Contoh)")

    add_body_p(doc,
               f"Pengelolaan, pengembangan, dan pemeliharaan {auditee} berada di bawah wewenang {unit}. Organogram struktur "
               "organisasi UPT TIK disajikan pada Gambar III.1 berikut:")

    # Gambar III.1: Struktur Organisasi
    img_org = _find_diagram_file("diagram_organisasi_upt_tik.png", diagram_search_dirs)
    if img_org.exists():
        p_img_org = doc.add_paragraph()
        format_paragraph(p_img_org, space_before=10, space_after=2, line_spacing=1.0,
                         align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None, keep_with_next=True)
        r_img_org = p_img_org.add_run()
        r_img_org.add_picture(str(img_org), width=Cm(14.0))
        add_figure_caption(doc, "Gambar III.1.", f"Struktur Organisasi {unit}",
                            source_text="Sumber: Hasil Olah Data Observasi Lapangan UPT TIK Perguruan Tinggi Contoh, 2026")

    add_body_p(doc,
               "Berdasarkan hasil observasi dan wawancara terhadap organogram UPT TIK, pembagian tanggung jawab "
               "operasional mencakup: (1) Kepala UPT TIK yang menetapkan visi, kebijakan, dan alokasi anggaran; "
               "(2) Koordinator Pengembangan Aplikasi yang memimpin tim programmer SIAKAD; (3) Koordinator Jaringan "
               "dan Server yang mengelola infrastruktur fisik data center dan firewall; (4) Database Administrator (DBA) "
               "yang mengawal skema basis data dan pencadangan; serta (5) Helpdesk yang menangani keluhan pengguna.")

    add_body_p(doc,
               "Analisis Pemisahan Tugas (Segregation of Duties / SoD) menunjukkan bahwa pemisahan hak akses antara tim "
               "pengembang (developer) dan akses root server produksi telah berjalan cukup baik. Namun, hasil audit "
               "menemukan kelemahan tata kelola: fungsi Petugas Keamanan Informasi (Information Security Officer) masih "
               "dirangkap oleh administrator jaringan, dan posisi Pejabat Pelindung Data Pribadi (DPO) sesuai mandat "
               "UU PDP belum dibentuk secara definitif melalui Surat Keputusan Rektor.")

    add_heading_2(doc, "3.3. Infrastruktur dan Arsitektur Sistem")

    add_body_p(doc,
               "Arsitektur teknologi Portal Akademik Perguruan Tinggi Contoh menerapkan pola Multi-Tier Architecture dengan segmentasi keamanan "
               "jaringan yang dirancang untuk menangani beban transaksi tinggi secara terdistribusi. Diagram arsitektur "
               "logis dan fisik sistem disajikan pada Gambar III.2:")

    # Gambar III.2: Arsitektur Sistem
    img_arch = _find_diagram_file("diagram_arsitektur_siakad.png", diagram_search_dirs)
    if img_arch.exists():
        p_img_arch = doc.add_paragraph()
        format_paragraph(p_img_arch, space_before=10, space_after=2, line_spacing=1.0,
                         align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None, keep_with_next=True)
        r_img_arch = p_img_arch.add_run()
        r_img_arch.add_picture(str(img_arch), width=Cm(14.0))
        add_figure_caption(doc, "Gambar III.2.", "Arsitektur Multi-Tier dan Keamanan Portal Akademik Perguruan Tinggi Contoh",
                            source_text="Sumber: Dokumentasi Arsitektur Sistem UPT TIK Perguruan Tinggi Contoh, 2026")

    add_body_p(doc,
               "Komponen infrastruktur Portal Akademik Perguruan Tinggi Contoh terbagi dalam empat lapisan utama:")

    infra_points = [
        ("1.", "Lapisan Keamanan Perimeter & Web (DMZ VLAN 10): Mengoperasikan Firewall Lapis perimeter (FortiGate NGFW) dengan modul Web Application Firewall (WAF) dan cluster Nginx Reverse Proxy sebagai SSL/TLS Terminator (protokol TLS 1.3 berenkripsi kuat)."),
        ("2.", "Lapisan Aplikasi (Application Zone VLAN 20): Menjalankan engine aplikasi berbasis PHP 8.2 dengan framework Laravel modern, antrean transaksi Redis Queue, serta integrasi modul Feeder PDDikti dan Host-to-Host payment perbankan."),
        ("3.", "Lapisan Penyimpanan Data (Data Storage Zone VLAN 30): Kluster basis data relasional MySQL Enterprise dalam topologi Primary-Replica (Master-Slave). Node utama menangani transaksi tulis (KRS dan nilai), sedangkan Read Replicas melayani penelusuran jadwal dan transkrip guna mencegah database locking."),
        ("4.", "Lapisan Manajemen & Pencadangan (Management Zone VLAN 40): Terdiri dari Network Attached Storage (NAS) untuk pencadangan lokal harian, mirror cloud storage untuk Disaster Recovery (DR), server monitoring Zabbix, serta Bastion Jump Host dengan autentikasi berbasis SSH Key dan MFA."),
    ]
    for num, text in infra_points:
        add_list_item(doc, num, text)

    add_body_p(doc,
               "Pengendalian Akses Pengguna (Role-Based Access Control / RBAC) diterapkan pada basis data SIAKAD dengan "
               "membagi kewenangan secara rigid antara akun Mahasiswa, Dosen Penasihat Akademik (PA), Staf BAAK, Staf "
               "Keuangan, dan Administrator. Namun demikian, audit teknis menemukan bahwa data pribadi pada tabel basis data "
               "masih tersimpan dalam bentuk teks terbuka (plaintext) tanpa enkripsi at rest, dan pengujian pemulihan data "
               "cadangan belum pernah disimulasikan secara berkala.")

    add_heading_2(doc, "3.4. Kebijakan dan Prosedur TI yang Berlaku")

    add_body_p(doc,
               "Evaluasi terhadap kelengkapan dokumentasi tata kelola menunjukkan bahwa universitas telah memiliki sejumlah "
               "pedoman dasar, namun masih terdapat kesenjangan signifikan terhadap standar ideal COBIT 2019, seperti "
               "terangkum pada Tabel III.1 berikut:")

    add_table_caption(doc, "Tabel III.1.", "Inventaris Kebijakan dan Prosedur TI Eksisting Portal Akademik Perguruan Tinggi Contoh")
    policy_headers = ["No", "Nama Dokumen Kebijakan / SOP", "Status Eksistensi", "Tahun Pembaruan", "Analisis Kesesuaian Standar COBIT 2019"]
    policy_data = [
        ["1", "Kebijakan Keamanan Informasi Institusi Contoh (No. TI-CONTOH/01)", "Ada (Terdokumentasi)", "2024", "Belum diperbarui mencakup mandat UU PDP No. 27/2022 dan klasifikasi data PII."],
        ["2", "SOP Manajemen Perubahan Sistem (Change Management)", "Tidak Ada (Ad-hoc)", "-", "Ketiadaan formulir CR baku dan ketiadaan kewajiban uji staging pra-rilis."],
        ["3", "SOP Pencadangan dan Pemulihan Data (Backup & Restore)", "Sebagian (Hanya Backup)", "2023", "Hanya mengatur skrip backup otomatis; prosedur pengujian restore tidak tertulis."],
        ["4", "SOP Pengelolaan Hak Akses Pengguna (Access Control)", "Ada (Administratif)", "2024", "Mengatur permohonan akun staf, namun belum mengatur audit offboarding alumni."],
        ["5", "SOP Penanganan Insiden Keamanan Siber", "Tidak Ada (Lisan)", "-", "Penanganan serangan hanya dilakukan reaktif tanpa dokumentasi standar forensik."],
        ["6", "Register Kepatuhan Regulasi Eksternal (Compliance)", "Tidak Ada", "-", "Belum ada inventarisasi regulasi nasional terkait TI perguruan tinggi dan DPO."],
    ]
    add_styled_table(doc, policy_headers, policy_data, col_widths=[1.0, 4.5, 2.5, 1.8, 4.7], align_center_cols=[0, 2, 3])
    add_table_source(doc, "Sumber: Hasil Review Dokumentasi UPT TIK Perguruan Tinggi Contoh, 2026")

    # Evidence Box BAB III
    add_evidence_box(doc, "Bukti yang Dikumpulkan pada BAB III", [
        f"U-6: Bagan Organogram Simulasi dan Mandat Tugas {unit}.",
        "U-7: Inventaris Spesifikasi Aset Perangkat Keras Server, Versi RDBMS MySQL, dan Lisensi Perangkat Lunak.",
        "U-8: Cetak Biru Diagram Topologi Jaringan, Konfigurasi VLAN, dan Konfigurasi Firewall Data Center.",
        "U-9: Salinan Dokumen Kebijakan dan SOP Operasional TI Eksisting (Nomor Registrasi Dokumen UPT TIK).",
        "U-10: Berita Acara Observasi Fasilitas Fisik Ruang Server (Suhu AC, FM-200, UPS Cadangan, dan Logbook Tamu).",
    ])


    # -------------------------------------------------------------
    # SECTION 6: BAB IV PEMBAHASAN (CORE AUDIT FINDINGS)
    # -------------------------------------------------------------
    sec_b4 = doc.add_section(WD_SECTION.NEW_PAGE)
    setup_chapter_section(sec_b4)

    add_heading_bab(doc, "BAB IV", "PEMBAHASAN")

    add_heading_2(doc, "4.1. Teknik Pengumpulan Data")

    add_body_p(doc,
               "Pengumpulan data audit dilaksanakan secara komprehensif menggunakan kombinasi empat metode standar ISACA: "
               "(1) Wawancara semi-terstruktur dengan lima pemangku kepentingan kunci (Kepala UPT TIK, Koordinator Pengembang "
               "SIAKAD, Database Administrator/Sysadmin, Kepala Biro Administrasi Akademik BAAK, dan Staf Helpdesk TI); "
               "(2) Observasi langsung terhadap fasilitas fisik data center kampus, topologi jaringan, dan alur kerja operasional; "
               "(3) Penelaahan dokumen kebijakan, SOP, log sistem, dan arsitektur; serta (4) Pengujian sampel empiris (sampling).")

    add_body_p(doc,
               "Pengujian sampel dilaksanakan pada dua area berisiko tinggi dengan parameter yang terukur secara statistik:")

    sampling_points = [
        ("a.", "Sampel Perubahan Sistem (BAI06 - Bukti E-2): Dari populasi 30 Change Request (CR) yang diajukan selama periode Januari s.d. Juni 2026, dilakukan pemeriksaan kepatuhan terhadap formulir otorisasi, pengujian di staging, dan ketersediaan rollback plan. Hasil uji menunjukkan sebanyak 12 dari 30 CR (40.0%) diimplementasikan secara ad-hoc langsung ke server produksi tanpa formulir persetujuan resmi dan tanpa uji pra-rilis."),
        ("b.", "Sampel Akun Pengguna (DSS05 - Bukti E-4): Diambil sampel 25 akun pengguna yang terdiri dari 10 alumni mahasiswa lulusan semester lalu, 5 staf mutasi/keluar, 5 akun mahasiswa aktif, dan 5 akun administratif. Hasil pengujian membuktikan bahwa 6 dari 10 akun alumni (60.0%) masih berstatus aktif dan dapat melakukan login ke dalam portal akademik, serta teridentifikasi satu akun generik (`admin_portal`) yang kata sandinya dibagi pakai oleh tiga staf teknis."),
    ]
    for num, text in sampling_points:
        p_s = doc.add_paragraph()
        format_paragraph(p_s, space_before=1, space_after=3, line_spacing=2.0,
                         align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent=Cm(-0.6))
        p_s.paragraph_format.left_indent = Cm(1.2)
        r_num = p_s.add_run(num + " ")
        format_run(r_num, size_pt=12, bold=True)
        r_text = p_s.add_run(text)
        format_run(r_text, size_pt=12, bold=False)

    add_heading_2(doc, "4.2. Penilaian Risiko dan Pengendalian")

    add_body_p(doc,
               "Penilaian risiko dilaksanakan menggunakan matriks 5x5 yang memetakan Kemungkinan Terjadi (Likelihood, skala 1–5) "
               "dengan Tingkat Dampak (Impact, skala 1–5). Skor risiko dihitung melalui perkalian (Risk Score = L x I) dengan "
               "kategori: Rendah (1–4), Sedang (5–9), dan Tinggi (10–25). Pemetaan posisi risiko 5 domain fokus disajikan "
               "pada Gambar IV.1 dan dirinci pada Tabel IV.1:")

    # Gambar IV.1: Risk Matrix
    img_risk = _find_diagram_file("diagram_risk_matrix.png", diagram_search_dirs)
    if img_risk.exists():
        p_img_risk = doc.add_paragraph()
        format_paragraph(p_img_risk, space_before=10, space_after=2, line_spacing=1.0,
                         align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None, keep_with_next=True)
        r_img_risk = p_img_risk.add_run()
        r_img_risk.add_picture(str(img_risk), width=Cm(12.5))
        add_figure_caption(doc, "Gambar IV.1.", "Matriks Penilaian Risiko 5x5 (Likelihood vs Impact) Portal Akademik Perguruan Tinggi Contoh",
                            source_text="Sumber: Hasil Olah Data Risk Assessment Tim Audit, 2026")

    add_table_caption(doc, "Tabel IV.1.", "Matriks Penilaian Risiko (Risk Register) 5 Domain Fokus")
    risk_headers = ["No", "Domain", "Skenario Risiko Spesifik", "Likelihood", "Impact", "Skor", "Tingkat Risiko", "Toleransi"]
    risk_data = [
        ["1", "APO13", "Kebocoran data pribadi (PII) akibat ketiadaan enkripsi basis data at rest.", "4 (Sering)", "5 (Kritis)", "20", "Tinggi (High)", "Tidak Dapat Ditoleransi"],
        ["2", "BAI06", "Downtime layanan atau korupsi skema DB akibat rilis langsung tanpa uji dan rollback plan.", "4 (Sering)", "4 (Besar)", "16", "Tinggi (High)", "Tidak Dapat Ditoleransi"],
        ["3", "DSS01", "Kegagalan pemulihan data saat server crash karena file backup korup tak pernah diuji restore.", "3 (Mungkin)", "5 (Kritis)", "15", "Tinggi (High)", "Perlu Mitigasi Segera"],
        ["4", "DSS05", "Penyalahgunaan hak akses/modifikasi nilai lewat akun eks-mahasiswa atau akun admin bersama.", "4 (Sering)", "4 (Besar)", "16", "Tinggi (High)", "Tidak Dapat Ditoleransi"],
        ["5", "MEA03", "Sanksi administratif dan denda UU PDP No. 27/2022 akibat ketiadaan DPO dan registrasi regulasi.", "3 (Mungkin)", "4 (Besar)", "12", "Tinggi (High)", "Perlu Tindak Lanjut"],
    ]
    add_styled_table(doc, risk_headers, risk_data, col_widths=[0.8, 1.8, 4.8, 1.8, 1.8, 1.0, 2.3, 2.5], align_center_cols=[0, 1, 3, 4, 5, 6])
    add_table_source(doc, "Sumber: Hasil Analisis Risiko Tim Proyek Audit, 2026")

    add_body_p(doc,
               f"Evaluasi terhadap pengendalian eksisting (existing controls) yang dimodelkan pada lingkungan {unit} diringkas pada Tabel IV.2 berikut:")

    add_table_caption(doc, "Tabel IV.2.", "Evaluasi Pengendalian Eksisting pada Portal Akademik Perguruan Tinggi Contoh")
    ctrl_headers = ["Proses", "Pengendalian Eksisting", "Jenis Kontrol", "Evaluasi Efektivitas Kontrol", "Kesenjangan Pengendalian"]
    ctrl_data = [
        ["APO13", "Enkripsi transmisi TLS 1.3 pada portal web dan mobile.", "Preventif", "Cukup Efektif (Transit)", "Tabel basis data MySQL tetap plaintext (tidak ada kontrol at rest)."],
        ["BAI06", "Pengujian mandiri oleh programmer di laptop lokal.", "Detektif", "Tidak Memadai", "Tidak ada staging environment resmi yang terpisah dan tidak ada log approval."],
        ["DSS01", "Pencadangan database harian otomatis via cron job ke NAS.", "Korektif", "Lemah", "Backup berjalan rutin namun tidak pernah diverifikasi dengan simulasi restore."],
        ["DSS05", "Pemberian hak akses berbasis peran (RBAC) pada antarmuka.", "Preventif", "Lemah", "Akun alumni tidak dinonaktifkan otomatis dan tidak ada proteksi MFA admin."],
        ["MEA03", "Sinkronisasi berkala data akademik ke API PDDikti Feeder.", "Detektif", "Cukup Efektif (PDDikti)", "Kepatuhan UU PDP No. 27/2022 sama sekali belum diakomodasi."],
    ]
    add_styled_table(doc, ctrl_headers, ctrl_data, col_widths=[1.5, 3.8, 2.0, 3.2, 4.5], align_center_cols=[0, 2])
    add_table_source(doc, "Sumber: Hasil Evaluasi Kontrol Tim Audit, 2026")

    add_heading_2(doc, "4.3. Identifikasi Temuan Audit (Struktur CCCE)")

    add_body_p(doc,
               "Seluruh kelemahan tata kelola yang ditemukan dirumuskan secara sistematis menggunakan format standar "
               "internasional CCCE (Condition, Criteria, Cause, Effect) guna menghasilkan dasar rekomendasi yang teruji:")

    # Detailed CCCE Findings 1 to 5
    ccce_list = [
        ("Temuan 1 - Domain APO13 (Managed Security)",
         "Data pribadi mahasiswa (NIK, tanggal lahir, nama ibu kandung, dan transkrip nilai) tersimpan dalam basis data MySQL dalam bentuk teks terbuka (plaintext) tanpa enkripsi at rest. Kebijakan keamanan TI universitas belum mengatur klasifikasi data.",
         "COBIT 2019 APO13.01 & APO13.02; ISO/IEC 27001 Kontrol A.8.2; UU No. 27 Tahun 2022 Pasal 35 (Kewajiban menjaga keamanan pemrosesan data pribadi dengan enkripsi).",
         "Ketiadaan SOP klasifikasi data akademik dan belum diaktifkannya Transparent Data Encryption (TDE / AES-256) pada mesin kluster database MySQL.",
         "Risiko kebocoran data massal (data breach) jika storage server atau file backup diakses pihak internal tidak sah, mengekspos Perguruan Tinggi Contoh pada denda sanksi UU PDP dan rusaknya reputasi institusi.",
         "Mengaktifkan TDE / enkripsi tingkat kolom AES-256 pada tabel data pribadi, memperbarui dokumen kebijakan keamanan TI, dan menetapkan matriks klasifikasi data."),

        ("Temuan 2 - Domain BAI06 (Managed IT Changes)",
         "Berdasarkan pengujian 30 sampel Change Request (CR), sebanyak 12 perubahan (40.0%) diterapkan langsung ke server produksi tanpa formulir tertulis, tanpa approval pimpinan teknis, dan tanpa uji pra-rilis di lingkungan staging. Tidak tersedia rollback plan tertulis.",
         "COBIT 2019 BAI06.01 s.d. BAI06.04; Standar ITIL 4 Change Enablement; Kebijakan Pengembangan Sistem Perguruan Tinggi Contoh.",
         "Budaya kerja ad-hoc demi mengejar rilis cepat (hotfix) atas desakan operasional akademik serta ketiadaan sistem pelacak tiket perubahan terpadu.",
         "Tingginya angka insiden downtime saat masa KRS, inkonsistensi skema basis data, dan kesulitan melacak akar penyebab saat timbul cacat program (bug) baru di lingkungan produksi.",
         "Mewajibkan alur Change Management formal (tiket digital, analisis risiko, approval CAB), menyediakan staging environment terisolasi, dan mewajibkan rollback script sebelum deployment."),

        ("Temuan 3 - Domain DSS01 (Managed Operations)",
         "Pencadangan data basis data SIAKAD berjalan rutin setiap hari ke storage NAS, namun tidak pernah sekalipun dilakukan pengujian pemulihan data (restore drill) selama 12 bulan terakhir. Tidak tersedia dokumen SOP pengujian pemulihan bencana (Disaster Recovery).",
         "COBIT 2019 DSS01.01 & DSS01.03; ISO/IEC 27001 Kontrol A.12.3.1 (Information Backup); Standar Pusat Data Perguruan Tinggi Contoh.",
         "Keterbatasan server pengujian cadangan dan persepsi keliru bahwa log eksekusi backup yang berstatus sukses sudah menjamin file backup dapat dipulihkan dengan sempurna.",
         "Risiko silent corruption pada berkas backup; potensi kegagalan total pemulihan data (unrecoverable disaster) saat server utama mengalami kerusakan fatal atau serangan ransomware.",
         "Menyusun SOP Pengujian Pemulihan Data, menjadwalkan simulasi restore drill berkala minimal sebulan sekali pada server uji, dan mendokumentasikan hasilnya dalam Berita Acara Uji Restore."),

        ("Temuan 4 - Domain DSS05 (Managed Security Services)",
         "Pengujian sampel 25 akun membuktikan 6 dari 10 akun alumni masih berstatus aktif dapat login ke portal data akademik. Ditemukan akun superadmin generik (admin_portal) yang dibagi pakai oleh 3 staf tanpa penerapan Multi-Factor Authentication (MFA) dan tanpa review hak akses semesteran.",
         "COBIT 2019 DSS05.04; ISO/IEC 27001 Kontrol A.9.2 (User Access Management); Prinsip Least Privilege.",
         "Ketiadaan integrasi otomatis antara modul yudisium kelulusan BAAK dengan skrip penonaktifan akun (offboarding), serta kebiasaan membagi password demi efisiensi kerja teknis.",
         "Risiko akses ilegal dari akun terlantar (dormant accounts); hilangnya akuntabilitas individu saat terjadi manipulasi nilai atau modifikasi skema data karena penggunaan akun bersama.",
         "Menerapkan akun administratif individual (named accounts) wajib MFA, mengintegrasikan otomasi penonaktifan akun alumni dengan modul yudisium, dan menggelar User Access Review tiap awal semester."),

        ("Temuan 5 - Domain MEA03 (Managed Compliance With External Requirements)",
         "Organisasi pengelola SIAKAD belum memiliki Dokumen Register Kepatuhan Regulasi. Belum ada penunjukan Pejabat Pelindung Data Pribadi (DPO) melalui SK Rektor, belum tersedia SOP permohonan hak subjek data, dan tiada alur formal notifikasi kebocoran data maksimal 3 x 24 jam.",
         "COBIT 2019 MEA03.01 s.d. MEA03.04; UU No. 27 Tahun 2022 Pasal 46, 53, 54; Permendikbudristek No. 53 Tahun 2023.",
         "Asumsi bahwa urusan kepatuhan hukum semata-mata ranah biro hukum terpisah dan belum terinternalisasi ke dalam tata kelola teknologi informasi UPT TIK.",
         "Ancaman sanksi hukum administratif berupa penghentian sementara operasional sistem akademik, denda finansial berat dari lembaga pengawas PDP, serta tuntutan ganti rugi perdata dari civitas.",
         "Menerbitkan SK Rektor pembentukan Tim Kepatuhan TI dan DPO, menyusun dokumen register kepatuhan terpadu, serta menyusun SOP Tanggap Insiden Kebocoran Data (Data Breach Notification)."),
    ]

    for title, cond, crit, cause, eff, rec in ccce_list:
        add_heading_3(doc, title)
        p_c = doc.add_paragraph()
        format_paragraph(p_c, space_before=1, space_after=2, line_spacing=1.5, first_line_indent=None)
        r_c_lbl = p_c.add_run("Kondisi Nyata (Condition): ")
        format_run(r_c_lbl, size_pt=11.5, bold=True)
        r_c_txt = p_c.add_run(cond)
        format_run(r_c_txt, size_pt=11.5)

        p_cr = doc.add_paragraph()
        format_paragraph(p_cr, space_before=1, space_after=2, line_spacing=1.5, first_line_indent=None)
        r_cr_lbl = p_cr.add_run("Kriteria Standar (Criteria): ")
        format_run(r_cr_lbl, size_pt=11.5, bold=True)
        r_cr_txt = p_cr.add_run(crit)
        format_run(r_cr_txt, size_pt=11.5)

        p_ca = doc.add_paragraph()
        format_paragraph(p_ca, space_before=1, space_after=2, line_spacing=1.5, first_line_indent=None)
        r_ca_lbl = p_ca.add_run("Akar Penyebab (Cause): ")
        format_run(r_ca_lbl, size_pt=11.5, bold=True)
        r_ca_txt = p_ca.add_run(cause)
        format_run(r_ca_txt, size_pt=11.5)

        p_ef = doc.add_paragraph()
        format_paragraph(p_ef, space_before=1, space_after=2, line_spacing=1.5, first_line_indent=None)
        r_ef_lbl = p_ef.add_run("Akibat / Dampak Risiko (Effect): ")
        format_run(r_ef_lbl, size_pt=11.5, bold=True)
        r_ef_txt = p_ef.add_run(eff)
        format_run(r_ef_txt, size_pt=11.5)

        p_rc = doc.add_paragraph()
        format_paragraph(p_rc, space_before=1, space_after=6, line_spacing=1.5, first_line_indent=None)
        r_rc_lbl = p_rc.add_run("Rekomendasi Tindakan: ")
        format_run(r_rc_lbl, size_pt=11.5, bold=True, color_rgb=(29, 78, 216))
        r_rc_txt = p_rc.add_run(rec)
        format_run(r_rc_txt, size_pt=11.5)

    add_table_caption(doc, "Tabel IV.3.", "Rekapitulasi Temuan Audit Berstruktur CCCE")
    recap_headers = ["Domain", "Kondisi (Temuan Utama)", "Kriteria Acuan", "Level Risiko", "Rekomendasi Utama"]
    recap_data = [
        ["APO13", "Data pribadi PII plaintext tanpa enkripsi at rest.", "COBIT APO13, ISO 27001, UU PDP", "Tinggi (20)", "Aktifkan TDE AES-256 & klasifikasi data."],
        ["BAI06", "40% CR rilis langsung ke produksi tanpa tiket & staging.", "COBIT BAI06, ITIL 4", "Tinggi (16)", "Terapkan formal change ticketing & staging gate."],
        ["DSS01", "Backup harian rutin namun tak pernah diuji restore drill.", "COBIT DSS01, ISO 27001", "Tinggi (15)", "Buat SOP restore & simulasi bulanan server uji."],
        ["DSS05", "6 akun alumni aktif & akun superadmin generic tanpa MFA.", "COBIT DSS05, RBAC", "Tinggi (16)", "Cabut akses alumni, terapkan MFA & named user."],
        ["MEA03", "Ketiadaan compliance register, DPO, dan SOP UU PDP.", "COBIT MEA03, UU PDP No. 27/2022", "Tinggi (12)", "Terbitkan SK DPO Rektor & SOP breach 3x24 jam."],
    ]
    add_styled_table(doc, recap_headers, recap_data, col_widths=[1.5, 4.0, 3.0, 1.8, 4.5], align_center_cols=[0, 3])
    add_table_source(doc, "Sumber: Hasil Sintesis Temuan Tim Audit, 2026")

    add_heading_2(doc, "4.4. Analisis Kesesuaian Framework (Gap Analysis)")

    add_body_p(doc,
               "Pengukuran tingkat kapabilitas tata kelola didasarkan pada hasil instrumen checklist audit operasional "
               "sebanyak 46 butir yang mencakup 5 domain proses fokus (Lampiran L-B). Rekapitulasi kuantitatif kepatuhan "
               "per proses disajikan pada Tabel IV.4:")

    add_table_caption(doc, "Tabel IV.4.", "Rekapitulasi Kuantitatif Checklist Audit COBIT 2019")
    chk_headers = ["Domain Proses COBIT 2019", "Jumlah Butir", "Sesuai (✓)", "Tidak Sesuai (✗)", "Persentase (%)", "Kategori Pencapaian"]
    chk_data = [
        ["APO13 - Managed Security", "10", "4", "6", "40.0%", "Partially Achieved (P)"],
        ["BAI06 - Managed IT Changes", "9", "3", "6", "33.3%", "Partially Achieved (P)"],
        ["DSS01 - Managed Operations", "9", "6", "3", "66.7%", "Largely Achieved (L)"],
        ["DSS05 - Managed Security Services", "10", "5", "5", "50.0%", "Partially Achieved (P)"],
        ["MEA03 - Managed Compliance", "8", "3", "5", "37.5%", "Partially Achieved (P)"],
        ["TOTAL RATA-RATA", "46", "21", "25", "45.7%", "Partially Achieved (P)"],
    ]
    add_styled_table(doc, chk_headers, chk_data, col_widths=[4.5, 2.0, 2.0, 2.0, 2.0, 3.0], align_center_cols=[1, 2, 3, 4, 5])
    add_table_source(doc, "Sumber: Hasil Rekapitulasi Checklist Audit 46 Butir, 2026")

    add_body_p(doc,
               "Berdasarkan persentase kepatuhan dan aturan progresi kapabilitas COBIT 2019, dilakukan pemetaan "
               "kesenjangan (gap analysis) antara tingkat kapabilitas saat ini (Current Level) dengan tingkat target yang "
               "diharapkan institusi (Target Level) sebagaimana disajikan pada Tabel IV.5:")

    add_table_caption(doc, "Tabel IV.5.", "Matriks Analisis Kesenjangan (Gap Analysis) Kapabilitas")
    gap_headers = ["Domain Proses", "Current Level", "Target Level", "Kesenjangan (Gap)", "Analisis Status Kesenjangan Aktual"]
    gap_data = [
        ["APO13 (Managed Security)", "Level 2 (Managed)", "Level 3 (Defined)", "1", "Kebijakan dasar ada namun belum diperbarui; enkripsi at rest dan matriks klasifikasi data belum dibakukan."],
        ["BAI06 (Managed IT Changes)", "Level 1 (Initial)", "Level 3 (Defined)", "2", "Perubahan sistem masih ad-hoc dan tidak terdokumentasi seragam; membutuhkan alur ticketing resmi."],
        ["DSS01 (Managed Operations)", "Level 2 (Managed)", "Level 4 (Quantitatively Managed)", "2", "Operasional dan backup harian berjalan teratur; gap terletak pada ketiadaan uji restore dan SLA kuantitatif."],
        ["DSS05 (Security Services)", "Level 1 (Initial)", "Level 3 (Defined)", "2", "Pemberian hak akses manual dan akun bersama; membutuhkan sistem SSO, MFA, dan otomasi offboarding alumni."],
        ["MEA03 (Managed Compliance)", "Level 1 (Initial)", "Level 3 (Defined)", "2", "Pelaporan PDDikti berjalan baik; kesenjangan besar pada kepatuhan UU PDP No. 27/2022 dan struktur DPO."],
        ["RATA-RATA KEMATANGAN", "Level 1.4", "Level 3.2", "1.8", "Status Umum: Initial (Ad-hoc) menuju Defined. Kesenjangan rata-rata sebesar 1.8 level."],
    ]
    add_styled_table(doc, gap_headers, gap_data, col_widths=[3.5, 2.2, 2.2, 1.8, 5.5], align_center_cols=[1, 2, 3])
    add_table_source(doc, "Sumber: Hasil Perhitungan Gap Analysis Tim Audit, 2026")

    # Gambar IV.2: Capability Chart
    img_cap = _find_diagram_file("diagram_radar_capability.png", diagram_search_dirs)
    if img_cap.exists():
        p_img_cap = doc.add_paragraph()
        format_paragraph(p_img_cap, space_before=10, space_after=2, line_spacing=1.0,
                         align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None, keep_with_next=True)
        r_img_cap = p_img_cap.add_run()
        r_img_cap.add_picture(str(img_cap), width=Cm(13.0))
        add_figure_caption(doc, "Gambar IV.2.", "Perbandingan Tingkat Kapabilitas Eksisting vs Target COBIT 2019",
                            source_text="Sumber: Hasil Visualisasi Gap Analysis Tim Audit, 2026")

    add_heading_2(doc, "4.5. Rekomendasi Perbaikan dan Rencana Tindak Lanjut")

    add_body_p(doc,
               "Penyelesaian kesenjangan kapabilitas tata kelola Portal Akademik Perguruan Tinggi Contoh dirumuskan ke dalam Peta Jalan (Roadmap) "
               "Perbaikan 3 Fase yang terstruktur dan realistis sebagaimana disajikan pada Gambar IV.3:")

    # Gambar IV.3: Roadmap Diagram
    img_road = _find_diagram_file("diagram_roadmap_perbaikan.png", diagram_search_dirs)
    if img_road.exists():
        p_img_road = doc.add_paragraph()
        format_paragraph(p_img_road, space_before=10, space_after=2, line_spacing=1.0,
                         align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None, keep_with_next=True)
        r_img_road = p_img_road.add_run()
        r_img_road.add_picture(str(img_road), width=Cm(13.5))
        add_figure_caption(doc, "Gambar IV.3.", "Peta Jalan (Roadmap) Perbaikan Tata Kelola Portal Akademik Perguruan Tinggi Contoh 3 Fase",
                            source_text="Sumber: Rencana Strategis Perbaikan UPT TIK Perguruan Tinggi Contoh, 2026")

    add_body_p(doc,
               "Penjabaran rincian tindakan pada masing-masing fase roadmap adalah sebagai berikut:")

    roadmap_narrative = [
        ("1.", "Fase 1: Quick Wins & Pengendalian Kritis (Bulan 1 s.d. 3)\n"
               "Fokus utama fase ini adalah mengeliminasi kerentanan berisiko tinggi secara cepat tanpa membutuhkan belanja modal besar: "
               "(a) Melakukan penonaktifan segera seluruh akun alumni yang masih aktif (6 dari 10 akun sampel) dan akun pegawai resign; "
               "(b) Menghapus penggunaan akun admin generik bersama (admin_portal) dan menegakkan kewajiban akun individual dengan autentikasi MFA; "
               "(c) Membekukan praktik rilis langsung tanpa tiket dan memberlakukan formulir Change Request darurat; "
               "(d) Melaksanakan uji coba pemulihan data (restore drill) perdana terhadap file backup database; serta "
               "(e) Mengajukan draf SK Rektor mengenai penunjukan Pejabat Pelindung Data Pribadi (DPO)."),

        ("2.", "Fase 2: Standarisasi Proses & Dokumentasi Sistemik (Bulan 4 s.d. 6)\n"
               "Fase ini bertujuan membakukan seluruh proses tata kelola agar mencapai Level 3 (Defined): "
               "(a) Mengesahkan Dokumen Kebijakan Keamanan TI terbaru beserta Matriks Klasifikasi Data Akademik; "
               "(b) Menerapkan Transparent Data Encryption (TDE / AES-256) pada kluster basis data MySQL untuk melindungi data PII; "
               "(c) Menyediakan staging environment terisolasi yang identik dengan lingkungan produksi dan memberlakukan review persetujuan CAB; "
               "(d) Menyusun dan mengesahkan SOP Backup & Restore rutin bulanan serta monitoring alert Zabbix; "
               "(e) Membangun otomatisasi integrasi siklus akun dengan modul yudisium BAAK; serta "
               "(f) Menyusun Register Kepatuhan UU PDP No. 27/2022 dan SOP notifikasi insiden kebocoran data maksimal 3 x 24 jam."),

        ("3.", "Fase 3: Integrasi, Optimalisasi Kuantitatif & Re-Audit (Bulan 7 s.d. 12)\n"
               "Fase ini bertujuan memantapkan tata kelola menuju Level 4 (Quantitatively Managed): "
               "(a) Mengimplementasikan Security Information and Event Management (SIEM) terpusat untuk korelasi log audit sistem; "
               "(b) Mengotomatiskan pipeline CI/CD dengan pengujian keamanan kode statis (SAST) dan mandatory rollback scripts; "
               "(c) Menerapkan dashboard metrik SLA ketersediaan 99.5% dan analisis kapasitas proaktif menghadapi musim KRS; "
               "(d) Menyelenggarakan program pelatihan kesadaran keamanan siber berkelanjutan bagi dosen dan tenaga kependidikan; serta "
               "(e) Melaksanakan Re-Audit COBIT 2019 independen untuk memvalidasi pencapaian tingkat target Level 3.2."),
    ]
    for num, text in roadmap_narrative:
        p_rn = doc.add_paragraph()
        format_paragraph(p_rn, space_before=2, space_after=4, line_spacing=1.5,
                         align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent=Cm(-0.6))
        p_rn.paragraph_format.left_indent = Cm(1.2)
        r_num = p_rn.add_run(num + " ")
        format_run(r_num, size_pt=12, bold=True)
        r_text = p_rn.add_run(text)
        format_run(r_text, size_pt=12, bold=False)

    add_body_p(doc,
               "Matriks prioritas rekomendasi perbaikan disajikan pada Tabel IV.6:")

    add_table_caption(doc, "Tabel IV.6.", "Matriks Prioritas Rekomendasi Perbaikan Tata Kelola SIAKAD")
    rec_headers = ["No", "Domain", "Temuan Masalah", "Tindakan Rekomendasi Perbaikan", "Prioritas", "Unit Penanggung Jawab (PIC)", "Target Waktu"]
    rec_data = [
        ["1", "DSS05", "Akun alumni aktif & shared generic superadmin", "Hapus akun bersama, tegakkan named user + MFA, cabut akun alumni.", "P1 (Sangat Tinggi)", "Sysadmin & Admin Portal", "2 Minggu"],
        ["2", "BAI06", "Rilis perubahan ad-hoc tanpa tiket & staging", "Terapkan formal change ticketing, staging gate, dan wajib rollback plan.", "P1 (Sangat Tinggi)", "Koordinator Programmer & CAB", "1 Bulan"],
        ["3", "DSS01", "Backup database tidak pernah diuji restore", "Susun SOP restore, laksanakan simulasi restore bulanan pada server uji.", "P1 (Sangat Tinggi)", "Database Administrator (DBA)", "3 Minggu"],
        ["4", "APO13", "Data pribadi (NIK, nilai) plaintext tanpa enkripsi", "Implementasikan TDE AES-256 pada MySQL dan sahkan klasifikasi data.", "P2 (Tinggi)", "DBA & Tim Keamanan TI", "2 Bulan"],
        ["5", "MEA03", "Belum ada DPO dan compliance register UU PDP", "Terbitkan SK Rektor DPO, susun compliance register dan SOP notifikasi 3x24 jam.", "P2 (Tinggi)", "Kepala UPT TIK & Biro Hukum", "3 Bulan"],
        ["6", "DSS01", "Monitoring infrastruktur belum prediktif", "Optimalkan Zabbix/Prometheus dengan alert bot Telegram/Email real-time.", "P3 (Sedang)", "Network Engineer", "4 Bulan"],
        ["7", "BAI06", "Tiada pipeline otomatisasi rilis aman", "Bangun pipeline CI/CD dengan SAST static code security scanning.", "P3 (Sedang)", "Tim Pengembang / DevOps", "6 Bulan"],
        ["8", "APO13", "Belum ada pelatihan kesadaran keamanan", "Gelar sosialisasi cyber security awareness bagi dosen dan staf BAAK.", "P4 (Berkelanjutan)", "UPT TIK & Biro SDM", "6 - 12 Bulan"],
    ]
    add_styled_table(doc, rec_headers, rec_data, col_widths=[0.8, 1.5, 3.2, 4.2, 2.0, 2.3, 1.5], align_center_cols=[0, 1, 4, 6])
    add_table_source(doc, "Sumber: Hasil Formulasi Rekomendasi Tim Audit, 2026")

    # Evidence Box BAB IV
    add_evidence_box(doc, "Bukti yang Dikumpulkan pada BAB IV", [
        "U-11: Pedoman Wawancara dan Transkrip Lengkap 5 Narasumber Kunci (Kepala UPT, Programmer, DBA, BAAK, Helpdesk).",
        "U-12: Lembar Observasi Fasilitas Fisik Data Center, Prosedur Backup, dan Alur Kerja Deployment Aplikasi.",
        "U-13: Lembar Kerja Sampling Audit (Sampling Sheet) Populasi 30 CR dan 25 Akun Pengguna.",
        "E-1: Berkas Bukti APO13 (Dokumen Kebijakan Keamanan TI, Matriks Klasifikasi, Konfigurasi TLS 1.3, dan Log Penilaian Risiko).",
        "E-2: Berkas Bukti BAI06 (Sampel 30 Formulir CR, Log Commit Git, Diagram Staging, dan Rencana Rollback).",
        "E-3: Berkas Bukti DSS01 (Dokumen SOP Operasional, Log Eksekusi Backup 3 Bulan, Berita Acara Uji Restore, Dashboard Zabbix).",
        "E-4: Berkas Bukti DSS05 (Matriks RBAC, Log Login Pengguna, Hasil Uji Akun Alumni, Log Antivirus, dan SOP Insiden).",
        "E-5: Berkas Bukti MEA03 (Kompilasi Regulasi Eksternal, Draf SK DPO, Log Riwayat Sinkronisasi PDDikti Feeder).",
        "E-6: Instrumen Lengkap Checklist Audit COBIT 2019 (46 Butir Terisi) Disajikan Lengkap pada Lampiran L-B.",
    ])


    # -------------------------------------------------------------
    # SECTION 7: BAB V KESIMPULAN DAN SARAN
    # -------------------------------------------------------------
    sec_b5 = doc.add_section(WD_SECTION.NEW_PAGE)
    setup_chapter_section(sec_b5)

    add_heading_bab(doc, "BAB V", "KESIMPULAN DAN SARAN")

    add_heading_2(doc, "5.1. Kesimpulan")

    add_body_p(doc,
               "Berdasarkan seluruh tahapan audit teknologi informasi yang telah dilaksanakan pada Sistem Informasi "
               "Akademik Perguruan Tinggi Contoh menggunakan kerangka kerja COBIT 2019, ditarik "
               "enam kesimpulan pokok yang menjawab rumusan masalah penelitian:")

    concl_points = [
        ("1.", "Tingkat Kemampuan Keamanan Informasi (APO13): Berada pada Level 2 (Managed) dengan skor pemenuhan checklist sebesar 40.0% (Partially Achieved). Kebijakan keamanan dasar telah ada dan transmisi data dilindungi TLS 1.3, namun universitas belum mengimplementasikan enkripsi basis data at rest untuk data pribadi sensitif (PII) serta belum memiliki matriks klasifikasi data akademik resmi."),
        ("2.", "Efektivitas Manajemen Perubahan TI (BAI06): Berada pada Level 1 (Initial) dengan skor kepatuhan checklist sebesar 33.3% (Partially Achieved). Praktik rilis perubahan modul masih bersifat ad-hoc, di mana pengujian sampel membuktikan 40.0% perubahan diterapkan langsung ke server produksi tanpa formulir approval formal, tanpa pengujian terisolasi di staging environment, dan tanpa dokumen rollback plan."),
        ("3.", "Keandalan Manajemen Operasional TI (DSS01): Mencapai Level 2 (Managed) dengan persentase kepatuhan tertinggi sebesar 66.7% (Largely Achieved). Penjadwalan pencadangan (backup) database otomatis berjalan rutin setiap hari dan pemantauan ketersediaan aktif melalui Zabbix, namun ditemukan celah kritis di mana pengujian pemulihan data (restore drill) belum pernah dilakukan selama 12 bulan terakhir."),
        ("4.", "Efektivitas Layanan Keamanan dan Hak Akses (DSS05): Berada pada Level 1 (Initial) dengan skor pemenuhan sebesar 50.0% (Partially Achieved). Meskipun sistem antarmuka telah menerapkan RBAC, audit menemukan 60.0% akun alumni sampel masih aktif dan teridentifikasi penggunaan akun administratif bersama tanpa proteksi MFA, yang melemahkan akuntabilitas modifikasi data nilai."),
        ("5.", "Tingkat Kepatuhan Regulasi Eksternal (MEA03): Berada pada Level 1 (Initial) dengan skor pemenuhan 37.5% (Partially Achieved). Pelaporan transaksi data semesteran ke PDDikti Feeder berjalan sangat baik dan tepat waktu, namun kepatuhan terhadap amanat UU PDP No. 27/2022 belum diterapkan, ditandai dengan belum adanya SK Rektor penunjukan DPO dan ketiadaan register kepatuhan regulasi terpadu."),
        ("6.", "Status Kematangan dan Kesenjangan Tata Kelola: Rata-rata tingkat kapabilitas tata kelola Portal Akademik Perguruan Tinggi Contoh saat ini berada pada Level 1.4 (Initial menuju Repeatable) dengan kesenjangan (gap) rata-rata sebesar 1.8 level terhadap tingkat target Level 3.2 (Defined menuju Managed). Diperlukan intervensi manajemen yang sistematis melalui roadmap 3 fase untuk mencapai target kepatuhan yang diharapkan."),
    ]
    for num, text in concl_points:
        add_list_item(doc, num, text)

    add_heading_2(doc, "5.2. Saran")

    add_body_p(doc,
               "Berdasarkan kesimpulan dan temuan audit yang telah diuraikan, tim auditor merumuskan saran konstruktif "
               "yang terbagi ke dalam tiga tingkatan implementasi:")

    add_body_p(doc,
               "a. Rekomendasi Manajerial bagi Pimpinan Perguruan Tinggi Contoh:\n"
               "1) Menerbitkan Surat Keputusan (SK) Rektor tentang Penunjukan Pejabat Pelindung Data Pribadi (Data Protection Officer / DPO) "
               "dan Tim Tanggap Insiden Keamanan Informasi (CSIRT) tingkat universitas guna memenuhi amanat UU No. 27 Tahun 2022.\n"
               "2) Mengesahkan Dokumen Kebijakan Tata Kelola Keamanan TI Terpadu dan Matriks Klasifikasi Aset Informasi sebagai standar baku institusi.\n"
               "3) Mengalokasikan anggaran investasi TI prioritas untuk penyediaan infrastruktur server pengujian (staging environment mandiri) "
               "dan implementasi teknologi enkripsi basis data enterprise.",
               first_line_indent=Cm(1.2), space_after=4)

    add_body_p(doc,
               "b. Rekomendasi Teknis bagi Pengelola TI Perguruan Tinggi Contoh:\n"
               "1) Melakukan penonaktifan massal terhadap seluruh akun alumni dan staf nonaktif serta menghapus penggunaan akun bersama "
               "dengan menerapkan Single Sign-On (SSO) individual berbasis Multi-Factor Authentication (MFA).\n"
               "2) Menghentikan praktik rilis perubahan langsung ke produksi dengan mewajibkan Change Request ticketing, pengujian staging, "
               "dan ketersediaan skrip rollback teruji.\n"
               "3) Menyusun SOP dan menyelenggarakan jadwal simulasi pemulihan data cadangan (restore drill) berkala minimal satu bulan sekali "
               "untuk menjamin pemulihan data saat menghadapi kondisi darurat bencana teknis.\n"
               "4) Menerapkan Transparent Data Encryption (TDE / AES-256) pada tabel data pribadi (PII) dan rekam nilai mahasiswa.",
               first_line_indent=Cm(1.2), space_after=4)

    add_body_p(doc,
               "c. Rekomendasi untuk Penelitian dan Audit Lanjutan:\n"
               "1) Memperluas cakupan audit tata kelola TI pada domain COBIT 2019 lainnya yang relevan, seperti APO07 (Managed Human Resources) "
               "dan DSS04 (Managed Continuity / Business Continuity Plan).\n"
               "2) Mengintegrasikan kerangka penilaian kematangan dengan standar spesifik ISO/IEC 27001:2022 guna mempersiapkan universitas "
               "memperoleh sertifikasi keamanan sistem informasi bertaraf internasional.\n"
               "3) Melaksanakan kegiatan re-audit secara berkala (semesteran) untuk mengevaluasi progres implementasi roadmap dan memverifikasi "
               "peningkatan tingkat kapabilitas tata kelola menuju target Level 3.2.",
               first_line_indent=Cm(1.2), space_after=12)

    # Evidence Box BAB V
    add_evidence_box(doc, "Bukti yang Dikumpulkan pada BAB V", [
        "U-14: Dokumen Berita Acara Exit Meeting dan Presentasi Hasil Temuan Audit kepada Pimpinan UPT TIK Perguruan Tinggi Contoh.",
        "U-15: Lembar Komitmen Tindak Lanjut Perbaikan (Management Action Plan) yang Ditandatangani Pihak Pengelola SIAKAD.",
    ])


    # -------------------------------------------------------------
    # DAFTAR PUSTAKA (PATUH ATURAN R1 MENDELEY)
    # -------------------------------------------------------------
    p_dp_title = doc.add_paragraph()
    format_paragraph(p_dp_title, space_before=0, space_after=18, line_spacing=1.0,
                     align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=None,
                     keep_with_next=True, page_break_before=True)
    r_dp_title = p_dp_title.add_run("DAFTAR PUSTAKA")
    format_run(r_dp_title, size_pt=14, bold=True)
    if mendeley_mode:
        add_body_p(
            doc,
            "[REFERENSI DIKELOLA VIA MENDELEY APA V.7 - Sesuai Aturan Sakral R1 dan R3, daftar pustaka akhir disisipkan menggunakan plugin Mendeley Cite dengan menulis seluruh nama pengarang lengkap tanpa singkatan et al. atau dkk. Kandidat referensi ber-DOI Crossref aktif tersedia pada berkas .txt terpisah.]",
            italic=True,
            first_line_indent=None,
            space_after=12,
        )

    # -------------------------------------------------------------
    # SECTION 8: LAMPIRAN (INSTRUMEN CHECKLIST 46 BUTIR LENGKAP)
    # -------------------------------------------------------------
    sec_app = doc.add_section(WD_SECTION.NEW_PAGE)
    setup_chapter_section(sec_app)

    add_heading_bab(doc, "LAMPIRAN", "INSTRUMEN AUDIT DAN DOKUMEN PENDUKUNG")

    # --- LAMPIRAN L-A ---
    add_heading_2(doc, "Lampiran L-A: Ringkasan Artikel Ilmiah Rujukan (Bukti U-4)")
    add_body_p(doc,
               "Berikut adalah ringkasan eksekutif lima artikel ilmiah primer yang dijadikan landasan komparasi dan "
               "metodologi pelaksanaan audit tata kelola pada Portal Akademik Perguruan Tinggi Contoh:")

    articles = [
        ("1. Artikel Ilmiah 1",
         "ISACA (2021). \"COBIT 2019 Framework: Governance and Management Objectives\". Information Systems Audit and Control Association.",
         "Menyediakan taksonomi 40 proses tata kelola, definisi kapabilitas level 0–5, kriteria penilaian N-P-L-F, dan faktor desain untuk merancang sistem tata kelola TI adaptif."),
        ("2. Artikel Ilmiah 2",
         "Taliwongso, I., Mambu, J. Y., Putra, E. Y., & Waworundeng, J. (2023). \"Designing IT Governance Using COBIT 2019 at PT Unicharm Indonesia\". Jurnal Indonesia: Manajemen Informatika dan Komunikasi (JIMIK), 4(2), 515-528. https://doi.org/10.35870/jimik.v4i2.274",
         "Menjelaskan pemetaan faktor desain COBIT 2019 dan penyusunan instrumen penilaian kapabilitas proses tata kelola teknologi informasi."),
        ("3. Artikel Ilmiah 3",
         "Rusdi, A. F., Hardian, B., & Raharjo, T. (2023). \"Service Automation Implementation for Delivering CaaS at the Ministry of Finance of Indonesia\". Jurnal RESTI (Rekayasa Sistem dan Teknologi Informasi), 7(5), 1174-1181. https://doi.org/10.29207/resti.v7i5.5032",
         "Menyajikan analisis manajemen perubahan layanan terotomatisasi (BAI06) dan pengendalian lingkungan staging-production pada organisasi berskala besar."),
        ("4. Artikel Ilmiah 4",
         "Khudori, A., & Lala, A. (2024). \"Legal Implications of Data Breach Cases in Indonesia: Challenges and Solutions in the Era of Personal Data Protection\". Indonesian Cyber Law Review, 1(1), 13-20. https://doi.org/10.59261/iclr.v1i1.1",
         "Memberikan kerangka integrasi kewajiban hukum UU No. 27 Tahun 2022 (UU PDP) ke dalam matriks compliance register dan mandat Pejabat Pelindung Data Pribadi (DPO)."),
        ("5. Artikel Ilmiah 5",
         "Harvard University IT (2024). \"Information Technology Audit and Internal Control Standards for Higher Education Enterprise Systems\". Harvard University Publications.",
         "Menjadi acuan standar pemisahan tugas (Segregation of Duties) antara developer dan sysadmin serta metodologi uji restore backup harian."),
    ]
    for lbl, cit, annot in articles:
        p_art = doc.add_paragraph()
        format_paragraph(p_art, space_before=2, space_after=3, line_spacing=1.5, first_line_indent=None)
        r_art_lbl = p_art.add_run(f"{lbl}: {cit}\n")
        format_run(r_art_lbl, size_pt=10.5, bold=True)
        r_art_ann = p_art.add_run(f"Anotasi Relevansi: {annot}")
        format_run(r_art_ann, size_pt=10, italic=True)

    # --- LAMPIRAN L-B: CHECKLIST 46 BUTIR LENGKAP ---
    add_heading_2(doc, "Lampiran L-B: Instrumen Checklist Audit COBIT 2019 Lengkap 46 Butir Terisi (Bukti E-6)")
    add_body_p(doc,
               "Instrumen checklist audit operasional di bawah ini memuat 46 butir pengujian terinci yang mencakup "
               "kelima domain proses fokus (APO13, BAI06, DSS01, DSS05, dan MEA03), dilengkapi rujukan berkas bukti, "
               "status kesesuaian faktual (✓ Sesuai / ✗ Tidak Sesuai), dan catatan observasi auditor:")

    # 1. APO13 Checklist (10 Items)
    add_table_caption(doc, "Tabel L-B.1.", "Checklist Audit APO13 Managed Security (10 Butir)")
    apo_headers = ["No", "Pertanyaan Audit", "Bukti yang Diperiksa", "Status", "Catatan Auditor"]
    apo_data = [
        ["1", "Apakah terdapat kebijakan keamanan informasi yang terdokumentasi dan disahkan pimpinan universitas?", "Dokumen Kebijakan Keamanan TI No. TI-CONTOH/01 (U-9)", "✓ Sesuai", "Dokumen ada disahkan Rektorat, namun versi terakhir tercatat tahun 2024 dan belum mencakup regulasi data privasi terbaru."],
        ["2", "Apakah kebijakan keamanan direview dan diperbarui secara berkala (minimal 1 tahun sekali)?", "Riwayat revisi dokumen kebijakan (U-9)", "✗ Tidak Sesuai", "Tidak terdapat catatan review atau pembaruan berkala selama 2 tahun terakhir."],
        ["3", "Apakah aset informasi akademik (data mahasiswa, nilai, keuangan) diklasifikasi berdasarkan sensitivitasnya?", "Matriks Klasifikasi Data Akademik (E-1)", "✗ Tidak Sesuai", "Belum ada dokumen resmi pengelompokan tingkat kerahasiaan data (Public/Internal/Confidential/Restricted)."],
        ["4", "Apakah data sensitif mahasiswa dienkripsi saat transit (in transit) dan saat disimpan (at rest)?", "Konfigurasi SSL/TLS web server dan skema database MySQL (E-1)", "✗ Tidak Sesuai", "Enkripsi in transit telah aktif (TLS 1.3), namun data at rest pada tabel biodata dan nilai masih plaintext."],
        ["5", "Apakah penilaian risiko keamanan (security risk assessment) dilakukan dan didokumentasikan berkala?", "Laporan Risk Assessment Tahunan (E-1)", "✗ Tidak Sesuai", "Penilaian risiko hanya dilakukan secara ad-hoc pasca terjadinya insiden, tidak terprogram tahunan."],
        ["6", "Apakah struktur organisasi telah menetapkan peran dan tanggung jawab pengelola keamanan informasi secara formal?", "SK Rektor tentang Organogram UPT TIK (U-6)", "✓ Sesuai", "Terdapat fungsi Information Security Officer, namun masih dirangkap oleh Network Administrator."],
        ["7", "Apakah staf pengelola TI dan civitas akademika mendapatkan pelatihan kesadaran keamanan (security awareness)?", "Daftar hadir dan modul pelatihan keamanan (E-1)", "✗ Tidak Sesuai", "Belum pernah diadakan pelatihan kesadaran keamanan terstruktur bagi staf operasional dalam 1 tahun terakhir."],
        ["8", "Apakah tingkat pemenuhan kebijakan keamanan dipantau dan dilaporkan secara rutin ke pimpinan?", "Laporan Kepatuhan Keamanan Triwulanan (E-1)", "✗ Tidak Sesuai", "Tidak ada mekanisme pelaporan berkala mengenai status kepatuhan keamanan TI ke Rektorat."],
        ["9", "Apakah terdapat persyaratan keamanan informasi tertulis dalam kontrak kerjasama dengan pihak ketiga/vendor?", "Salinan kontrak vendor ISP dan payment gateway (E-1)", "✓ Sesuai", "Terdapat klausul Non-Disclosure Agreement (NDA) dan batasan kerahasiaan dalam kontrak pihak ketiga."],
        ["10", "Apakah setiap insiden keamanan informasi ditinjau ulang (incident review) untuk penyempurnaan kontrol keamanan?", "Log insiden keamanan dan notula evaluasi (E-4)", "✓ Sesuai", "Tinjauan dilakukan saat terjadi serangan brute-force login awal semester, menghasilkan blokir IP otomatis."],
    ]
    add_styled_table(doc, apo_headers, apo_data, col_widths=[0.8, 4.2, 3.2, 1.8, 4.5], align_center_cols=[0, 3])
    add_table_source(doc, "Sumber: Hasil Checklist Audit Auditor Sistem Informasi, 2026")

    # 2. BAI06 Checklist (9 Items)
    add_table_caption(doc, "Tabel L-B.2.", "Checklist Audit BAI06 Managed IT Changes (9 Butir)")
    bai_headers = ["No", "Pertanyaan Audit", "Bukti yang Diperiksa", "Status", "Catatan Auditor"]
    bai_data = [
        ["1", "Apakah setiap permohonan perubahan sistem didokumentasikan melalui formulir Change Request (CR) resmi?", "Arsip formulir Change Request fisik/digital (E-2)", "✗ Tidak Sesuai", "Dari 30 sampel CR yang diperiksa, 12 perubahan (40.0%) hanya diajukan via pesan instan/lisan tanpa tiket formal."],
        ["2", "Apakah setiap perubahan sistem mendapatkan telaah dampak dan persetujuan formal sebelum diimplementasikan?", "Lembar tanda tangan/approval form CR (E-2)", "✗ Tidak Sesuai", "Persetujuan formal hanya ditemukan pada 18 dari 30 sampel; perubahan minor sering dirilis tanpa approval."],
        ["3", "Apakah pengujian fungsional dan keamanan dilakukan di lingkungan terpisah (staging) sebelum rilis ke produksi?", "Log uji sistem dan diagram lingkungan server (E-2, U-8)", "✗ Tidak Sesuai", "Lingkungan staging tidak selalu disinkronkan; beberapa patch darurat langsung diuji di server produksi."],
        ["4", "Apakah tersedia rencana pemulihan kembali (rollback plan) yang teruji untuk setiap rilis perubahan sistem?", "Dokumen prosedur rollback per rilis (E-2)", "✗ Tidak Sesuai", "Hanya 8 rilis modul besar yang menyertakan script rollback; perubahan skema database minor tidak memiliki rollback."],
        ["5", "Apakah terdapat pemisahan hak akses logis dan lingkungan yang tegas antara Development, Staging, dan Production?", "Konfigurasi akses server dan repositori kode (U-8)", "✓ Sesuai", "Hak akses server produksi dibatasi hanya untuk sysadmin; developer tidak memiliki akses root langsung."],
        ["6", "Apakah prosedur perubahan darurat (emergency change) telah ditetapkan dan dievaluasi retrospektif pasca-rilis?", "Log Emergency Change dan notula Emergency CAB (E-2)", "✗ Tidak Sesuai", "Perubahan darurat sering terjadi pada masa KRS tanpa didukung laporan review retrospektif pasca kejadian."],
        ["7", "Apakah pemberitahuan jadwal rilis (release maintenance notice) disampaikan kepada pengguna sebelum rilis diterapkan?", "Pengumuman broadcast portal dan email mahasiswa (E-2)", "✓ Sesuai", "Terdapat banner pengumuman pemeliharaan sistem di portal akademik minimal 24 jam sebelum downtime."],
        ["8", "Apakah dilakukan evaluasi pasca-implementasi (Post-Implementation Review / PIR) untuk perubahan signifikan?", "Laporan PIR per rilis modul (E-2)", "✗ Tidak Sesuai", "Tidak pernah diterbitkan laporan evaluasi pasca implementasi untuk menilai stabilitas modul baru."],
        ["9", "Apakah seluruh catatan rilis (release notes) dan riwayat versi tersimpan terpusat dan dapat ditelusuri?", "Log commit repositori Git dan arsip rilis (E-2)", "✓ Sesuai", "Seluruh kode sumber dikelola menggunakan repositori Git dengan riwayat commit dan tag versi yang rapi."],
    ]
    add_styled_table(doc, bai_headers, bai_data, col_widths=[0.8, 4.2, 3.2, 1.8, 4.5], align_center_cols=[0, 3])
    add_table_source(doc, "Sumber: Hasil Checklist Audit Auditor Sistem Informasi, 2026")

    # 3. DSS01 Checklist (9 Items)
    add_table_caption(doc, "Tabel L-B.3.", "Checklist Audit DSS01 Managed Operations (9 Butir)")
    dss01_headers = ["No", "Pertanyaan Audit", "Bukti yang Diperiksa", "Status", "Catatan Auditor"]
    dss01_data = [
        ["1", "Apakah terdapat Standard Operating Procedure (SOP) operasional harian TI yang terdokumentasi dan dipatuhi?", "Buku panduan SOP Operasional TI (U-9, E-3)", "✓ Sesuai", "Tersedia SOP baku untuk checklist harian pemeriksaan server, start/stop service, dan pergantian shift operator."],
        ["2", "Apakah proses pencadangan data (backup) berjalan secara otomatis sesuai jadwal yang telah ditetapkan?", "Skrip cron/job scheduler dan log eksekusi backup (E-3)", "✓ Sesuai", "Backup harian berjalan otomatis setiap pukul 02.00 WIB; log mencatat keberhasilan eksekusi selama 3 bulan."],
        ["3", "Apakah salinan file backup disimpan pada media dan lokasi yang terpisah dari server produksi utama?", "Konfigurasi storage NAS dan cloud off-site (E-3)", "✓ Sesuai", "File backup ditransfer otomatis ke NAS lokal di gedung terpisah dan disinkronkan ke cloud storage."],
        ["4", "Apakah pengujian pemulihan data (restore drill) dilakukan secara berkala dan terdokumentasi hasilnya?", "Berita Acara dan Laporan Uji Restore Backup (E-3)", "✗ Tidak Sesuai", "Tidak ditemukan bukti pengujian pemulihan data dalam 12 bulan terakhir; ketiadaan SOP uji restore."],
        ["5", "Apakah ketersediaan (uptime) dan performa SIAKAD dipantau secara kontinu dengan peringatan otomatis?", "Dashboard sistem monitoring Zabbix / Grafana (E-3)", "✓ Sesuai", "Pemantauan aktif 24/7 dengan notifikasi bot Telegram jika terjadi lonjakan CPU >90% atau layanan HTTP down."],
        ["6", "Apakah terdapat alur dan sistem pencatatan resmi untuk penanganan insiden dan tiket gangguan operasional?", "Sistem Helpdesk Ticketing dan log tiket keluhan (E-3)", "✓ Sesuai", "Mahasiswa dan staf melaporkan gangguan melalui portal helpdesk; tiket terlacak dari status open hingga closed."],
        ["7", "Apakah tren kapasitas infrastruktur (CPU, memori, disk storage) dianalisis untuk perencanaan masa depan?", "Laporan Capacity Planning Semesteran (E-3, U-7)", "✗ Tidak Sesuai", "Peningkatan kapasitas disk dan RAM dilakukan secara reaktif saat server penuh menjelang musim KRS."],
        ["8", "Apakah kegiatan pemeliharaan perangkat keras dan perangkat lunak dijadwalkan secara berkala?", "Jadwal dan buku log maintenance preventif (E-3)", "✓ Sesuai", "Pemeliharaan berkala server dan update security patch OS dijadwalkan sebulan sekali pada akhir pekan."],
        ["9", "Apakah target tingkat layanan ketersediaan (SLA Uptime) ditetapkan secara resmi dan tercapai dalam operasional?", "Laporan performa ketersediaan tahunan (E-3)", "✗ Tidak Sesuai", "Target ketersediaan belum dituangkan dalam Service Level Agreement (SLA) kuantitatif formal antara UPT TIK dan unit pengguna; pemantauan uptime server berjalan namun belum memiliki tolok ukur komitmen SLA resmi."],
    ]
    add_styled_table(doc, dss01_headers, dss01_data, col_widths=[0.8, 4.2, 3.2, 1.8, 4.5], align_center_cols=[0, 3])
    add_table_source(doc, "Sumber: Hasil Checklist Audit Auditor Sistem Informasi, 2026")

    # 4. DSS05 Checklist (10 Items)
    add_table_caption(doc, "Tabel L-B.4.", "Checklist Audit DSS05 Managed Security Services (10 Butir)")
    dss05_headers = ["No", "Pertanyaan Audit", "Bukti yang Diperiksa", "Status", "Catatan Auditor"]
    dss05_data = [
        ["1", "Apakah hak akses pengguna ke menu dan data SIAKAD diterapkan berdasarkan peran kerja (Role-Based Access Control)?", "Matriks RBAC dan konfigurasi permission tabel (E-4)", "✓ Sesuai", "Telah dipisahkan menu untuk mahasiswa, dosen, staf BAAK, dan keuangan secara sistematis."],
        ["2", "Apakah pemberian hak akses khusus/administratif melalui prosedur otorisasi dan formulir permohonan resmi?", "Formulir Hak Akses Pengguna ditandatangani (E-4)", "✓ Sesuai", "Pembuatan akun staf dan admin baru memerlukan persetujuan tertulis dari Kepala Biro terkait."],
        ["3", "Apakah evaluasi dan sertifikasi ulang hak akses pengguna (user access review) dilakukan secara berkala?", "Catatan audit semesteran hak akses pengguna (E-4)", "✗ Tidak Sesuai", "Belum pernah dilakukan tinjauan ulang berkala terhadap kesesuaian hak akses staf yang mengalami mutasi."],
        ["4", "Apakah akun pengguna yang sudah tidak berhak (mahasiswa lulus/alumni atau pegawai resign) dinonaktifkan segera?", "Uji sampling 25 akun eks-mahasiswa dan pegawai (E-4)", "✗ Tidak Sesuai", "Uji sampel membuktikan 6 dari 10 akun alumni masih aktif dapat login ke portal data akademik."],
        ["5", "Apakah setiap akun administratif bersifat individual (named user) dan bebas dari penggunaan kata sandi bersama?", "Daftar user root/admin di server dan basis data (E-4)", "✗ Tidak Sesuai", "Ditemukan akun admin_portal dipakai bersama oleh 3 staf tanpa identifikasi personel yang jelas."],
        ["6", "Apakah diterapkan kebijakan kata sandi yang kuat (panjang, kompleksitas, masa kedaluwarsa) dan verifikasi MFA?", "Konfigurasi password policy dan modul MFA (E-4)", "✗ Tidak Sesuai", "Kebijakan kompleksitas password dasar ada, namun belum ada Multi-Factor Authentication (MFA) bagi admin."],
        ["7", "Apakah seluruh aktivitas autentikasi, akses kritis, dan modifikasi nilai terekam dalam audit log yang aman?", "Tabel database audit_trail dan log syslog terpusat (E-4)", "✓ Sesuai", "Modifikasi nilai mahasiswa mencatat tanggal, jam, dan ID penginput; namun integritas log belum write-only."],
        ["8", "Apakah seluruh server SIAKAD dilindungi oleh perangkat lunak antimalware/EDR dengan definisi terkini?", "Status lisensi dan konsol antimalware server (E-4)", "✓ Sesuai", "Antivirus server terpasang dengan pembaruan definisi otomatis harian terpusat."],
        ["9", "Apakah pembaruan keamanan (security patching) sistem operasi dan web server diterapkan secara teratur?", "Log riwayat update patch keamanan OS Linux (E-4)", "✓ Sesuai", "Patch keamanan kernel dan paket web server diperbarui secara terjadwal setiap rilis versi stabil."],
        ["10", "Apakah terdapat Standard Operating Procedure (SOP) penanganan insiden keamanan siber dan pencatatannya?", "Dokumen SOP Incident Response dan log insiden (E-4)", "✗ Tidak Sesuai", "Prosedur respon insiden masih tidak tertulis; pencatatan insiden serangan dilakukan tidak standar."],
    ]
    add_styled_table(doc, dss05_headers, dss05_data, col_widths=[0.8, 4.2, 3.2, 1.8, 4.5], align_center_cols=[0, 3])
    add_table_source(doc, "Sumber: Hasil Checklist Audit Auditor Sistem Informasi, 2026")

    # 5. MEA03 Checklist (8 Items)
    add_table_caption(doc, "Tabel L-B.5.", "Checklist Audit MEA03 Managed Compliance External (8 Butir)")
    mea_headers = ["No", "Pertanyaan Audit", "Bukti yang Diperiksa", "Status", "Catatan Auditor"]
    mea_data = [
        ["1", "Apakah organisasi memiliki dan memelihara daftar regulasi eksternal (compliance register) yang mengikat sistem TI?", "Dokumen Register Regulasi Eksternal TI (E-5)", "✗ Tidak Sesuai", "Tidak terdapat dokumen inventarisasi peraturan perundang-undangan yang relevan dengan TI kampus."],
        ["2", "Apakah telah ditunjuk penanggung jawab kepatuhan TI dan Pejabat Pelindung Data Pribadi (DPO) secara formal?", "Surat Keputusan Rektor penetapan DPO (E-5, U-6)", "✗ Tidak Sesuai", "Belum ada penunjukan Pejabat Pelindung Data Pribadi (DPO) sesuai amanat UU PDP No. 27/2022."],
        ["3", "Apakah kebijakan dan prosedur internal TI ditinjau secara berkala terhadap perkembangan regulasi nasional terbaru?", "Laporan Review Kepatuhan Hukum Tahunan (E-5)", "✗ Tidak Sesuai", "Tinjauan kepatuhan belum terprogram; kebijakan TI belum diselaraskan dengan UU PDP."],
        ["4", "Apakah kewajiban pokok perlindungan data pribadi (dasar pemrosesan sah, hak subjek data) telah diterapkan?", "Kebijakan Privasi Portal dan Form Persetujuan (E-5)", "✗ Tidak Sesuai", "Portal belum menyertakan lembar persetujuan (consent) pemrosesan data pribadi mahasiswa."],
        ["5", "Apakah pelaporan transaksi data akademik ke Pangkalan Data Pendidikan Tinggi (PDDikti) berjalan sesuai standar?", "Bukti riwayat sinkronisasi PDDikti Feeder (E-5)", "✓ Sesuai", "Pelaporan data 100% tepat waktu setiap semester sesuai tenggat waktu LLDIKTI / Kemendikbudristek."],
        ["6", "Apakah temuan dari audit internal atau audit kepatuhan sebelumnya ditindaklanjuti secara terdokumentasi?", "Tindak lanjut hasil audit internal (E-5)", "✓ Sesuai", "Rekomendasi audit mutu internal BAAK mengenai akurasi data nilai telah ditindaklanjuti."],
        ["7", "Apakah terdapat alur konsultasi hukum formal ketika muncul regulasi atau standar kepatuhan eksternal baru?", "Dokumen korespondensi UPT TIK dan Biro Hukum (E-5)", "✓ Sesuai", "Tersedia saluran koordinasi resmi dengan bagian hukum rektorat untuk penelaahan kontrak pihak ketiga."],
        ["8", "Apakah staf pengelola data dan TI mendapatkan sosialisasi/pelatihan mengenai kepatuhan regulasi data pribadi?", "Daftar hadir dan materi sosialisasi UU PDP (E-5)", "✗ Tidak Sesuai", "Belum pernah diadakan sosialisasi ketentuan dan sanksi UU PDP No. 27/2022 bagi operator sistem."],
    ]
    add_styled_table(doc, mea_headers, mea_data, col_widths=[0.8, 4.2, 3.2, 1.8, 4.5], align_center_cols=[0, 3])
    add_table_source(doc, "Sumber: Hasil Checklist Audit Auditor Sistem Informasi, 2026")

    # --- LAMPIRAN L-C ---
    add_heading_2(doc, "Lampiran L-C: Matriks Sampling Pengujian Audit (Bukti U-13, E-2, E-4)")
    add_body_p(doc,
               "Pengujian kepatuhan dilaksanakan dengan metode purposive and random sampling terhadap populasi transaksi "
               "selama semester berjalan:")

    sampling_summary = [
        ("1. Sampel Perubahan Modul (Change Request - Bukti E-2)",
         "Populasi: 30 Change Request (Januari–Juni 2026).\n"
         "Hasil Uji: 18 CR (60.0%) memiliki approval formal dan melalui uji staging; 12 CR (40.0%) berstatus non-compliant (rilis ad-hoc langsung ke produksi)."),
        ("2. Sampel Akun Pengguna & Privilese (User Accounts - Bukti E-4)",
         "Populasi Uji: 25 Akun Pengguna.\n"
         "Hasil Uji: 6 dari 10 akun alumni terbukti masih aktif; 1 akun generik admin_portal terbukti digunakan bersama oleh 3 staf; seluruh akun administratif belum menerapkan MFA."),
    ]
    for title, text in sampling_summary:
        p_ss = doc.add_paragraph()
        format_paragraph(p_ss, space_before=2, space_after=3, line_spacing=1.5, first_line_indent=None)
        r_ss_lbl = p_ss.add_run(title + "\n")
        format_run(r_ss_lbl, size_pt=10.5, bold=True)
        r_ss_txt = p_ss.add_run(text)
        format_run(r_ss_txt, size_pt=10)

    # --- LAMPIRAN L-D ---
    add_heading_2(doc, "Lampiran L-D: Panduan Skoring dan Rubrik Kriteria Kemampuan COBIT 2019")
    add_body_p(doc,
               "Kriteria penilaian pemenuhan aktivitas COBIT 2019 mengacu pada rubrik standar ISACA:\n"
               "• N (Not Achieved) : 0% - 15% (Aktivitas tidak dilaksanakan atau bukti tidak ada).\n"
               "• P (Partially Achieved) : >15% - 50% (Aktivitas dilaksanakan sporadis/ad-hoc, ada bukti terbatas).\n"
               "• L (Largely Achieved) : >50% - 85% (Aktivitas dilaksanakan sistematis dan efektif, ada kekurangan minor).\n"
               "• F (Fully Achieved) : >85% - 100% (Aktivitas dilaksanakan sempurna, terdokumentasi dan terverifikasi penuh).")

    # --- LAMPIRAN L-E ---
    add_heading_2(doc, "Lampiran L-E: Matriks Peta Panas Risiko (Risk Heatmap 5x5)")
    add_body_p(doc,
               "Peta panas risiko (Risk Heatmap) memetakan lima skenario risiko audit pada sumbu Kemungkinan Terjadi "
               "(Likelihood) dan Tingkat Dampak (Impact). Seluruh temuan utama (APO13, BAI06, DSS01, DSS05, MEA03) "
               "berada pada kuadran Merah (High Risk), yang menuntut tindakan mitigasi terencana melalui Roadmap 3 Fase "
               "sebagaimana telah disahkan dalam laporan proyek ini.")

    # Save Document atomically with lock protection
    saved_path = atomic_save_docx(doc, str(target_out), backup=False)
    print(f"Document successfully created and saved at: {saved_path}")
    print(f"File size: {os.path.getsize(saved_path):,} bytes")
    return saved_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generator Dokumen Laporan Audit TI COBIT 2019 (.docx)")
    parser.add_argument("-o", "--output", default=str(DEFAULT_OUTPUT_FILE), help="Path file .docx keluaran")
    parser.add_argument("--title", default="Audit Tata Kelola Keamanan dan Kepatuhan Portal Akademik Perguruan Tinggi Contoh Menggunakan Framework COBIT 2019", help="Judul laporan audit")
    parser.add_argument("--subtitle", default="(Studi pada Proses APO13, BAI06, DSS01, DSS05, dan MEA03)", help="Subjudul laporan audit")
    parser.add_argument("--author", default="Penulis Contoh", help="Nama penulis/auditor")
    parser.add_argument("--nim", default="00000001", help="NIM penulis/auditor")
    parser.add_argument("--auditee", default="Portal Akademik Perguruan Tinggi Contoh", help="Nama sistem/objek audit")
    parser.add_argument("--unit", default="UPT Teknologi Informasi dan Komunikasi Perguruan Tinggi Contoh", help="Unit pengelola TI")
    parser.add_argument("--city", default="Kota Contoh", help="Kota instansi")
    parser.add_argument("--year", default="2026", help="Tahun laporan")
    parser.add_argument("--no-mendeley-mode", dest="mendeley_mode", action="store_false", help="Nonaktifkan placeholder Mendeley R1")
    parser.add_argument("--diagrams-dir", default=None, help="Direktori PNG diagram audit (opsional; otomatis dibangkitkan jika belum ada)")
    parser.add_argument("--no-auto-diagrams", dest="auto_diagrams", action="store_false", help="Jangan bangkitkan diagram audit otomatis bila file PNG belum ada")
    args = parser.parse_args()
    build_audit_report(
        output_path=args.output,
        title=args.title,
        subtitle=args.subtitle,
        author=args.author,
        nim=args.nim,
        auditee=args.auditee,
        unit=args.unit,
        city=args.city,
        year=args.year,
        mendeley_mode=args.mendeley_mode,
        diagrams_dir=args.diagrams_dir,
        auto_diagrams=args.auto_diagrams,
    )
