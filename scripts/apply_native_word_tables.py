# /// script
# requires-python = ">=3.10"
# dependencies = ["python-docx"]
# ///
import argparse
import os
import sys
import docx
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
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


def apply_word_table_format(table):
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = table._element.xpath("w:tblPr")[0]
    for b in tblPr.xpath("w:tblBorders"):
        tblPr.remove(b)
    borders_xml = (
        f'<w:tblBorders {nsdecls("w")}>'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        "</w:tblBorders>"
    )
    tblPr.append(parse_xml(borders_xml))

    for r_idx, row in enumerate(table.rows):
        trPr = row._tr.get_or_add_trPr()
        if not trPr.xpath("w:cantSplit"):
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if r_idx == 0 and not trPr.xpath("w:tblHeader"):
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        for cell in row.cells:
            tcPr = cell._element.get_or_add_tcPr()
            for shd in tcPr.xpath("w:shd"):
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
                    if r_idx == 0:
                        r.font.bold = True
                    r.font.color.rgb = RGBColor(0, 0, 0)


def format_docx_tables(target_path):
    doc = docx.Document(target_path)
    for table in doc.tables:
        apply_word_table_format(table)
    atomic_save_docx(doc, target_path, backup=False)
    return len(doc.tables)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format semua tabel .docx ke gaya bawaan Word Table Grid.")
    parser.add_argument("-i", "--input", required=True, help="Path file .docx target")
    args = parser.parse_args()
    n = format_docx_tables(args.input)
    print(f"SUKSES: {n} tabel diformat in-place di {args.input}")
