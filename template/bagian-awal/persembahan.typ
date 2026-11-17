#import "../../lib.typ": *
#import "../metadata.typ": *

// =============================================================================
// LEMBAR PERSEMBAHAN & MOTTO
// =============================================================================

#page(
  header: none,
  footer: context {
    let page-num = counter(page).display("i")
    align(center)[#text(size: 12pt)[#page-num]]
  }
)[
  #heading(level: 1, numbering: none, outlined: true)[Lembar Persembahan]

  #align(center)[
    #text(size: 14pt, weight: "bold")[
      LEMBAR PERSEMBAHAN DAN MOTTO
    ]
  ]

  #v(1.5cm)
  #align(center)[
    #block(width: 80%)[
      #text(style: "italic")[
        \"Sebaik-baik manusia adalah yang paling bermanfaat bagi sesamanya.\"\
        *(HR. Ahmad & Thabrani)*
      ]
    ]
  ]

  #v(2cm)
  Naskah skripsi ini saya persembahkan dengan penuh ketulusan hati dan rasa syukur kepada:

  + *Kedua Orang Tua Tercinta:*\
    Ayahanda dan Ibunda yang tiada henti memanjatkan doa, melimpahkan kasih sayang, memberikan dukungan moril dan materil, serta menjadi sumber inspirasi terbesar dalam setiap langkah kehidupan ananda.
  + *Dosen Pembimbing Skripsi:*\
    Bapak/Ibu dosen pembimbing yang senantiasa membimbing dengan penuh kesabaran, memberikan arahan bernilai, serta membagikan wawasan keilmuan yang luas hingga skripsi ini terselesaikan.
  + *Sivitas Akademika Universitas Bina Sarana Informatika:*\
    Seluruh dosen dan staf pengajar Program Studi #program-studi Fakultas #fakultas yang telah mendidik dan membekali ilmu pengetahuan selama masa perkuliahan.
  + *Sahabat dan Rekan Seperjuangan:*\
    Teman-teman mahasiswa Program Studi #program-studi angkatan #tahun-akademik yang telah berbagi suka, duka, semangat, dan kebersamaan dalam menuntaskan jenjang sarjana.
  + *Almamater Tercinta:*\
    #universitas sebagai wadah menimba ilmu dan tempat berproses menggapai masa depan.
]
