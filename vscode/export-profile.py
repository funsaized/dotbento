#!/usr/bin/env python3
"""Write an importable Dotbento VS Code profile to stdout."""

import json
import sys
from pathlib import Path


def main():
    directory = Path(__file__).resolve().parent
    settings = (directory / "settings.json").read_text(encoding="utf-8")
    keybindings = (directory / "keybindings.json").read_text(encoding="utf-8")
    recommendations = json.loads(
        (directory / "extensions.json").read_text(encoding="utf-8")
    )["recommendations"]

    # VS Code stores profile resources as JSON strings. Settings and keybindings
    # each wrap the original editor file so it can be restored verbatim.
    platform = {"darwin": 1, "linux": 2, "win32": 3}.get(sys.platform, 2)
    profile = {
        "name": "Dotbento",
        "settings": json.dumps({"settings": settings}),
        "keybindings": json.dumps({"keybindings": keybindings, "platform": platform}),
        "extensions": json.dumps(
            [{"identifier": {"id": extension}, "preRelease": False} for extension in recommendations]
        ),
    }
    print(json.dumps(profile, indent=2))


if __name__ == "__main__":
    main()
