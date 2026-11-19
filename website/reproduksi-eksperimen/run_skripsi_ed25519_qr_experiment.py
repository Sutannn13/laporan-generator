# /// script
# requires-python = ">=3.10"
# dependencies = ["cryptography", "qrcode[pil]"]
# ///
"""
Skrip Reproduksi Eksperimen Kriptografi Ed25519, Kode QR Versi 13, dan 10 Uji Black-Box
(Dokumen 2 - Sampel Skripsi TI UBSI Outline 156).
Cara uji: uv run website/reproduksi-eksperimen/run_skripsi_ed25519_qr_experiment.py
"""
import base64
import datetime
import hashlib
import json
import platform
import time
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
import qrcode

HERE = Path(__file__).resolve().parent


def b64u_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def b64u_decode(s: str) -> bytes:
    pad = "=" * ((4 - len(s) % 4) % 4)
    return base64.urlsafe_b64decode((s + pad).encode("ascii"))


def canonical_payload(doc_id: str, nim: str, sha256_hex: str, issued_date: str, status: str) -> bytes:
    obj = {
        "d": doc_id,
        "h": sha256_hex,
        "i": issued_date,
        "n": nim,
        "s": status,
    }
    return json.dumps(obj, separators=(",", ":"), sort_keys=True).encode("utf-8")


def sign_academic_pdf(priv_key: Ed25519PrivateKey, pdf_bytes: bytes, doc_id: str, nim: str, issued_date: str, status: str = "AKTIF"):
    if not pdf_bytes:
        raise ValueError("ERR_EMPTY_FILE")
    if not pdf_bytes.startswith(b"%PDF-"):
        raise ValueError("ERR_NOT_PDF")
    if len(pdf_bytes) > 5 * 1024 * 1024:
        raise ValueError("ERR_SIZE_EXCEEDED")
    digest_hex = hashlib.sha256(pdf_bytes).hexdigest()
    msg = canonical_payload(doc_id, nim, digest_hex, issued_date, status)
    sig = priv_key.sign(msg)
    token = b64u_encode(msg) + "." + b64u_encode(sig)
    return {"sha256": digest_hex, "sig_bytes": len(sig), "token": token, "token_len": len(token)}


def verify_academic_token(pub_key: Ed25519PublicKey, token: str, uploaded_pdf: bytes | None = None):
    if "." not in token:
        return {"valid": False, "code": "ERR_TOKEN_FORMAT"}
    part_msg, part_sig = token.split(".", 1)
    try:
        msg_bytes = b64u_decode(part_msg)
        sig_bytes = b64u_decode(part_sig)
        payload = json.loads(msg_bytes.decode("utf-8"))
    except Exception:
        return {"valid": False, "code": "ERR_BASE64_DECODE"}

    if len(sig_bytes) != 64:
        return {"valid": False, "code": "ERR_SIG_LENGTH"}

    try:
        pub_key.verify(sig_bytes, msg_bytes)
    except InvalidSignature:
        return {"valid": False, "code": "ERR_INVALID_SIGNATURE"}

    if payload.get("s") != "AKTIF":
        return {"valid": False, "code": "ERR_DOC_REVOKED"}

    if uploaded_pdf is not None:
        actual_hash = hashlib.sha256(uploaded_pdf).hexdigest()
        if actual_hash != payload.get("h"):
            return {"valid": False, "code": "ERR_HASH_MISMATCH"}

    return {"valid": True, "code": "VALID_AUTHENTIC", "payload": payload}


def main():
    # 1. RFC 8032 Section 7.1 Test Vector 1 deterministic verification
    rfc_sk_hex = "9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60"
    rfc_pk_expected = "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a"
    rfc_sig_expected = (
        "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e06522490155"
        "5fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b"
    )
    sk_tv1 = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(rfc_sk_hex))
    pk_tv1_bytes = sk_tv1.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    sig_tv1_bytes = sk_tv1.sign(b"")
    rfc8032_pass = (pk_tv1_bytes.hex() == rfc_pk_expected) and (sig_tv1_bytes.hex() == rfc_sig_expected)

    # 2. Sample Academic Document Signing & QR Version 13 Generation
    sample_seed = hashlib.sha256(b"Kunci-Sampel-Akademik-Perguruan-Tinggi-Contoh-2026").digest()
    priv_a = Ed25519PrivateKey.from_private_bytes(sample_seed)
    pub_a = priv_a.public_key()
    pub_a_raw = pub_a.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)

    other_priv = Ed25519PrivateKey.from_private_bytes(hashlib.sha256(b"Kunci-Tidak-Sah").digest())
    other_pub = other_priv.public_key()

    sample_pdf_bytes = (
        b"%PDF-1.4\n% Dokumen Sampel Surat Keterangan Aktif Kuliah\n"
        b"1 0 obj << /Type /Catalog /Author (Penulis Contoh) /NIM (00000001) >> endobj\n%%EOF\n"
    )

    t0 = time.perf_counter()
    n_iter = 1000
    signed = None
    for _ in range(n_iter):
        signed = sign_academic_pdf(priv_a, sample_pdf_bytes, "SKAK-2026-0001", "00000001", "2026-11-18", "AKTIF")
    sign_avg_ms = round(((time.perf_counter() - t0) * 1000.0) / n_iter, 4)

    t1 = time.perf_counter()
    for _ in range(n_iter):
        verify_academic_token(pub_a, signed["token"], sample_pdf_bytes)
    verify_avg_ms = round(((time.perf_counter() - t1) * 1000.0) / n_iter, 4)

    qr_url = f"https://verifikasi.contoh.ac.id/v?t={signed['token']}"
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=3)
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#0f172a", back_color="#ffffff")
    qr_img.save(str(HERE / "qr_ed25519_sample.png"))

    # 3. 10 Black-Box Equivalence Partitioning Test Cases
    tampered_pdf = sample_pdf_bytes.replace(b"00000001", b"00000009")
    p_msg, p_sig = signed["token"].split(".", 1)
    raw_sig = bytearray(b64u_decode(p_sig))
    raw_sig[0] ^= 0x01
    forged_sig_token = p_msg + "." + b64u_encode(bytes(raw_sig))
    revoked_signed = sign_academic_pdf(priv_a, sample_pdf_bytes, "SKAK-2026-0002", "00000001", "2026-11-18", "DICABUT")

    bb_cases = []

    def rec(tc_id, partition, scenario, expected, actual_code, passed):
        bb_cases.append(
            {
                "id": tc_id,
                "partition": partition,
                "scenario": scenario,
                "expected": expected,
                "actual": actual_code,
                "status": "Valid (Sesuai)" if passed else "Gagal",
            }
        )

    rec("TC-01", "Kelas Masukan Sah", "Unggah PDF sah (%PDF-1.4, 146 byte) dan terbitkan token Ed25519", "Token terbentuk (tanda tangan 64 byte)", f"Token {signed['token_len']} karakter (sig {signed['sig_bytes']} byte)", signed["sig_bytes"] == 64)
    r2 = verify_academic_token(pub_a, signed["token"], sample_pdf_bytes)
    rec("TC-02", "Kelas Masukan Sah", "Verifikasi token QR sah beserta berkas PDF asli tanpa perubahan", "VALID_AUTHENTIC", r2["code"], r2["valid"] and r2["code"] == "VALID_AUTHENTIC")
    r3 = verify_academic_token(pub_a, signed["token"], None)
    rec("TC-03", "Kelas Masukan Sah", "Pindai kode QR tanpa unggah ulang berkas PDF", "VALID_AUTHENTIC", r3["code"], r3["valid"] and r3["code"] == "VALID_AUTHENTIC")
    r4 = verify_academic_token(pub_a, signed["token"], tampered_pdf)
    rec("TC-04", "Kelas Tidak Sah (Integritas)", "Ubah 1 digit NIM pada berkas PDF lalu uji terhadap token QR asli", "ERR_HASH_MISMATCH", r4["code"], (not r4["valid"]) and r4["code"] == "ERR_HASH_MISMATCH")
    r5 = verify_academic_token(pub_a, forged_sig_token, sample_pdf_bytes)
    rec("TC-05", "Kelas Tidak Sah (Kriptografi)", "Balik 1 bit pada komponen tanda tangan Ed25519 di dalam token", "ERR_INVALID_SIGNATURE", r5["code"], (not r5["valid"]) and r5["code"] == "ERR_INVALID_SIGNATURE")
    r6 = verify_academic_token(other_pub, signed["token"], sample_pdf_bytes)
    rec("TC-06", "Kelas Tidak Sah (Otorisasi)", "Verifikasi token menggunakan kunci publik penanda tangan lain", "ERR_INVALID_SIGNATURE", r6["code"], (not r6["valid"]) and r6["code"] == "ERR_INVALID_SIGNATURE")
    r7 = verify_academic_token(pub_a, revoked_signed["token"], sample_pdf_bytes)
    rec("TC-07", "Kelas Tidak Sah (Status)", "Verifikasi token dokumen berstatus DICABUT", "ERR_DOC_REVOKED", r7["code"], (not r7["valid"]) and r7["code"] == "ERR_DOC_REVOKED")
    r8 = verify_academic_token(pub_a, "token_tanpa_titik_pemisah", None)
    rec("TC-08", "Kelas Tidak Sah (Format)", "Masukan string QR rusak tanpa pemisah titik", "ERR_TOKEN_FORMAT", r8["code"], (not r8["valid"]) and r8["code"] == "ERR_TOKEN_FORMAT")
    try:
        sign_academic_pdf(priv_a, b"", "SKAK-00", "00000001", "2026-11-18")
        c9 = "NO_ERROR"
    except ValueError as e:
        c9 = str(e)
    rec("TC-09", "Kelas Batas Kosong", "Unggah berkas 0 byte pada form penerbitan dokumen", "ERR_EMPTY_FILE", c9, c9 == "ERR_EMPTY_FILE")
    try:
        sign_academic_pdf(priv_a, b"PK\x03\x04bukan_berkas_pdf", "SKAK-00", "00000001", "2026-11-18")
        c10 = "NO_ERROR"
    except ValueError as e:
        c10 = str(e)
    rec("TC-10", "Kelas Format Berkas", "Unggah berkas non-PDF (header ZIP/DOCX) ke modul penandatanganan PDF", "ERR_NOT_PDF", c10, c10 == "ERR_NOT_PDF")

    out_metrics = {
        "timestamp_iso": datetime.datetime.now().isoformat(),
        "python_version": platform.python_version(),
        "os_platform": f"{platform.system()} {platform.release()}",
        "rfc8032_tv1_verified": rfc8032_pass,
        "public_key_bytes": len(pub_a_raw),
        "signature_bytes": signed["sig_bytes"],
        "sha256_hex_len": len(signed["sha256"]),
        "sample_sha256": signed["sha256"],
        "token_char_len": signed["token_len"],
        "qr_url_char_len": len(qr_url),
        "qr_version": qr.version,
        "qr_modules_per_side": qr.modules_count,
        "sign_avg_ms_1000_runs": sign_avg_ms,
        "verify_avg_ms_1000_runs": verify_avg_ms,
        "blackbox_total": len(bb_cases),
        "blackbox_passed": sum(1 for c in bb_cases if c["status"].startswith("Valid")),
        "blackbox_cases": bb_cases,
    }
    (HERE / "skripsi_ed25519_metrics.json").write_text(json.dumps(out_metrics, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(out_metrics, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
