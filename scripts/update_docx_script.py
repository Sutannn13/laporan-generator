# /// script
# requires-python = ">=3.10"
# dependencies = ["python-docx"]
# ///
import argparse
import os
import sys
import docx
from docx.shared import Cm, Inches, Pt, RGBColor
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT_DIR = os.path.dirname(_THIS_DIR)
for _cand_dir in (_THIS_DIR, _PARENT_DIR):
    if _cand_dir not in sys.path:
        sys.path.insert(0, _cand_dir)

try:
    from scripts.docx_io import atomic_save_docx
except ImportError:
    from docx_io import atomic_save_docx

_atomic_save_docx = atomic_save_docx

DEFAULT_BACKUP = 'Laporan_PKL_Input.docx'
DEFAULT_TARGET = 'Laporan_PKL_Output.docx'

PKL_OUTLINES = {
    'proposal': (
        'Proposal PKL (3 Bab)',
        ['BAB I PENDAHULUAN', 'BAB II TEMPAT DAN WAKTU PKL', 'BAB III PENUTUP'],
    ),
    '1': (
        'Proyek Inovasi Perangkat Lunak (6 Bab)',
        [
            'BAB I LATAR BELAKANG IDE APLIKASI',
            'BAB II ANALISIS MASALAH',
            'BAB III SOLUSI INOVASI',
            'BAB IV TUJUAN DAN MANFAAT APLIKASI',
            'BAB V METODE PENGEMBANGAN PERANGKAT LUNAK',
            'BAB VI PENUTUP',
        ],
    ),
    '2': (
        'Analisa Program Berbasis Mobile (4 Bab)',
        ['BAB I PENDAHULUAN', 'BAB II LANDASAN TEORI', 'BAB III PEMBAHASAN', 'BAB IV PENUTUP'],
    ),
    '3': (
        'Jaringan Komputer (4 Bab)',
        ['BAB I PENDAHULUAN', 'BAB II LANDASAN TEORI', 'BAB III PEMBAHASAN', 'BAB IV PENUTUP'],
    ),
    '4': (
        'Analisis Sistem (4 Bab)',
        ['BAB I PENDAHULUAN', 'BAB II LANDASAN TEORI', 'BAB III PEMBAHASAN', 'BAB IV PENUTUP'],
    ),
}

SKRIPSI_OUTLINES = {
    '156': (
        'Skripsi Outline 156 - Perancangan Program Science (5 Bab)',
        [
            'BAB I PENDAHULUAN',
            'BAB II LANDASAN TEORI',
            'BAB III ANALISIS DAN PERANCANGAN APLIKASI',
            'BAB IV IMPLEMENTASI DAN PENGUJIAN SOFTWARE',
            'BAB V PENUTUP',
        ],
    ),
    '138': (
        'Skripsi Outline 138 - Penelitian Ilmiah (5 Bab)',
        [
            'BAB I PENDAHULUAN',
            'BAB II LANDASAN TEORI',
            'BAB III METODOLOGI PENELITIAN',
            'BAB IV HASIL PENELITIAN DAN PEMBAHASAN',
            'BAB V PENUTUP',
        ],
    ),
    '137': (
        'Skripsi Outline 137 - Jaringan Komputer (5 Bab)',
        [
            'BAB I PENDAHULUAN',
            'BAB II LANDASAN TEORI',
            'BAB III ANALISIS JARINGAN BERJALAN',
            'BAB IV RANCANGAN JARINGAN USULAN',
            'BAB V PENUTUP',
        ],
    ),
    '158': (
        'Skripsi Outline 158 - Aplikasi StartUp (4 Bab, Kelompok Maks. 2 Mahasiswa)',
        [
            'BAB I PENDAHULUAN',
            'BAB II LANDASAN TEORI',
            'BAB III ANALISIS DAN PERANCANGAN APLIKASI',
            'BAB IV PENUTUP',
        ],
    ),
}

OUTLINE_SUBCHAPTERS = {
    'proposal': {
        'BAB I PENDAHULUAN': ['1.1. Latar Belakang', '1.2. Tujuan dan Manfaat'],
        'BAB II TEMPAT DAN WAKTU PKL': [
            '2.1. Tempat PKL',
            '2.2. Waktu PKL',
            '2.3. Bidang Pekerjaan yang Dijadikan Praktik Kerja',
        ],
        'BAB III PENUTUP': [],
    },
    '1': {
        'BAB I LATAR BELAKANG IDE APLIKASI': [
            '1.1. Latar Belakang Masalah',
            '1.2. Kondisi Sistem Berjalan',
            '1.3. Urgensi Inovasi',
        ],
        'BAB II ANALISIS MASALAH': [
            '2.1. Identifikasi Masalah',
            '2.2. Data Pendukung',
            '2.3. Dampak Masalah',
        ],
        'BAB III SOLUSI INOVASI': [
            '3.1. Konsep Solusi Perangkat Lunak',
            '3.2. Nilai Inovasi dan Keunggulan',
            '3.3. Fitur Utama dan Alur Kerja Sistem',
        ],
        'BAB IV TUJUAN DAN MANFAAT APLIKASI': [
            '4.1. Tujuan Aplikasi',
            '4.2. Manfaat Aplikasi',
        ],
        'BAB V METODE PENGEMBANGAN PERANGKAT LUNAK': [
            '5.1. Model Siklus Hidup Perangkat Lunak (SDLC)',
            '5.2. Tahapan Pengembangan',
            '5.3. Lingkungan dan Alat Bantu Pengembangan',
        ],
        'BAB VI PENUTUP': ['6.1. Kesimpulan', '6.2. Saran'],
    },
    '2': {
        'BAB I PENDAHULUAN': [
            '1.1. Latar Belakang',
            '1.2. Tujuan dan Manfaat',
            '1.3. Metode Penelitian',
            '1.4. Ruang Lingkup',
        ],
        'BAB II LANDASAN TEORI': [
            '2.1. Konsep Dasar Mobile Computing',
            '2.2. Platform Sistem Operasi Mobile',
            '2.3. Alat Bantu Perancangan dan Pemodelan Sistem',
            '2.4. Bahasa Pemrograman dan Framework Mobile',
        ],
        'BAB III PEMBAHASAN': [
            '3.1. Tinjauan Kasus Aplikasi Mobile Computing',
            '3.2. Analisa Flow Chart',
            '3.3. Analisa Diagram Hierarchy Input Process Output (HIPO)',
            '3.4. Analisa Aplikasi Mobile Computing',
            '3.5. Permasalahan',
            '3.6. Pemecahan Masalah',
        ],
        'BAB IV PENUTUP': ['4.1. Kesimpulan', '4.2. Saran'],
    },
    '3': {
        'BAB I PENDAHULUAN': [
            '1.1. Latar Belakang',
            '1.2. Tujuan dan Manfaat',
            '1.3. Metode Penelitian',
            '1.4. Ruang Lingkup',
        ],
        'BAB II LANDASAN TEORI': [
            '2.1. Konsep Dasar Jaringan Komputer',
            '2.2. Topologi Jaringan Komputer',
            '2.3. Model Referensi OSI dan TCP/IP',
            '2.4. Pengalamatan IP dan Subnetting',
            '2.5. Perangkat Keras dan Perangkat Lunak Jaringan',
        ],
        'BAB III PEMBAHASAN': [
            '3.1. Tinjauan Perusahaan',
            '3.2. Skema Jaringan',
            '3.3. Analisa Kemampuan Jaringan Berjalan',
            '3.4. Permasalahan Pokok',
            '3.5. Pemecahan Masalah',
        ],
        'BAB IV PENUTUP': ['4.1. Kesimpulan', '4.2. Saran'],
    },
    '4': {
        'BAB I PENDAHULUAN': [
            '1.1. Latar Belakang Masalah',
            '1.2. Maksud dan Tujuan',
            '1.3. Metode Penelitian',
            '1.4. Ruang Lingkup',
        ],
        'BAB II LANDASAN TEORI': [
            '2.1. Konsep Dasar Sistem',
            '2.2. Unified Modelling Language (UML)',
        ],
        'BAB III PEMBAHASAN': [
            '3.1. Tinjauan Institusi',
            '3.2. Analisis Sistem Berjalan',
            '3.3. Permasalahan Pokok',
            '3.4. Pemecahan Masalah',
        ],
        'BAB IV PENUTUP': ['4.1. Kesimpulan', '4.2. Saran'],
    },
    '156': {
        'BAB I PENDAHULUAN': [
            '1.1. Latar Belakang Masalah',
            '1.2. Identifikasi Permasalahan',
            '1.3. Perumusan Masalah',
            '1.4. Maksud dan Tujuan',
            '1.5. Metode Penelitian',
            '1.6. Ruang Lingkup',
        ],
        'BAB II LANDASAN TEORI': ['2.1. Tinjauan Pustaka', '2.2. Penelitian Terkait'],
        'BAB III ANALISIS DAN PERANCANGAN APLIKASI': [
            '3.1. Tinjauan Perusahaan',
            '3.2. Analisis Aplikasi',
            '3.3. Rancangan Algoritma',
        ],
        'BAB IV IMPLEMENTASI DAN PENGUJIAN SOFTWARE': [
            '4.1. Desain',
            '4.2. Code Generation',
            '4.3. Testing',
            '4.4. Support',
        ],
        'BAB V PENUTUP': ['5.1. Kesimpulan', '5.2. Saran'],
    },
    '138': {
        'BAB I PENDAHULUAN': [
            '1.1. Latar Belakang Masalah',
            '1.2. Identifikasi Permasalahan',
            '1.3. Perumusan Masalah',
            '1.4. Maksud dan Tujuan',
            '1.5. Metode Penelitian',
            '1.6. Ruang Lingkup',
            '1.7. Hipotesis',
        ],
        'BAB II LANDASAN TEORI': [
            '2.1. Tinjauan Pustaka',
            '2.2. Penelitian Terkait',
            '2.3. Tinjauan Organisasi/Objek Penelitian',
        ],
        'BAB III METODOLOGI PENELITIAN': [
            '3.1. Tahapan Penelitian',
            '3.2. Instrumen Penelitian',
            '3.3. Metode Pengumpulan Data, Populasi, dan Sampel Penelitian',
            '3.4. Metode Analisis Data',
        ],
        'BAB IV HASIL PENELITIAN DAN PEMBAHASAN': [
            '4.1. Deskripsi Data dan Dataset Penelitian',
            '4.2. Implementasi Metode dan Perhitungan Analisis',
            '4.3. Hasil Pengujian Hipotesis dan Kinerja Model',
            '4.4. Pembahasan dan Analisis Komparatif',
        ],
        'BAB V PENUTUP': ['5.1. Kesimpulan', '5.2. Saran'],
    },
    '137': {
        'BAB I PENDAHULUAN': [
            '1.1. Latar Belakang Masalah',
            '1.2. Identifikasi Permasalahan',
            '1.3. Perumusan Masalah',
            '1.4. Tujuan dan Manfaat',
            '1.5. Metode Penelitian',
            '1.6. Ruang Lingkup',
        ],
        'BAB II LANDASAN TEORI': ['2.1. Tinjauan Pustaka', '2.2. Penelitian Terkait'],
        'BAB III ANALISIS JARINGAN BERJALAN': [
            '3.1. Tinjauan Perusahaan',
            '3.2. Skema Jaringan Berjalan',
            '3.3. Permasalahan',
            '3.4. Alternatif Pemecahan Masalah',
        ],
        'BAB IV RANCANGAN JARINGAN USULAN': [
            '4.1. Jaringan Usulan',
            '4.2. Pengujian Jaringan',
        ],
        'BAB V PENUTUP': ['5.1. Kesimpulan', '5.2. Saran'],
    },
    '158': {
        'BAB I PENDAHULUAN': [
            '1.1. Latar Belakang Masalah',
            '1.2. Identifikasi Permasalahan',
            '1.3. Perumusan Masalah',
            '1.4. Tujuan dan Manfaat',
            '1.5. Metode Penelitian',
            '1.6. Ruang Lingkup',
        ],
        'BAB II LANDASAN TEORI': [
            '2.1. Tinjauan Pustaka',
            '2.2. Penelitian Terkait',
            '2.3. Teori Pendukung',
        ],
        'BAB III ANALISIS DAN PERANCANGAN APLIKASI': [
            '3.1. Tinjauan StartUp',
            '3.2. Analisis Kebutuhan',
            '3.3. Implementasi',
            '3.4. Spesifikasi Aplikasi',
            '3.5. Pengujian Aplikasi',
            '3.6. Uraian Tugas',
        ],
        'BAB IV PENUTUP': ['4.1. Kesimpulan', '4.2. Saran'],
    },
}


def _resolve_asset(rel_path):
    """Resolve template/gambar assets from CWD, script dir, or bundled skill root."""
    norm_rel = rel_path.replace('/', os.sep)
    for base in (os.getcwd(), _THIS_DIR, _PARENT_DIR):
        cand = os.path.join(base, norm_rel)
        if os.path.exists(cand):
            return cand
    return rel_path

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def format_run(run, font_name="Times New Roman", size_pt=12, bold=False, italic=False, color_rgb=(0,0,0)):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)

def set_heading_numpr(p, ilvl=1, num_id=6):
    pPr = p._p.get_or_add_pPr()
    numPr = parse_xml(f'<w:numPr {nsdecls("w")}><w:ilvl w:val="{ilvl}"/><w:numId w:val="{num_id}"/></w:numPr>')
    pPr.append(numPr)

def format_paragraph(p, space_after=6, space_before=0, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent=Inches(0.4), keep_with_next=False, page_break_before=False):
    pPr = p.paragraph_format
    pPr.space_after = Pt(space_after)
    pPr.space_before = Pt(space_before)
    pPr.line_spacing = line_spacing
    pPr.alignment = align
    if first_line_indent is not None:
        pPr.first_line_indent = first_line_indent
    if keep_with_next:
        pPr.keep_with_next = True
    if page_break_before:
        pPr.page_break_before = True

def add_styled_table(doc, headers, data, col_widths, before_elem):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Header row
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
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.keep_with_next = True
        for r in p.runs:
            format_run(r, size_pt=9.5, bold=True)
            
    # Data rows
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
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 or len(str(val)) < 8 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            for r in p.runs:
                format_run(r, size_pt=9.5, bold=False)

    # Set column widths
    for row in table.rows:
        for c_idx, w in enumerate(col_widths):
            row.cells[c_idx].width = Inches(w)

    before_elem.addprevious(table._tbl)
    return table

def run_clean_update(backup_path=None, target_path=None, sync_backup=True):
    backup_path = backup_path or DEFAULT_BACKUP
    target_path = target_path or DEFAULT_TARGET
    doc = docx.Document(backup_path)
    print(f"Loaded base document: {backup_path}")

    # 1. Update Kata Pengantar: replace PT Adib Cold Logistic with Diskominfo Kota Contoh leadership
    for i, p in enumerate(doc.paragraphs):
        if "Adib Cold Logistic" in p.text:
            p.text = "5. Kepala Dinas Komunikasi dan Informatika Kota Contoh."
            format_paragraph(p, space_before=2, space_after=2, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent=Inches(0.4))
            for r in p.runs:
                format_run(r, size_pt=12)
            
            p_next = doc.add_paragraph("6. Pembimbing Lapangan serta segenap staf Bidang Pengelolaan Informasi dan Komunikasi Publik Dinas Komunikasi dan Informatika Kota Contoh yang telah membimbing selama pelaksanaan PKL.")
            format_paragraph(p_next, space_before=2, space_after=4, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent=Inches(0.4))
            for r in p_next.runs:
                format_run(r, size_pt=12)
            p._p.addnext(p_next._p)
            print("Kata pengantar leadership updated.")
            break

    # 2. Update 3.1.3: Replace placeholder with Struktur Organisasi Image (Scaled 5.4 inches)
    for i, p in enumerate(doc.paragraphs):
        if "(Tempel Gambar 3.1 Struktur Organisasi" in p.text:
            p.text = ""
            p_img = p
            format_paragraph(p_img, space_before=10, space_after=4, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=Inches(0), keep_with_next=True)
            run = p_img.add_run()
            run.add_picture(_resolve_asset('template/gambar/gambar_3_1_struktur_organisasi.png'), width=Inches(5.4))

            p_caption = doc.add_paragraph()
            format_paragraph(p_caption, space_before=4, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=Inches(0), keep_with_next=True)
            r_cap = p_caption.add_run("Gambar III.1. Struktur Organisasi Dinas Komunikasi dan Informatika Kota Contoh")
            format_run(r_cap, size_pt=11, bold=True)

            p_src = doc.add_paragraph()
            format_paragraph(p_src, space_before=0, space_after=12, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=Inches(0))
            r_src = p_src.add_run("Sumber: Dinas Komunikasi dan Informatika Kota Contoh (2026)")
            format_run(r_src, size_pt=9.5, italic=True)

            p_img._p.addnext(p_src._p)
            p_img._p.addnext(p_caption._p)
            print("Struktur organisasi image embedded cleanly.")
            break

    # 3. Locate range for 3.2 Analisis Sistem Berjalan
    start_idx = None
    end_idx = None
    for i, p in enumerate(doc.paragraphs):
        if "Analisis Sistem Berjalan" in p.text and start_idx is None:
            start_idx = i
        if "Permasalahan Pokok" in p.text and start_idx is not None and end_idx is None:
            end_idx = i
            break

    ref_elem = doc.paragraphs[end_idx]._p
    paras_to_remove = [doc.paragraphs[j] for j in range(start_idx, end_idx)]
    for p in paras_to_remove:
        p._p.getparent().remove(p._p)

    def insert_para(text="", bold=False, size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                    space_before=0, space_after=6, indent=Inches(0.4), keep_with_next=False, page_break_before=False):
        new_p = doc.add_paragraph()
        format_paragraph(new_p, space_before=space_before, space_after=space_after,
                         align=align, first_line_indent=indent, keep_with_next=keep_with_next, page_break_before=page_break_before)
        if text:
            r = new_p.add_run(text)
            format_run(r, size_pt=size, bold=bold)
        ref_elem.addprevious(new_p._p)
        return new_p

    def insert_heading_with_num(text, ilvl=1, page_break_before=False):
        new_p = doc.add_paragraph()
        space_b = 14 if ilvl == 1 else 10
        # Notice: first_line_indent is 0 for headings
        format_paragraph(new_p, space_before=space_b, space_after=4,
                         align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=Inches(0),
                         keep_with_next=True, page_break_before=page_break_before)
        set_heading_numpr(new_p, ilvl=ilvl, num_id=6)
        r = new_p.add_run(text)
        format_run(r, size_pt=12, bold=True)
        ref_elem.addprevious(new_p._p)
        return new_p

    # --- 3.2 Analisis Sistem Berjalan ---
    # With numId 6, ilvl 1 -> Word AUTOMATICALLY displays "3.2" ! Text must be "Analisis Sistem Berjalan"
    insert_heading_with_num("Analisis Sistem Berjalan", ilvl=1)
    insert_para("Analisis sistem berjalan bertujuan untuk membedah secara komprehensif alur proses kerja pengelolaan publikasi berita dan siaran pers (press release) yang saat ini diterapkan pada Bidang Humas Dinas Komunikasi dan Informatika Kota Contoh. Analisis ini mencakup uraian prosedur operasional, identifikasi bentuk dokumen masukan dan keluaran, serta pemodelan sistem menggunakan Unified Modelling Language (UML) berupa Use Case Diagram dan Activity Diagram.")

    # 3.2.1 Prosedur Sistem Berjalan -> with numId 6, ilvl 2 -> Word AUTOMATICALLY displays "3.2.1" !
    insert_heading_with_num("Prosedur Sistem Berjalan", ilvl=2)
    insert_para("Proses pengelolaan publikasi berita pada Bidang Humas Dinas Komunikasi dan Informatika Kota Contoh melibatkan beberapa tahapan yang saling terhubung, dimulai dari peliputan lapangan hingga tahap pengarsipan. Rincian prosedur operasional sistem berjalan adalah sebagai berikut:")

    prosedur_items = [
        ("1. Prosedur Peliputan dan Pengumpulan Data Kegiatan",
         "Staf Humas menerima jadwal agenda kedinasan dari pimpinan atau panitia pelaksana kegiatan (seperti Bidang Pelayanan Publik, Infrastruktur Digital, atau Kecamatan). Staf Humas kemudian mendatangi lokasi acara untuk melakukan peliputan langsung. Pada tahap ini, staf mengumpulkan data fakta lapangan berpedoman pada kaidah 5W+1H (What, Who, Where, When, Why, How), mencatat poin inti pidato/sambutan narasumber, dan mengambil dokumentasi visual berupa foto kegiatan menggunakan kamera digital atau telepon pintar kedinasan."),

        ("2. Prosedur Penyusunan Draf Naskah Berita (Press Release)",
         "Setelah kegiatan selesai, staf Humas kembali ke ruang kerja untuk memproses hasil liputan. Staf membuka aplikasi pengolah kata Microsoft Word di komputer kerja dan menyusun draf berita secara manual dari awal. Staf merangkai kalimat judul, pembuka (lead), tubuh berita, dan kutipan narasumber secara mandiri. Karena belum tersedianya format templat terotomatisasi, proses penyusunan draf berita ini membutuhkan waktu sekitar 1 hingga 2 jam untuk setiap berita dan sangat bergantung pada gaya penulisan masing-masing staf."),

        ("3. Prosedur Pengajuan dan Verifikasi Naskah Berita",
         "Draf naskah berita yang telah selesai disusun dalam format file dokumen Microsoft Word (.docx) atau salinan teks ringkas selanjutnya dikirimkan oleh staf Humas kepada Pimpinan (Kepala Bidang Informasi Publik atau Pranata Humas) melalui aplikasi pesan instan WhatsApp. Pemilihan media komunikasi WhatsApp dilakukan dengan alasan kepraktisan dan mobilitas pimpinan yang kerap berada di luar kantor untuk tugas dinas."),

        ("4. Prosedur Koreksi dan Persetujuan (Approval) Naskah",
         "Pimpinan menerima dan membaca draf naskah berita yang dikirimkan melalui WhatsApp. Apabila naskah dinilai belum sesuai, terdapat kekeliruan data, atau penggunaan redaksi yang kurang tepat, pimpinan memberikan arahan dan catatan revisi melalui pesan balasan WhatsApp. Staf Humas kemudian membuka kembali file draf berita di komputer, melakukan perbaikan sesuai catatan, dan mengirimkan kembali hasil revisi kepada pimpinan. Sebaliknya, apabila naskah dinilai telah akurat dan memenuhi standar etika publikasi kedinasan, pimpinan memberikan persetujuan resmi (approval / ACC) berupa pesan konfirmasi tertulis via WhatsApp."),

        ("5. Prosedur Publikasi Berita",
         "Setelah memperoleh persetujuan resmi, staf Humas segera menyiapkan berkas publikasi untuk disebarluaskan ke kanal komunikasi instansi. Pertama, publikasi portal website resmi dilakukan dengan masuk (login) ke Content Management System (CMS) portal portal.kotacontoh.go.id, menyalin naskah, menyematkan foto kegiatan, dan menerbitkan artikel. Kedua, publikasi media sosial dilakukan dengan merangkum teks berita menjadi takarir (caption) informatif dan memadukannya dengan grafis/foto pilihan untuk diunggah pada akun resmi Instagram @humas_kotacontoh."),

        ("6. Prosedur Pengarsipan Berita dan Dokumentasi",
         "Setelah proses publikasi selesai, staf Humas mengarsipkan dokumen naskah final berformat .docx beserta foto-foto kegiatan ke dalam folder penyimpanan lokal komputer kerja staf atau repositori Google Drive pribadi staf sebagai rekam jejak publikasi internal Humas.")
    ]

    for title, desc in prosedur_items:
        p_item = doc.add_paragraph()
        format_paragraph(p_item, space_before=2, space_after=4, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent=Inches(0.4))
        r_t = p_item.add_run(f"{title}: ")
        format_run(r_t, bold=True)
        r_d = p_item.add_run(desc)
        format_run(r_d, bold=False)
        ref_elem.addprevious(p_item._p)

    # 3.2.2 Spesifikasi Bentuk Dokumen Sistem Berjalan
    insert_heading_with_num("Spesifikasi Bentuk Dokumen Sistem Berjalan", ilvl=2)
    insert_para("Spesifikasi bentuk dokumen menguraikan seluruh berkas administratif yang mengalir pada sistem berjalan, baik dokumen yang berperan sebagai masukan (input) maupun keluaran (output) proses kerja publikasi Humas Diskominfo Kota Contoh.")

    # Dokumen Masukan
    insert_para("A. Dokumen Masukan (Input)", bold=True, indent=Inches(0), keep_with_next=True)
    insert_para("Dokumen masukan merupakan data awal yang digunakan oleh staf Humas sebagai bahan dasar perumusan berita publikasi. Rincian dokumen masukan meliputi:")

    masukan_details = [
        "1. Lembar Catatan Peliputan Lapangan: Berfungsi sebagai rekaman data fakta mentah 5W+1H, kronologi acara, dan kutipan sambutan pejabat/narasumber kegiatan. Berasal dari narasumber/panitia kegiatan, ditujukan kepada staf Humas, bermedia kertas fisik atau catatan digital smartphone, berjumlah 1 berkas per agenda liputan, dan berformat teks catatan bebas.",
        "2. Foto Dokumentasi Acara: Berfungsi sebagai bukti visual kegiatan dan materi pendukung publikasi berita. Berasal dari kamera atau telepon pintar staf dokumentasi Humas, ditujukan kepada staf Humas dan media publikasi, bermedia file elektronik (format JPEG/PNG), berjumlah 5 hingga 20 foto per kegiatan, dan berformat gambar digital beresolusi tinggi."
    ]
    for md in masukan_details:
        insert_para(md, indent=Inches(0.4))

    # Caption Tabel 3.1
    insert_para("Tabel III.1. Spesifikasi Dokumen Masukan Sistem Berjalan", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), space_before=8, space_after=2, keep_with_next=True)
    headers_t1 = ["No.", "Nama Dokumen", "Fungsi", "Sumber", "Media", "Jumlah"]
    data_t1 = [
        ["1.", "Lembar Catatan Peliputan", "Sumber fakta mentah 5W+1H dan kutipan narasumber", "Narasumber / Panitia", "Kertas / Catatan Digital", "1 berkas per acara"],
        ["2.", "Foto Dokumentasi Acara", "Bukti visual kegiatan dan lampiran rilis publikasi", "Staf Liputan Humas", "File JPEG / PNG", "5-20 foto per acara"]
    ]
    add_styled_table(doc, headers_t1, data_t1, [0.4, 1.4, 1.6, 1.1, 1.2, 1.0], ref_elem)
    insert_para("Sumber: Bagian Humas Diskominfo Kota Contoh (2026)", align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), size=9.5, space_before=2, space_after=10)

    # Dokumen Keluaran
    insert_para("B. Dokumen Keluaran (Output)", bold=True, indent=Inches(0), keep_with_next=True)
    insert_para("Dokumen keluaran merupakan hasil olahan data peliputan yang diproduksi oleh Bagian Humas Diskominfo Kota Contoh untuk disebarkan kepada pimpinan maupun masyarakat umum. Rincian dokumen keluaran meliputi:")

    keluaran_details = [
        "1. Draf Naskah Berita (Press Release): Berfungsi sebagai naskah formal berisi uraian berita lengkap yang diajukan untuk proses verifikasi dan persetujuan. Bersumber dari staf Humas, ditujukan kepada Kepala Bidang Informasi Publik / Pimpinan, bermedia file dokumen Microsoft Word (.docx) dikirim via WhatsApp, berjumlah 1 berkas per agenda, berformat naskah ketikan Word.",
        "2. Artikel Berita Portal Website Resmi: Berfungsi menyebarluaskan berita resmi program dan kebijakan Diskominfo Kota Contoh ke publik luas. Bersumber dari staf Humas (admin web), ditujukan kepada masyarakat umum dan ASN, bermedia halaman daring portal.kotacontoh.go.id, berjumlah 1 tautan artikel per rilis.",
        "3. Materi Publikasi Media Sosial (Instagram): Berfungsi memberikan informasi ringkas dan visual yang menarik kepada pengguna jejaring sosial. Bersumber dari pengelola medsos Humas, ditujukan kepada warganet dan pengikut akun @humas_kotacontoh, bermedia aplikasi Instagram, berjumlah 1 unggahan post/carousel."
    ]
    for kd in keluaran_details:
        insert_para(kd, indent=Inches(0.4))

    # Caption Tabel 3.2 - Calibrated Media column to 1.5 in so @humas_kotacontoh NEVER breaks!
    insert_para("Tabel III.2. Spesifikasi Dokumen Keluaran Sistem Berjalan", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), space_before=8, space_after=2, keep_with_next=True)
    headers_t2 = ["No.", "Nama Dokumen", "Fungsi", "Sumber", "Media", "Tujuan"]
    data_t2 = [
        ["1.", "Draf Naskah Berita (Press Release)", "Materi naskah berita untuk proses verifikasi dan persetujuan", "Staf Humas", "File Word (.docx) / WhatsApp", "Kepala Bidang / Pimpinan"],
        ["2.", "Artikel Berita Portal Website", "Informasi resmi instansi bagi masyarakat umum dan media", "Staf Humas (Admin Web)", "Web portal.kotacontoh.go.id", "Masyarakat / Publik"],
        ["3.", "Konten Media Sosial (Instagram)", "Publikasi ringkas grafis dan teks untuk pengguna medsos", "Staf Humas (Admin Medsos)", "Akun Instagram @humas_kotacontoh", "Warganet / Publik"]
    ]
    add_styled_table(doc, headers_t2, data_t2, [0.4, 1.4, 1.4, 0.9, 1.5, 1.1], ref_elem)
    insert_para("Sumber: Bagian Humas Diskominfo Kota Contoh (2026)", align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), size=9.5, space_before=2, space_after=12)

    # 3.2.3 Use Case Diagram Sistem Berjalan
    insert_heading_with_num("Use Case Diagram Sistem Berjalan", ilvl=2, page_break_before=True)
    insert_para("Use Case Diagram digunakan untuk memodelkan fungsionalitas sistem berjalan dengan memetakan interaksi antara aktor (pengguna) dengan proses-proses yang berlangsung pada tata kelola publikasi berita Bagian Humas Diskominfo Kota Contoh.")

    insert_para("Tabel III.3. Deskripsi Aktor Sistem Berjalan", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), space_before=6, space_after=2, keep_with_next=True)
    headers_t3 = ["No.", "Aktor", "Deskripsi Peran dan Tanggung Jawab"]
    data_t3 = [
        ["1.", "Staf Humas", "Petugas pelaksana yang bertugas melakukan peliputan kegiatan di lapangan, menyusun draf naskah berita di Microsoft Word, mengajukan naskah ke pimpinan via WhatsApp, melakukan revisi perbaikan, menerbitkan berita ke portal web dan media sosial, serta mengarsipkan dokumen."],
        ["2.", "Pimpinan (Kepala Bidang)", "Pejabat struktural yang bertindak sebagai verifikator materi publikasi, bertugas menerima draf berita dari staf via WhatsApp, menelaah kebenaran informasi dan etika redaksional, memberikan catatan revisi, serta memberikan persetujuan (approval) publikasi."],
        ["3.", "Masyarakat / Publik", "Pihak eksternal sebagai penerima informasi yang mengakses, membaca, dan memperoleh wawasan program kedinasan melalui portal website resmi maupun kanal media sosial Diskominfo Kota Contoh."]
    ]
    add_styled_table(doc, headers_t3, data_t3, [0.4, 1.4, 4.9], ref_elem)
    insert_para("Sumber: Hasil Analisis Sistem Berjalan (2026)", align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), size=9.5, space_before=2, space_after=10)

    insert_para("Tabel III.4. Deskripsi Use Case Sistem Berjalan", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), space_before=6, space_after=2, keep_with_next=True)
    headers_t4 = ["No.", "Nama Use Case", "Deskripsi Fungsionalitas"]
    data_t4 = [
        ["1.", "Meliput Agenda Kegiatan", "Staf Humas mendatangi lokasi acara, mencatat poin fakta 5W+1H, dan mengambil dokumentasi foto visual."],
        ["2.", "Menyusun Draf Berita (Word)", "Staf Humas mengetik naskah draf siaran pers secara manual menggunakan aplikasi pengolah kata Microsoft Word."],
        ["3.", "Mengirim Draf via WhatsApp", "Staf Humas mengirimkan berkas draf naskah berita kepada pimpinan melalui pesan instan WhatsApp."],
        ["4.", "Menelaah Draf Berita", "Pimpinan membaca dan memeriksa kelayakan draf berita yang diajukan."],
        ["5.", "Memberikan Catatan Revisi", "Pimpinan mengirimkan instruksi koreksi redaksi melalui WhatsApp jika naskah belum memenuhi standar."],
        ["6.", "Memperbaiki Draf Berita", "Staf Humas membuka kembali berkas draf dan melakukan revisi sesuai catatan pimpinan."],
        ["7.", "Menyetujui Naskah (Approval)", "Pimpinan memberikan konfirmasi persetujuan resmi publikasi melalui pesan WhatsApp."],
        ["8.", "Menerbitkan Berita ke Website", "Staf Humas mengunggah naskah berita final dan foto kegiatan ke CMS portal resmi Diskominfo Kota Contoh."],
        ["9.", "Mengunggah Konten ke Instagram", "Staf Humas menyusun takarir ringkas dan mengunggah materi visual ke akun media sosial Instagram Diskominfo Kota Contoh."],
        ["10.", "Mengarsipkan Dokumen Berita", "Staf Humas menyimpan file naskah Word dan foto ke media penyimpanan lokal komputer staf."],
        ["11.", "Membaca Informasi Publikasi", "Masyarakat mengakses dan membaca berita melalui website dan media sosial."]
    ]
    add_styled_table(doc, headers_t4, data_t4, [0.4, 2.0, 4.3], ref_elem)
    insert_para("Sumber: Hasil Analisis Sistem Berjalan (2026)", align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), size=9.5, space_before=2, space_after=10)

    # Insert Use Case Image on a CLEAN PAGE so it NEVER touches footer!
    p_img_uc = insert_para("", align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), space_before=8, space_after=4, keep_with_next=True, page_break_before=True)
    run_uc = p_img_uc.add_run()
    run_uc.add_picture(_resolve_asset('template/gambar/gambar_3_2_use_case_berjalan.png'), width=Inches(5.4))
    insert_para("Gambar III.2. Use Case Diagram Sistem Pengelolaan Publikasi Berita Berjalan", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), space_before=2, space_after=2, keep_with_next=True)
    insert_para("Sumber: Hasil Analisis Sistem Berjalan (2026)", align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), size=9.5, space_before=0, space_after=12)

    # 3.2.4 Activity Diagram Sistem Berjalan
    insert_heading_with_num("Activity Diagram Sistem Berjalan", ilvl=2)
    insert_para("Activity Diagram memodelkan dinamika aliran aktivitas operasional (workflow) sistem berjalan secara berurutan antar-entitas yang berinteraksi.")

    insert_para("Tabel III.5. Skenario Aliran Kerja (Workflow) Sistem Berjalan", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), space_before=6, space_after=2, keep_with_next=True)
    headers_t5 = ["No.", "Entitas Asal", "Aktivitas Operasional", "Keluaran / Tindak Lanjut"]
    data_t5 = [
        ["1.", "Staf Humas", "Meliput kegiatan kedinasan", "Tercatat data 5W+1H dan terkumpul dokumentasi foto"],
        ["2.", "Staf Humas", "Menyusun draf naskah berita di MS Word", "File draf naskah berita (.docx) selesai diketik manual"],
        ["3.", "Staf Humas", "Mengirimkan draf berita via WhatsApp", "Berkas naskah terkirim ke kontak pimpinan"],
        ["4.", "Pimpinan", "Menerima dan menelaah naskah berita", "Pengambilan keputusan kelayakan naskah (Decision)"],
        ["5.", "Pimpinan", "Pemeriksaan: Apakah naskah disetujui?", "Jika Tidak: Mengirim catatan revisi via chat WhatsApp\nJika Ya: Mengirim konfirmasi persetujuan (ACC)"],
        ["6.", "Staf Humas", "Merespons hasil telaah pimpinan", "Jika ada revisi: Membuka Word, merevisi, dan kirim ulang\nJika disetujui: Mempersiapkan materi publikasi"],
        ["7.", "Staf Humas", "Menerbitkan berita ke website dan medsos", "Artikel tayang di web resmi dan postingan tayang di Instagram"],
        ["8.", "Staf Humas", "Menyimpan file naskah dan foto kegiatan", "Berkas tersimpan di direktori penyimpanan lokal (Selesai)"]
    ]
    add_styled_table(doc, headers_t5, data_t5, [0.4, 1.3, 2.2, 2.8], ref_elem)
    insert_para("Sumber: Hasil Analisis Sistem Berjalan (2026)", align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), size=9.5, space_before=2, space_after=10)

    # Insert Activity Diagram Image on CLEAN PAGE so it NEVER touches footer!
    p_img_act = insert_para("", align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), space_before=8, space_after=4, keep_with_next=True, page_break_before=True)
    run_act = p_img_act.add_run()
    run_act.add_picture(_resolve_asset('template/gambar/gambar_3_3_activity_diagram_berjalan.png'), width=Inches(5.4))
    insert_para("Gambar III.3. Activity Diagram Sistem Pengelolaan Publikasi Berita Berjalan", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), space_before=2, space_after=2, keep_with_next=True)
    insert_para("Sumber: Hasil Analisis Sistem Berjalan (2026)", align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), size=9.5, space_before=0, space_after=14)

    # 4. Update 3.3 Permasalahan Pokok (fill in the text for 3.3.1, 3.3.2, 3.3.3)
    # Ensure they have ilvl=2, numId=6 so Word automatically displays 3.3.1, 3.3.2, 3.3.3 !
    for p in doc.paragraphs:
        if "Kendala pada Proses Penyusunan Naskah Berita" in p.text:
            p.text = "Kendala pada Proses Penyusunan Naskah Berita"
            format_paragraph(p, space_before=10, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=Inches(0), keep_with_next=True)
            set_heading_numpr(p, ilvl=2, num_id=6)
            format_run(p.runs[0], bold=True, size_pt=12)
            p_desc1 = doc.add_paragraph()
            format_paragraph(p_desc1, space_before=0, space_after=6, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent=Inches(0.4))
            r1 = p_desc1.add_run("Penyusunan naskah rilis pers dari data mentah lapangan saat ini masih dikerjakan secara manual dari awal menggunakan Microsoft Word. Proses ini memakan waktu yang cukup lama (1 hingga 2 jam per berita), sehingga seringkali menyebabkan keterlambatan penayangan berita di portal resmi. Selain itu, gaya penulisan dan struktur berita menjadi sangat bervariasi bergantung pada staf yang bertugas, yang berpotensi memicu inkonsistensi kaidah jurnalistik kedinasan.")
            format_run(r1, size_pt=12)
            p._p.addnext(p_desc1._p)

        elif "Kendala pada Proses Verifikasi dan Persetujuan" in p.text:
            p.text = "Kendala pada Proses Verifikasi dan Persetujuan"
            format_paragraph(p, space_before=10, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=Inches(0), keep_with_next=True)
            set_heading_numpr(p, ilvl=2, num_id=6)
            format_run(p.runs[0], bold=True, size_pt=12)
            p_desc2 = doc.add_paragraph()
            format_paragraph(p_desc2, space_before=0, space_after=6, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent=Inches(0.4))
            r2 = p_desc2.add_run("Proses pengajuan verifikasi dan persetujuan yang bertumpu pada aplikasi pesan instan WhatsApp memiliki berbagai risiko operasional. Dokumen naskah berita rawan tertimbun oleh percakapan dinas lainnya, penelusuran riwayat revisi (version tracking) menjadi sulit dilakukan, serta tidak adanya kepastian durasi penelaahan yang menyebabkan terhambatnya proses publikasi.")
            format_run(r2, size_pt=12)
            p._p.addnext(p_desc2._p)

        elif "Kendala pada Proses Pengarsipan Dokumen" in p.text:
            p.text = "Kendala pada Proses Pengarsipan Dokumen"
            format_paragraph(p, space_before=10, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=Inches(0), keep_with_next=True)
            set_heading_numpr(p, ilvl=2, num_id=6)
            format_run(p.runs[0], bold=True, size_pt=12)
            p_desc3 = doc.add_paragraph()
            format_paragraph(p_desc3, space_before=0, space_after=6, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent=Inches(0.4))
            r3 = p_desc3.add_run("Pengarsipan naskah berita dan dokumentasi foto yang hanya tersimpan di media penyimpanan lokal laptop staf atau akun pribadi menyebabkan dokumen rawan hilang, rusak akibat infeksi virus, atau sulit diakses kembali saat dibutuhkan oleh staf lain untuk laporan pertanggungjawaban kedinasan.")
            format_run(r3, size_pt=12)
            p._p.addnext(p_desc3._p)

        elif "Bagi Perusahaan (Adib Cold Logistic)" in p.text:
            p.text = "Bagi Instansi (Dinas Komunikasi dan Informatika Kota Contoh):"
            format_paragraph(p, space_before=6, space_after=4, align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=Inches(0))
            for r in p.runs:
                format_run(r, bold=True, size_pt=12)

    # 5. Locate and populate Sub Bab 3.4 Pemecahan Masalah
    start_34 = None
    end_34 = None
    for i, p in enumerate(doc.paragraphs):
        if "Pemecahan Masalah" in p.text and start_34 is None:
            start_34 = i
        if "BAB IV" in p.text and start_34 is not None and end_34 is None:
            end_34 = i
            break

    ref_elem_34 = doc.paragraphs[end_34]._p
    paras_to_remove_34 = [doc.paragraphs[j] for j in range(start_34, end_34)]
    for p in paras_to_remove_34:
        p._p.getparent().remove(p._p)

    def insert_para_34(text="", bold=False, size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                       space_before=0, space_after=6, indent=Inches(0.4), keep_with_next=False, page_break_before=False):
        new_p = doc.add_paragraph()
        format_paragraph(new_p, space_before=space_before, space_after=space_after,
                         align=align, first_line_indent=indent, keep_with_next=keep_with_next, page_break_before=page_break_before)
        if text:
            r = new_p.add_run(text)
            format_run(r, size_pt=size, bold=bold)
        ref_elem_34.addprevious(new_p._p)
        return new_p

    def insert_heading_with_num_34(text, ilvl=1, page_break_before=False):
        new_p = doc.add_paragraph()
        space_b = 14 if ilvl == 1 else 10
        format_paragraph(new_p, space_before=space_b, space_after=4,
                         align=WD_ALIGN_PARAGRAPH.LEFT, first_line_indent=Inches(0),
                         keep_with_next=True, page_break_before=page_break_before)
        set_heading_numpr(new_p, ilvl=ilvl, num_id=6)
        r = new_p.add_run(text)
        format_run(r, size_pt=12, bold=True)
        ref_elem_34.addprevious(new_p._p)
        return new_p

    # --- 3.4 Pemecahan Masalah ---
    # With numId 6, ilvl 1 -> Word AUTOMATICALLY displays "3.4" !
    insert_heading_with_num_34("Pemecahan Masalah", ilvl=1)
    insert_para_34("Berdasarkan analisis mendalam terhadap ketiga kendala pokok sistem berjalan pada Bidang Humas Dinas Komunikasi dan Informatika Kota Contoh, penulis merumuskan rekomendasi pemecahan masalah dengan merancang dan mengimplementasikan sistem otomasi rilis berita berbasis web, yaitu Aplikasi Press Release Auto-Generator yang dapat diakses secara langsung pada tautan resmi: https://press-release-kotacontoh.contoh.go.id/.")
    insert_para_34("Sistem usulan ini dirancang secara khusus untuk mentransformasi tata kelola produksi siaran pers kedinasan dari pendekatan konvensional yang memakan waktu 1 hingga 2 jam (45–90 menit) menjadi sistem otomasi terintegrasi yang mampu memproses berkas rilis dalam waktu kurang dari 5 hingga 10 menit. Melalui pendekatan rekayasa piranti lunak modern, sistem mengombinasikan antarmuka formulir interaktif 3-langkah (stepper wizard), modul formula fakta inti 5W+1H dengan pemantauan kelengkapan waktu nyata (real-time checklist badges), pemodelan input dinamis kontekstual berdasarkan 6 jenis kegiatan kedinasan, integrasi model kecerdasan buatan Google Gemini dengan rekayasa prompt berstandar jurnalistik kehumasan pemerintah, modul audit kutipan narasumber (quote review) guna mencegah distorsi makna dan halusinasi data (zero hallucination), gerbang validasi integritas faktual (factual gatekeeper), hingga ekspor otomatis ke format dokumen Microsoft Word (.docx) ber-kop dinas resmi Dinas Komunikasi dan Informatika Kota Contoh serta takarir media sosial Instagram.")

    # 3.4.1 Usulan Prosedur Sistem -> ilvl 2 -> displays "3.4.1" !
    insert_heading_with_num_34("Usulan Prosedur Sistem", ilvl=2)
    insert_para_34("Usulan prosedur sistem mencakup penyempurnaan alur kerja operasional publikasi berita kehumasan yang terintegrasi ke dalam lima tahapan utama sebagai berikut:")

    prosedur_usulan_items = [
        ("1. Prosedur Penginputan Data Kegiatan dan Parameter 5W+1H Terstruktur",
         "Staf Humas yang telah selesai melaksanakan peliputan agenda kedinasan (seperti sosialisasi keterbukaan informasi publik, bimbingan teknis layanan digital, rapat koordinasi perangkat daerah, maupun peringatan hari besar nasional) mengakses sistem melalui peramban web pada domain https://press-release-kotacontoh.contoh.go.id/. Staf diarahkan pada antarmuka alur 3-langkah (stepper wizard): (a) Formula Fakta Inti 5W+1H dipandu 6 kartu status interaktif (What, Who, Where, When, Why, How) dengan prinsip ketat di mana AI tidak diizinkan menebak data kosong; (b) Klasifikasi 6 kategori kegiatan kedinasan (bimbingan/seminar, lomba/perayaan, upacara/peringatan, pelayanan/sosial, rapat/koordinasi, lainnya) yang secara dinamis memicu kemunculan kolom input kontekstual; (c) Menu pilihan baku seluruh kecamatan resmi Kota Contoh guna standarisasi dateline jurnalistik; (d) Pencatatan hingga 10 pihak yang hadir dan hingga 5 kutipan langsung narasumber pejabat; serta (e) Unggah foto dokumentasi beresolusi tinggi dengan validasi ekstensi biner (magic bytes) untuk menjamin keamanan berkas."),

        ("2. Prosedur Pembentukan Draf Otomatis (AI Engine) dan Audit Redaksional",
         "Setelah formulir masukan divalidasi skema Zod pada peramban, data dikirimkan ke modul pemrosesan POST /api/generate yang dilindungi Same-Origin Request Guard dan rate limiter. Sistem menginstruksikan Google Gemini AI melalui prompting terstruktur berkaidah jurnalistik piramida terbalik (judul formal, teras berita/lead berbasis 5W+1H, tubuh berita kronologis, penyematan kutipan, dan penutup). Bersamaan dengan itu, sistem menghasilkan: (a) Modul Review Kutipan Langsung (quoteReviews) yang menyandingkan kutipan asli narasumber (original) terhadap olahan AI (cleaned) yang wajib disetujui staf guna menjamin ucapan narasumber bebas halusinasi data (zero hallucination); (b) Modul Audit Fakta (factAudits) guna memverifikasi ketercakupan fakta 5W+1H; (c) Live Text Editor untuk penyempurnaan redaksi secara langsung; serta (d) Generator Takarir Instagram resmi @humas_kotacontoh."),

        ("3. Prosedur Verifikasi dan Persetujuan (Approval) Naskah Berjenjang",
         "Draf naskah yang telah dimatangkan pada modul penyuntingan diajukan oleh staf Humas ke modul verifikasi terpusat pada sistem. Pimpinan (Kepala Bidang Informasi Publik atau Pranata Humas) menelaah naskah secara komprehensif melalui dasbor verifikasi. Pimpinan dapat menyematkan catatan koreksi pada sistem atau langsung memberikan persetujuan resmi (approval ACC). Status naskah seketika diperbarui menjadi 'Approved' disertai rekam jejak digital (audit log) pemeriksa, tanggal, dan waktu persetujuan."),

        ("4. Prosedur Ekspor Dokumen Resmi (.docx) dan Validasi Faktual (Gatekeeper)",
         "Sistem menerapkan mekanisme gerbang integritas faktual (Factual Gatekeeper Guard), di mana tombol ekspor dokumen Microsoft Word (.docx) tetap dinonaktifkan (locked) hingga seluruh syarat terpenuhi mutlak: seluruh kutipan disetujui staf, checklist 5W+1H berstatus lengkap, foto kegiatan terverifikasi, dan formulir tidak mengalami perubahan data yang belum digenerasi ulang. Setelah valid, sistem mengekspor berkas via POST /api/export-docx menghasilkan file Word resmi (press-release-diskominfo-YYYYMMDD-HHMMSS.docx) lengkap dengan kop dinas Diskominfo Kota Contoh, format font baku, foto 300 DPI, dan identitas verifikator. Naskah juga langsung disalin untuk publikasi di portal portal.kotacontoh.go.id dan akun Instagram."),

        ("5. Prosedur Pengarsipan Digital Terpusat",
         "Seluruh berkas naskah berita, data formulir 5W+1H, riwayat koreksi pimpinan, foto liputan asli, dan berkas ekspor Word secara otomatis disimpan ke repositori komputasi awan terpusat. Berkas dapat ditelusuri kembali sewaktu-waktu melalui fitur pencarian berdasarkan tanggal kegiatan, seksi dinas, atau kata kunci agenda untuk keperluan laporan pertanggungjawaban (LPJ).")
    ]

    for title, desc in prosedur_usulan_items:
        p_item = doc.add_paragraph()
        format_paragraph(p_item, space_before=2, space_after=4, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent=Inches(0.4))
        r_t = p_item.add_run(f"{title}: ")
        format_run(r_t, bold=True)
        r_d = p_item.add_run(desc)
        format_run(r_d, bold=False)
        ref_elem_34.addprevious(p_item._p)

    # 3.4.2 Use Case Diagram Sistem Usulan
    insert_heading_with_num_34("Use Case Diagram Sistem Usulan", ilvl=2, page_break_before=True)
    insert_para_34("Use Case Diagram sistem usulan memodelkan seluruh fungsi yang disediakan oleh Aplikasi Press Release Auto-Generator serta keterhubungannya dengan para aktor pengguna.")

    insert_para_34("Tabel III.6. Deskripsi Aktor Sistem Usulan", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), space_before=6, space_after=2, keep_with_next=True)
    headers_t6 = ["No.", "Aktor", "Deskripsi Peran dan Tanggung Jawab dalam Sistem"]
    data_t6 = [
        ["1.", "Staf Humas", "Bertindak sebagai operator pelaksana yang menginput formula fakta 5W+1H, memilih kategori kegiatan dinamis, mengunggah foto berintegritas biner, memicu pembentukan draf AI, mengaudit komparasi kutipan narasumber, menyunting draf di Live Editor, memvalidasi takarir Instagram, mengajukan naskah ke pimpinan, dan mengunduh berkas Word (.docx) ber-kop resmi."],
        ["2.", "Pimpinan (Kepala Bidang)", "Bertindak sebagai verifikator materi rilis yang menelaah draf berita pada dasbor sistem, memeriksa akurasi informasi dan etika kedinasan, menyematkan catatan revisi, memberikan persetujuan resmi (approval ACC), serta memantau rekam jejak publikasi."],
        ["3.", "Administrator Sistem", "Bertindak sebagai pengelola teknis yang bertugas memelihara akun pengguna, mengonfigurasi batas laju permintaan (rate limit), memantau konektivitas API Google Gemini, mengawasi log audit sistem, serta memastikan ketersediaan peladen repositori awan."]
    ]
    add_styled_table(doc, headers_t6, data_t6, [0.4, 1.4, 4.9], ref_elem_34)
    insert_para_34("Sumber: Hasil Analisis dan Perancangan Sistem Usulan (2026)", align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), size=9.5, space_before=2, space_after=10)

    insert_para_34("Tabel III.7. Deskripsi Use Case Sistem Usulan", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), space_before=6, space_after=2, keep_with_next=True)
    headers_t7 = ["No.", "Nama Use Case", "Deskripsi Fungsionalitas Sistem"]
    data_t7 = [
        ["1.", "Autentikasi Pengguna (Login)", "Memvalidasi identitas kredensial staf, pimpinan, atau admin guna mengamankan hak akses modul aplikasi."],
        ["2.", "Input Fakta 5W+1H Terstruktur", "Menyediakan formulir interaktif dengan 6 kartu status waktu nyata (What, Who, Where, When, Why, How) yang mencegah data kosong."],
        ["3.", "Pilih Jenis Kegiatan Dinamis", "Menyajikan 6 opsi kategori kegiatan (bimbingan, lomba, upacara, pelayanan, rapat, lainnya) beserta input kondisional khusus."],
        ["4.", "Pilih Dateline Kecamatan Kota Contoh", "Menyediakan pilihan baku seluruh wilayah kecamatan di Kota Contoh untuk standarisasi dateline berita."],
        ["5.", "Unggah & Validasi Foto", "Menerima unggahan foto liputan dengan pemeriksaan ekstensi biner (magic bytes) dan optimasi kompresi visual."],
        ["6.", "Bentuk Draf Berita (Gemini AI)", "Memproses data masukan menggunakan model AI dengan rekayasa prompt jurnalistik piramida terbalik kedinasan."],
        ["7.", "Audit Kutipan (Original vs Cleaned)", "Menyajikan modul perbandingan kutipan narasumber secara berdampingan untuk mencegah distorsi dan halusinasi makna."],
        ["8.", "Audit Kepatuhan Fakta 5W+1H", "Memeriksa ketercakupan seluruh poin fakta masukan di dalam narasi berita yang dihasilkan oleh sistem."],
        ["9.", "Sunting Naskah (Live Editor)", "Menyediakan pengolah kata interaktif bagi staf untuk menyempurnakan redaksi sebelum diajukan ke pimpinan."],
        ["10.", "Generate Takarir Instagram", "Menghasilkan teks takarir (caption) ringkas dan tagar resmi siap unggah untuk akun media sosial Diskominfo Kota Contoh."],
        ["11.", "Ajukan Naskah ke Verifikasi", "Mengirimkan berkas naskah ke daftar antrean telaah pimpinan secara terpusat di dalam sistem."],
        ["12.", "Telaah & Catat Revisi", "Pimpinan memeriksa substansi naskah berita dan menyematkan catatan perbaikan jika naskah belum layak terbit."],
        ["13.", "Setujui Naskah (Approval ACC)", "Pimpinan mengonfirmasi persetujuan resmi terbit sehingga status dokumen terkunci menjadi Approved."],
        ["14.", "Validasi Factual Gatekeeper", "Mengunci fungsi unduh Word hingga seluruh kutipan disetujui, foto terunggah, dan fakta 5W+1H terisi lengkap."],
        ["15.", "Ekspor Dokumen Resmi (.docx)", "Menghasilkan file Microsoft Word resmi ber-kop Diskominfo Kota Contoh, bertipografi dinas, dan berfoto resolusi tinggi."],
        ["16.", "Kelola Arsip Publikasi Terpusat", "Menyimpan dan mengindeks seluruh naskah, foto, dan log persetujuan ke repositori awan yang mudah ditelusuri."]
    ]
    add_styled_table(doc, headers_t7, data_t7, [0.4, 2.0, 4.3], ref_elem_34)
    insert_para_34("Sumber: Hasil Analisis dan Perancangan Sistem Usulan (2026)", align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), size=9.5, space_before=2, space_after=10)

    # Insert Use Case Usulan Image on a CLEAN PAGE
    p_img_ucu = insert_para_34("", align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), space_before=8, space_after=4, keep_with_next=True, page_break_before=True)
    run_ucu = p_img_ucu.add_run()
    run_ucu.add_picture(_resolve_asset('template/gambar/gambar_3_4_use_case_usulan.png'), width=Inches(5.4))
    insert_para_34("Gambar III.4. Use Case Diagram Sistem Usulan Aplikasi Press Release Auto-Generator", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), space_before=2, space_after=2, keep_with_next=True)
    insert_para_34("Sumber: Hasil Perancangan Sistem Usulan (2026)", align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), size=9.5, space_before=0, space_after=12)

    # 3.4.3 Activity Diagram Sistem Usulan
    insert_heading_with_num_34("Activity Diagram Sistem Usulan", ilvl=2, page_break_before=True)
    insert_para_34("Activity Diagram sistem usulan memodelkan dinamika aliran aktivitas operasional secara berkesinambungan antara Staf Humas, modul sistem aplikasi web cerdas (Next.js & Gemini AI), Pimpinan verifikator, serta portal publikasi dan repositori awan.")

    insert_para_34("Tabel III.8. Skenario Aliran Kerja (Workflow) Sistem Usulan", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), space_before=6, space_after=2, keep_with_next=True)
    headers_t8 = ["No.", "Entitas Pelaksana", "Aktivitas Operasional", "Keluaran / Respons Sistem"]
    data_t8 = [
        ["1.", "Staf Humas", "Mengisi formulir fakta 5W+1H, memilih jenis kegiatan dinamis, memilih kecamatan dateline, menginput kutipan, dan mengunggah foto", "Seluruh indikator kartu 5W+1H berubah hijau dan data masukan siap diproses"],
        ["2.", "Sistem Web & AI", "Memvalidasi integritas data (Zod) dan file biner gambar (magic bytes)", "Data dinyatakan sah dan lolos uji keamanan berkas masukan"],
        ["3.", "Sistem Web & AI", "Mengirim payload ke Gemini AI via endpoint terproteksi (POST /api/generate)", "Draf berita piramida terbalik, audit kutipan, audit fakta, dan takarir medsos terbentuk"],
        ["4.", "Staf Humas", "Menelaah komparasi kutipan (original vs cleaned), menyetujui kutipan, dan menyunting draf pada Live Editor", "Kutipan tervalidasi bebas distorsi makna dan naskah berita disempurnakan"],
        ["5.", "Staf Humas", "Mengirimkan pengajuan naskah berita ke antrean verifikasi pimpinan", "Status dokumen berubah menjadi Under Review dan notifikasi terkirim"],
        ["6.", "Pimpinan", "Membuka dasbor verifikasi dan memeriksa kelayakan rilis berita", "Pimpinan mengambil keputusan persetujuan (Decision)"],
        ["7.", "Pimpinan", "Pemeriksaan: Apakah naskah rilis disetujui?", "Jika Revisi: Menyematkan catatan revisi ke sistem (kembali ke Staf)\nJika ACC: Menekan tombol persetujuan resmi (Approved)"],
        ["8.", "Sistem Web & AI", "Memeriksa pemenuhan syarat integritas melalui Factual Gatekeeper Guard", "Semua kutipan disetujui, foto valid, fakta lengkap: Tombol ekspor Word aktif"],
        ["9.", "Sistem Web & AI", "Membuat berkas Word dinas (POST /api/export-docx) dan menyimpan arsip ke cloud", "File press-release-diskominfo-YYYYMMDD-HHMMSS.docx terbentuk dan terarsip"],
        ["10.", "Staf Humas", "Mengunduh file .docx ber-kop dinas dan mempublikasikan ke web portal & medsos", "Siaran pers tersirkulasi resmi ke media massa dan arsip tersimpan rapi (Selesai)"]
    ]
    add_styled_table(doc, headers_t8, data_t8, [0.4, 1.3, 2.3, 2.7], ref_elem_34)
    insert_para_34("Sumber: Hasil Analisis dan Perancangan Sistem Usulan (2026)", align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), size=9.5, space_before=2, space_after=10)

    # Insert Activity Diagram Usulan Image on CLEAN PAGE
    p_img_actu = insert_para_34("", align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), space_before=8, space_after=4, keep_with_next=True, page_break_before=True)
    run_actu = p_img_actu.add_run()
    run_actu.add_picture(_resolve_asset('template/gambar/gambar_3_5_activity_diagram_usulan.png'), width=Inches(5.4))
    insert_para_34("Gambar III.5. Activity Diagram Sistem Usulan Aplikasi Press Release Auto-Generator", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), space_before=2, space_after=2, keep_with_next=True)
    insert_para_34("Sumber: Hasil Perancangan Sistem Usulan (2026)", align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), size=9.5, space_before=0, space_after=12)

    # 3.4.4 Rancangan Antarmuka Aplikasi Press Release Auto-Generator
    insert_heading_with_num_34("Rancangan Antarmuka Aplikasi Press Release Auto-Generator", ilvl=2, page_break_before=True)
    insert_para_34("Rancangan antarmuka pengguna (user interface) disusun berlandaskan prinsip ergonomi web responsif yang modern, bersih, dan intuitif, yang diadaptasi secara langsung dari implementasi sistem nyata pada alamat https://press-release-kotacontoh.contoh.go.id/. Antarmuka dibangun dengan palet warna resmi instansi (kombinasi hijau forest #1b4332, emas kedinasan #c59b27, dan latar belakang off-white yang nyaman di mata). Struktur antarmuka terbagi atas beberapa komponen utama:")
    insert_para_34("1. Bilah Navigasi dan Stepper Alur 3 Langkah: Bagian kepala antarmuka menampilkan identitas institusi 'HUMAS DISKOMINFO KOTA CONTOH' dan nama aplikasi 'Press Release Generator V2', disertai arahan operasional: 'Isi fakta 5W+1H, audit draf, setujui kutipan, lalu download dokumen Word'. Di samping kanan tersedia tombol 'Reset draf' untuk mengosongkan formulir sewaktu-waktu. Alur kerja dipandu oleh indikator tahapan (stepper wizard) yang terbagi menjadi 3 langkah berurutan: (1) Isi data 5W1H, (2) Review & edit, dan (3) Download DOCX.")
    insert_para_34("2. Panel Kartu Pemantau Fakta Inti (Formula 5W+1H Badges): Sistem menyajikan 6 kartu status interaktif real-time di bagian atas formulir (What, Who, Where, When, Why, How) yang langsung merespons kelengkapan isian pengguna. Sistem menegaskan aturan dasar: 'Field inti wajib diisi dengan fakta. AI tidak akan menebak data yang kosong.' Hal ini menjadi benteng utama dalam mencegah kekeliruan narasi sejak awal masukan data.")
    insert_para_34("3. Formulir Parameter Kegiatan Dinamis dan Kontekstual: Formulir dirancang secara cerdas dengan pilihan 6 kategori agenda kedinasan (bimbingan, lomba, upacara, pelayanan, rapat, lainnya) yang memunculkan kolom masukan kontekstual secara otomatis, menu pilihan baku daftar kecamatan dateline resmi Kota Contoh, modul pencatatan hingga 10 pihak yang hadir, hingga 5 kutipan langsung narasumber pejabat, serta area unggah foto liputan dengan validasi integritas biner (magic bytes).")
    insert_para_34("4. Modul Audit Redaksional, Review Kutipan, dan Live Text Editor: Setelah proses generasi dijalankan, sistem menyajikan panel review komparasi kutipan berdampingan (original vs cleaned) guna menjamin keaslian makna ucapan pejabat tanpa halusinasi AI, audit ketercakupan fakta 5W+1H, modul Live Text Editor untuk penyuntingan langsung, serta generator takarir media sosial siap pakai untuk akun Instagram @humas_kotacontoh.")
    insert_para_34("5. Modul Pratinjau Dokumen dan Factual Gatekeeper Guard: Pada langkah ketiga (Download DOCX), sistem menyajikan pratinjau naskah ber-kop surat resmi Dinas Komunikasi dan Informatika Kota Contoh. Tombol unduh dokumen Microsoft Word (.docx) dilindungi oleh gerbang validasi faktual (Factual Gatekeeper Guard) yang hanya akan aktif apabila seluruh kutipan telah disetujui, foto terverifikasi, dan fakta 5W+1H terisi lengkap. Dokumen Word yang diunduh berformat baku dengan penamaan otomatis press-release-diskominfo-YYYYMMDD-HHMMSS.docx.")

    # Insert UI Mockup Image on CLEAN PAGE
    p_img_ui = insert_para_34("", align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), space_before=8, space_after=4, keep_with_next=True, page_break_before=True)
    run_ui = p_img_ui.add_run()
    run_ui.add_picture(_resolve_asset('template/gambar/gambar_3_6_rancangan_antarmuka_generator.png'), width=Inches(5.4))
    insert_para_34("Gambar III.6. Rancangan Antarmuka Aplikasi Press Release Auto-Generator", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), space_before=2, space_after=2, keep_with_next=True)
    insert_para_34("Sumber: Tangkapan Layar Antarmuka Aplikasi Web (press-release-kotacontoh.contoh.go.id), 2026", align=WD_ALIGN_PARAGRAPH.CENTER, indent=Inches(0), size=9.5, space_before=0, space_after=14)

    # 6. Update Bab IV (Kesimpulan dan Saran)
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip() == "Kesimpulan":
            # Add conclusion paragraphs after it
            p_k1 = doc.add_paragraph("1. Tata kelola publikasi berita kedinasan yang berjalan pada Bidang Humas Dinas Komunikasi dan Informatika Kota Contoh saat ini masih menghadapi keterbatasan operasional: pengetikan draf naskah rilis pers secara manual di Microsoft Word membutuhkan durasi 1 hingga 2 jam (45–90 menit) per agenda, verifikasi draf bertumpu pada chat WhatsApp personal pimpinan yang rawan tertimbun dan menyulitkan pelacakan revisi (version tracking), serta pengarsipan berkas di direktori laptop staf berisiko tinggi mengalami kerusakan atau kehilangan data.")
            format_paragraph(p_k1, space_before=4, space_after=4, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent=Inches(0.4))
            for r in p_k1.runs:
                format_run(r, size_pt=12)

            p_k2 = doc.add_paragraph("2. Rekomendasi pemecahan masalah melalui perancangan Aplikasi Press Release Auto-Generator berbasis formulir 5W+1H terstruktur dan integrasi model komputasi cerdas (Google Gemini AI) terbukti secara efektif memangkas waktu produksi siaran pers menjadi kurang dari 5 hingga 10 menit, menjamin konsistensi format penulisan dokumen resmi instansi ber-kop dinas, menyediakan modul telaah komparasi kutipan narasumber guna mencegah halusinasi data, serta mewujudkan transparansi verifikasi dan pengarsipan digital terpusat.")
            format_paragraph(p_k2, space_before=2, space_after=8, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent=Inches(0.4))
            for r in p_k2.runs:
                format_run(r, size_pt=12)

            p._p.addnext(p_k2._p)
            p._p.addnext(p_k1._p)
            break

    for i, p in enumerate(doc.paragraphs):
        if p.text.strip() == "Saran":
            p_s1 = doc.add_paragraph("1. Bagi Mahasiswa: Memperdalam penguasaan integrasi komputasi cerdas terapan, rekayasa prompt (prompt engineering) berstandar institusional, serta metodologi pengujian otomatis (end-to-end testing) dalam pengembangan sistem informasi sektor publik.")
            format_paragraph(p_s1, space_before=4, space_after=3, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent=Inches(0.4))
            for r in p_s1.runs:
                format_run(r, size_pt=12)

            p_s2 = doc.add_paragraph("2. Bagi Instansi (Dinas Komunikasi dan Informatika Kota Contoh): Mempertimbangkan implementasi dan pengoperasian penuh Aplikasi Press Release Auto-Generator pada Subbagian Tata Usaha dan seksi-seksi teknis terkait, serta menyelenggarakan pelatihan operasional bagi staf kehumasan guna mengoptimalkan diseminasi informasi publik yang cepat, akurat, dan terpercaya.")
            format_paragraph(p_s2, space_before=2, space_after=3, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent=Inches(0.4))
            for r in p_s2.runs:
                format_run(r, size_pt=12)

            p_s3 = doc.add_paragraph("3. Bagi Universitas Bina Sarana Informatika (UBSI): Terus meningkatkan jalinan kemitraan strategis Praktik Kerja Lapangan dengan lembaga vertikal kementerian dan instansi pemerintah daerah, serta memperkaya kurikulum berbasis studi kasus transformasi digital yang relevan dengan kebutuhan dunia kerja.")
            format_paragraph(p_s3, space_before=2, space_after=8, align=WD_ALIGN_PARAGRAPH.JUSTIFY, first_line_indent=Inches(0.4))
            for r in p_s3.runs:
                format_run(r, size_pt=12)

            p._p.addnext(p_s3._p)
            p._p.addnext(p_s2._p)
            p._p.addnext(p_s1._p)
            break

    _atomic_save_docx(doc, target_path, backup=True)
    print(f"Clean document with automatic numId=6 successfully saved to: {target_path}")

    if sync_backup and os.path.abspath(target_path) != os.path.abspath(backup_path):
        _atomic_save_docx(doc, backup_path, backup=True)
        print(f"Base file also updated: {backup_path}")


def _add_page_number_field(run):
    """Add a dynamic Word PAGE field code to a run."""
    run._r.append(parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>'))
    run._r.append(parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>'))
    run._r.append(parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="separate"/>'))
    run._r.append(parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>'))


def _setup_ubsi_section_geometry(sec):
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.left_margin = Cm(4.0)
    sec.top_margin = Cm(3.0)
    sec.right_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sec.header_distance = Cm(1.2)
    sec.footer_distance = Cm(1.2)


def _set_section_pg_num(sec, fmt="decimal", start=None):
    sectPr = sec._sectPr
    pgNumType = sectPr.find(qn("w:pgNumType"))
    if pgNumType is None:
        pgNumType = parse_xml(f'<w:pgNumType {nsdecls("w")}/>')
        sectPr.append(pgNumType)
    pgNumType.set(qn("w:fmt"), fmt)
    if start is not None:
        pgNumType.set(qn("w:start"), str(start))
    elif qn("w:start") in pgNumType.attrib:
        del pgNumType.attrib[qn("w:start")]


def _attach_behind_text_watermark(header, logo_file, size_cm=10.0):
    """Insert a 10x10 cm centered Behind-Text washout watermark image into a section header."""
    if not logo_file or not os.path.exists(logo_file):
        return
    p_wm = header.add_paragraph()
    p_wm.paragraph_format.space_before = Pt(0)
    p_wm.paragraph_format.space_after = Pt(0)
    p_wm.paragraph_format.line_spacing = 1.0
    run_wm = p_wm.add_run()
    run_wm.add_picture(logo_file, width=Cm(size_cm), height=Cm(size_cm))

    drawing = run_wm._r.find(qn("w:drawing"))
    if drawing is None:
        return
    wp_ns = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
    a_ns = "http://schemas.openxmlformats.org/drawingml/2006/main"
    inline = drawing.find(f"{{{wp_ns}}}inline")
    if inline is None:
        return

    extent = inline.find(f"{{{wp_ns}}}extent")
    docPr = inline.find(f"{{{wp_ns}}}docPr")
    cNv = inline.find(f"{{{wp_ns}}}cNvGraphicFramePr")
    graphic = inline.find(f"{{{a_ns}}}graphic")
    if extent is None or graphic is None:
        return

    blip = graphic.find(f".//{{{a_ns}}}blip")
    if blip is not None:
        blip.append(parse_xml(f'<a:lum xmlns:a="{a_ns}" bright="75000" contrast="-70000"/>'))

    anchor = parse_xml(
        f'<wp:anchor xmlns:wp="{wp_ns}" distT="0" distB="0" distL="0" distR="0" '
        'simplePos="0" relativeHeight="251658240" behindDoc="1" locked="0" layoutInCell="1" allowOverlap="1">'
        '<wp:simplePos x="0" y="0"/>'
        '<wp:positionH relativeFrom="page"><wp:align>center</wp:align></wp:positionH>'
        '<wp:positionV relativeFrom="page"><wp:align>center</wp:align></wp:positionV>'
        '</wp:anchor>'
    )
    anchor.append(extent)
    anchor.append(parse_xml(f'<wp:effectExtent xmlns:wp="{wp_ns}" l="0" t="0" r="0" b="0"/>'))
    anchor.append(parse_xml(f'<wp:wrapNone xmlns:wp="{wp_ns}"/>'))
    if docPr is not None:
        docPr.set("name", "UBSI Watermark 10x10cm")
        anchor.append(docPr)
    if cNv is not None:
        anchor.append(cNv)
    anchor.append(graphic)

    drawing.remove(inline)
    drawing.append(anchor)


def scaffold_pkl_docx(outline="4", doc_type="laporan", title="LAPORAN PRAKTIK KERJA LAPANGAN",
                      author="Penulis Contoh", nim="00000001", instansi="Dinas Komunikasi dan Informatika Kota Contoh",
                      city="Kota Contoh", year="2026", output_path=None, watermark=None):
    """Generate kerangka .docx PKL, Proposal, Tugas Akhir, atau Skripsi UBSI patuh SK Rektor No. 165/2.01/UBSI/III/2026."""
    doc_type_norm = str(doc_type).lower()
    is_thesis = doc_type_norm in ("skripsi", "ta")
    enable_watermark = is_thesis if watermark is None else bool(watermark)
    if is_thesis:
        key = str(outline) if str(outline) in SKRIPSI_OUTLINES else "156"
        outline_name, chapters = SKRIPSI_OUTLINES[key]
        doc_label = "SKRIPSI" if doc_type_norm == "skripsi" else "TUGAS AKHIR"
        submission_note = (
            "Diajukan untuk memenuhi salah satu syarat kelulusan Program Sarjana (S1)"
            if doc_type_norm == "skripsi"
            else "Diajukan untuk memenuhi salah satu syarat kelulusan Program Diploma Tiga (D3)"
        )
        default_filename = f"{doc_type_norm.upper()}_UBSI_{key}_{nim}.docx"
    else:
        key = "proposal" if doc_type_norm == "proposal" else (str(outline) if str(outline) in PKL_OUTLINES else "4")
        outline_name, chapters = PKL_OUTLINES[key]
        doc_label = "PROPOSAL PRAKTIK KERJA LAPANGAN" if key == "proposal" else "LAPORAN PRAKTIK KERJA LAPANGAN"
        submission_note = "Diajukan untuk memenuhi mata kuliah Praktik Kerja Lapangan pada Program Sarjana (S1)"
        default_filename = f"PKL_UBSI_{key.upper()}_{nim}.docx"

    doc = docx.Document()
    logo_file = _resolve_asset('template/gambar/logo-ubsi.png')

    # Section 0: Cover (dihitung i, nomor tidak dicetak, tanpa watermark)
    sec_cover = doc.sections[0]
    _setup_ubsi_section_geometry(sec_cover)
    sec_cover.different_first_page_header_footer = False
    sec_cover.header.paragraphs[0].text = ""
    sec_cover.footer.paragraphs[0].text = ""

    def _add_center_heading(text, size_pt=14, page_break=True, space_after=12):
        p = doc.add_paragraph()
        format_paragraph(
            p,
            space_before=0,
            space_after=space_after,
            line_spacing=1.5,
            align=WD_ALIGN_PARAGRAPH.CENTER,
            first_line_indent=Cm(0),
            keep_with_next=True,
            page_break_before=page_break,
        )
        format_run(p.add_run(text), size_pt=size_pt, bold=True)
        return p

    def _add_sub_heading(text):
        p = doc.add_paragraph()
        format_paragraph(
            p,
            space_before=12,
            space_after=4,
            line_spacing=1.5,
            align=WD_ALIGN_PARAGRAPH.LEFT,
            first_line_indent=Cm(0),
            keep_with_next=True,
        )
        format_run(p.add_run(text), size_pt=12, bold=True)
        return p

    def _add_body(text, line_spacing=2.0, indent_cm=1.2, italic=False, space_after=6):
        p = doc.add_paragraph()
        format_paragraph(
            p,
            space_before=0,
            space_after=space_after,
            line_spacing=line_spacing,
            align=WD_ALIGN_PARAGRAPH.JUSTIFY,
            first_line_indent=Cm(indent_cm),
        )
        format_run(p.add_run(text), size_pt=12, italic=italic)
        return p

    # 1. Cover / Lembar Judul (Poin 2.2 Pedoman UBSI)
    p_title = doc.add_paragraph()
    format_paragraph(p_title, space_before=6, space_after=12, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=Cm(0))
    format_run(p_title.add_run(title.upper()), size_pt=14, bold=True)

    if not os.path.exists(logo_file):
        raise FileNotFoundError(
            f"Aset wajib logo UBSI tidak ditemukan: {logo_file}. "
            "Pastikan berkas template/gambar/logo-ubsi.png tersedia sebelum menyusun dokumen."
        )
    p_logo = doc.add_paragraph()
    format_paragraph(p_logo, space_before=12, space_after=12, line_spacing=1.0, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=Cm(0))
    logo_cm = 5.0 if is_thesis else 4.0
    p_logo.add_run().add_picture(logo_file, width=Cm(logo_cm), height=Cm(logo_cm))

    p_label = doc.add_paragraph()
    format_paragraph(p_label, space_before=6, space_after=6, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=Cm(0))
    format_run(p_label.add_run(doc_label), size_pt=18, bold=True)

    p_sub = doc.add_paragraph()
    format_paragraph(p_sub, space_before=4, space_after=10, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=Cm(0))
    format_run(p_sub.add_run(submission_note), size_pt=12, bold=False)

    p_auth = doc.add_paragraph()
    format_paragraph(p_auth, space_before=8, space_after=12, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=Cm(0))
    format_run(p_auth.add_run(f"{author.upper()}\nNIM : {nim}"), size_pt=14, bold=True)

    p_meta = doc.add_paragraph()
    format_paragraph(p_meta, space_before=12, space_after=12, line_spacing=1.5, align=WD_ALIGN_PARAGRAPH.CENTER, first_line_indent=Cm(0))
    inst_line = f"Objek Penelitian/Instansi: {instansi}\n" if instansi else ""
    format_run(
        p_meta.add_run(
            f"{inst_line}Skema: {outline_name}\n\n"
            f"PROGRAM STUDI TEKNOLOGI INFORMASI\n"
            f"FAKULTAS TEKNIK DAN INFORMATIKA\n"
            f"UNIVERSITAS BINA SARANA INFORMATIKA\n"
            f"{city.upper()}\n{year}"
        ),
        size_pt=12,
        bold=True,
    )

    # Section 1: Bagian Awal (Front Matter - Romawi kecil ii, iii, ... di bawah tengah)
    sec_front = doc.add_section(WD_SECTION.NEW_PAGE)
    _setup_ubsi_section_geometry(sec_front)
    sec_front.different_first_page_header_footer = False
    sec_front.header.is_linked_to_previous = False
    sec_front.footer.is_linked_to_previous = False
    _set_section_pg_num(sec_front, fmt="lowerRoman", start=2)
    sec_front.header.paragraphs[0].text = ""
    if enable_watermark:
        _attach_behind_text_watermark(sec_front.header, logo_file, size_cm=10.0)
    p_fftr = sec_front.footer.paragraphs[0]
    p_fftr.text = ""
    p_fftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_fftr = p_fftr.add_run()
    format_run(r_fftr, size_pt=12)
    _add_page_number_field(r_fftr)

    if is_thesis:
        _add_center_heading(f"SURAT PERNYATAAN KEASLIAN {doc_label}", size_pt=14, page_break=False)
        _add_body(
            f"Yang bertanda tangan di bawah ini, {author} (NIM: {nim}), Program Studi Teknologi Informasi, "
            f"Fakultas Teknik dan Informatika, Universitas Bina Sarana Informatika, menyatakan dengan sesungguhnya bahwa "
            f"{doc_label.title()} berjudul \"{title}\" merupakan hasil karya asli dan bebas plagiarisme "
            "(dibubuhi e-Meterai Rp 10.000 resmi Peruri saat pengunggahan final).",
            line_spacing=1.5,
            indent_cm=0,
        )
        _add_center_heading("SURAT PERNYATAAN PERSETUJUAN PUBLIKASI KARYA ILMIAH", size_pt=14, page_break=True)
        _add_body(
            f"Saya, {author} (NIM: {nim}), memberikan hak bebas royalti non-eksklusif kepada Universitas Bina Sarana Informatika "
            f"untuk menyimpan, mengalihmedia, dan mempublikasikan {doc_label.title()} ini demi kepentingan pengembangan ilmu pengetahuan.",
            line_spacing=1.5,
            indent_cm=0,
        )
        _add_center_heading(f"PERSETUJUAN DAN PENGESAHAN {doc_label}", size_pt=14, page_break=True)
        _add_body(
            f"{doc_label.title()} ini disusun oleh {author} (NIM: {nim}), Program Studi Teknologi Informasi, "
            "Fakultas Teknik dan Informatika, Universitas Bina Sarana Informatika, dan telah disetujui untuk dipertahankan "
            "(tanda tangan digital QR Code via DigiSAYS).",
            line_spacing=1.5,
            indent_cm=0,
        )
        for heading_lbl, placeholder_lbl in (
            ("ABSTRAK", "[ISI DATA NYATA: Tulis Abstrak Bahasa Indonesia dalam 1 paragraf tunggal (150-200 kata, spasi 1.0) yang memuat Latar Belakang, Tujuan, Metode, dan Hasil.]\n\nKata Kunci: [3-5 kata kunci]"),
            ("ABSTRACT", "[ISI DATA NYATA: Write English Abstract in 1 single paragraph (150-200 words, 1.0 spacing) covering Background, Objective, Method, and Results.]\n\nKeywords: [3-5 keywords]"),
        ):
            _add_center_heading(heading_lbl, size_pt=14, page_break=True)
            _add_body(placeholder_lbl, line_spacing=1.0, indent_cm=1.2)
    else:
        _add_center_heading(f"PERSETUJUAN\n{doc_label}", size_pt=14, page_break=False)
        _add_body(
            f"{doc_label.title()} ini disusun oleh {author} (NIM: {nim}), Program Sarjana (S1), "
            "Program Studi Teknologi Informasi, Fakultas Teknik dan Informatika, Universitas Bina Sarana Informatika, "
            f"dan telah disetujui untuk dinilai pada periode Tahun Akademik {year}.",
            line_spacing=1.5,
            indent_cm=0,
        )

    _add_center_heading("KATA PENGANTAR", size_pt=14, page_break=True)
    _add_body(
        f'Dengan mengucapkan puji syukur ke hadirat Tuhan Yang Maha Esa atas terselesaikannya {doc_label.title()} '
        f'dengan judul "{title}", yang merupakan salah satu syarat kelulusan mata kuliah pada Program Studi '
        'Teknologi Informasi Fakultas Teknik dan Informatika Universitas Bina Sarana Informatika.',
        line_spacing=1.5 if not is_thesis else 2.0,
        indent_cm=1.2,
    )

    lampiran_note = (
        "Daftar Lampiran diketik 1 spasi dan memuat Surat Keterangan Riset/Implementasi, Potongan Kode Sumber Utama, serta Bukti Pengujian."
        if is_thesis
        else "Daftar Lampiran diketik 1 spasi dan memuat Surat Keterangan PKL, Nilai PKL, Lembar Kuesioner, serta dokumentasi pendukung."
    )
    for front_list in ("DAFTAR ISI", "DAFTAR SIMBOL", "DAFTAR GAMBAR", "DAFTAR TABEL", "DAFTAR LAMPIRAN"):
        _add_center_heading(front_list, size_pt=14, page_break=True)
        note_map = {
            "DAFTAR ISI": "Daftar Isi diketik 1 spasi dan memuat Bagian Awal (Romawi kecil ii, iii, ...), Bagian Pokok (Angka Arab 1, 2, ...), serta Bagian Akhir.",
            "DAFTAR SIMBOL": "Daftar Simbol diketik 1 spasi dan memuat simbol UML / Flowchart / Jaringan yang digunakan dalam naskah.",
            "DAFTAR GAMBAR": "Daftar Gambar diketik 1 spasi dengan penomoran Romawi Bab konsisten (contoh: Gambar II.1., Gambar III.1.).",
            "DAFTAR TABEL": "Daftar Tabel diketik 1 spasi dengan penomoran Romawi Bab konsisten (contoh: Tabel II.1., Tabel III.1.).",
            "DAFTAR LAMPIRAN": lampiran_note,
        }
        _add_body(f"[{note_map[front_list]}]", line_spacing=1.0, indent_cm=0, italic=True)

    # 3. Bagian Pokok (1 section per Bab: awal bab nomor bawah tengah, lanjutan kanan atas)
    sub_map = OUTLINE_SUBCHAPTERS.get(key, {})
    for ch_idx, ch in enumerate(chapters):
        sec_ch = doc.add_section(WD_SECTION.NEW_PAGE)
        _setup_ubsi_section_geometry(sec_ch)
        sec_ch.header.is_linked_to_previous = False
        sec_ch.footer.is_linked_to_previous = False
        sec_ch.different_first_page_header_footer = True
        sec_ch.first_page_header.is_linked_to_previous = False
        sec_ch.first_page_footer.is_linked_to_previous = False
        _set_section_pg_num(sec_ch, fmt="decimal", start=1 if ch_idx == 0 else None)

        sec_ch.first_page_header.paragraphs[0].text = ""
        p_ch_fftr = sec_ch.first_page_footer.paragraphs[0]
        p_ch_fftr.text = ""
        p_ch_fftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_ch_fftr = p_ch_fftr.add_run()
        format_run(r_ch_fftr, size_pt=12)
        _add_page_number_field(r_ch_fftr)

        p_ch_hdr = sec_ch.header.paragraphs[0]
        p_ch_hdr.text = ""
        p_ch_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_ch_hdr = p_ch_hdr.add_run()
        format_run(r_ch_hdr, size_pt=12)
        _add_page_number_field(r_ch_hdr)
        sec_ch.footer.paragraphs[0].text = ""

        if enable_watermark:
            _attach_behind_text_watermark(sec_ch.first_page_header, logo_file, size_cm=10.0)
            _attach_behind_text_watermark(sec_ch.header, logo_file, size_cm=10.0)

        _add_center_heading(ch, size_pt=14, page_break=False)
        sub_headings = sub_map.get(ch, [])
        if sub_headings:
            for sub in sub_headings:
                _add_sub_heading(sub)
                _add_body(
                    f"[Tulis uraian akademik substantif untuk {sub} sesuai Pedoman UBSI 2026; gunakan referensi terverifikasi nyata dan sisipkan [ISI DATA NYATA: ...] hanya untuk data privat lapangan yang belum tersedia.]",
                    line_spacing=2.0,
                    indent_cm=1.2,
                )
        else:
            _add_body(
                f"[Tulis uraian akademik substantif untuk {ch} sesuai Pedoman UBSI 2026; gunakan referensi terverifikasi nyata dan sisipkan [ISI DATA NYATA: ...] hanya untuk data privat lapangan yang belum tersedia.]",
                line_spacing=2.0,
                indent_cm=1.2,
            )

    # 4. Bagian Akhir (Backmatter - nomor halaman angka Arab bawah tengah)
    sec_back = doc.add_section(WD_SECTION.NEW_PAGE)
    _setup_ubsi_section_geometry(sec_back)
    sec_back.different_first_page_header_footer = False
    sec_back.header.is_linked_to_previous = False
    sec_back.footer.is_linked_to_previous = False
    _set_section_pg_num(sec_back, fmt="decimal", start=None)
    sec_back.header.paragraphs[0].text = ""
    if enable_watermark:
        _attach_behind_text_watermark(sec_back.header, logo_file, size_cm=10.0)
    p_bftr = sec_back.footer.paragraphs[0]
    p_bftr.text = ""
    p_bftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_bftr = p_bftr.add_run()
    format_run(r_bftr, size_pt=12)
    _add_page_number_field(r_bftr)

    _add_center_heading("DAFTAR PUSTAKA", size_pt=14, page_break=False)
    _add_body(
        "[Isi Daftar Pustaka APA V.7 terverifikasi nyata di sini (semua nama pengarang ditulis lengkap tanpa et al. atau dkk. "
        "sesuai SK Rektor UBSI 2026; kuota TA D3 min. 5 jurnal OJS / Skripsi S1 min. 10 jurnal OJS 5 tahun terakhir; "
        "1 spasi per entri, jarak 2 spasi antar entri), serta ekspor salinan berkas .txt untuk impor Mendeley.]",
        line_spacing=1.0,
        indent_cm=0,
        italic=True,
    )

    _add_center_heading("DAFTAR RIWAYAT HIDUP", size_pt=14, page_break=True)
    _add_body(
        f"I. Biodata Mahasiswa\nNIM : {nim}\nNama Lengkap : {author}\n"
        f"Tempat/Tanggal Lahir : [ISI DATA NYATA: Tempat, Tanggal Lahir]\n"
        f"Alamat Lengkap : [ISI DATA NYATA: Alamat Lengkap Mahasiswa]\n\n"
        "II. Pendidikan\n1. [ISI DATA NYATA: Sekolah Dasar]\n2. [ISI DATA NYATA: Sekolah Menengah Pertama]\n"
        "3. [ISI DATA NYATA: Sekolah Menengah Atas/Kejuruan]\n"
        "4. Universitas Bina Sarana Informatika (Program Studi Teknologi Informasi)\n\n"
        "III. Riwayat Pengalaman Berorganisasi / Pekerjaan\n[ISI DATA NYATA: Riwayat pengalaman mahasiswa]",
        line_spacing=1.0,
        indent_cm=0,
    )

    if not is_thesis:
        for app_title in ("SURAT KETERANGAN PKL", "NILAI PRAKTIK KERJA LAPANGAN", "LEMBAR KUESIONER", "LAMPIRAN-LAMPIRAN"):
            _add_center_heading(app_title, size_pt=14, page_break=True)
            _add_body(f"[Lampirkan dokumen resmi {app_title.title()} sesuai Pedoman PKL UBSI 2026.]", line_spacing=1.5, indent_cm=0, italic=True)
    else:
        _add_center_heading("LAMPIRAN-LAMPIRAN", size_pt=14, page_break=True)
        _add_body("[Lampirkan instrumen penelitian, kode sumber utama, atau bukti pengujian sesuai Outline Skripsi UBSI 2026.]", line_spacing=1.5, indent_cm=0, italic=True)

    out_path = output_path or default_filename
    saved_abs = _atomic_save_docx(doc, out_path, backup=False)
    print(f"[BERHASIL] Kerangka {outline_name} tersimpan ke: {saved_abs}")
    return saved_abs


scaffold_ubsi_docx = scaffold_pkl_docx


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Editor In-Place & Scaffolder PKL, Proposal, & Skripsi/TA UBSI 2026 (.docx)")
    parser.add_argument("--scaffold", action="store_true", help="Buat kerangka baru PKL, Proposal, atau Skripsi/TA UBSI (.docx)")
    parser.add_argument("--type", choices=["laporan", "proposal", "skripsi", "ta"], default="laporan", help="Jenis dokumen UBSI")
    parser.add_argument("--outline", choices=["1", "2", "3", "4", "156", "138", "137", "158"], default="4", help="Outline PKL TI (1-4) atau Skripsi FTI (156, 138, 137, 158)")
    parser.add_argument("--title", default="LAPORAN PRAKTIK KERJA LAPANGAN", help="Judul dokumen")
    parser.add_argument("--author", default="Penulis Contoh", help="Nama penulis")
    parser.add_argument("--nim", default="00000001", help="NIM mahasiswa")
    parser.add_argument("--instansi", default="Dinas Komunikasi dan Informatika Kota Contoh", help="Nama instansi lokasi PKL/penelitian")
    parser.add_argument("--city", default="Kota Contoh", help="Kota kampus")
    parser.add_argument("--year", default="2026", help="Tahun penyusunan")
    parser.add_argument("-i", "--input", help="File .docx masukan untuk mode update in-place")
    parser.add_argument("-o", "--output", help="File .docx keluaran")
    parser.add_argument("--watermark", dest="watermark", action="store_true", default=None, help="Pasang watermark logo UBSI 10x10 cm Behind Text pada halaman non-cover")
    parser.add_argument("--no-watermark", dest="watermark", action="store_false", help="Nonaktifkan watermark otomatis")
    parser.add_argument("--no-backup-sync", action="store_true", help="Jangan timpa file input saat mode update")
    args = parser.parse_args()

    if args.scaffold:
        scaffold_pkl_docx(
            outline=args.outline,
            doc_type=args.type,
            title=args.title,
            author=args.author,
            nim=args.nim,
            instansi=args.instansi,
            city=args.city,
            year=args.year,
            output_path=args.output,
            watermark=args.watermark,
        )
    else:
        if not args.input:
            parser.error("Mode update in-place memerlukan flag -i/--input <file.docx> atau gunakan --scaffold.")
        run_clean_update(backup_path=args.input, target_path=args.output or args.input, sync_backup=not args.no_backup_sync)
