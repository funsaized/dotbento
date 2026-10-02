#!/usr/bin/env python3
"""Merge portable Pi preferences without replacing machine-local settings."""

import argparse
import json
import shutil
from pathlib import Path


def configure(source: Path, destination: Path, stamp: str, dry_run: bool = False) -> None:
    defaults = json.loads(source.read_text())
    current = json.loads(destination.read_text()) if destination.exists() else {}
    if not isinstance(defaults, dict) or not isinstance(current, dict):
        raise ValueError("Pi settings must be JSON objects")
    merged = {**current, **defaults}
    merged["modelThinkingLevels"] = {
        **current.get("modelThinkingLevels", {}),
        **defaults["modelThinkingLevels"],
    }
    if merged == current:
        print(f"  Pi settings already current: {destination}")
        return
    if dry_run:
        print(f"  would merge {source} into {destination} (backing up existing settings)")
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        backup = destination.with_name(f"{destination.name}.bak-{stamp}")
        if backup.exists():
            raise FileExistsError(f"Backup already exists: {backup}")
        shutil.copy2(destination, backup)
        print(f"  backed up {destination} to {backup}")
    destination.write_text(json.dumps(merged, indent=2) + "\n")
    print(f"  merged Pi settings: {destination}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("stamp")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    configure(args.source, args.destination, args.stamp, args.dry_run)
