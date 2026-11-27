# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "pillow"]
# ///
"""
Script to generate publication-grade technical audit diagrams for the
IT Audit Project Report of Portal Akademik Perguruan Tinggi Contoh (Simulation) using COBIT 2019.
Output: High-DPI PNGs saved into template/gambar/
"""

import argparse
import os

plt = None
patches = None

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _default_output_dir():
    if os.path.exists(os.path.join(ROOT_DIR, "package.json")):
        return os.path.join(ROOT_DIR, "template", "gambar")
    return os.path.join(os.getcwd(), "audit_diagrams")


GAMBAR_DIR = _default_output_dir()


def _ensure_matplotlib():
    global plt, patches
    if plt is None or patches is None:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as _plt
        import matplotlib.patches as _patches
        plt = _plt
        patches = _patches
    os.makedirs(GAMBAR_DIR, exist_ok=True)


def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(13, 8.5), dpi=300)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 9.5)
    ax.axis("off")
    fig.patch.set_facecolor("#ffffff")

    # Title
    ax.text(
        6.5,
        9.1,
        "ARSITEKTUR MULTI-TIER & KEAMANAN PORTAL AKADEMIK PERGURUAN TINGGI CONTOH (SIMULASI)",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color="#0f172a",
        fontfamily="sans-serif",
    )

    def draw_rounded_rect(x, y, w, h, bg="#f8fafc", border="#64748b", lw=1.2, r=0.15):
        rect = patches.FancyBboxPatch(
            (x, y), w, h, boxstyle=f"round,pad=0.04,rounding_size={r}", ec=border, fc=bg, lw=lw
        )
        ax.add_patch(rect)
        return rect

    # Top: Clients
    draw_rounded_rect(1.0, 7.8, 11.0, 0.9, bg="#eff6ff", border="#3b82f6", lw=1.5)
    ax.text(6.5, 8.25, "KLIEN CIVITAS AKADEMIKA PERGURUAN TINGGI CONTOH\n(Portal Mahasiswa, Portal Dosen, Aplikasi Mobile, Integrasi PDDikti)",
            ha="center", va="center", fontsize=9.5, fontweight="bold", color="#1e3a8a")

    # Arrow down
    ax.annotate("", xy=(6.5, 7.2), xytext=(6.5, 7.8),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#2563eb"))
    ax.text(6.7, 7.5, "HTTPS / TLS 1.3 (Cipher Suite AES-256-GCM)", fontsize=8, color="#2563eb", fontweight="bold")

    # Perimeter: NGFW & WAF
    draw_rounded_rect(1.0, 6.4, 11.0, 0.8, bg="#fef2f2", border="#ef4444", lw=1.5)
    ax.text(6.5, 6.8, "PERIMETER SECURITY: FIREWALL GATEWAY (NGFW) & WEB APPLICATION FIREWALL (WAF)\n(Inspeksi Paket Mendalam, Proteksi Anti-DDoS, Mitigasi Serangan OWASP Top 10)",
            ha="center", va="center", fontsize=9, fontweight="bold", color="#991b1b")

    # Arrow down
    ax.annotate("", xy=(6.5, 5.8), xytext=(6.5, 6.4),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#dc2626"))

    # DMZ Zone
    draw_rounded_rect(1.0, 4.9, 11.0, 0.9, bg="#fffbeb", border="#f59e0b", lw=1.5)
    ax.text(1.2, 5.6, "DEMILITARIZED ZONE (DMZ) - VLAN 10", fontsize=8.5, fontweight="bold", color="#92400e")
    ax.text(6.5, 5.3, "Nginx Reverse Proxy & Load Balancer (Cluster Aktif-Pasif)\nSSL/TLS Termination, Security Headers (HSTS, CSP, X-Frame-Options), Rate Limiting Akses KRS",
            ha="center", va="center", fontsize=8.5, color="#78350f")

    # Arrow down
    ax.annotate("", xy=(6.5, 4.3), xytext=(6.5, 4.9),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#d97706"))

    # Application Zone
    draw_rounded_rect(1.0, 3.3, 11.0, 1.0, bg="#f0fdf4", border="#16a34a", lw=1.5)
    ax.text(1.2, 4.1, "APPLICATION & SERVICE ZONE - VLAN 20", fontsize=8.5, fontweight="bold", color="#166534")
    ax.text(6.5, 3.75, "Cluster Engine Aplikasi Portal Akademik (PHP 8.2 / Framework Laravel Modern)\nWorker Antrean Asinkron (Redis Queue), API Feeder PDDikti Kemendikbudristek, Host-to-Host Payment Gateway",
            ha="center", va="center", fontsize=8.5, color="#14532d")

    # Arrow down
    ax.annotate("", xy=(6.5, 2.7), xytext=(6.5, 3.3),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#15803d"))

    # Database Zone & Management Zone side by side
    draw_rounded_rect(1.0, 0.6, 6.0, 2.1, bg="#faf5ff", border="#9333ea", lw=1.5)
    ax.text(1.2, 2.5, "DATA STORAGE ZONE - VLAN 30", fontsize=8.5, fontweight="bold", color="#6b21a8")
    ax.text(4.0, 1.6, "Kluster Basis Data Portal Akademik\n- Node Utama (Primary/Master MySQL): Transaksi Tulis KRS & Nilai\n- Node Replikasi (Read Replica): Pelaporan & Transkrip\n- In-Memory Cache (Redis Cluster): Session Store Mahasiswa\n[Simulasi Audit: Pengujian enkripsi data at rest AES-256 / TDE]",
            ha="center", va="center", fontsize=8, color="#581c87")

    draw_rounded_rect(7.5, 0.6, 4.5, 2.1, bg="#f1f5f9", border="#475569", lw=1.5)
    ax.text(7.7, 2.5, "MANAGEMENT & DR ZONE - VLAN 40", fontsize=8.5, fontweight="bold", color="#334155")
    ax.text(9.75, 1.6, "- Bastion Jump Server (MFA SSH)\n- Storage NAS On-Premise (Backup Harian)\n- Mirror Cloud DR (Sinkronisasi Mingguan)\n- Zabbix / Prometheus Monitoring\n[Simulasi Audit: Evaluasi jadwal uji pemulihan backup]",
            ha="center", va="center", fontsize=8, color="#1e293b")

    # Inter-zone link
    ax.annotate("", xy=(7.5, 1.6), xytext=(7.0, 1.6),
                arrowprops=dict(arrowstyle="<->", lw=1.2, color="#475569", ls="--"))

    out_path = os.path.join(GAMBAR_DIR, "diagram_arsitektur_siakad.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated: {out_path}")


def generate_org_chart():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8.5)
    ax.axis("off")
    fig.patch.set_facecolor("#ffffff")

    ax.text(
        6.0,
        8.1,
        "STRUKTUR ORGANISASI PENGELOLA TI (UPT TIK) PERGURUAN TINGGI CONTOH (SIMULASI)",
        ha="center",
        va="center",
        fontsize=11.5,
        fontweight="bold",
        color="#0f172a",
        fontfamily="sans-serif",
    )

    def draw_box(x, y, w, h, title, sub, bg="#f8fafc", border="#3b82f6", lw=1.4):
        rect = patches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.04,rounding_size=0.15", ec=border, fc=bg, lw=lw
        )
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h * 0.65, title, ha="center", va="center", fontsize=9, fontweight="bold", color="#0f172a")
        ax.text(x + w / 2, y + h * 0.3, sub, ha="center", va="center", fontsize=7.5, color="#475569")

    # Level 1: Kepala UPT TIK
    draw_box(4.25, 6.6, 3.5, 0.9, "KEPALA UPT TIK CONTOH", "Penetapan Strategi, Kebijakan & Tata Kelola TI", bg="#dbeafe", border="#1d4ed8", lw=2.0)

    # DPO (Staff / Penasihat Khusus di samping)
    draw_box(8.5, 6.6, 2.8, 0.9, "TIM KEPATUHAN & DPO*", "*Rekomendasi MEA03: SK Rektor DPO UU PDP", bg="#fee2e2", border="#dc2626", lw=1.5)
    ax.annotate("", xy=(8.5, 7.05), xytext=(7.75, 7.05),
                arrowprops=dict(arrowstyle="-", lw=1.2, color="#dc2626", ls="--"))

    # Vertical bus from Kepala UPT
    ax.plot([6.0, 6.0], [6.6, 5.8], color="#1d4ed8", lw=1.8)
    ax.plot([1.5, 10.5], [5.8, 5.8], color="#1d4ed8", lw=1.8)

    # 4 Units below
    # Unit 1: Pengembangan Sistem
    ax.plot([1.5, 1.5], [5.8, 5.1], color="#1d4ed8", lw=1.8)
    draw_box(0.2, 4.0, 2.6, 1.1, "KOORDINATOR SISTEM &\nPENGEMBANGAN APLIKASI", "Manajemen Perubahan (BAI06)\nProgrammer Portal & Mobile", bg="#f0fdf4", border="#16a34a")

    # Unit 2: Infrastruktur & Jaringan
    ax.plot([4.5, 4.5], [5.8, 5.1], color="#1d4ed8", lw=1.8)
    draw_box(3.2, 4.0, 2.6, 1.1, "KOORDINATOR JARINGAN &\nINFRASTRUKTUR DATA CENTER", "Operasional & Fasilitas (DSS01)\nSysadmin, Network Admin, NGFW", bg="#f0fdf4", border="#16a34a")

    # Unit 3: Database & Keamanan
    ax.plot([7.5, 7.5], [5.8, 5.1], color="#1d4ed8", lw=1.8)
    draw_box(6.2, 4.0, 2.6, 1.1, "DATABASE ADMINISTRATOR (DBA)\n& PETUGAS KEAMANAN TI", "Manajemen Keamanan (APO13/DSS05)\nBackup, Enkripsi, Hak Akses RBAC", bg="#fef3c7", border="#d97706")

    # Unit 4: Layanan Pengguna & Helpdesk
    ax.plot([10.5, 10.5], [5.8, 5.1], color="#1d4ed8", lw=1.8)
    draw_box(9.2, 4.0, 2.6, 1.1, "DUKUNGAN PENGGUNA &\nHELPDESK PORTAL", "Tiket Insiden & Layanan Mahasiswa\nVerifikasi Masalah Akademik", bg="#f0fdf4", border="#16a34a")

    # Operational staff level
    def draw_sub_box(x, y, w, h, text, bg="#ffffff", border="#94a3b8"):
        rect = patches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.03,rounding_size=0.1", ec=border, fc=bg, lw=1.0
        )
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=7.5, color="#1e293b")

    # Sub under Unit 1
    ax.plot([1.5, 1.5], [4.0, 3.4], color="#16a34a", lw=1.2)
    draw_sub_box(0.2, 2.4, 2.6, 0.9, "- Web Programmer Portal\n- Mobile App Developer\n- QA / Software Tester")

    # Sub under Unit 2
    ax.plot([4.5, 4.5], [4.0, 3.4], color="#16a34a", lw=1.2)
    draw_sub_box(3.2, 2.4, 2.6, 0.9, "- Server / Linux Administrator\n- Network Engineer (FortiGate)\n- Data Center Facilities Operator")

    # Sub under Unit 3
    ax.plot([7.5, 7.5], [4.0, 3.4], color="#d97706", lw=1.2)
    draw_sub_box(6.2, 2.4, 2.6, 0.9, "- MySQL Database Administrator\n- Information Security Officer\n- Backup & Storage Specialist")

    # Sub under Unit 4
    ax.plot([10.5, 10.5], [4.0, 3.4], color="#16a34a", lw=1.2)
    draw_sub_box(9.2, 2.4, 2.6, 0.9, "- Operator Layanan Helpdesk\n- Staf Registrasi & Akun Civitas\n- Pemantau Log Tiket Gangguan")

    # Bottom note on Segregation of Duties
    rect_note = patches.FancyBboxPatch(
        (0.2, 0.6), 11.6, 1.2, boxstyle="round,pad=0.05,rounding_size=0.15", ec="#cbd5e1", fc="#f8fafc", lw=1.2
    )
    ax.add_patch(rect_note)
    ax.text(6.0, 1.35, "ANALISIS PEMISAHAN TUGAS (SEGREGATION OF DUTIES / SoD) HASIL AUDIT:",
            ha="center", va="center", fontsize=8.5, fontweight="bold", color="#0f172a")
    ax.text(6.0, 0.95, "✓ Pemisahan Pengembang dan Akses Root Produksi telah terpenuhi secara memadai.\n✗ Peran Information Security Officer masih dirangkap oleh Network Engineer, dan DBA merangkap backup operator tanpa verifikasi independen.\n* Pembentukan Tim Kepatuhan TI dan DPO merupakan rekomendasi kritis proses MEA03.",
            ha="center", va="center", fontsize=7.5, color="#334155")

    out_path = os.path.join(GAMBAR_DIR, "diagram_organisasi_upt_tik.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated: {out_path}")


def generate_risk_matrix():
    fig, ax = plt.subplots(figsize=(9, 8), dpi=300)
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0.5, 5.5)
    fig.patch.set_facecolor("#ffffff")

    # Grid colors based on Likelihood x Impact
    # L: 1 to 5, I: 1 to 5
    for l in range(1, 6):
        for i in range(1, 6):
            score = l * i
            if score >= 10:
                color = "#fecaca"  # High (Red)
                border = "#ef4444"
            elif score >= 5:
                color = "#fef08a"  # Medium (Yellow)
                border = "#eab308"
            else:
                color = "#bbf7d0"  # Low (Green)
                border = "#22c55e"
            rect = patches.Rectangle((i - 0.48, l - 0.48), 0.96, 0.96, ec=border, fc=color, lw=1.0)
            ax.add_patch(rect)
            if (l, i) not in {(4, 5), (4, 4), (3, 5), (3, 4)}:
                ax.text(i, l, f"Skor {score}", ha="center", va="center", fontsize=8, color="#475569", alpha=0.6)

    # Plot the 5 audit findings
    # 1. APO13: L=4, I=5, Score=20
    ax.plot(5, 4, "o", markersize=31, color="#b91c1c", markeredgecolor="#ffffff", markeredgewidth=2)
    ax.text(5, 4, "APO13\n(20)", ha="center", va="center", fontsize=7.0, fontweight="bold", color="#ffffff", zorder=5)

    # 2. BAI06: L=4, I=4, Score=16
    ax.plot(4, 4.15, "o", markersize=31, color="#dc2626", markeredgecolor="#ffffff", markeredgewidth=2)
    ax.text(4, 4.15, "BAI06\n(16)", ha="center", va="center", fontsize=7.0, fontweight="bold", color="#ffffff", zorder=5)

    # 4. DSS05: L=4, I=4, Score=16 (shift slightly)
    ax.plot(4, 3.85, "o", markersize=31, color="#ea580c", markeredgecolor="#ffffff", markeredgewidth=2)
    ax.text(4, 3.85, "DSS05\n(16)", ha="center", va="center", fontsize=7.0, fontweight="bold", color="#ffffff", zorder=5)

    # 3. DSS01: L=3, I=5, Score=15
    ax.plot(5, 3, "o", markersize=31, color="#c2410c", markeredgecolor="#ffffff", markeredgewidth=2)
    ax.text(5, 3, "DSS01\n(15)", ha="center", va="center", fontsize=7.0, fontweight="bold", color="#ffffff", zorder=5)

    # 5. MEA03: L=3, I=4, Score=12
    ax.plot(4, 3, "o", markersize=31, color="#d97706", markeredgecolor="#ffffff", markeredgewidth=2)
    ax.text(4, 3, "MEA03\n(12)", ha="center", va="center", fontsize=7.0, fontweight="bold", color="#ffffff", zorder=5)

    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xticklabels(["1\nTidak Signifikan", "2\nKecil", "3\nSedang", "4\nBesar", "5\nKritis / Bencana"], fontsize=8)
    ax.set_xlabel("DAMPAK RISIKO (IMPACT)", fontsize=9.5, fontweight="bold", labelpad=10)

    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1 - Sangat Jarang", "2 - Jarang", "3 - Mungkin", "4 - Sering", "5 - Hampir Pasti"], fontsize=8)
    ax.set_ylabel("KEMUNGKINAN TERJADI (LIKELIHOOD)", fontsize=9.5, fontweight="bold", labelpad=10)

    ax.set_title("MATRIKS PENILAIAN RISIKO (RISK REGISTER 5x5)\nPADA PORTAL AKADEMIK PERGURUAN TINGGI CONTOH (SIMULASI)",
                 fontsize=10.5, fontweight="bold", pad=15, color="#0f172a")

    # Legend
    legend_elements = [
        patches.Patch(facecolor="#fecaca", edgecolor="#ef4444", label="Tinggi (10 - 25) : Perlu Mitigasi Segera"),
        patches.Patch(facecolor="#fef08a", edgecolor="#eab308", label="Sedang (5 - 9) : Perlu Pengendalian Terjadwal"),
        patches.Patch(facecolor="#bbf7d0", edgecolor="#22c55e", label="Rendah (1 - 4) : Risiko Dapat Ditoleransi"),
    ]
    ax.legend(handles=legend_elements, loc="upper left", bbox_to_anchor=(0.02, 0.98), fontsize=8, framealpha=0.95)

    out_path = os.path.join(GAMBAR_DIR, "diagram_risk_matrix.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated: {out_path}")


def generate_capability_chart():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    fig.patch.set_facecolor("#ffffff")

    domains = ["APO13\n(Managed Security)", "BAI06\n(Managed Changes)", "DSS01\n(Managed Operations)",
               "DSS05\n(Security Services)", "MEA03\n(Compliance)", "RATA-RATA\n(Tata Kelola)"]
    current_levels = [2.0, 1.0, 2.0, 1.0, 1.0, 1.4]
    target_levels = [3.0, 3.0, 4.0, 3.0, 3.0, 3.2]

    x = range(len(domains))
    width = 0.35

    rects1 = ax.bar([p - width / 2 for p in x], current_levels, width, label="Capaian Saat Ini (Current Level)",
                    color="#f87171", edgecolor="#dc2626", lw=1.2)
    rects2 = ax.bar([p + width / 2 for p in x], target_levels, width, label="Tingkat Target (Target Level)",
                    color="#60a5fa", edgecolor="#2563eb", lw=1.2)

    ax.set_ylabel("Tingkat Kapabilitas COBIT 2019 (Skala 0 - 5)", fontsize=9.5, fontweight="bold")
    ax.set_title("PERBANDINGAN TINGKAT KAPABILITAS EKSISTING VS TARGET\nPADA 5 DOMAIN COBIT 2019 PERGURUAN TINGGI CONTOH (SIMULASI)",
                 fontsize=10.5, fontweight="bold", pad=15, color="#0f172a")
    ax.set_xticks(list(x))
    ax.set_xticklabels(domains, fontsize=8.5)
    ax.set_ylim(0, 5.0)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    # Annotate bars
    def autolabel(rects, is_target=False):
        for rect in rects:
            height = rect.get_height()
            offset = 0.08
            label = f"Lv. {height:.1f}" if not height.is_integer() else f"Lv. {int(height)}"
            ax.annotate(label,
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 4), textcoords="offset points",
                        ha="center", va="bottom", fontsize=8, fontweight="bold",
                        color="#1d4ed8" if is_target else "#b91c1c")

    autolabel(rects1)
    autolabel(rects2, is_target=True)

    # Annotate gaps
    for i in range(len(domains)):
        gap = target_levels[i] - current_levels[i]
        ax.annotate(f"Gap: {gap:.1f}",
                    xy=(i, target_levels[i] + 0.35),
                    ha="center", va="bottom", fontsize=8, fontweight="bold",
                    color="#475569", bbox=dict(boxstyle="round,pad=0.2", fc="#f1f5f9", ec="#94a3b8", lw=0.8))

    ax.legend(loc="upper right", fontsize=8.5, framealpha=0.9)

    out_path = os.path.join(GAMBAR_DIR, "diagram_radar_capability.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated: {out_path}")


def generate_roadmap_diagram():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(-0.6, 8.6)
    ax.axis("off")
    fig.patch.set_facecolor("#ffffff")

    ax.text(
        6.0,
        8.2,
        "PETA JALAN (ROADMAP) PENINGKATAN TATA KELOLA PORTAL AKADEMIK CONTOH (SIMULASI)",
        ha="center",
        va="center",
        fontsize=11.5,
        fontweight="bold",
        color="#0f172a",
        fontfamily="sans-serif",
    )

    def draw_phase(x, y, w, h, phase_num, title, timeline, items, bg="#f8fafc", border="#3b82f6"):
        rect = patches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.06,rounding_size=0.15", ec=border, fc=bg, lw=1.5
        )
        ax.add_patch(rect)
        # Header banner
        rect_hdr = patches.FancyBboxPatch(
            (x, y + h - 0.7), w, 0.7, boxstyle="round,pad=0.04,rounding_size=0.15", ec=border, fc=border, lw=1.0
        )
        ax.add_patch(rect_hdr)
        ax.text(x + w / 2, y + h - 0.35, f"{phase_num}: {title.upper()} ({timeline})",
                ha="center", va="center", fontsize=9, fontweight="bold", color="#ffffff")

        # Content bullets
        text_y = y + h - 0.98
        for item in items:
            ax.text(x + 0.3, text_y, item, ha="left", va="center", fontsize=8, color="#1e293b")
            text_y -= 0.30

    # Phase 1: bottom=5.65, top=8.00
    items1 = [
        "1. Penonaktifan segera seluruh akun alumni (6/10 terbukti aktif) & akun pegawai mutasi (DSS05).",
        "2. Penghapusan akun admin generik bersama (admin_portal); penegakan akun individual + MFA (DSS05).",
        "3. Pembekuan rilis langsung tanpa tiket; kewajiban formulir Change Request darurat (BAI06).",
        "4. Pelaksanaan uji pemulihan (restore drill) perdana terhadap berkas backup database MySQL (DSS01).",
        "5. Penerbitan draf SK Rektor penunjukan Pejabat Pelindung Data Pribadi (DPO) sesuai UU PDP (MEA03)."
    ]
    draw_phase(0.5, 5.65, 11.0, 2.35, "FASE 1", "Quick Wins & Pengendalian Kritis", "Bulan 1 - 3", items1,
               bg="#fef2f2", border="#dc2626")

    # Arrow 1 -> 2 (strictly in gap 5.60 -> 5.15)
    ax.annotate("", xy=(6.0, 5.14), xytext=(6.0, 5.60),
                arrowprops=dict(arrowstyle="->", lw=2.2, color="#dc2626"))

    # Phase 2: bottom=2.30, top=5.06 (h=2.76 accommodates 6 lines comfortably)
    items2 = [
        "1. Pengesahan Dokumen Kebijakan Keamanan TI & Matriks Klasifikasi Data Akademik (APO13).",
        "2. Implementasi Transparent Data Encryption (TDE / AES-256) pada tabel PII & transkrip nilai (APO13).",
        "3. Penyediaan server Staging terisolasi identik produksi & alur persetujuan CAB (BAI06).",
        "4. Pembakuan SOP Backup & Restore rutin bulanan serta monitoring alert proaktif Zabbix (DSS01).",
        "5. Otomatisasi siklus akun terintegrasi sistem yudisium & User Access Review semesteran (DSS05).",
        "6. Penyusunan Register Kepatuhan UU PDP No. 27/2022 & SOP notifikasi insiden 3x24 jam (MEA03)."
    ]
    draw_phase(0.5, 2.30, 11.0, 2.76, "FASE 2", "Standarisasi Proses & Dokumentasi Sistemik", "Bulan 4 - 6", items2,
               bg="#eff6ff", border="#2563eb")

    # Arrow 2 -> 3 (strictly in gap 2.25 -> 1.80)
    ax.annotate("", xy=(6.0, 1.79), xytext=(6.0, 2.25),
                arrowprops=dict(arrowstyle="->", lw=2.2, color="#2563eb"))

    # Phase 3: bottom=-0.70, top=1.70
    items3 = [
        "1. Pemasangan SIEM terpusat untuk korelasi log audit modifikasi nilai & akses administratif (DSS05).",
        "2. Otomatisasi pipeline CI/CD dengan static code security scanning & mandatory rollback script (BAI06).",
        "3. Penerapan dashboard metrik SLA ketersediaan 99.5% dan capacity planning proaktif musim KRS (DSS01).",
        "4. Program pelatihan berkelanjutan kesadaran keamanan siber bagi dosen, tendik & mahasiswa (APO13).",
        "5. Pelaksanaan Re-Audit COBIT 2019 berkala untuk validasi pencapaian tingkat target Level 3.2 (MEA03)."
    ]
    draw_phase(0.5, -0.70, 11.0, 2.40, "FASE 3", "Integrasi, Optimalisasi Kuantitatif & Re-Audit", "Bulan 7 - 12", items3,
               bg="#f0fdf4", border="#16a34a")

    ax.set_ylim(-0.85, 8.75)

    out_path = os.path.join(GAMBAR_DIR, "diagram_roadmap_perbaikan.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated: {out_path}")


def main():
    global GAMBAR_DIR
    parser = argparse.ArgumentParser(
        description="Generator 5 diagram teknis 300 DPI untuk Laporan Audit TI COBIT 2019."
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=_default_output_dir(),
        help="Direktori keluaran PNG diagram (default: template/gambar di dalam repo, atau ./audit_diagrams di luar repo)",
    )
    args = parser.parse_args()
    GAMBAR_DIR = os.path.abspath(args.output_dir)
    _ensure_matplotlib()
    generate_architecture_diagram()
    generate_org_chart()
    generate_risk_matrix()
    generate_capability_chart()
    generate_roadmap_diagram()
    print(f"All diagrams generated successfully in: {GAMBAR_DIR}")


if __name__ == "__main__":
    main()
