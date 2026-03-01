#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SyncChange:
    rel_path: str
    kind: str  # 'copy' | 'delete' | 'mkdir'


def _read_bytes(path: Path) -> bytes | None:
    try:
        return path.read_bytes()
    except FileNotFoundError:
        return None


def _copy_if_needed(src: Path, dst: Path, changes: list[SyncChange]) -> None:
    src_b = _read_bytes(src)
    if src_b is None:
        raise FileNotFoundError(str(src))

    dst_b = _read_bytes(dst)
    if dst_b == src_b:
        return

    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    changes.append(SyncChange(str(dst), "copy"))


def _sync_tree(src_dir: Path, dst_dir: Path, changes: list[SyncChange]) -> None:
    if not src_dir.is_dir():
        raise FileNotFoundError(str(src_dir))

    dst_dir.mkdir(parents=True, exist_ok=True)

    src_files = {p.name: p for p in src_dir.glob("*.h") if p.is_file()}
    dst_files = {p.name: p for p in dst_dir.glob("*.h") if p.is_file()}

    for name, src in sorted(src_files.items()):
        _copy_if_needed(src, dst_dir / name, changes)

    for name, dst in sorted(dst_files.items()):
        if name in src_files:
            continue
        dst.unlink()
        changes.append(SyncChange(str(dst), "delete"))


def _check_tree(src_dir: Path, dst_dir: Path, changes: list[SyncChange]) -> None:
    if not src_dir.is_dir():
        raise FileNotFoundError(str(src_dir))

    src_files = {p.name: p for p in src_dir.glob("*.h") if p.is_file()}
    dst_files = {p.name: p for p in dst_dir.glob("*.h") if p.is_file()}

    for name, src in sorted(src_files.items()):
        dst = dst_dir / name
        if _read_bytes(dst) != _read_bytes(src):
            changes.append(SyncChange(str(dst), "copy"))

    for name, dst in sorted(dst_files.items()):
        if name in src_files:
            continue
        changes.append(SyncChange(str(dst), "delete"))


def main() -> int:
    ap = argparse.ArgumentParser(description="Sync OBI/abi headers from the canonical OBI-ABI repo.")
    ap.add_argument(
        "--obi-abi",
        default="../OBI-ABI",
        help="Path to OBI-ABI repo (default: ../OBI-ABI)",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="Only check; exit nonzero if out of sync.",
    )
    ap.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-file output (still sets exit status).",
    )
    args = ap.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    src_root = (repo_root / args.obi_abi).resolve()
    src_obi = src_root / "include" / "obi"
    dst_abi = repo_root / "abi"

    src_core = src_obi / "obi_core_v0.h"
    dst_core = dst_abi / "obi_core_v0.h"

    src_profiles = src_obi / "profiles"
    dst_profiles = dst_abi / "profiles"

    changes: list[SyncChange] = []

    if args.check:
        if _read_bytes(dst_core) != _read_bytes(src_core):
            changes.append(SyncChange(str(dst_core), "copy"))
        _check_tree(src_profiles, dst_profiles, changes)
    else:
        _copy_if_needed(src_core, dst_core, changes)
        _sync_tree(src_profiles, dst_profiles, changes)

    if not args.quiet:
        for ch in changes:
            print(f"{ch.kind:>6} {Path(ch.rel_path).relative_to(repo_root)}")

    if changes and args.check:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

