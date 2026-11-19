# /// script
# requires-python = ">=3.10"
# dependencies = ["python-docx"]
# ///
import argparse
import os
import sys
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT

_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT_DIR = os.path.dirname(_THIS_DIR)
for _cand_dir in (_THIS_DIR, _PARENT_DIR):
    if _cand_dir not in sys.path:
        sys.path.insert(0, _cand_dir)

try:
    from scripts.docx_io import atomic_save_docx
except ImportError:
    from docx_io import atomic_save_docx

_p = argparse.ArgumentParser()
_p.add_argument("-i", "--input", required=True)
doc_path = _p.parse_args().input

doc = docx.Document(doc_path)
body = doc._element.body

# 1. IDENTIFY & REMOVE MERGED ANOMALY TABLES (Table 2 and Table 8)
t2_el = doc.tables[2]._element
t8_el = doc.tables[8]._element

# Verify Table 2 has 32 rows and starts with No., Nama Dokumen
assert len(doc.tables[2].rows) == 32, "Table 2 does not have 32 rows"
assert len(doc.tables[8].rows) == 28, "Table 8 does not have 28 rows"

# Collect preceding blank paragraphs for t8
p_blanks_t8 = []
el = t8_el.getprevious()
while el is not None and el.tag.split('}')[-1] == 'p' and not el.xpath('string(.)').strip():
    p_blanks_t8.append(el)
    el = el.getprevious()

# Collect preceding blank paragraphs for t2
p_blanks_t2 = []
el = t2_el.getprevious()
while el is not None and el.tag.split('}')[-1] == 'p' and not el.xpath('string(.)').strip():
    p_blanks_t2.append(el)
    el = el.getprevious()

# Remove Table 8 and its preceding blank paragraphs first
for p in p_blanks_t8:
    body.remove(p)
body.remove(t8_el)
print("Removed merged Table 8 (28 rows) and its preceding blank paragraph")

# Remove Table 2 and its preceding blank paragraphs
for p in p_blanks_t2:
    body.remove(p)
body.remove(t2_el)
print("Removed merged Table 2 (32 rows) and its preceding blank paragraphs")

# 2. ENSURE ALL REMAINING TABLES USE NATIVE WORD TABLE GRID FORMAT
print(f"Remaining legitimate tables: {len(doc.tables)}")

def apply_word_table_format(table):
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    tblPr = table._element.xpath('w:tblPr')[0]
    
    existing_tbl_borders = tblPr.xpath('w:tblBorders')
    for b in existing_tbl_borders:
        tblPr.remove(b)
        
    borders_xml = (
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>\n'
        f'  <w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>\n'
        f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>\n'
        f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>\n'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>\n'
        f'  <w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(parse_xml(borders_xml))
    
    for r_idx, row in enumerate(table.rows):
        tr = row._tr
        trPr = tr.get_or_add_trPr()
        
        if not trPr.xpath('w:cantSplit'):
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
            
        if r_idx == 0:
            if not trPr.xpath('w:tblHeader'):
                trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        
        for cell in row.cells:
            tcPr = cell._element.get_or_add_tcPr()
            for shd in tcPr.xpath('w:shd'):
                tcPr.remove(shd)
                
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            
            for p in cell.paragraphs:
                p.paragraph_format.first_line_indent = 0
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.0
                
                if r_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for r in p.runs:
                        r.font.name = "Times New Roman"
                        r.font.size = Pt(10)
                        r.font.bold = True
                        r.font.color.rgb = RGBColor(0, 0, 0)
                else:
                    for r in p.runs:
                        r.font.name = "Times New Roman"
                        r.font.size = Pt(10)
                        r.font.color.rgb = RGBColor(0, 0, 0)

for i, table in enumerate(doc.tables):
    apply_word_table_format(table)

# 3. ADD DAFTAR TABEL IN FRONT MATTER (BETWEEN DAFTAR GAMBAR AND DAFTAR LAMPIRAN)
# Locate DAFTAR LAMPIRAN heading
p_daftar_lampiran = None
for p in doc.paragraphs:
    if p.text.strip() == "DAFTAR LAMPIRAN":
        p_daftar_lampiran = p
        break

assert p_daftar_lampiran is not None, "DAFTAR LAMPIRAN not found"

# Clean up empty paragraphs between DAFTAR GAMBAR and DAFTAR LAMPIRAN
# Find DAFTAR GAMBAR
p_daftar_gambar = None
for p in doc.paragraphs:
    if p.text.strip() == "DAFTAR GAMBAR":
        p_daftar_gambar = p
        break

# In p_daftar_gambar, find the caption paragraph right after it
el = p_daftar_gambar._element.getnext()
while el is not None and el != p_daftar_lampiran._element:
    next_el = el.getnext()
    txt = el.xpath('string(.)').strip()
    if not txt:
        body.remove(el)
    el = next_el

# Now insert DAFTAR TABEL heading and contents before DAFTAR LAMPIRAN
# Heading DAFTAR TABEL
p_dt_heading = p_daftar_lampiran.insert_paragraph_before()
p_dt_heading.style = 'Heading 1'
p_dt_heading.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_dt_heading.paragraph_format.space_before = Pt(12)
p_dt_heading.paragraph_format.space_after = Pt(12)
p_dt_heading.paragraph_format.page_break_before = True
r_dt = p_dt_heading.add_run("DAFTAR TABEL")
r_dt.font.name = "Times New Roman"
r_dt.font.size = Pt(14)
r_dt.font.bold = True
r_dt.font.color.rgb = RGBColor(0, 0, 0)

# Content of DAFTAR TABEL with dot leaders matching DAFTAR GAMBAR style
p_dt_content = p_daftar_lampiran.insert_paragraph_before()
p_dt_content.style = 'Caption'
p_dt_content.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
p_dt_content.paragraph_format.line_spacing = 1.5
p_dt_content.paragraph_format.space_after = Pt(6)

daftar_tabel_entries = [
    "Tabel II.1. Simbol Use Case Diagram…………………………………………………………",
    "Tabel II.2. Simbol Activity Diagram…………………………………………………………",
    "Tabel III.1. Spesifikasi Dokumen Masukan Sistem Berjalan……………………………",
    "Tabel III.2. Spesifikasi Dokumen Keluaran Sistem Berjalan……………………………",
    "Tabel III.3. Deskripsi Aktor Sistem Berjalan……………………………………………",
    "Tabel III.4. Deskripsi Use Case Sistem Berjalan………………………………………",
    "Tabel III.5. Skenario Aliran Kerja (Workflow) Sistem Berjalan………………………",
    "Tabel III.6. Deskripsi Aktor Sistem Usulan………………………………………………",
    "Tabel III.7. Deskripsi Use Case Sistem Usulan…………………………………………",
    "Tabel III.8. Skenario Aliran Kerja (Workflow) Sistem Usulan………………………"
]

content_text = "\n".join(daftar_tabel_entries)
r_cnt = p_dt_content.add_run(content_text)
r_cnt.font.name = "Times New Roman"
r_cnt.font.size = Pt(12)
r_cnt.font.color.rgb = RGBColor(0, 0, 0)

atomic_save_docx(doc, doc_path, backup=False)
print(f"SUCCESS: Document saved in-place to {doc_path}")

