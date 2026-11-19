"""Shared atomic Word (.docx) persistence boundary for generated & in-place edited manuscripts."""
import os
import shutil


def atomic_save_docx(doc, target_path, backup=False):
    """Save a python-docx Document via temporary file + atomic replace.

    Preserves the original file intact and raises an actionable PermissionError
    pointing to the staged `.tmp.docx` if Microsoft Word or an IDE viewer holds
    a Windows file lock on the target path.
    """
    out_abs = os.path.abspath(str(target_path))
    out_dir = os.path.dirname(out_abs)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    if backup and os.path.exists(out_abs):
        shutil.copy2(out_abs, out_abs + ".bak")

    tmp_path = out_abs + ".tmp.docx"
    try:
        doc.save(tmp_path)
    except Exception:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass
        raise

    try:
        os.replace(tmp_path, out_abs)
    except PermissionError as exc:
        raise PermissionError(
            f"[TERKUNCI] Tidak dapat memperbarui '{out_abs}' karena berkas sedang dibuka oleh Microsoft Word "
            f"atau dikunci viewer di Windows. Tutup berkas target terlebih dahulu lalu jalankan ulang, atau ambil "
            f"hasil sementara terbaru di: '{tmp_path}'."
        ) from exc
    return out_abs
