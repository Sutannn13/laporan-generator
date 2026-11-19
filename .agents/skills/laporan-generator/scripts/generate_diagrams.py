# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAMBAR_DIR = os.path.join(ROOT_DIR, "template", "gambar")
os.makedirs(GAMBAR_DIR, exist_ok=True)


def out_img(filename):
    return os.path.join(GAMBAR_DIR, filename)


def generate_org_chart():
    fig, ax = plt.subplots(figsize=(14, 8.5), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9.5)
    ax.axis("off")
    fig.patch.set_facecolor("#ffffff")

    ax.text(
        7.0,
        8.9,
        "STRUKTUR ORGANISASI DINAS KOMUNIKASI DAN INFORMATIKA KOTA CONTOH",
        ha="center",
        va="center",
        fontsize=13,
        fontweight="bold",
        color="#113322",
        fontfamily="sans-serif",
    )

    def draw_box(x, y, w, h, text, title="", bg="#f0fdf4", border="#166534", bold=True, is_highlight=False):
        box_bg = "#dcfce7" if is_highlight else bg
        box_border = "#15803d" if is_highlight else border
        linewidth = 2.2 if is_highlight else 1.2
        rect = patches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.15", ec=box_border, fc=box_bg, lw=linewidth
        )
        ax.add_patch(rect)
        if title:
            ax.text(
                x + w / 2,
                y + h - 0.22,
                title,
                ha="center",
                va="center",
                fontsize=8.5,
                fontweight="bold",
                color="#14532d",
                fontfamily="sans-serif",
            )
            ax.text(
                x + w / 2,
                y + (h - 0.2) / 2,
                text,
                ha="center",
                va="center",
                fontsize=8,
                fontweight="normal" if not bold else "bold",
                color="#1f2937",
                fontfamily="sans-serif",
            )
        else:
            ax.text(
                x + w / 2,
                y + h / 2,
                text,
                ha="center",
                va="center",
                fontsize=8.5,
                fontweight="bold" if bold else "normal",
                color="#1f2937",
                fontfamily="sans-serif",
            )

    draw_box(
        4.8,
        7.3,
        4.4,
        0.9,
        "Kepala Dinas Contoh, S.Kom., M.Si.",
        title="KEPALA DINAS KOMINFO KOTA CONTOH",
        bg="#bbf7d0",
        border="#15803d",
    )
    ax.plot([7.0, 7.0], [7.3, 6.7], color="#166534", lw=1.5)
    ax.plot([7.0, 7.0], [6.7, 6.1], color="#166534", lw=1.5)
    draw_box(4.8, 5.3, 4.4, 0.8, "SEKRETARIAT DINAS", bg="#e0f2fe", border="#0284c7")

    ax.plot([7.0, 7.0], [5.3, 4.7], color="#0284c7", lw=1.2)
    ax.plot([1.6, 12.4], [4.7, 4.7], color="#0284c7", lw=1.2)

    urusan_list = [
        ("Bidang Statistik\n& Persandian", 0.6, 3.4, 2.2, 0.9, False),
        ("Subbagian Keuangan\n& Perencanaan", 3.1, 3.4, 2.3, 0.9, False),
        ("Bidang Pengelolaan\nInformasi Publik\n(HUMAS)", 5.7, 3.1, 2.6, 1.3, True),
        ("Subbagian Umum\n& Kepegawaian", 8.6, 3.4, 2.3, 0.9, False),
        ("Bidang Infrastruktur\n& Aplikasi Informatika", 11.2, 3.4, 2.2, 0.9, False),
    ]

    for label, ux, uy, uw, uh, hl in urusan_list:
        ax.plot([ux + uw / 2, ux + uw / 2], [4.7, uy + uh], color="#0284c7", lw=1.2)
        draw_box(ux, uy, uw, uh, label, bg="#eff6ff", border="#0369a1" if not hl else "#dc2626", is_highlight=hl)

    ax.plot([7.0, 2.4], [6.7, 6.7], color="#166534", lw=1.5)
    ax.plot([2.4, 2.4], [6.7, 6.0], color="#166534", lw=1.5)
    draw_box(0.9, 5.2, 3.0, 0.8, "KELOMPOK JABATAN\nFUNGSIONAL", bg="#fef3c7", border="#d97706")

    ax.plot([7.0, 11.6], [6.7, 6.7], color="#166534", lw=1.5)
    ax.plot([11.6, 11.6], [6.7, 6.0], color="#166534", lw=1.5)
    draw_box(10.1, 5.2, 3.0, 0.8, "BIDANG LAYANAN\nE-GOVERNMENT", bg="#fef3c7", border="#d97706")

    ax.plot([7.0, 7.0], [3.1, 2.1], color="#166534", lw=1.2)
    ax.plot([3.8, 10.2], [2.1, 2.1], color="#166534", lw=1.2)

    ax.plot([3.8, 3.8], [2.1, 1.6], color="#166534", lw=1.2)
    draw_box(1.8, 0.7, 4.0, 0.9, "UNIT LAYANAN PPID\nKecamatan se-Kota Contoh", bg="#f3f4f6", border="#4b5563")

    ax.plot([10.2, 10.2], [2.1, 1.6], color="#166534", lw=1.2)
    draw_box(8.2, 0.7, 4.0, 0.9, "UNIT LAYANAN PENGADUAN\nMasyarakat Kota Contoh", bg="#f3f4f6", border="#4b5563")

    plt.tight_layout()
    target = out_img("gambar_3_1_struktur_organisasi.png")
    plt.savefig(target, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {target}")


def generate_use_case_chart():
    fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 9.0)
    ax.axis("off")
    fig.patch.set_facecolor("#ffffff")

    ax.text(
        7.5, 8.65, "USE CASE DIAGRAM SISTEM PUBLIKASI BERITA BERJALAN", ha="center", va="center", fontsize=12, fontweight="bold", color="#1e3a8a"
    )

    system_rect = patches.FancyBboxPatch(
        (3.6, 0.4), 7.4, 7.9, boxstyle="round,pad=0.1,rounding_size=0.18", ec="#1e40af", fc="#f8fafc", lw=1.5
    )
    ax.add_patch(system_rect)
    ax.text(
        7.3,
        8.0,
        "«Sistem Berjalan»\nPengelolaan Publikasi Berita Humas Diskominfo Kota Contoh",
        ha="center",
        va="center",
        fontsize=9.5,
        fontweight="bold",
        color="#1e40af",
    )

    def draw_actor(x, y, name, role):
        circle = patches.Circle((x, y), 0.22, ec="#1f2937", fc="#e2e8f0", lw=1.3)
        ax.add_patch(circle)
        ax.plot([x, x], [y - 0.22, y - 0.65], color="#1f2937", lw=1.3)
        ax.plot([x - 0.32, x + 0.32], [y - 0.38, y - 0.38], color="#1f2937", lw=1.3)
        ax.plot([x, x - 0.25], [y - 0.65, y - 1.05], color="#1f2937", lw=1.3)
        ax.plot([x, x + 0.25], [y - 0.65, y - 1.05], color="#1f2937", lw=1.3)
        ax.text(x, y - 1.25, f"«Aktor»\n{name}", ha="center", va="top", fontsize=8.5, fontweight="bold", color="#0f172a")
        ax.text(x, y - 1.7, f"({role})", ha="center", va="top", fontsize=7.5, style="italic", color="#475569")

    draw_actor(1.8, 5.0, "Staf Humas", "Pelaksana & Penulis")
    draw_actor(13.2, 6.8, "Kepala Bidang\n/ Pimpinan", "Verifikator & Approval")
    draw_actor(13.2, 2.7, "Masyarakat\n/ Publik", "Pembaca Berita")

    use_cases = [
        ("UC-1: Meliput Agenda Kegiatan", 7.3, 7.3),
        ("UC-2: Menyusun Draf Berita (Word)", 7.3, 6.6),
        ("UC-3: Mengirim Draf via WhatsApp", 7.3, 5.9),
        ("UC-4: Menelaah Draf Berita", 7.3, 5.2),
        ("UC-5: Memberikan Catatan Revisi", 7.3, 4.5),
        ("UC-6: Memperbaiki Draf Berita", 7.3, 3.8),
        ("UC-7: Menyetujui Naskah (Approval ACC)", 7.3, 3.1),
        ("UC-8: Menerbitkan Berita ke Website", 7.3, 2.4),
        ("UC-9: Mengunggah Konten ke Instagram", 7.3, 1.7),
        ("UC-10: Mengarsipkan Berita & Foto", 7.3, 1.0),
    ]

    for name, cx, cy in use_cases:
        oval = patches.Ellipse((cx, cy), 6.0, 0.55, ec="#0284c7", fc="#f0f9ff", lw=1.2)
        ax.add_patch(oval)
        ax.text(cx, cy, name, ha="center", va="center", fontsize=8, color="#0369a1", fontweight="bold")

    staf_pos = (2.2, 5.0)
    for uc_idx in [0, 1, 2, 5, 7, 8, 9]:
        cx, cy = use_cases[uc_idx][1], use_cases[uc_idx][2]
        ax.plot([staf_pos[0], cx - 3.0], [staf_pos[1], cy], color="#64748b", lw=1.0)

    pim_pos = (12.4, 6.5)
    for uc_idx in [3, 4, 6]:
        cx, cy = use_cases[uc_idx][1], use_cases[uc_idx][2]
        ax.plot([pim_pos[0], cx + 3.0], [pim_pos[1], cy], color="#64748b", lw=1.0)

    pub_pos = (12.4, 2.4)
    for uc_idx in [7, 8]:
        cx, cy = use_cases[uc_idx][1], use_cases[uc_idx][2]
        ax.plot([pub_pos[0], cx + 3.0], [pub_pos[1], cy], color="#64748b", lw=1.0, linestyle="--")

    plt.tight_layout()
    target = out_img("gambar_3_2_use_case_berjalan.png")
    plt.savefig(target, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {target}")


def generate_activity_diagram():
    fig, ax = plt.subplots(figsize=(14, 9.0), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9.6)
    ax.axis("off")
    fig.patch.set_facecolor("#ffffff")

    ax.text(7.0, 9.3, "ACTIVITY DIAGRAM SISTEM PUBLIKASI BERITA BERJALAN", ha="center", va="center", fontsize=12, fontweight="bold", color="#111827")

    lane_y_bot = 0.4
    headers = [
        ("STAF HUMAS", 0.6, 4.3),
        ("PIMPINAN / KEPALA BIDANG", 4.9, 4.2),
        ("PORTAL & MEDIA SOSIAL", 9.1, 4.3),
    ]
    for title, lx, lw in headers:
        rect = patches.Rectangle((lx, 8.5), lw, 0.5, ec="#1f2937", fc="#e5e7eb", lw=1.2)
        ax.add_patch(rect)
        ax.text(lx + lw / 2, 8.75, title, ha="center", va="center", fontsize=9, fontweight="bold", color="#1f2937")
        ax.plot([lx, lx], [lane_y_bot, 8.5], color="#9ca3af", lw=1.0, linestyle=":")
    ax.plot([13.4, 13.4], [lane_y_bot, 8.5], color="#9ca3af", lw=1.0, linestyle=":")

    def draw_act(cx, cy, text, w=3.7, h=0.52, bg="#ffffff", ec="#1f2937"):
        rect = patches.FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle="round,pad=0.05,rounding_size=0.15", ec=ec, fc=bg, lw=1.1)
        ax.add_patch(rect)
        ax.text(cx, cy, text, ha="center", va="center", fontsize=7.5, color="#111827", fontfamily="sans-serif")

    start_c = patches.Circle((2.75, 8.1), 0.13, fc="#000000")
    ax.add_patch(start_c)
    ax.annotate("", xy=(2.75, 7.6), xytext=(2.75, 7.97), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))

    draw_act(2.75, 7.35, "Meliput kegiatan kedinasan &\nmengambil foto dokumentasi")
    ax.annotate("", xy=(2.75, 6.75), xytext=(2.75, 7.09), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))

    draw_act(2.75, 6.5, "Mengetik draf berita manual\nmenggunakan Microsoft Word")
    ax.annotate("", xy=(2.75, 5.9), xytext=(2.75, 6.24), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))

    draw_act(2.75, 5.65, "Mengirim file naskah .docx\nkepada pimpinan via WhatsApp")

    ax.plot([4.6, 7.0], [5.65, 5.65], color="#000000", lw=1.2)
    ax.annotate("", xy=(7.0, 5.15), xytext=(7.0, 5.65), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))

    draw_act(7.0, 4.9, "Menerima file draf & menelaah\nmuatan informasi naskah berita", w=3.6)
    ax.annotate("", xy=(7.0, 4.25), xytext=(7.0, 4.64), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))

    diamond = patches.Polygon([[7.0, 4.15], [7.6, 3.85], [7.0, 3.55], [6.4, 3.85]], ec="#b45309", fc="#fef3c7", lw=1.2)
    ax.add_patch(diamond)
    ax.text(7.0, 3.85, "Disetujui?", ha="center", va="center", fontsize=7.5, fontweight="bold", color="#92400e")

    ax.plot([6.4, 5.7], [3.85, 3.85], color="#b91c1c", lw=1.2)
    ax.text(6.0, 4.0, "[Tidak]", fontsize=7, color="#b91c1c", fontweight="bold")
    ax.plot([5.7, 5.7], [3.85, 3.55], color="#b91c1c", lw=1.2)
    draw_act(5.7, 3.3, "Kirim catatan revisi\nvia chat WhatsApp", w=2.1, h=0.48, bg="#fee2e2", ec="#b91c1c")
    ax.plot([4.65, 2.75], [3.3, 3.3], color="#b91c1c", lw=1.2)
    draw_act(2.75, 3.3, "Merevisi naskah di Word &\nmengirim ulang ke Pimpinan", w=3.4, h=0.5, bg="#fef2f2", ec="#b91c1c")
    ax.plot([2.75, 2.75], [3.55, 4.2], color="#b91c1c", lw=1.2)
    ax.plot([2.75, 6.0], [4.2, 4.2], color="#b91c1c", lw=1.2)
    ax.annotate("", xy=(7.0, 4.64), xytext=(6.0, 4.2), arrowprops=dict(arrowstyle="->", lw=1.0, color="#b91c1c"))

    ax.annotate("", xy=(7.0, 2.85), xytext=(7.0, 3.55), arrowprops=dict(arrowstyle="->", lw=1.2, color="#15803d"))
    ax.text(7.15, 3.25, "[Ya / ACC]", fontsize=7, color="#15803d", fontweight="bold")
    draw_act(7.0, 2.6, "Mengirim konfirmasi persetujuan\n(ACC) publikasi via WhatsApp", w=3.6, bg="#f0fdf4", ec="#15803d")

    ax.plot([5.2, 2.75], [2.6, 2.6], color="#000000", lw=1.2)
    ax.annotate("", xy=(2.75, 2.15), xytext=(2.75, 2.6), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))
    draw_act(2.75, 1.9, "Menyiapkan materi berita &\nmelakukan unggah publikasi")

    ax.plot([4.6, 11.25], [1.9, 1.9], color="#000000", lw=1.2)
    ax.annotate("", xy=(11.25, 1.6), xytext=(11.25, 1.9), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))
    draw_act(11.25, 1.35, "Menerbitkan artikel di Portal\n& posting di Media Sosial @humas_kotacontoh", w=3.8, h=0.52, bg="#f0f9ff", ec="#0284c7")

    ax.plot([9.35, 2.75], [1.35, 1.35], color="#000000", lw=1.2)
    ax.annotate("", xy=(2.75, 1.05), xytext=(2.75, 1.35), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))
    draw_act(2.75, 0.8, "Menyimpan file naskah Word &\nfoto di folder penyimpanan lokal")

    ax.annotate("", xy=(2.75, 0.42), xytext=(2.75, 0.54), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))
    end_outer = patches.Circle((2.75, 0.28), 0.14, ec="#000000", fc="#ffffff", lw=1.5)
    end_inner = patches.Circle((2.75, 0.28), 0.08, fc="#000000")
    ax.add_patch(end_outer)
    ax.add_patch(end_inner)

    plt.tight_layout()
    target = out_img("gambar_3_3_activity_diagram_berjalan.png")
    plt.savefig(target, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {target}")


def generate_apk_attack_and_liability_diagram():
    fig, ax = plt.subplots(figsize=(14.5, 8.2), dpi=300)
    ax.set_xlim(0, 14.5)
    ax.set_ylim(0, 8.5)
    ax.axis("off")
    fig.patch.set_facecolor("#ffffff")

    ax.text(
        7.25,
        8.15,
        "VEKTOR EKSPLOITASI MALICIOUS APK & MATRIKS PERTANGGUNGJAWABAN HUKUM PERBANKAN",
        ha="center",
        va="center",
        fontsize=11.5,
        fontweight="bold",
        color="#0f172a",
    )
    ax.text(
        7.25,
        7.82,
        "(Analisis Teknis Android Accessibility/SMS Stealer vs. Rezim UU No. 1/2023 KUHP Baru, UU ITE 1/2024 & POJK 22/2023)",
        ha="center",
        va="center",
        fontsize=8.5,
        style="italic",
        color="#334155",
    )

    def draw_node(x, y, w, h, title, body, bg="#f8fafc", ec="#1e293b", title_color="#0f172a"):
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.14", ec=ec, fc=bg, lw=1.3)
        ax.add_patch(box)
        ax.text(x + w / 2, y + h - 0.34, title, ha="center", va="center", fontsize=8.3, fontweight="bold", color=title_color)
        ax.text(x + w / 2, y + (h - 0.58) / 2, body, ha="center", va="center", fontsize=7.5, color="#1e293b", linespacing=1.35)

    zone1 = patches.FancyBboxPatch(
        (0.4, 4.45), 13.7, 3.05, boxstyle="round,pad=0.08,rounding_size=0.15", ec="#b91c1c", fc="#fff5f5", lw=1.2, linestyle="--"
    )
    ax.add_patch(zone1)
    ax.text(
        7.25,
        7.28,
        "FASE 1: RANTAI SERANGAN TEKNIS UNAUTHORIZED ACCESS MELALUI MALICIOUS APK (DI LUAR PLAY STORE)",
        ha="center",
        va="center",
        fontsize=8.5,
        fontweight="bold",
        color="#991b1b",
    )

    steps = [
        (
            0.65,
            4.75,
            2.9,
            2.2,
            "1. Social Engineering\n& Sideloading APK",
            "Pelaku mengirim file .APK\n(Undangan/Kurir/Tagihan)\nvia WhatsApp; memicu izin\nREQUEST_INSTALL_PACKAGES",
            "#fee2e2",
            "#dc2626",
            "#7f1d1d",
        ),
        (
            4.05,
            4.75,
            3.1,
            2.2,
            "2. Penyalahgunaan Izin\nAccessibility & SMS",
            "Eksploitasi izin berbahaya:\nBIND_ACCESSIBILITY_SERVICE,\nRECEIVE_SMS & READ_SMS\nserta Overlay Attack Window",
            "#fee2e2",
            "#dc2626",
            "#7f1d1d",
        ),
        (
            7.65,
            4.75,
            3.0,
            2.2,
            "3. Intersepsi OTP & Keylogging\nKredensial M-Banking",
            "Perekaman PIN/Password via\nAccessibilityEvent + forwarding\nSMS OTP secara siluman ke\nServer Command & Control (C2)",
            "#fee2e2",
            "#dc2626",
            "#7f1d1d",
        ),
        (
            11.15,
            4.75,
            2.7,
            2.2,
            "4. Pengambilalihan Akun\n& Pengurasan Dana",
            "Account Takeover (ATO)\npada sesi Mobile Banking &\ntransfer RTOL/BI-FAST ke\nrekening penampung (Mule)",
            "#fecaca",
            "#991b1b",
            "#7f1d1d",
        ),
    ]

    for x, y, w, h, t, b, bg, ec, tc in steps:
        draw_node(x, y, w, h, t, b, bg, ec, tc)

    for ax_x in [(3.55, 4.05), (7.15, 7.65), (10.65, 11.15)]:
        ax.annotate("", xy=(ax_x[1], 5.85), xytext=(ax_x[0], 5.85), arrowprops=dict(arrowstyle="->", lw=1.6, color="#b91c1c"))

    zone2 = patches.FancyBboxPatch((0.4, 0.45), 13.7, 3.55, boxstyle="round,pad=0.08,rounding_size=0.15", ec="#1e3a8a", fc="#f0f9ff", lw=1.2)
    ax.add_patch(zone2)
    ax.text(
        7.25,
        3.78,
        "FASE 2: KONSTRUKSI PERTANGGUNGJAWABAN HUKUM PIDANA (KUHP BARU) & PERDATA/REGULASI PERBANKAN",
        ha="center",
        va="center",
        fontsize=8.5,
        fontweight="bold",
        color="#1e3a8a",
        bbox=dict(boxstyle="round,pad=0.25", fc="#f0f9ff", ec="none"),
        zorder=5,
    )

    legal_boxes = [
        (
            0.65,
            0.75,
            4.1,
            2.75,
            "Pertanggungjawaban Pidana Pelaku\n(UU 1/2023 KUHP Baru & UU ITE 1/2024)",
            "• Pasal 332 UU 1/2023 (Akses Ilegal Sistem\n  Elektronik): Pidana penjara maks. 6-8 tahun\n• Pasal 334 UU 1/2023 (Intersepsi Ilegal OTP)\n• Pasal 492 UU 1/2023 (Penipuan Digital)\n• Lex Specialis Pasal 30 & 32 UU ITE 1/2024\n  selama masa transisi s.d. 2 Januari 2026",
            "#e0f2fe",
            "#0369a1",
            "#0c4a6e",
        ),
        (
            5.2,
            0.75,
            4.1,
            2.75,
            "Kewajiban Mitigasi Teknis Bank (PSE)\n(UU PDP 27/2022 & POJK 11/POJK.03/2022)",
            "• Deteksi Runtime Application Self-Protection\n  (RASP) terhadap layanan Accessibility aktif\n• Pemblokiran sesi pada perangkat terindikasi\n  overlay/hook & penguatan Device Binding\n• Fraud Detection System (FDS) anomali transaksi\n• Pelaporan insiden siber & perlindungan data",
            "#dcfce7",
            "#15803d",
            "#14532d",
        ),
        (
            9.75,
            0.75,
            4.1,
            2.75,
            "Alokasi Tanggung Jawab Kerugian Nasabah\n(POJK 22/2023 & Beban Pembuktian Terbalik)",
            "• Pasal 30-31 POJK 22/2023: PUJK wajib ganti\n  rugi jika terdapat kegagalan keamanan sistem\n• Pembuktian Terbalik (Shifting Burden of Proof):\n  Bank wajib buktikan audit log FDS & RASP\n• Tanggung Jawab Proporsional jika nasabah\n  terbukti lalai berat (Gross Negligence)",
            "#fef3c7",
            "#b45309",
            "#78350f",
        ),
    ]

    for x, y, w, h, t, b, bg, ec, tc in legal_boxes:
        draw_node(x, y, w, h, t, b, bg, ec, tc)

    ax.annotate("", xy=(2.7, 3.5), xytext=(2.7, 4.75), arrowprops=dict(arrowstyle="->", lw=1.4, color="#1e3a8a"))
    ax.annotate("", xy=(7.25, 3.5), xytext=(7.25, 4.75), arrowprops=dict(arrowstyle="->", lw=1.4, color="#15803d"))
    ax.annotate("", xy=(11.8, 3.5), xytext=(11.8, 4.75), arrowprops=dict(arrowstyle="->", lw=1.4, color="#b45309"))

    plt.tight_layout()
    target = out_img("gambar_sinta1_apk_attack_flow.png")
    plt.savefig(target, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {target}")


def generate_use_case_usulan_chart():
    fig, ax = plt.subplots(figsize=(15.5, 9.6), dpi=300)
    ax.set_xlim(0, 15.5)
    ax.set_ylim(0, 9.8)
    ax.axis("off")
    fig.patch.set_facecolor("#ffffff")

    ax.text(
        7.75,
        9.45,
        "USE CASE DIAGRAM SISTEM USULAN APLIKASI PRESS RELEASE AUTO-GENERATOR",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="#1e3a8a",
    )
    ax.text(
        7.75,
        9.15,
        "Bidang Humas Dinas Komunikasi dan Informatika Kota Contoh",
        ha="center",
        va="center",
        fontsize=9.5,
        style="italic",
        color="#475569",
    )

    system_rect = patches.FancyBboxPatch(
        (3.4, 0.4), 8.7, 8.4, boxstyle="round,pad=0.1,rounding_size=0.18", ec="#1e40af", fc="#f8fafc", lw=1.5
    )
    ax.add_patch(system_rect)
    ax.text(
        7.75,
        8.5,
        "«Sistem Usulan»\nAplikasi Press Release Auto-Generator Berbasis Web",
        ha="center",
        va="center",
        fontsize=9.5,
        fontweight="bold",
        color="#1e40af",
    )

    def draw_actor(x, y, name, role):
        circle = patches.Circle((x, y), 0.22, ec="#1f2937", fc="#e2e8f0", lw=1.3)
        ax.add_patch(circle)
        ax.plot([x, x], [y - 0.22, y - 0.65], color="#1f2937", lw=1.3)
        ax.plot([x - 0.32, x + 0.32], [y - 0.38, y - 0.38], color="#1f2937", lw=1.3)
        ax.plot([x, x - 0.25], [y - 0.65, y - 1.05], color="#1f2937", lw=1.3)
        ax.plot([x, x + 0.25], [y - 0.65, y - 1.05], color="#1f2937", lw=1.3)
        ax.text(x, y - 1.25, f"«Aktor»\n{name}", ha="center", va="top", fontsize=8.5, fontweight="bold", color="#0f172a")
        ax.text(x, y - 1.7, f"({role})", ha="center", va="top", fontsize=7.5, style="italic", color="#475569")

    draw_actor(1.7, 5.0, "Staf Humas", "Operator & Penulis")
    draw_actor(13.8, 6.8, "Kepala Bidang\n/ Pimpinan", "Verifikator & Approval")
    draw_actor(13.8, 2.7, "Administrator\nSistem", "Pengelola Sistem")

    use_cases = [
        ("UC-1: Melakukan Autentikasi Pengguna (Login)", 7.75, 7.85),
        ("UC-2: Menginput Data Agenda & Fakta 5W+1H (Wizard)", 7.75, 7.20),
        ("UC-3: Mengunggah & Memvalidasi Foto Dokumentasi", 7.75, 6.55),
        ("UC-4: Membentuk Draf Berita Otomatis (Gemini AI)", 7.75, 5.90),
        ("UC-5: Melakukan Review Komparasi Kutipan Narasumber", 7.75, 5.25),
        ("UC-6: Menyunting Naskah pada Live Editor", 7.75, 4.60),
        ("UC-7: Mengajukan Naskah ke Verifikasi Terpusat", 7.75, 3.95),
        ("UC-8: Menelaah Naskah & Memberikan Catatan Revisi", 7.75, 3.30),
        ("UC-9: Menyetujui Naskah Berita (Approval ACC)", 7.75, 2.65),
        ("UC-10: Mengekspor Dokumen Resmi MS Word (.docx)", 7.75, 2.00),
        ("UC-11: Menerbitkan Berita ke Portal Web & Medsos", 7.75, 1.35),
        ("UC-12: Mengelola Repositori Arsip Publikasi Terpusat", 7.75, 0.70),
    ]

    for name, cx, cy in use_cases:
        oval = patches.Ellipse((cx, cy), 6.8, 0.48, ec="#0284c7", fc="#f0f9ff", lw=1.2)
        ax.add_patch(oval)
        ax.text(cx, cy, name, ha="center", va="center", fontsize=7.8, color="#0369a1", fontweight="bold")

    staf_pos = (2.2, 5.0)
    for uc_idx in [0, 1, 2, 3, 4, 5, 6, 9, 10, 11]:
        cx, cy = use_cases[uc_idx][1], use_cases[uc_idx][2]
        ax.plot([staf_pos[0], cx - 3.4], [staf_pos[1], cy], color="#64748b", lw=1.0)

    pim_pos = (13.0, 6.5)
    for uc_idx in [0, 7, 8, 11]:
        cx, cy = use_cases[uc_idx][1], use_cases[uc_idx][2]
        ax.plot([pim_pos[0], cx + 3.4], [pim_pos[1], cy], color="#64748b", lw=1.0)

    admin_pos = (13.0, 2.7)
    for uc_idx in [0, 11]:
        cx, cy = use_cases[uc_idx][1], use_cases[uc_idx][2]
        ax.plot([admin_pos[0], cx + 3.4], [admin_pos[1], cy], color="#64748b", lw=1.0, linestyle="--")

    plt.tight_layout()
    target = out_img("gambar_3_4_use_case_usulan.png")
    plt.savefig(target, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {target}")


def generate_activity_usulan_chart():
    fig, ax = plt.subplots(figsize=(15.5, 9.8), dpi=300)
    ax.set_xlim(0, 15.5)
    ax.set_ylim(0, 10.0)
    ax.axis("off")
    fig.patch.set_facecolor("#ffffff")

    ax.text(
        7.75,
        9.65,
        "ACTIVITY DIAGRAM SISTEM USULAN APLIKASI PRESS RELEASE AUTO-GENERATOR",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="#111827",
    )
    ax.text(
        7.75,
        9.35,
        "Alur Kerja Otomatisasi Publikasi Berita Humas Diskominfo Kota Contoh",
        ha="center",
        va="center",
        fontsize=9.5,
        style="italic",
        color="#475569",
    )

    lane_y_bot = 0.35
    headers = [
        ("STAF HUMAS", 0.5, 3.5),
        ("SISTEM AUTO-GENERATOR (WEB & AI)", 4.1, 4.2),
        ("PIMPINAN / KEPALA BIDANG", 8.4, 3.5),
        ("PORTAL PUBLIKASI & ARSIP", 12.0, 3.1),
    ]
    for title, lx, lw in headers:
        rect = patches.Rectangle((lx, 8.7), lw, 0.45, ec="#1f2937", fc="#e5e7eb", lw=1.2)
        ax.add_patch(rect)
        ax.text(lx + lw / 2, 8.92, title, ha="center", va="center", fontsize=8.5, fontweight="bold", color="#1f2937")
        ax.plot([lx, lx], [lane_y_bot, 8.7], color="#9ca3af", lw=1.0, linestyle=":")
    ax.plot([15.1, 15.1], [lane_y_bot, 8.7], color="#9ca3af", lw=1.0, linestyle=":")

    def draw_act(cx, cy, text, w=3.1, h=0.52, bg="#ffffff", ec="#1f2937"):
        rect = patches.FancyBboxPatch(
            (cx - w / 2, cy - h / 2), w, h, boxstyle="round,pad=0.05,rounding_size=0.15", ec=ec, fc=bg, lw=1.1
        )
        ax.add_patch(rect)
        ax.text(cx, cy, text, ha="center", va="center", fontsize=7.2, color="#111827", fontfamily="sans-serif")

    start_c = patches.Circle((2.25, 8.35), 0.12, fc="#000000")
    ax.add_patch(start_c)
    ax.annotate("", xy=(2.25, 7.95), xytext=(2.25, 8.23), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))

    draw_act(2.25, 7.68, "Meliput kegiatan & mengisi\nformulir 5W+1H, kutipan, & foto")
    ax.plot([3.8, 6.2], [7.68, 7.68], color="#000000", lw=1.2)
    ax.annotate("", xy=(6.2, 7.3), xytext=(6.2, 7.68), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))

    draw_act(6.2, 7.05, "Validasi skema form (Zod) &\nvalidasi biner gambar (magic bytes)", w=3.8, bg="#f0f9ff", ec="#0284c7")
    ax.annotate("", xy=(6.2, 6.4), xytext=(6.2, 6.79), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))

    draw_act(6.2, 6.15, "Proses prompt terstruktur via\nGoogle Gemini AI Engine", w=3.8, bg="#eff6ff", ec="#2563eb")
    ax.annotate("", xy=(6.2, 5.5), xytext=(6.2, 5.89), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))

    draw_act(6.2, 5.25, "Generate draf berita piramida\nterbalik & sinkronkan kutipan", w=3.8, bg="#f0fdf4", ec="#16a34a")
    ax.plot([4.3, 2.25], [5.25, 5.25], color="#000000", lw=1.2)
    ax.annotate("", xy=(2.25, 4.85), xytext=(2.25, 5.25), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))

    draw_act(2.25, 4.6, "Review kutipan berdampingan &\nsunting draf pada Live Editor")
    ax.annotate("", xy=(2.25, 3.9), xytext=(2.25, 4.34), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))

    draw_act(2.25, 3.65, "Kirim pengajuan verifikasi draf\nmelalui modul sistem terpusat")
    ax.plot([3.8, 10.15], [3.65, 3.65], color="#000000", lw=1.2)
    ax.annotate("", xy=(10.15, 3.25), xytext=(10.15, 3.65), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))

    draw_act(10.15, 3.0, "Buka draf via dashboard &\ntelaah akurasi materi publikasi", w=3.1)
    ax.annotate("", xy=(10.15, 2.38), xytext=(10.15, 2.74), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))

    diamond = patches.Polygon([[10.15, 2.28], [10.75, 1.98], [10.15, 1.68], [9.55, 1.98]], ec="#b45309", fc="#fef3c7", lw=1.2)
    ax.add_patch(diamond)
    ax.text(10.15, 1.98, "Disetujui?", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#92400e")

    ax.plot([9.55, 8.8], [1.98, 1.98], color="#b91c1c", lw=1.2)
    ax.text(9.0, 2.12, "[Revisi]", fontsize=6.8, color="#b91c1c", fontweight="bold")
    ax.plot([8.8, 8.8], [1.98, 4.6], color="#b91c1c", lw=1.2)
    ax.annotate("", xy=(3.8, 4.6), xytext=(8.8, 4.6), arrowprops=dict(arrowstyle="->", lw=1.0, color="#b91c1c"))

    ax.annotate("", xy=(10.15, 1.05), xytext=(10.15, 1.68), arrowprops=dict(arrowstyle="->", lw=1.2, color="#15803d"))
    ax.text(10.3, 1.4, "[Ya / ACC]", fontsize=6.8, color="#15803d", fontweight="bold")
    draw_act(10.15, 0.8, "Klik \"Setujui / ACC\" naskah\npada dashboard verifikasi", w=3.1, bg="#f0fdf4", ec="#15803d")

    ax.plot([8.6, 6.2], [0.8, 0.8], color="#000000", lw=1.2)
    ax.annotate("", xy=(6.2, 1.55), xytext=(6.2, 0.8), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))
    draw_act(6.2, 1.8, "Auto-generate dokumen resmi\nWord (.docx) ber-kop Instansi", w=3.8, bg="#fef9c3", ec="#ca8a04")

    ax.plot([8.1, 13.55], [1.8, 1.8], color="#000000", lw=1.2)
    ax.annotate("", xy=(13.55, 1.45), xytext=(13.55, 1.8), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))
    draw_act(13.55, 1.2, "Auto-arsip naskah final, foto &\nriwayat versi ke Cloud Storage", w=2.8, bg="#f0f9ff", ec="#0284c7")

    ax.plot([6.2, 2.25], [2.06, 2.06], color="#000000", lw=1.2)
    ax.annotate("", xy=(2.25, 2.3), xytext=(2.25, 2.06), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))
    draw_act(2.25, 2.55, "Unduh berkas .docx resmi &\npublikasi ke Portal Web & Medsos")
    ax.annotate("", xy=(2.25, 1.5), xytext=(2.25, 2.29), arrowprops=dict(arrowstyle="->", lw=1.2, color="#000000"))

    end_outer = patches.Circle((2.25, 1.35), 0.14, ec="#000000", fc="#ffffff", lw=1.5)
    end_inner = patches.Circle((2.25, 1.35), 0.08, fc="#000000")
    ax.add_patch(end_outer)
    ax.add_patch(end_inner)

    plt.tight_layout()
    target = out_img("gambar_3_5_activity_diagram_usulan.png")
    plt.savefig(target, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {target}")


def generate_ui_mockup_chart():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16.0, 9.2), dpi=300)
    fig.patch.set_facecolor("#f8fafc")

    # PANEL 1: Form Wizard
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 12)
    ax1.axis("off")
    ax1.set_facecolor("#ffffff")

    card1 = patches.FancyBboxPatch((0.4, 0.4), 9.2, 11.2, boxstyle="round,pad=0.1,rounding_size=0.2", ec="#cbd5e1", fc="#ffffff", lw=1.5)
    ax1.add_patch(card1)

    topbar1 = patches.Rectangle((0.4, 10.6), 9.2, 1.0, ec="#0284c7", fc="#0284c7")
    ax1.add_patch(topbar1)
    ax1.text(5.0, 11.1, "DISKOMINFO PRESS RELEASE AUTO-GENERATOR", ha="center", va="center", color="#ffffff", fontsize=9.5, fontweight="bold")
    ax1.text(5.0, 10.8, "Form Wizard: Input Data Kegiatan & Parameter 5W+1H Terstruktur", ha="center", va="center", color="#e0f2fe", fontsize=7.5)

    steps = [("1. Info Acara", True), ("2. Fakta 5W+1H", True), ("3. Kutipan Pejabat", False), ("4. Foto & Generate", False)]
    for idx, (st_name, active) in enumerate(steps):
        sx = 0.8 + idx * 2.2
        s_rect = patches.FancyBboxPatch((sx, 9.9), 1.9, 0.5, boxstyle="round,pad=0.03,rounding_size=0.08", ec="#0284c7" if active else "#cbd5e1", fc="#e0f2fe" if active else "#f1f5f9", lw=1.2)
        ax1.add_patch(s_rect)
        ax1.text(sx + 0.95, 10.15, st_name, ha="center", va="center", fontsize=7.0, fontweight="bold" if active else "normal", color="#0369a1" if active else "#64748b")

    fields = [
        ("Nama Agenda Kedinasan *", "Sosialisasi Keterbukaan Informasi Publik 2026 Tingkat Kota Contoh", 9.0),
        ("Seksi / Unit Kerja Penyelenggara *", "Bidang Pengelolaan Informasi dan Komunikasi Publik", 7.9),
        ("Waktu & Tempat Pelaksanaan *", "Kamis, 22 Oktober 2026 | Aula Utama Diskominfo Kota Contoh", 6.8),
        ("Fakta What & Who (Pokok Acara & Pejabat) *", "Forum koordinasi PPID daerah, dipimpin Kepala Dinas Kominfo Kota Contoh", 5.7),
        ("Fakta Why & How (Tujuan & Kronologi Acara) *", "Meningkatkan transparansi layanan informasi publik & standar rilis berita daerah", 4.4),
        ("Narasumber & Kutipan Langsung *", "Kepala Dinas Contoh: \"Keterbukaan informasi publik adalah fondasi layanan transparan.\"", 3.1),
    ]

    for label, val, fy in fields:
        ax1.text(0.9, fy + 0.45, label, fontsize=7.5, fontweight="bold", color="#1e293b")
        h_box = 0.5 if "How" not in label and "Narasumber" not in label else 0.65
        f_box = patches.FancyBboxPatch((0.9, fy - h_box + 0.35), 8.2, h_box, boxstyle="round,pad=0.04,rounding_size=0.08", ec="#94a3b8", fc="#f8fafc", lw=1.0)
        ax1.add_patch(f_box)
        ax1.text(1.1, fy - h_box / 2 + 0.35, val, fontsize=7.2, color="#334155", va="center")

    btn_gen = patches.FancyBboxPatch((5.4, 0.8), 3.7, 0.7, boxstyle="round,pad=0.06,rounding_size=0.12", ec="#16a34a", fc="#16a34a", lw=1.0)
    ax1.add_patch(btn_gen)
    ax1.text(7.25, 1.15, "Generate Siaran Pers (Gemini AI)", ha="center", va="center", color="#ffffff", fontsize=8.0, fontweight="bold")

    ax1.text(5.0, 0.15, "(a) Rancangan Formulir Stepper Input Berita (5W+1H & Narasumber)", ha="center", va="center", fontsize=9.0, fontweight="bold", color="#0f172a")

    # PANEL 2: Live Editor & Review
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 12)
    ax2.axis("off")
    ax2.set_facecolor("#ffffff")

    card2 = patches.FancyBboxPatch((0.4, 0.4), 9.2, 11.2, boxstyle="round,pad=0.1,rounding_size=0.2", ec="#cbd5e1", fc="#ffffff", lw=1.5)
    ax2.add_patch(card2)

    topbar2 = patches.Rectangle((0.4, 10.6), 9.2, 1.0, ec="#15803d", fc="#15803d")
    ax2.add_patch(topbar2)
    ax2.text(5.0, 11.1, "LIVE EDITOR & PRATINJAU SIARAN PERS RESMI", ha="center", va="center", color="#ffffff", fontsize=9.5, fontweight="bold")
    ax2.text(5.0, 10.8, "Review Komparasi Kutipan, Status Approval, & Ekspor Dokumen DOCX", ha="center", va="center", color="#dcfce7", fontsize=7.5)

    stat_rect = patches.FancyBboxPatch((0.8, 9.9), 8.4, 0.5, boxstyle="round,pad=0.04,rounding_size=0.08", ec="#bbf7d0", fc="#f0fdf4", lw=1.0)
    ax2.add_patch(stat_rect)
    ax2.text(1.0, 10.15, "Status Dokumen: Disetujui (Approved by Kepala Bidang)", fontsize=7.5, fontweight="bold", color="#15803d", va="center")
    ax2.text(8.8, 10.15, "Verifikasi: ACC [OK]", ha="right", fontsize=7.5, fontweight="bold", color="#15803d", va="center")

    ax2.text(0.9, 9.55, "Modul Komparasi Kutipan Narasumber (Pencegah Halusinasi):", fontsize=7.5, fontweight="bold", color="#1e293b")
    q_box = patches.FancyBboxPatch((0.9, 8.4), 8.2, 1.0, boxstyle="round,pad=0.04,rounding_size=0.08", ec="#e2e8f0", fc="#f8fafc", lw=1.0)
    ax2.add_patch(q_box)
    ax2.text(1.1, 9.15, "Kutipan Mentah Input: \"Keterbukaan informasi fondasi layanan transparan\"", fontsize=6.8, style="italic", color="#64748b")
    ax2.text(1.1, 8.65, "Hasil Narasi AI: Kepala Dinas Kominfo Kota Contoh menegaskan bahwa\nketerbukaan informasi publik adalah fondasi layanan yang transparan.", fontsize=7.0, color="#15803d", fontweight="bold")

    ax2.text(0.9, 8.0, "Pratinjau Tata Letak Format Dokumen Resmi (Word Layout Preview):", fontsize=7.5, fontweight="bold", color="#1e293b")
    doc_sheet = patches.Rectangle((0.9, 1.8), 8.2, 6.0, ec="#94a3b8", fc="#ffffff", lw=1.2)
    ax2.add_patch(doc_sheet)

    ax2.text(5.0, 7.45, "PEMERINTAH KOTA CONTOH\nDINAS KOMUNIKASI DAN INFORMATIKA\nSIARAN PERS RESMI", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#0f172a")
    ax2.plot([1.3, 8.7], [7.0, 7.0], color="#0f172a", lw=1.5)

    lead_text = (
        "KOTA CONTOH (Diskominfo) - Dinas Komunikasi dan Informatika Kota Contoh\n"
        "menggelar Forum Koordinasi Keterbukaan Informasi Publik 2026 yang dihadiri\n"
        "oleh seluruh perwakilan PPID kecamatan di aula utama pada Kamis (22/10/2026).\n\n"
        "Dalam sambutannya, Kepala Dinas Kominfo Kota Contoh menegaskan bahwa\n"
        "keterbukaan informasi publik merupakan fondasi tata kelola pemerintahan yang\n"
        "transparan dan responsif terhadap kebutuhan masyarakat.\n\n"
        "Kegiatan dilanjutkan dengan penandatanganan standar operasional layanan PPID..."
    )
    ax2.text(1.3, 5.5, lead_text, fontsize=6.8, color="#334155", va="center", linespacing=1.35)

    btn_exp = patches.FancyBboxPatch((4.8, 0.8), 4.3, 0.7, boxstyle="round,pad=0.06,rounding_size=0.12", ec="#1e40af", fc="#1e40af", lw=1.0)
    ax2.add_patch(btn_exp)
    ax2.text(6.95, 1.15, "Ekspor Dokumen Resmi (.docx)", ha="center", va="center", color="#ffffff", fontsize=8.0, fontweight="bold")

    ax2.text(5.0, 0.15, "(b) Rancangan Modul Review Kutipan, Live Editor, & Ekspor Dokumen", ha="center", va="center", fontsize=9.0, fontweight="bold", color="#0f172a")

    plt.tight_layout()
    target = out_img("gambar_3_6_rancangan_antarmuka_generator.png")
    plt.savefig(target, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {target}")


if __name__ == "__main__":
    generate_org_chart()
    generate_use_case_chart()
    generate_activity_diagram()
    generate_apk_attack_and_liability_diagram()
    generate_use_case_usulan_chart()
    generate_activity_usulan_chart()
    generate_ui_mockup_chart()
