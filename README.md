# Template Typst PKL UBSI (Teknologi Informasi)

Template penulisan naskah Proposal dan Laporan Praktik Kerja Lapangan (PKL) berbasis [Typst](https://typst.app) untuk Program Studi **Teknologi Informasi (S1)**, Fakultas Teknik & Informatika, Universitas Bina Sarana Informatika.

Implementasi tata letak dan tipografi mengacu secara ketat pada **Buku Pedoman Praktik Kerja Lapangan (PKL) UBSI Tahun 2026**.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Typst](https://img.shields.io/badge/Typst-0.15%2B-orange.svg)](https://typst.app)
[![Format: Pedoman UBSI](https://img.shields.io/badge/Format-Pedoman%20UBSI%202026-green.svg)](https://bsi.ac.id)

---

## Spesifikasi Format Dokumen

Format dokumen dikonfigurasi secara baku pada pustaka layout (`lib.typ`):

| Parameter | Ketentuan Pedoman UBSI (Bab II) | Konfigurasi Template |
| :--- | :--- | :--- |
| **Ukuran Kertas** | A4 (Poin 2.1.1) | `paper: "a4"` |
| **Batas Margin** | Kiri 4 cm, Atas 3 cm, Kanan 2.5 cm, Bawah 2.5 cm (Poin 2.1.2) | `margin: (left: 4cm, top: 3cm, right: 2.5cm, bottom: 2.5cm)` |
| **Jenis & Ukuran Font** | Times New Roman, 12pt (Poin 2.1.4) | `font: "Times New Roman", size: 12pt` |
| **Spasi Teks** | Spasi 2 pada isi bab (Poin 2.1.3); Spasi 1.5 pada bagian awal | `leading: 12pt` (Isi Bab); `leading: 9pt` (Bagian Awal) |
| **Alinea Baru** | Menjorok 1.2 cm (5-7 ketukan) | `first-line-indent: 1.2cm` |
| **Perataan Teks** | Rata Kanan-Kiri (*Justified*) | `justify: true` |
| **Penomoran Bab & Sub-bab** | Bab: Romawi kapital; Sub-bab: Latin berakhiran titik (Poin 2.3) | `BAB I`, `1.1.`, `1.1.1.` |
| **Penomoran Halaman** | Awal: Romawi kecil bawah-tengah (Poin 2.4.1)<br>Pokok: Awal bab bawah-tengah, lanjutan kanan-atas (Poin 2.4.2)<br>Akhir: Angka latin bawah-tengah (Poin 2.4.3) | Terintegrasi otomatis melalui query posisi bab |
| **Tabel & Gambar** | Judul tabel di atas tengah; Judul gambar di bawah tengah (Poin 2.5) | Penomoran romawi bab (`Gambar III.1`, `Tabel IV.1`) |
| **Sitasi & Pustaka** | Standar Mendeley APA Style V.7 (SK Rektor UBSI 2026) | `style: "apa"`, pustaka spasi 1, jarak antar pustaka 2 spasi |

---

## Cakupan Outline Program Studi Teknologi Informasi

### A. Outline Praktik Kerja Lapangan (PKL)
Disediakan draf bab sesuai 4 outline resmi peminatan TI S1 serta Proposal PKL:

1. **Proposal PKL** (3 Bab):
   - Bab I Pendahuluan
   - Bab II Tempat dan Waktu PKL
   - Bab III Penutup
2. **Laporan PKL - Proyek Inovasi Perangkat Lunak** (6 Bab):
   - Bab I Latar Belakang Ide Aplikasi
   - Bab II Analisis Masalah
   - Bab III Solusi Inovasi
   - Bab IV Tujuan dan Manfaat Aplikasi
   - Bab V Metode Pengembangan Perangkat Lunak
   - Bab VI Penutup
3. **Laporan PKL - Analisa Program Berbasis Mobile** (4 Bab):
   - Bab I Pendahuluan
   - Bab II Landasan Teori
   - Bab III Pembahasan (Flowchart, HIPO, Analisis Program)
   - Bab IV Penutup
4. **Laporan PKL - Jaringan Komputer** (4 Bab):
   - Bab I Pendahuluan
   - Bab II Landasan Teori
   - Bab III Pembahasan (Topologi, IP Address, Hardware/Software, Analisis)
   - Bab IV Penutup
5. **Laporan PKL - Analisis Sistem** (4 Bab):
   - Bab I Pendahuluan
   - Bab II Landasan Teori
   - Bab III Pembahasan (Dokumen/File/Kode/Program Berjalan, UML)
   - Bab IV Penutup

### B. Outline Skripsi Program Sarjana (S1)
1. **Skripsi - Kode 156: Perancangan Program Science** (5 Bab):
   - Bab I Pendahuluan (Latar Belakang, Identifikasi Permasalahan, Perumusan Masalah, Maksud dan Tujuan, Metode Penelitian, Ruang Lingkup)
   - Bab II Landasan Teori (Tinjauan Pustaka, UML, Penelitian Terkait Min. 5 Jurnal)
   - Bab III Analisis dan Perancangan Aplikasi (Tinjauan Perusahaan, Analisis Masalah/Kebutuhan, Rancangan Algoritma)
   - Bab IV Implementasi dan Pengujian Software (Desain Basis Data, Software Architecture/Pseudocode, UI, Code Generation, Testing, Support/Publikasi)
   - Bab V Penutup (Kesimpulan, Saran Manajerial, Sistem & Penelitian Lanjutan)
2. **Skripsi - Kode 138: Penelitian Ilmiah** (5 Bab):
   - Bab I Pendahuluan (Latar Belakang, Identifikasi Permasalahan, Perumusan Masalah, Maksud dan Tujuan, Metode Penelitian, Ruang Lingkup, Hipotesis)
   - Bab II Landasan Teori (Tinjauan Pustaka, Penelitian Terkait Min. 5 Jurnal, Tinjauan Organisasi/Objek Penelitian)
   - Bab III Metodologi Penelitian (Tahapan Penelitian, Instrumen Penelitian, Metode Pengumpulan Data/Populasi/Sampel, Metode Analisis Data)
   - Bab IV Hasil Penelitian dan Pembahasan (Deskripsi Dataset, Implementasi Metode/Perhitungan, Hasil Uji Hipotesis, Pembahasan Komparatif)
   - Bab V Penutup (Kesimpulan, Saran Manajerial, Sistem/Teknis & Penelitian Lanjutan)
3. **Skripsi - Kode 137: Jaringan Komputer** (5 Bab):
   - Bab I Pendahuluan (Latar Belakang, Identifikasi Permasalahan, Perumusan Masalah, Tujuan dan Manfaat, Metode Penelitian NDLC, Ruang Lingkup)
   - Bab II Landasan Teori (Tinjauan Pustaka, OSI/TCP-IP, Routing, QoS, Firewall/VPN, Penelitian Terkait Min. 5 Jurnal)
   - Bab III Analisis Jaringan Berjalan (Tinjauan Perusahaan, Skema Jaringan Berjalan Simulator, Keamanan, Spesifikasi Hardware/Software, Permasalahan, Alternatif Pemecahan)
   - Bab IV Rancangan Jaringan Usulan (Topologi & Skema Usulan Simulator, Keamanan, Layanan Jaringan, QoS/Queue Tree, Pengujian Jaringan Awal & Akhir)
   - Bab V Penutup (Kesimpulan, Saran Manajerial, Sistem & Penelitian Lanjutan)
4. **Skripsi - Kode 158: Aplikasi StartUp** (4 Bab - Kelompok Maksimal 2 Mahasiswa):
   - Bab I Pendahuluan (Latar Belakang Masalah 4 Konten, Identifikasi Masalah, Perumusan Masalah, Tujuan dan Manfaat, Metode RUP, Ruang Lingkup)
   - Bab II Landasan Teori (Konsep Dasar Aplikasi, Algoritma, BMC 9 Blok, Penelitian Terkait Min. 5 Jurnal, Pengujian & Peralatan Pendukung)
   - Bab III Analisis dan Perancangan Aplikasi (Matriks BMC 9 Blok, Analisis Kebutuhan, Use Case/Activity, UI Mockup, Basis Data ERD/LRS, Bukti Rilis Play Store, Spesifikasi Hardware/Software, Pengujian Blackbox, Uraian Tugas Tim)
   - Bab IV Penutup (Kesimpulan, Saran Manajerial/Bisnis, Sistem & Penelitian Lanjutan)

---

## Struktur Direktori Proyek (Workspace Map untuk User, AI Agent, & CLI)

```text
project-laporan-ai/
├── .agents/                          # Kustomisasi AI Agent (1 Skill Terpadu laporan-generator & Always-on Rule)
│   ├── rules/sinta-journal-prompt.md # Protokol wajib SINTA 1-6, OJS, DOI Crossref, & Anti-Slop
│   └── skills/laporan-generator/     # 1 Skill Terpadu (SKILL.md, references/, scripts/, presets/, humanizer_id/, data/)
├── bin/
│   └── cli.js                        # Interactive CLI Scaffolder (npx create-templatebsi)
├── contoh-template-ai/               # Katalog hasil jadi Jurnal SINTA 1-6 (.docx/.pdf) & Laporan PKL
│   ├── 00_Jurnal_SINTA1_HukumSiber_APK_KUHP_Baru_PJIH_Unpad.docx
│   ├── 01_Jurnal_SINTA1_IJAIN_UAD_2Kolom.docx
│   ├── 02_Jurnal_SINTA2_JTIIK_UB_2Kolom.docx
│   ├── 03_Jurnal_SINTA3_JISKA_UIN_2Kolom.docx
│   ├── 04_Jurnal_SINTA4_JKI_UBSI_2Kolom.docx
│   ├── 05_Jurnal_SINTA4_JKI_UBSI_1Kolom_Biasa.docx
│   ├── 06_Jurnal_SINTA5_TEKNOIF_ITP_2Kolom.docx
│   ├── 07_Jurnal_SINTA6_METIK_Jayakarta_1Kolom_Biasa.docx
│   ├── 08_Jurnal_SINTA6_METIK_Jayakarta_2Kolom.docx
│   ├── 09_Laporan_PKL_UBSI_Analisis_Sistem.docx
│   ├── 10_Laporan_PKL_UBSI_Analisis_Sistem.pdf
│   ├── 11_Jurnal_SINTA4_JKI_UBSI_Typst.pdf
│   └── README.md
├── presets/
│   ├── sinta-catalog.json.gz         # Katalog 16.617 jurnal terakreditasi SINTA 1-6
│   └── sinta-journals.json           # Spesifikasi OJS, ISSN, DOI Prefix, & Layout Jurnal SINTA 1-6
├── scripts/                          # Seluruh modul data, generator diagram, & automated test suite
│   ├── generate_diagrams.py          # Generator diagram arsitektur & UML 300 DPI (ke template/gambar/)
│   ├── install_agent_skills.py       # Installer skill mandiri ke Antigravity, OpenCode, Freebuff, Claude, Cursor, KiloCode
│   ├── sinta_content_data.py         # Database sitasi DOI Crossref terverifikasi & isi naskah SINTA 1-6
│   ├── test.js                       # Unit test Node.js CLI & Typst (PKL, Proposal, Skripsi, Jurnal SINTA)
│   ├── test_sinta.py                 # Audit otomatis XML Word, Header/Footer OJS, DOI, & Anti-Slop
│   └── update_docx_script.py         # Scaffolder & editor in-place Laporan PKL / Skripsi Word (.docx)
├── template/                         # Template Typst (.typ) & aset gambar diagram
│   ├── gambar/                       # Seluruh diagram 300 DPI (.png) & aset visual
│   ├── bagian-awal/                  # Pengesahan, Persetujuan, Hak Cipta, Konsultasi, Persembahan, Abstraksi, Kata Pengantar, Daftar Isi/Simbol/Gambar/Tabel/Lampiran
│   ├── bagian-akhir/                 # Riwayat Hidup, Bukti Plagiarisme, Surat Keterangan, Nilai, Kuesioner, Lampiran
│   ├── outlines/                     # Draf bab per outline peminatan S1 Teknologi Informasi:
│   │   ├── proposal/                 # Bab 1 s.d. Bab 3 Proposal PKL
│   │   ├── pkl-ti-inovasi/           # PKL Outline 1: Proyek Inovasi Perangkat Lunak (6 Bab)
│   │   ├── pkl-ti-mobile/            # PKL Outline 2: Analisa Program Mobile (4 Bab)
│   │   ├── pkl-ti-jaringan/          # PKL Outline 3: Jaringan Komputer (4 Bab)
│   │   ├── pkl-ti-analisis-sistem/   # PKL Outline 4: Analisis Sistem (4 Bab)
│   │   ├── skripsi-ti-156/           # Skripsi Outline 156: Perancangan Program Science (5 Bab)
│   │   ├── skripsi-ti-138/           # Skripsi Outline 138: Penelitian Ilmiah (5 Bab)
│   │   ├── skripsi-ti-137/           # Skripsi Outline 137: Jaringan Komputer (5 Bab)
│   │   └── skripsi-ti-158/           # Skripsi Outline 158: Aplikasi StartUp (4 Bab)
│   ├── jurnal-sinta.typ              # Entrypoint Typst Jurnal SINTA 1-6
│   ├── main.typ                      # Entrypoint Typst Laporan PKL
│   ├── metadata.typ                  # Konfigurasi identitas penulis (1-2 orang), dosen PA, penguji, pembimbing, & switch catatan
│   ├── proposal.typ                  # Entrypoint Typst Proposal PKL (3 Bab)
│   └── skripsi.typ                   # Entrypoint resmi Skripsi Sarjana (S1)
├── website/                          # Halaman dokumentasi & galeri spesimen interaktif (Vite + React)
├── generate_sinta_journal_docx.py    # CLI utama Generator & Inspector Jurnal SINTA 1-6 (.docx)
├── lib.typ                           # Engine format baku Pedoman PKL & Skripsi UBSI 2026
├── sinta.typ                         # Engine format baku Jurnal Ilmiah SINTA 1-6 (2 Kolom & 1 Kolom)
├── package.json                      # NPM scripts terpadu untuk User, AI Agent, & CI
└── typst.toml                        # Manifes paket Typst
```

---

## Pintasan Perintah Cepat (Untuk User & AI Agent)

Seluruh workflow utama dapat dijalankan langsung melalui `npm run` maupun `uv run`:

```powershell
# 1. Pasang Skill & Slash Commands ke Antigravity, OpenCode, Freebuff, Claude Code, Cursor, & KiloCode:
npm run agent:install

# 2. Jalankan Generator Interaktif Jurnal SINTA 1-6 (Word .docx):
npm run sinta

# 3. Buat Jurnal SINTA 1 Topik "Unauthorized Access APK Berbahaya & KUHP Baru":
uv run generate_sinta_journal_docx.py --sinta 1 --layout 2col --citation ieee --topic apk-kuhp --yes

# 4. Inspeksi struktur / template .docx dari jurnal kampus lain atau draf yang sedang dibangun:
npm run sinta:inspect -- "nama_file_jurnal.docx"

# 5. Generate ulang seluruh 12 contoh file di folder contoh-template-ai/:
npm run sinta:showcase

# 6. Generate ulang seluruh diagram 300 DPI ke template/gambar/:
npm run diagrams

# 7. Jalankan seluruh pengujian otomatis (Typst PKL/Skripsi/SINTA + Audit OpenXML SINTA 1-6):
npm run test:all
```

---

## Panduan Penggunaan (How to Use)

### 1. Cara Memulai Proyek

Pilih salah satu metode kerja yang paling nyaman untuk Anda:

#### Opsi A: Menggunakan CLI Scaffolder (Paling Praktis)
Perintah ini akan membuat folder kerja mandiri yang hanya memuat outline pilihan Anda (tanpa folder outline lain):
```bash
# Mode Interaktif:
npx -y --allow-git=all github:Sutannn13/laporan-generator <nama-folder-proyek>

# Mode Otomatis / Non-interaktif:
npx -y --allow-git=all github:Sutannn13/laporan-generator my-laporan --type laporan --outline 1 --yes
npx -y --allow-git=all github:Sutannn13/laporan-generator my-proposal --type proposal --yes

# Di dalam folder yang sudah ada / folder aktif (.):
npx -y --allow-git=all github:Sutannn13/laporan-generator . --force
```

#### Pemasangan 1 Skill AI Agent Tanpa Clone & Scaffolder Word (.docx) SK Rektor UBSI 2026
Pasang **1 skill terpadu (`laporan-generator`)** yang sudah mencakup modul `mode-ilmiah`, `jurnal-sinta`, `humanizer-id` preset UBSI 2026, serta seluruh skrip OpenXML & katalog 16.617 jurnal SINTA ke Antigravity, Claude Code, Cursor, OpenCode, Freebuff, dan KiloCode **tanpa perlu `git clone`**:
```powershell
# Rekomendasi utama (banner LAPORAN GENERATOR + pasang 1 skill terpadu, 5 slash command, aturan scoped, & cek runtime uv; kompatibel npm 12+):
npx -y --allow-git=all github:Sutannn13/laporan-generator install

# Utilitas opsional: cek status runtime atau pasang skill saja via skills.sh:
npx -y --allow-git=all github:Sutannn13/laporan-generator status
npx skills add Sutannn13/laporan-generator

# Buat kerangka Word (.docx) Skripsi / TA / PKL UBSI 2026:
uv run scripts/update_docx_script.py --scaffold --type skripsi --outline 156 --title "JUDUL SKRIPSI" --author "Penulis Contoh" --nim "00000001" --output "Skripsi_UBSI.docx"
```

*(Opsional - Live Preview di IDE): Extension `.docx` (`cweijan.vscode-office`) dan `.pdf` (`tomoki1207.pdf`) direkomendasikan di `.vscode/extensions.json` untuk memantau perubahan dokumen secara langsung di tab IDE. Saat agent menulis ke file `.docx` via `atomic_save_docx()`, pastikan file tersebut sedang tidak terbuka di aplikasi Microsoft Word desktop agar Windows tidak mengunci berkas (`PermissionError`); untuk tampilan cetak final 2 kolom, header/footer OJS, dan watermark tetap cek lewat Microsoft Word atau ekspor PDF.)*

CLI mendukung opsi flag berikut:
- `-t, --type <proposal|laporan|skripsi>` : Memilih jenis dokumen (proposal 3 bab, laporan PKL, atau skripsi sarjana).
- `-o, --outline <1|2|3|4|156|138|137|158>` : Memilih outline naskah (PKL: 1-4; Skripsi: 156 untuk Perancangan Program Science, 138 untuk Penelitian Ilmiah, 137 untuk Jaringan Komputer, 158 untuk Aplikasi StartUp).
- `-y, --yes` : Menggunakan seluruh konfigurasi default tanpa prompt interaktif.
- `-f, --force` : Mengizinkan inisialisasi pada direktori yang sudah ada atau menimpa berkas proyek yang konflik.
- `-h, --help` : Menampilkan petunjuk opsi CLI.

#### Opsi B: Menggunakan Visual Studio Code (Lokal)
1. Pasang ekstensi **Tinymist Typst** (`myriad-dreamin.tinymist`) di VS Code.
2. Buka folder repositori ini di VS Code.
3. Buka berkas `template/main.typ` (untuk Laporan Akhir) atau `template/proposal.typ` (untuk Proposal).
4. Klik tombol ikon **Preview** Tinymist di pojok kanan atas editor (atau gunakan pintasan `Ctrl + K, V`) untuk melihat pratinjau dokumen langsung secara *real-time*.

#### Opsi C: Menggunakan Web Editor Typst (typst.app)
1. Unduh repositori ini dalam bentuk berkas ZIP.
2. Buka akun Anda di [typst.app](https://typst.app), klik **Create Project**, lalu pilih **Upload from ZIP**.
3. Buka berkas `template/main.typ` atau `template/proposal.typ`.

---

### 2. Langkah-Langkah Penulisan Naskah

#### Langkah 1: Mengisi Identitas pada `template/metadata.typ`
Buka berkas `template/metadata.typ` dan lengkapi data Anda:
```typst
#let judul = "SISTEM PEMANTAUAN INFRASTRUKTUR JARINGAN..."
#let penulis = "Nama Mahasiswa"
#let nim = "12200001"
#let kelas = "7A.01"
#let dosen-pa = "Nama Dosen Penasehat Akademik, M.Kom"
#let nama-instansi = "PT. Telekomunikasi Indonesia Prima"
#let divisi-instansi = "Divisi Information Technology & Infrastructure"
#let tanggal-mulai-pkl = "1 Agustus 2026"
#let tanggal-selesai-pkl = "31 Oktober 2026"

// Konfigurasi Kampus (Sesuai Lampiran 1 & 2):
// true  = Kampus Utama (mencantumkan Kota pada cover dan persetujuan)
// false = PSDKU / Luar Kampus Utama (tanpa Kota)
#let is-kampus-utama = true

// Master Switch Catatan Petunjuk Pedoman:
// true  = Menampilkan catatan petunjuk pedoman kampus (disertai peringatan wajib dihapus)
// false = Otomatis menyembunyikan SELURUH catatan petunjuk pedoman saat dijilid/dicetak
#let tampilkan-catatan-pedoman = true
```

#### Langkah 2: Memilih / Mengganti Outline Laporan
Secara default, berkas `template/main.typ` memuat **Outline 1: Proyek Inovasi Perangkat Lunak (6 Bab)**. Jika Anda mengerjakan topik peminatan lain, cukup sesuaikan baris `#include` pada `template/main.typ`:

- **Jaringan Komputer (4 Bab):**
  ```typst
  #include "outlines/pkl-ti-jaringan/bab1.typ"
  #include "outlines/pkl-ti-jaringan/bab2.typ"
  #include "outlines/pkl-ti-jaringan/bab3.typ"
  #include "outlines/pkl-ti-jaringan/bab4.typ"
  ```
- **Program Berbasis Mobile (4 Bab):**
  Ganti dengan folder `outlines/pkl-ti-mobile/bab1.typ` s.d. `bab4.typ`.
- **Analisis Sistem (4 Bab):**
  Ganti dengan folder `outlines/pkl-ti-analisis-sistem/bab1.typ` s.d. `bab4.typ`.

*(Jika Anda menulis Proposal PKL, gunakan langsung `template/proposal.typ` yang memuat 3 Bab resmi).*

#### Langkah 3: Menulis Isi Bab & Fitur Format Baku
Tulis konten naskah Anda pada berkas bab masing-masing. Seluruh format baku Pedoman UBSI sudah diatur otomatis:

- **Heading & Sub-bab (Gambar 2):**
  ```typst
  = Latar Belakang Masalah   // Otomatis tercetak: BAB I \ (2 spasi) \ LATAR BELAKANG MASALAH
  == Kondisi Sistem Berjalan // Otomatis tercetak: 1.1. Kondisi Sistem Berjalan (12pt Bold Rata Kiri)
  === Analisis Kebutuhan     // Otomatis tercetak: 1.1.1. Analisis Kebutuhan (12pt Bold Rata Kiri)
  ```
- **Menyisipkan Gambar (Lampiran 21):**
  ```typst
  #figure(
    image("../gambar/topologi.png", width: 80%),
    caption: [Topologi Jaringan Usulan],
  )
  ```
  *Caption otomatis diformat 2 baris terpusat (`Gambar III.1.` di baris atas dan judul gambar di baris bawah), serta otomatis masuk ke Daftar Gambar dengan nomor urut (`1. Gambar III.1. Topologi Jaringan Usulan ......... 28`).*

- **Menyisipkan Tabel (Lampiran 22):**
  ```typst
  #figure(
    table(
      columns: (1fr, 2fr),
      [*Komponen Perangkat*], [*Spesifikasi Teknis*],
      [Komputer Server], [Intel Xeon 3.2GHz, RAM 32GB],
      [Switch Managed], [Cisco Catalyst 2960 24-Port],
    ),
    caption: [Spesifikasi Perangkat Jaringan],
  )
  ```
  *Isi tabel otomatis berukuran font 10pt dan spasi 1, judul tabel berada di atas, serta otomatis masuk ke Daftar Tabel.*

- **Kutipan Langsung Panjang ($\ge$ 5 Baris) – Poin 2.6.7:**
  ```typst
  #kutipan-panjang(sumber: "Pressman, 2014, hal. 45")[
    Rekayasa perangkat lunak adalah penerapan pendekatan yang sistematis, disiplin, dan terukur terhadap pengembangan, pengoperasian, dan pemeliharaan perangkat lunak, yaitu penerapan rekayasa terhadap perangkat lunak.
  ]
  ```
  *Otomatis diketik dengan spasi 1, teks menjorok 1.2 cm, dan tanpa tanda petik sesuai pedoman.*

- **Sitasi & Daftar Pustaka (APA 6th Edition) – Poin 2.6 & 2.7:**
  - Tambahkan pustaka buku/jurnal ke berkas `template/pustaka.bib`.
  - **Sitasi dalam kurung (*Parenthetical*)**: Cukup tulis `@pressman2014` atau `@tanenbaum2011[hal. 12]`. Typst otomatis merendernya menjadi `(Pressman, 2014)`. *Jangan menambahkan tanda kurung manual seperti `(@pressman2014)` karena akan menghasilkan kurung dobel `((Pressman, 2014))`.*
  - **Sitasi naratif dalam kalimat**: Gunakan `#cite(<pressman2014>, form: "prose")` atau helper `#sitasi-naratif(<pressman2014>)` agar tercetak alami: `Menurut Pressman (2014), ...`.
  - **Penulis Institusi / Lembaga**: Pada `pustaka.bib`, bungkus dengan tanda kurung kurawal ganda, contoh: `author = {{Badan Pusat Statistik}}` agar nama lembaga tidak dipisah menjadi nama depan/belakang.
  - Daftar pustaka di akhir naskah otomatis diformat dengan *hanging indent*, spasi 1 per entri, dan spasi 2 antar-entri.

#### Langkah 4: Melampirkan Berkas Scan Instansi (Opsional)
Jika instansi tempat PKL Anda telah menerbitkan surat keterangan atau nilai dengan format asli bertanda tangan/stempel:
1. Simpan foto/scan berkas (`.png` atau `.jpg`) di `template/gambar/`.
2. Cantumkan nama berkas pada `template/metadata.typ`:
   ```typst
   #let file-surat-keterangan = "gambar/scan-surat-pkl.png" // Lampiran 26
   #let file-nilai-perusahaan = "gambar/scan-nilai-pkl.png"  // Lampiran 27
   #let file-bukti-kuesioner = "gambar/scan-kuesioner.png"   // Lampiran 32
   ```
   *Jika nilai variabel dibiarkan `none`, template akan otomatis mencetak formulir resmi standar pedoman UBSI.*

#### Langkah 5: Menghilangkan Catatan Petunjuk Sebelum Dijilid / Dicetak
Ketika seluruh naskah sudah selesai diisi dan siap dijilid atau dikumpulkan:
Buka `template/metadata.typ` dan ubah master switch menjadi `false`:
```typst
#let tampilkan-catatan-pedoman = false
```
Seluruh catatan petunjuk pedoman di Daftar Isi, Daftar Simbol, Daftar Gambar, Daftar Tabel, Daftar Lampiran, Daftar Riwayat Hidup, Surat Keterangan, Lembar Nilai, dan Kuesioner **otomatis bersih dan tidak akan muncul di hasil cetak**.

#### Langkah 6: Kompilasi Dokumen ke PDF via Terminal
Jika Anda ingin mengompilasi naskah menjadi berkas PDF melalui terminal / command prompt:
```bash
# Kompilasi Laporan Akhir PKL:
typst compile --root . template/main.typ laporan-pkl.pdf

# Kompilasi Proposal PKL:
typst compile --root . template/proposal.typ proposal-pkl.pdf
```
> [!IMPORTANT]
> Selalu gunakan opsi `--root .` saat mengompilasi agar Typst dapat mengakses pustaka inti `lib.typ` dari direktori root.

---

## Validasi & Pengujian Otomatis

Repositori ini dilengkapi suite pengujian otomatis untuk memvalidasi bahwa seluruh berkas laporan dan proposal dapat dikompilasi secara bebas error:

```bash
npm test
```
*Pengujian memverifikasi kompilasi Proposal PKL dan seluruh 4 outline Laporan PKL S1 TI.*

---

## Lisensi

Repositori ini didistribusikan di bawah lisensi [MIT License](LICENSE).
