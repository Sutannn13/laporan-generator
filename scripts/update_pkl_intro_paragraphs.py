# /// script
# requires-python = ">=3.10"
# dependencies = ["python-docx"]
# ///
import argparse
import os
import sys
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

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

def format_intro_paragraph(p):
    p.style = "Normal"
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.first_line_indent = Cm(1.2)

def add_styled_run(p, text, italic=False, bold=False):
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.italic = italic
    r.font.bold = bold
    r.font.color.rgb = RGBColor(0, 0, 0)
    return r

# Target 1: Before 2.1.1. Definisi Sistem
# Heading 2.1 is: 2.1. Konsep Dasar Sistem dan Pengelolaan Informasi
p_target_211 = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "2.1.1. Definisi Sistem":
        p_target_211 = p
        break

if p_target_211:
    p_intro_21 = p_target_211.insert_paragraph_before()
    format_intro_paragraph(p_intro_21)
    add_styled_run(p_intro_21, "Konsep dasar sistem dan pengelolaan informasi merupakan landasan teoretis fundamental dalam menganalisis maupun merancang arsitektur sistem informasi pada suatu organisasi kedinasan. Pada sub-bab ini diuraikan landasan konseptual yang mencakup hakikat definisi, karakteristik, dan klasifikasi sistem, konsep dasar serta dimensi kualitas informasi, hingga tata kelola sistem informasi publikasi kehumasan pemerintah beserta kaidah penulisan siaran pers (")
    add_styled_run(p_intro_21, "press release", italic=True)
    add_styled_run(p_intro_21, ") yang memenuhi prinsip jurnalistik kedinasan.")
    print("Successfully inserted intro paragraph for 2.1")
else:
    print("ERROR: Target 2.1.1 not found!")

# Target 2: Before 2.2.1. Definisi dan Konsep Dasar UML
# Heading 2.2 is: 2.2. Unified Modelling Language (UML) dan Perancangan Perangkat Lunak Usulan
p_target_221 = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "2.2.1. Definisi dan Konsep Dasar UML":
        p_target_221 = p
        break

if p_target_221:
    p_intro_22 = p_target_221.insert_paragraph_before()
    format_intro_paragraph(p_intro_22)
    add_styled_run(p_intro_22, "Perancangan perangkat lunak usulan memerlukan metodologi pemodelan visual yang terstandarisasi untuk mengilustrasikan kebutuhan fungsional, alur kerja operasional, serta interaksi pengguna dengan sistem secara jelas dan terstruktur. Sub-bab ini menyajikan konsep dasar ")
    add_styled_run(p_intro_22, "Unified Modelling Language", italic=True)
    add_styled_run(p_intro_22, " (UML) beserta diagram pemodelan yang digunakan, khususnya ")
    add_styled_run(p_intro_22, "Use Case Diagram", italic=True)
    add_styled_run(p_intro_22, " dan ")
    add_styled_run(p_intro_22, "Activity Diagram", italic=True)
    add_styled_run(p_intro_22, ", serta teori pendukung mengenai arsitektur aplikasi berbasis web, prinsip desain antarmuka pengguna (")
    add_styled_run(p_intro_22, "User Interface/User Experience", italic=True)
    add_styled_run(p_intro_22, " atau UI/UX), dan pemanfaatan komputasi cerdas (")
    add_styled_run(p_intro_22, "Artificial Intelligence", italic=True)
    add_styled_run(p_intro_22, ") untuk optimalisasi validasi faktual dalam penyusunan naskah siaran pers kedinasan.")
    print("Successfully inserted intro paragraph for 2.2")
else:
    print("ERROR: Target 2.2.1 not found!")

# Target 3: Before 3.1.1. Sejarah Instansi
# Heading 3.1 is: 3.1. Tinjauan Institusi
p_target_311 = None
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "3.1.1. Sejarah Instansi":
        p_target_311 = p
        break

if p_target_311:
    p_intro_31 = p_target_311.insert_paragraph_before()
    format_intro_paragraph(p_intro_31)
    add_styled_run(p_intro_31, "Tinjauan institusi menyajikan gambaran umum mengenai profil dan lingkungan kerja tempat pelaksanaan Praktik Kerja Lapangan (PKL), yaitu Dinas Komunikasi dan Informatika Kota Contoh. Pembahasan pada sub-bab ini memaparkan latar belakang historis berdirinya instansi, visi dan misi yang melandasi seluruh program kerja pelayanan informasi dan komunikasi publik bagi masyarakat, serta bagan struktur organisasi institusi beserta penjabaran tugas pokok dan fungsi (tupoksi) Bidang Pengelolaan Informasi dan Komunikasi Publik (Humas) yang menjadi lokus penelitian.")
    print("Successfully inserted intro paragraph for 3.1")
else:
    print("ERROR: Target 3.1.1 not found!")

atomic_save_docx(doc, doc_path, backup=False)
print(f"Document saved in-place to: {doc_path}")

