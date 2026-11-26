# Anti-Slop Akademik & Panduan Anti-Detektor AI (Integrasi GitHub `antislop` + `antislop-copywriting`)

Dokumen ini mengadaptasi aturan inti `antislop` dan `antislop-copywriting` ke dalam penulisan karya ilmiah berbahasa Indonesia dan Inggris agar naskah terbaca alami seperti karya peneliti manusia serta lolos pemeriksaan Turnitin AI / GPTZero.

---

## 1. Aturan Keras (`Hard Gate`) dari `antislop` & `antislop-copywriting`

1. **`R-02` - Larangan Em Dash (`\u2014`) & Tanda Pisah Ganda (`--`)**:
   - Jangan pernah memakai karakter `\u2014` di dalam `.docx`, `.typ`, maupun `.md`.
   - Ganti dengan koma (`,`), titik dua (`:`), tanda kurung `()`, atau pecah menjadi dua kalimat yang tegas.
2. **`R-16` & Empty AI Vocabulary - Larangan Kosakata Klise AI**:
   - **Bahasa Indonesia terlarang**: *"di era digital yang semakin berkembang pesat"*, *"pada era revolusi industri 4.0 dewasa ini"*, *"tidak dapat dipungkiri bahwa"*, *"memainkan peran krusial/vital"*, *"membawa transformasi signifikan"*, *"secara komprehensif dan menyeluruh"*, *"menjadi jembatan antara"*, *"upaya tiada henti"*.
   - **Bahasa Inggris terlarang**: *"in today's rapidly evolving digital landscape"*, *"delve into"*, *"testament to"*, *"pivotal moment"*, *"seamless"*, *"cutting-edge"*, *"game-changer"*, *"holistic approach"*, *"multifaceted"*, *"underscore the importance"*.
   - **Perbaikan (*After*)**: Langsung buka paragraf dengan objek riset, data faktual, nama instansi, atau pasal hukum yang relevan.
3. **`R-36` - Larangan Pola Retorika Robotik**:
   - **Negative Parallelism Berulang**: Hindari pola *"Bukan hanya X, melainkan juga Y"*, *"Tidak semata-mata X, tetapi juga Y"*, atau *"It is not merely X; it is Y"* muncul berulang. Maksimal 1 kali dalam satu dokumen atau hilangkan sama sekali.
   - **Rule of Three Palsu**: Jangan memaksa setiap rincian menjadi tiga kata sifat/nomina sekaligus (*"cepat, tepat, dan akurat"*, *"efektif, efisien, dan berkelanjutan"*). Tuliskan jumlah unsur sesuai fakta sistem.
   - **Synonym Cycling**: Dalam teks hukum dan teknis, **tetap ulangi istilah yang sama** (`Pasal 332 KUHP Baru`, `BIND_ACCESSIBILITY_SERVICE`). Jangan mengganti istilah hukum/teknis dengan sinonim puitis hanya demi variasi kata.
   - **Generic Positive Conclusion**: Jangan menutup Kesimpulan dengan kalimat optimistis hampa seperti *"Hal ini membuka masa depan yang lebih cerah bagi bangsa."* Tutup dengan temuan terukur, batas kajian, dan saran riset lanjutan spesifik.
4. **`R-02` & `R-16` - Inanimate Subject with Human Verb & Actorless Passive**:
   - Jangan beri kata kerja berkesadaran kepada benda mati: ubah *"Data ini memahami dan menceritakan kendala nasabah"* atau *"Tabel 1 mengatakan..."* menjadi *"Data transaksi mencatat..."* dan *"Tabel 1 merinci..."*.
   - Sebutkan aktor nyata (Polri, OJK, Bank, Penulis, Sistem RASP) jika tersedia, bukan kalimat pasif kabur *"telah diputuskan bahwa..."*.
5. **`R-17` & `R-38` - Zero Fabricated Specifics**:
   - Jangan pernah menciptakan angka persentase, durasi uji, atau studi kasus tanpa sumber. Jika belum tersedia, gunakan `[ISI DATA NYATA: ...]`.

---

## 2. Teknik *Burstiness* & Variasi Ritme Kalimat (Anti-AI Detector)

Detektor AI (Turnitin AI, GPTZero, Copyleaks) mendeteksi *low perplexity* dan *low burstiness* karena AI cenderung menulis setiap kalimat sepanjang **18-24 kata secara seragam**.

**Standar Wajib Penulis Ilmiah (Diukur oleh `scripts/check_antislop_academic.py`):**
1. **Variasikan Panjang Kalimat Secara Sengaja (Target Std Dev `>= 5.5` kata)**:
   - Gunakan kalimat tesis pendek (`7-12 kata`) di awal paragraf atau saat menarik simpulan tegas.
   - Ikuti dengan kalimat analisis mendalam (`20-32 kata`) yang memuat nomor pasal, metrik teknis, atau rujukan `[1]`.
   - Selipkan satu kalimat menengah (`13-18 kata`) sebagai transisi atau perbandingan dengan penelitian terdahulu.
2. **Contoh Transformasi Nyata (`Before` -> `After`)**:
   - *Before (Pola AI, klise, panjang seragam)*:
     > "Di era transformasi digital yang berkembang pesat saat ini, tidak dapat dipungkiri bahwa kejahatan siber perbankan melalui file APK berbahaya memainkan peran krusial dalam mengancam keamanan data. Fenomena ini bukan hanya merugikan nasabah secara materiil, melainkan juga menguji ketahanan sistem pengamanan perbankan secara komprehensif dan menyeluruh."
   - *After (Manusiawi, bervariasi 9 kata -> 28 kata -> 14 kata, berbasis fakta)*:
     > "Penipuan perbankan melalui berkas APK berbahaya meningkat tajam sejak 2023 [1]. Setelah korban mengizinkan hak akses `BIND_ACCESSIBILITY_SERVICE`, trojan membaca ketukan PIN secara diam-diam dan meneruskan kode OTP SMS ke server pengendali jarak jauh [8], [10]. Kondisi tersebut menggeser sengketa pembuktian antara kelalaian nasabah dan keandalan sistem pengamanan bank [6]."
3. **Variasi Pembuka Paragraf**:
   - Jangan memulai 3 paragraf berturut-turut dengan kata penghubung seragam (*Selain itu,...*, *Selanjutnya,...*, *Oleh karena itu,...* / *Furthermore,...*, *Moreover,...*, *Additionally,...*). Gunakan langsung subjek hukum, nama teknik, atau temuan tabel sebagai pembuka.
