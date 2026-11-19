# /// script
# requires-python = ">=3.10"
# dependencies = ["python-docx"]
# ///
"""
Independent Verification and Inspection Script for the IT Audit Project Report (.docx).
Delegates to challenge_text_and_math.py with parameterized CLI arguments.
"""

import argparse
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from scripts.challenge_text_and_math import DEFAULT_TARGET_DOCX, run_challenge
except ImportError:
    from challenge_text_and_math import DEFAULT_TARGET_DOCX, run_challenge


def main():
    parser = argparse.ArgumentParser(description="Verify IT Audit Report (.docx) structure and math.")
    parser.add_argument("-t", "--target", default=str(BASE_DIR / DEFAULT_TARGET_DOCX), help="Target .docx path")
    parser.add_argument("--roster", default="Penulis Contoh:00000001", help="Expected author roster 'Name:NIM'")
    args = parser.parse_args()
    ok, _, _ = run_challenge(target_docx=args.target, roster_str=args.roster)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
