// =============================================================================
// METADATA DOKUMEN PKL / PROPOSAL PKL UBSI
// Program Studi: Teknologi Informasi (S1)
// =============================================================================

// Identitas Mahasiswa & Laporan
#let judul = "SISTEM PEMANTAUAN INFRASTRUKTUR JARINGAN BERBASIS SNMP PADA LABORATORIUM KOMPUTER"
#let jenis = "proposal" // Pilihan: "proposal" | "laporan"
#let penulis = "Nama Mahasiswa"
#let nim = "12200001"
// Mahasiswa Kedua (Khusus outline skripsi kelompok: Outline 158 Aplikasi StartUp)
#let penulis-2 = none // contoh: "Nama Mahasiswa Kedua"
#let nim-2 = none     // contoh: "12200002"
#let jenjang = "Sarjana (S1)" // "Sarjana (S1)" atau "Diploma Tiga (D3)"
#let program-studi = "Teknologi Informasi"
#let fakultas = "Teknik dan Informatika"
#let universitas = "Universitas Bina Sarana Informatika"
#let kota = "Jakarta"
#let tahun = "2026"

// Konfigurasi Kampus (Sesuai Lampiran 1 & 2):
// true  = Program Studi di Kampus Utama (mencantumkan Kota)
// false = Program Studi di Luar Kampus Utama / PSDKU (tanpa Kota)
#let is-kampus-utama = true

// Pembimbing & Penasehat Akademik (Sesuai Lampiran 5 & 6):
#let semester = "Gasal" // "Gasal" atau "Genap"
#let tahun-akademik = "2026"
#let kelas = "7A.01" // Kelas semester VII (S1) atau semester V (D3)
#let dosen-pa = "Nama Dosen Penasehat Akademik, M.Kom"
#let tanggal-persetujuan = "Jakarta, 15 Juli 2026"

// Detail Rencana Instansi PKL (Untuk Bab II Proposal):
#let nama-instansi = "PT. Telekomunikasi Indonesia Prima"
#let divisi-instansi = "Divisi Information Technology & Infrastructure"
#let alamat-instansi = "Jl. Gatot Subroto No. Kav 52, Jakarta Selatan"
#let kontak-instansi = "(021) 5215123 / info@telkomprima.co.id"
#let tanggal-mulai-pkl = "1 Agustus 2026"
#let tanggal-selesai-pkl = "31 Oktober 2026"
// Pembimbing Instansi / Perusahaan (Untuk Kata Pengantar Sesuai Lampiran 17):
#let nama-pembimbing-instansi = "Nama Pembimbing Instansi, S.T."
#let jabatan-pembimbing-instansi = "Kepala Divisi Teknologi Informasi"

// Berkas Bukti Lampiran Perusahaan (Scan PNG/JPG):
// Biarkan none jika ingin menggunakan template cetak resmi UBSI
#let file-surat-keterangan = none // contoh: "gambar/scan-surat-keterangan.png"
#let file-nilai-perusahaan = none  // contoh: "gambar/scan-lembar-nilai.png"
#let file-bukti-kuesioner = none   // contoh: "gambar/scan-bukti-kuesioner.png"

// Konfigurasi Catatan Petunjuk Pedoman:
// true  = Menampilkan catatan petunjuk pedoman kampus (disertai peringatan wajib dihapus)
// false = Otomatis menyembunyikan seluruh catatan petunjuk pedoman saat dijilid/dicetak
#let tampilkan-catatan-pedoman = true

// =============================================================================
// KONFIGURASI SKRIPSI / TUGAS AKHIR SARJANA (S1)
// =============================================================================
#let kode-outline = "156" // "156" = Perancangan Program Science
#let nama-outline = "Perancangan Program Science"

// Dewan Penguji, Pembimbing & Pejabat Prodi Skripsi
#let ketua-prodi = "Nama Ketua Program Studi, M.Kom"
#let dosen-pembimbing-1 = "Nama Dosen Pembimbing I, M.Kom"
#let dosen-pembimbing-2 = "Nama Dosen Pembimbing II, M.Kom"
#let dosen-penguji-1 = "Nama Ketua Penguji, M.Kom"
#let dosen-penguji-2 = "Nama Anggota Penguji, M.Kom"

// Abstrak Skripsi Dwibahasa (ID & EN)
#let abstrak-id = [
  Perkembangan teknologi informasi saat ini menuntut pengolahan data yang cepat, mangkus, dan akurat. Penelitian skripsi ini bertujuan untuk merancang dan membangun perangkat lunak menggunakan metode algoritma komputasi guna mengatasi permasalahan inefisiensi alur operasional pada objek penelitian. Metode pengembangan sistem mengadopsi model Waterfall yang mencakup analisis kebutuhan, perancangan arsitektur, pemodelan basis data, penulisan kode program, serta pengujian sistem. Hasil pengujian menunjukkan bahwa aplikasi berhasil memproses kalkulasi komputasi secara valid, bebas dari kesalahan logika, dan meningkatkan efektivitas kinerja sistem secara signifikan.
]
#let abstrak-en = [
  The rapid development of information technology demands fast, efficient, and accurate data processing. This thesis aims to design and implement application software utilizing computational algorithms to overcome operational workflow inefficiencies in the research object. The development methodology adopts the Waterfall model encompassing requirements analysis, architectural design, database modeling, code generation, and system testing. The testing results demonstrate that the application successfully performs computational tasks accurately, free from logic errors, and significantly optimizes operational efficiency.
]
#let kata-kunci-id = "Rekayasa Perangkat Lunak, Algoritma Komputasi, Perancangan Program, Basis Data"
#let kata-kunci-en = "Software Engineering, Computational Algorithm, Program Design, Database"

// Pengujian Plagiarisme Skripsi
#let tingkat-kemiripan-plagiarisme = "14%"
#let tanggal-cek-plagiarisme = "10 Januari 2026"
#let file-bukti-plagiarisme = none // contoh: "gambar/scan-turnitin.png"


