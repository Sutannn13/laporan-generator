// =============================================================================
// ENTRYPOINT RESMI: SKRIPSI PROGRAM SARJANA (S1) UBSI
// Program Studi: Teknologi Informasi, Fakultas Teknik & Informatika
// Outline: Kode 156 - Perancangan Program Science (5 Bab)
// =============================================================================

#import "../lib.typ": *
#import "metadata.typ": *

// 1. Lembar Judul Skripsi (Cover: nomor i dihitung tapi tidak dicetak)
#cover-skripsi(
  judul: judul,
  penulis: penulis,
  nim: nim,
  penulis-2: penulis-2,
  nim-2: nim-2,
  jenjang: jenjang,
  program-studi: program-studi,
  fakultas: fakultas,
  universitas: universitas,
  kota: kota,
  tahun: tahun,
  is-kampus-utama: is-kampus-utama,
  logo-path: "public/logo-ubsi.png",
)

// 2. Bagian Awal (Frontmatter: Romawi Kecil Bawah Tengah)
#show: frontmatter-skripsi

// Lembar Pernyataan Keaslian Skripsi
#include "bagian-awal/pernyataan-keaslian-skripsi.typ"

// Lembar Pernyataan Persetujuan Publikasi Karya Ilmiah
#include "bagian-awal/persetujuan-publikasi-skripsi.typ"

// Lembar Persetujuan dan Pengesahan Skripsi
#include "bagian-awal/pengesahan-skripsi.typ"

// Lembar Pedoman Penggunaan Hak Cipta
#include "bagian-awal/hak-cipta-skripsi.typ"

// Lembar Konsultasi Skripsi
#include "bagian-awal/konsultasi-skripsi.typ"

// Lembar Motto & Persembahan
#include "bagian-awal/persembahan.typ"

// Kata Pengantar Skripsi
#include "bagian-awal/kata-pengantar-skripsi.typ"

// Abstraksi (Dwibahasa ID & EN)
#include "bagian-awal/abstraksi.typ"

// Daftar Isi
#daftar-isi(tampilkan-catatan: tampilkan-catatan-pedoman)

// Daftar Simbol
#include "bagian-awal/daftar-simbol.typ"

// Daftar Gambar
#daftar-gambar(tampilkan-catatan: tampilkan-catatan-pedoman)

// Daftar Tabel
#daftar-tabel(tampilkan-catatan: tampilkan-catatan-pedoman)

// Daftar Lampiran
#include "bagian-awal/daftar-lampiran.typ"

// 3. Bagian Pokok (Mainmatter: Angka Latin 1, 2, 3...)
#pagebreak()
#counter(page).update(1)

#show: skripsi.with(
  judul: judul,
  jenis: "skripsi",
  penulis: penulis,
  nim: nim,
  program-studi: program-studi,
  fakultas: fakultas,
  universitas: universitas,
  kota: kota,
  tahun: tahun,
)

// OUTLINE SKRIPSI: KODE 156 - PERANCANGAN PROGRAM SCIENCE (5 BAB)
#include "outlines/skripsi-ti-156/bab1.typ"
#include "outlines/skripsi-ti-156/bab2.typ"
#include "outlines/skripsi-ti-156/bab3.typ"
#include "outlines/skripsi-ti-156/bab4.typ"
#include "outlines/skripsi-ti-156/bab5.typ"

// 4. Bagian Akhir (Backmatter: Nomor Halaman Bawah Tengah)
#show: backmatter-skripsi
#pagebreak()
#bibliography(
  "pustaka.bib",
  title: [DAFTAR PUSTAKA],
  style: "apa",
)

// Daftar Riwayat Hidup
#include "bagian-akhir/daftar-riwayat-hidup.typ"

// Surat Keterangan Riset (Opsional)
#include "bagian-akhir/surat-keterangan-pkl.typ"

// Bukti Hasil Pengecekan Plagiarisme (Turnitin)
#include "bagian-akhir/bukti-plagiarisme.typ"

// Lampiran-Lampiran
#include "bagian-akhir/lampiran-skripsi.typ"
