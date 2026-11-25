#!/usr/bin/env python3
"""Install shared Zed settings and keybindings into existing local JSONC files."""

import argparse
import json
import os
import re
import tempfile
from pathlib import Path


STRING = r'"(?:[^"\\]|\\.)*"'
COMMENTS = re.compile(STRING + r"|//[^\r\n]*|/\*[\s\S]*?\*/")
TRAILING_COMMAS = re.compile(STRING + r"|,(?=\s*[}\]])")


def read_jsonc(path, expected):
    def strip_comment(match):
        token = match[0]
        return token if token.startswith('"') else re.sub(r"[^\r\n]", " ", token)

    text = COMMENTS.sub(strip_comment, path.read_text(encoding="utf-8"))
    text = TRAILING_COMMAS.sub(lambda match: match[0] if match[0] != "," else "", text)
    try:
        value = json.loads(text)
    except json.JSONDecodeError as error:
        raise ValueError(f"{path}:{error.lineno}:{error.colno}: {error.msg}") from None
    if not isinstance(value, expected):
        raise ValueError(f"Unexpected JSON structure in {path}")
    return value


def merge_settings(current, shared):
    merged = current.copy()
    for key, value in shared.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_settings(merged[key], value)
        else:
            merged[key] = value
    return merged


def merge_keymap(current, shared):
    # Keep original group order for local bindings. Append managed bindings so
    # they take precedence over built-ins and older copies of the same group.
    def selector(group):
        return {key: value for key, value in group.items() if key != "bindings"}

    remaining = []
    for group in current:
        if not isinstance(group, dict) or not isinstance(group.get("bindings", {}), dict):
            raise ValueError("Expected objects with binding maps in the local Zed keymap")
        bindings = group.get("bindings", {}).copy()
        for managed in shared:
            if selector(group) == selector(managed):
                for key in managed["bindings"]:
                    bindings.pop(key, None)
        if bindings == group.get("bindings", {}):
            remaining.append(group)
        elif bindings:
            remaining.append({**group, "bindings": bindings})
    return remaining + shared


def install(path, current, merged, stamp, dry_run):
    if merged == current and path.is_file() and not path.is_symlink():
        print(f"  Zed config already current: {path}")
        return
    if dry_run:
        print(f"  would merge Zed config into {path}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        backup = path.with_name(f"{path.name}.bak-{stamp}")
        # Settings or task bindings can contain credentials. Use a private mode
        # from the moment the backup is created.
        contents = path.read_bytes()
        descriptor = os.open(backup, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "wb") as output:
            output.write(contents)
        print(f"  backed up {path} to {backup}")

    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, delete=False
    ) as output:
        temporary = Path(output.name)
        try:
            output.write(json.dumps(merged, indent=2, ensure_ascii=False) + "\n")
            output.close()
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)
    print(f"  merged Zed config: {path}")


def configure(source, destination, stamp, dry_run):
    settings_path = destination / "settings.json"
    keymap_path = destination / "keymap.json"
    shared_settings = read_jsonc(source / settings_path.name, dict)
    shared_keymap = read_jsonc(source / keymap_path.name, list)
    settings = read_jsonc(settings_path, dict) if settings_path.exists() else {}
    keymap = read_jsonc(keymap_path, list) if keymap_path.exists() else []
    if "theme" in settings:
        # Omarchy's Omazed hook owns the generated theme on that machine.
        shared_settings.pop("theme", None)
    merged_keymap = merge_keymap(keymap, shared_keymap)
    install(settings_path, settings, merge_settings(settings, shared_settings), stamp, dry_run)
    install(keymap_path, keymap, merged_keymap, stamp, dry_run)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("stamp")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        configure(args.source, args.destination, args.stamp, args.dry_run)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Zed configuration failed: {error}\n")
