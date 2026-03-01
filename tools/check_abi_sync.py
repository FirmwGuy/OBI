#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    sync = repo_root / "tools" / "sync_abi_from_obi_abi.py"
    proc = subprocess.run([sys.executable, str(sync), "--check"], cwd=str(repo_root))
    return int(proc.returncode)


if __name__ == "__main__":
    raise SystemExit(main())

