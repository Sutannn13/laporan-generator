#!/usr/bin/env python3
"""CLI pembungkus Humanizer ID di dalam bundel skill tunggal `laporan-generator`.

Dapat dijalankan dari direktori kerja mana saja tanpa instalasi pip tambahan:
    python "<skill_dir>/scripts/audit_humanizer.py" <path_ke_file.md> --preset akademik --kampus ubsi
    python "<skill_dir>/scripts/audit_humanizer.py" --demo
"""

import os
import sys

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

_SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _SKILL_ROOT not in sys.path:
    sys.path.insert(0, _SKILL_ROOT)

from humanizer_id.engine import (  # noqa: E402
    PRESET_EXCLUSIONS,
    PRESET_LABELS,
    audit_text,
    load_data,
    main,
    print_report,
)

if __name__ == "__main__":
    main()
