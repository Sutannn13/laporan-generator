#import "../../lib.typ": *
#import "../metadata.typ": *

// =============================================================================
// KATA PENGANTAR SKRIPSI
// =============================================================================

#heading(level: 1, numbering: none, outlined: true)[Kata Pengantar]

Puji dan syukur penulis panjatkan ke hadirat Allah SWT atas rahmat, berkah, dan karunia-Nya sehingga penulis dapat menyelesaikan penyusunan skripsi yang berjudul: "*#upper(judul)*", yang diajukan sebagai salah satu syarat kelulusan guna meraih gelar Sarjana Komputer (S.Kom) pada Program Studi #program-studi Fakultas #fakultas #universitas.

Dalam penyusunan skripsi ini, penulis menyadari sepenuhnya bahwa penyelesaian karya ilmiah ini tidak lepas dari bimbingan, dorongan, masukan, arahan, serta doa dari berbagai pihak. Oleh karena itu, pada kesempatan ini penulis menyampaikan ucapan terima kasih yang tulus dan penghargaan setinggi-tingginya kepada:

+ Rektor #universitas beserta jajaran pimpinan universitas.
+ Dekan Fakultas #fakultas #universitas.
+ Ketua Program Studi #program-studi Fakultas #fakultas #universitas.
+ #dosen-pembimbing-1 selaku Dosen Pembimbing I yang telah meluangkan waktu dan pemikiran dengan penuh kesabaran untuk membimbing penulis sejak awal hingga terselesaikannya skripsi ini.
+ #dosen-pembimbing-2 selaku Dosen Pembimbing II yang senantiasa memberikan arahan, koreksi berharga, dan saran penyempurnaan naskah skripsi.
+ #dosen-pa selaku Dosen Penasehat Akademik atas motivasi dan bimbingan akademis selama masa perkuliahan.
+ Pimpinan, staf, dan seluruh jajaran #nama-instansi yang telah memberikan izin riset dan membantu proses pengumpulan data penelitian.
+ Kedua Orang Tua dan keluarga tercinta atas doa yang tiada putus, limpahan kasih sayang, dan pengorbanan yang tak ternilai.
+ Rekan-rekan mahasiswa Program Studi #program-studi angkatan #tahun-akademik atas kebersamaan, motivasi, dan kerja samanya.

Penulis menyadari bahwa skripsi ini masih jauh dari kesempurnaan karena keterbatasan wawasan dan pengalaman penulis. Oleh sebab itu, kritik dan saran yang konstruktif sangat diharapkan demi penyempurnaan karya ilmiah ini. Akhir kata, semoga skripsi ini dapat memberikan manfaat nyata bagi pembaca dan perkembangan ilmu pengetahuan di bidang teknologi informasi.

#v(1.5cm)
#align(right)[
  #block(width: 6cm)[
    #set align(center)
    #let tgl = if tanggal-persetujuan != none { tanggal-persetujuan } else { kota + ", " + datetime.today().display("[day] [month repr:long] [year]") }
    #tgl\
    #v(0.6cm)
    Penulis\
    #v(1.8cm)
    #penulis
  ]
]
