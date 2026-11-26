# Skill Khusus Agent: Jurnal Ilmiah SINTA 1-6 & Laporan PKL (Kepatuhan R1-R4 Mendeley, Anti-Revisi, Verifikasi DOI Crossref, & Anatomi OJS)

Aktifkan skill ini bersama [`mode-ilmiah.md`](mode-ilmiah.md) setiap kali pengguna meminta:
1. **Menulis, melanjutkan, memperbaiki, merangkum, atau mengonversi** file naskah Jurnal SINTA 1-6 atau Laporan PKL yang **sudah ada** (`.docx` maupun `.typ`).
2. **Mengaudit atau me-review** draf jurnal/laporan layaknya *Peer Reviewer* / Auditor Kepatuhan.
3. **Membuat template atau contoh naskah baru** Jurnal Ilmiah SINTA 1 s.d. SINTA 6 atau Laporan/Proposal PKL di folder `contoh-template-ai/`.

---

## Skenario 1: Mengerjakan / Melanjutkan / Merangkum Naskah Jurnal Pemilik (Aturan Sakral R1-R4 & Anti-Revisi)

Ketika pemilik memberikan file `.docx` target (misalnya `kerjaan jurnal\Template JKI.docx`) atau meminta penulisan jurnal dari topik/laporan PKL, **aturan R1 s.d. R4 di bawah ini adalah HUKUM TERTINGGI**:

1. **R1 - Referensi Itu Sakral, TIDAK Ditulis Agent ke Dalam Dokumen (`.docx`)**:
   - Agent **DILARANG KERAS** menulis bagian `DAFTAR PUSTAKA` / `REFERENSI` / `REFERENCES` beserta daftar entrinya ke dalam file `.docx`.
   - Referensi final di dalam `.docx` ditulis manusia sendiri menggunakan **Mendeley**.
   - Hasil riset referensi oleh agent **HANYA** boleh disimpan sebagai file kandidat `.txt` terpisah (lihat **R3**).
2. **R2 - Satu File Target (*Live In-Place Editing*)**:
   - Jika pemilik memberikan file `.docx` untuk dikerjakan, agent **WAJIB bekerja *live* langsung di file `.docx` itu** (`docx.Document("<file_user.docx>")` -> `doc.save("<file_user.docx>")`) agar Logo, Header, Footer, Tabel Info Artikel, Style, dan Margin asli template 100% terjaga.
   - **DILARANG KERAS** membuat file `.docx` baru (termasuk file per-bab seperti `..._Bab1.docx` atau file turunan PDF/PNG) tanpa izin eksplisit pemilik.
3. **R3 - File `.txt` / Dosir `.docx` Kandidat Referensi Terpisah Sesuai Level SINTA Target**:
   - Agent **WAJIB** membuat tepat **satu file `.txt` terpisah** (misal `kerjaan jurnal\kandidat_referensi_sinta5.txt`, serta dosir `.docx` terpisah berhyperlink DOI + PDF bila diminta pengguna).
   - Seluruh kandidat referensi wajib memenuhi **4 syarat mutlak**: (1) **100% artikel jurnal primer terbitan maksimal 5 tahun terakhir (`2022-2026`)**; (2) **DOI aktif terverifikasi HTTP 200 di Crossref (`https://api.crossref.org/works/...`)**; (3) **tautan Download PDF Langsung HTTP 200 (`Content-Type: application/pdf` atau header `%PDF-`)**; (4) minimal 15 referensi untuk SINTA 2-5 dan minimal 25 untuk SINTA 1.
   - **Prioritas Setara Level SINTA**: Utamakan referensi dari jurnal yang **level SINTA-nya SETARA dengan jurnal target** (contoh: target JKI adalah **SINTA 4** -> utamakan jurnal **SINTA 4** atau setara).
   - **Label Level SINTA Jujur**: Tiap entri di file `.txt` wajib diberi label level SINTA jurnal sumbernya (`[Peringkat: SINTA 4 - Terverifikasi SINTA Kemdiktisaintek]`); **jika levelnya tidak bisa diverifikasi secara pasti, wajib tulis `[Level SINTA: tidak terverifikasi]`, dilarang mengarang**.
   - Gunakan MCP tool **`sinta-garuda`** (`sinta_search_journals`, `sinta_lookup_journal`, `garuda_search_articles`, `sinta_find_verified_references`) atau script ter-bundle `<skill_dir>/scripts/sinta_garuda_mcp.py` dan `<skill_dir>/scripts/verify_sinta_refs.py` (`--source both --sinta <1..6> --check-live --txt-out ... --docx-out ...`) yang mencocokkan ISSN/judul langsung ke katalog lokal **16.617 jurnal SINTA 1-6**.
4. **R4 - Jurnal Bukan Laporan (Ringkas, Fokus ke Topik, Tidak Kepanjangan, & Data Valid Anti-Revisi)**:
   - **Ringkas & Fokus ke Topik**: Isi naskah jurnal harus ringkas dan langsung fokus pada permasalahan inti. Penelitian **DIRANGKUM secara analitis**, bukan disalin panjang (*copy-paste*) dari laporan PKL/skripsi. Patuhi anggaran kata jurnal (Pendahuluan 4-6 paragraf / 500-750 kata; Metode 3-5 paragraf / 400-650 kata tanpa definisi buku teks dasar; Hasil & Pembahasan 1.400-2.000 kata fokus pada bukti dan komparasi temuan; Kesimpulan 1-2 paragraf / 150-250 kata menjawab tujuan).
   - **Zero Halusinasi & Data Valid**: Jangan pernah mengarang angka statistik, jumlah responden, hasil pengujian, nomor pasal UU, atau putusan pengadilan. Gunakan hanya data valid yang terverifikasi; jika ada data empiris pemilik yang belum tersedia, tulis placeholder `[ISI DATA NYATA: ...]` agar tidak terkena revisi dosen/reviewer.
   - **Patuhi Gaya Selingkung & TOS Jurnal Tujuan**: Untuk **JKI (*Jurnal Khatulistiwa Informatika*, SINTA 4, LPPM UBSI, DOI prefix `10.31294/jki`)**, wajib gunakan struktur artikel jurnal, **layout 2 kolom**, **gaya sitasi IEEE (`[1]`, `[2]`)**, minimal **15 referensi** (di file `.txt`), dan target *similarity index* maksimal **20%**.

---

## Skenario 2: Standar Anatomi OJS, Anti-AI Slop, & Kepatuhan Etika Publikasi (ARJUNA & COPE)

1. **Larangan Mutlak Teks "AI Indeks" / Debug Banner di Badan Dokumen**:
   - **DILARANG KERAS** menuliskan teks indikator buatan AI seperti `| Peringkat: SINTA 4 | Layout: 2 Kolom (Terbagi 2)` di bagian atas badan halaman (`document.body`).
   - Identitas jurnal, `p-ISSN`, `e-ISSN`, Volume/Nomor/Tahun, dan tautan DOI resmi **WAJIB** ditempatkan di dalam **Word Header (`section.header`)** dan **Word Footer (`section.footer`)** menggunakan struktur OpenXML asli (`w:hdr` dan `w:ftr`), ditambah baris **Riwayat Artikel (*Article History: Received ...; Revised ...; Accepted ... | DOI: ...*)** di bawah afiliasi penulis serta lisensi **Creative Commons (`CC BY-SA 4.0`)** di footer.
2. **Superscript Asli pada Indeks Penulis & Afiliasi**:
   - Gunakan properti `run.font.superscript = True` (`w:vertAlign="superscript"`) untuk penomoran afiliasi penulis (`1*`, `2`) dan alamat email korespondensi (`*Corresponding Author` / `*Penulis Korespondensi`).
3. **Filter Anti-Slop Bahasa, *Burstiness*, & Tipografi (Integrasi GitHub `antislop-copywriting`)**:
   - **Dilarang keras** menggunakan karakter *em dash* (`\u2014`) di dalam naskah Word, Typst, maupun Markdown (`R-02`).
   - Hindari kalimat pembuka klise AI (*Di era revolusi industri 4.0 yang berkembang pesat saat ini...*, *tidak dapat dipungkiri*, *memainkan peran krusial*, *delve into*, *testament to*, *negative parallelism* berulang *"bukan hanya X, melainkan juga Y"*).
   - Variasikan panjang kalimat (kalimat tesis 7-12 kata diselingi kalimat analisis 22-32 kata agar simpangan baku panjang kalimat `>= 5.5` kata) dan pastikan lulus `<skill_dir>/scripts/check_antislop_academic.py`.

---

## Skenario 3: Membuat Template Kosong / Showcase Jurnal SINTA 1-6 (1-6 Instansi Berbeda)

Jika pengguna meminta pembuatan template contoh baru dari nol:
1. **Pilih Peringkat Jurnal SINTA (1-6 dari Instansi Berbeda beserta DOI Prefix Resmi)**:
   - **SINTA 1 (Informatika/AI) - IJAIN** (*International Journal of Advances in Intelligent Informatics*): **Universitas Ahmad Dahlan (UAD) Yogyakarta** (`p-ISSN 2442-6571`, `e-ISSN 2548-3161`, DOI Prefix: `10.26555/ijain`, Wajib **100% Bahasa Inggris**, Margin `2.5/2.5/2.0/2.0 cm`, Default: **2 Kolom**, Min. 25 Referensi).
   - **SINTA 1 (Hukum/Hukum Siber) - PJIH** (*PADJADJARAN Jurnal Ilmu Hukum*): **Fakultas Hukum Universitas Padjadjaran (Unpad) Bandung** (`p-ISSN 2442-9325`, `e-ISSN 2460-1543`, DOI Prefix: `10.22304/pjih`, Bahasa Indonesia/Inggris Akademik, Min. 25 Referensi).
   - **SINTA 2 - JTIIK** (*Jurnal Teknologi Informasi dan Ilmu Komputer*): **FILKOM Universitas Brawijaya (UB) Malang** (`p-ISSN 2355-7699`, `e-ISSN 2528-6579`, DOI Prefix: `10.25126/jtiik`, Margin `2.5/2.5/2.5/2.0 cm`, Default: **2 Kolom**, Min. 15 Referensi).
   - **SINTA 3 - JISKA** (*Jurnal Informatika Sunan Kalijaga*): **UIN Sunan Kalijaga Yogyakarta** (`p-ISSN 2527-5836`, `e-ISSN 2528-0074`, DOI Prefix: `10.14421/jiska`, Margin `3.0/2.5/2.5/2.0 cm`, Default: **2 Kolom**, Min. 15 Referensi).
   - **SINTA 4 - JKI** (*Jurnal Khatulistiwa Informatika*): **LPPM Universitas Bina Sarana Informatika (UBSI)** (`p-ISSN 2339-1928`, `e-ISSN 2579-633X`, DOI Prefix: `10.31294/jki`, Margin `2.5/2.5/2.5/2.0 cm`, Default: **2 Kolom**, Sitasi: **IEEE**, Min. 15 Referensi, Similarity <= 20%).
   - **SINTA 5 - TEKNOIF** (*Jurnal Teknologi Informasi dan Komputer*): **Institut Teknologi Padang (ITP)** (`p-ISSN 2338-2724`, `e-ISSN 2598-9197`, DOI Prefix: `10.21063/jtif`, Margin `3.0/2.5/3.0/2.5 cm`, Default: **2 Kolom**, Min. 12 Referensi).
   - **SINTA 6 - METIK** (*Jurnal Manajemen dan Teknik Informatika*): **LPPM STMIK Jayakarta / Universitas Mulia** (`p-ISSN 2580-1503`, `e-ISSN 2654-8135`, DOI Prefix: `10.47002/metik`, Margin `3.0/2.5/3.0/2.5 cm`, Default: **1 Kolom Penuh**, Min. 12 Referensi).
2. **Pilih Tata Letak Kolom Jurnal**: `2col` (Layout Terbagi 2), `1col` (1 Kolom Penuh), atau `default`.
3. **Pilih Gaya Sitasi**: **IEEE (`[1]`, `[2]`)** (Rekomendasi utama jurnal IT SINTA 1-6) atau **APA (`(Penulis, Tahun)`)**.

---

## Skenario 4: Perintah CLI Mandiri (Berfungsi dari Workspace Mana Saja)

Gunakan script ter-bundle di `<skill_dir>/scripts/` (atau di root repo ini):

```powershell
# 1. Inspeksi DNA Template / Dokumen Existing (WAJIB sebelum edit in-place):
$env:PYTHONIOENCODING="utf-8"; uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --inspect-docx "<file_existing.docx>"

# 2. Generate draf baru Mode Mendeley (Daftar Pustaka .docx bersih sesuai R1, ekspor kandidat ke .txt sesuai R3):
uv run "<skill_dir>/scripts/generate_sinta_journal_docx.py" --sinta 4 --layout 2col --citation ieee --mendeley-mode --output "Naskah_JKI.docx" --yes

# 3. Verifikasi antislop, Burstiness (>= 5.5), dan kepatuhan R1 sebelum serahkan ke user:
uv run "<skill_dir>/scripts/check_antislop_academic.py" --input "<file_existing.docx>" --mendeley-mode

# 4. Generate / Perbarui katalog contoh showcase di contoh-template-ai/ (hanya jika diminta user):
uv run generate_sinta_journal_docx.py --generate-showcase contoh-template-ai
typst compile --root . template/jurnal-sinta.typ contoh-template-ai/11_Jurnal_SINTA4_JKI_UBSI_Typst.pdf
```
