#!/usr/bin/env python3
"""
Extracts rendered SVG assets from artifacts/SVG/2.txt into assets/icons/
and updates assets/asset_manifest.json status.
"""

import re
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SVG_SRC = ROOT_DIR / "artifacts" / "SVG" / "2.txt"
ICONS_DIR = ROOT_DIR / "assets" / "icons"
MANIFEST_PATH = ROOT_DIR / "assets" / "asset_manifest.json"

ICON_MAP = {
    "icon-start-button": ("start-idle-dark.svg", "start-idle-light.svg"),
    "icon-start-button-active": ("start-active-dark.svg", "start-active-light.svg"),
    "icon-start-button-offline": ("start-offline-dark.svg", "start-offline-light.svg"),
    "icon-search": ("search-dark.svg", "search-light.svg"),
    "icon-apps-grid": ("all-apps-dark.svg", "all-apps-light.svg"),
    "icon-power": ("power-shutdown-dark.svg", "power-shutdown-light.svg"),
    "icon-restart": ("power-restart-dark.svg", "power-restart-light.svg"),
    "icon-sleep": ("power-sleep-dark.svg", "power-sleep-light.svg"),
    "icon-settings": ("settings-dark.svg", "settings-light.svg"),
    "icon-quick-wifi": ("wifi-dark.svg", "wifi-light.svg"),
    "icon-quick-bluetooth": ("bluetooth-dark.svg", "bluetooth-light.svg"),
    "icon-quick-volume": ("volume-dark.svg", "volume-light.svg"),
    "icon-quick-volume-mute": ("mute-dark.svg", "mute-light.svg"),
    "icon-quick-theme": ("theme-switch-dark.svg", "theme-switch-light.svg"),
    "icon-quick-battery": ("battery-dark.svg", "battery-light.svg"),
    "icon-quick-bell": ("notifications-dark.svg", "notifications-light.svg"),
    "icon-chevron-right": ("chevron-down-dark.svg", "chevron-down-light.svg")
}

def main():
    ICONS_DIR.mkdir(parents=True, exist_ok=True)
    content = SVG_SRC.read_text(encoding="utf-8")
    pattern = re.compile(r'<!--\s*([a-zA-Z0-9\-_.]+\.svg)\s*-[^>]*-->\s*(<svg[\s\S]*?</svg>)', re.MULTILINE)
    matches = pattern.findall(content)

    print(f"Extracting {len(matches)} SVGs to {ICONS_DIR}...")
    for filename, svg_body in matches:
        target_path = ICONS_DIR / filename
        target_path.write_text(svg_body.strip() + "\n", encoding="utf-8")

    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)

        rendered_count = 0
        for asset in manifest.get("assets", []):
            aid = asset.get("asset_id")
            if aid in ICON_MAP:
                dark_f, light_f = ICON_MAP[aid]
                asset["status"] = "rendered"
                asset["rendered_file"] = f"assets/icons/{dark_f}"
                asset["rendered_file_light"] = f"assets/icons/{light_f}"
                rendered_count += 1

        manifest["status_summary"]["rendered"] = rendered_count
        manifest["status_summary"]["total_extracted_svgs"] = len(matches)
        
        with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        print(f"Updated asset manifest: {rendered_count} manifest assets fulfilled, {len(matches)} total SVGs available.")

if __name__ == "__main__":
    main()
