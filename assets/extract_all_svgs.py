#!/usr/bin/env python3
"""
Extracts all SVGs from both 2.txt (GLM batch 1) and 3.txt (DeepSeek DeepThink batch 2),
populating assets/icons/ with the complete merged library (74+ icons).
"""

import re
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
S2_SRC = ROOT_DIR / "artifacts" / "SVG" / "2.txt"
S3_SRC = ROOT_DIR / "artifacts" / "SVG" / "3.txt"
ICONS_DIR = ROOT_DIR / "assets" / "icons"
MANIFEST_PATH = ROOT_DIR / "assets" / "asset_manifest.json"

def extract_from_file(filepath, label):
    if not filepath.exists():
        print(f"Skipping {filepath} (not found)")
        return {}
    content = filepath.read_text(encoding="utf-8")
    pattern = re.compile(r'<!--\s*([a-zA-Z0-9\-_.]+\.svg)\s*-[^>]*-->\s*(<svg[\s\S]*?</svg>)', re.MULTILINE)
    matches = pattern.findall(content)
    print(f"Found {len(matches)} icons in {label} ({filepath.name})")
    out = {}
    for filename, body in matches:
        out[filename] = body.strip() + "\n"
    return out

def main():
    ICONS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Extract Batch 1 (GLM 5.3)
    b1_icons = extract_from_file(S2_SRC, "GLM Batch 1")
    
    # 2. Extract Batch 2 (DeepSeek DeepThink)
    b2_icons = extract_from_file(S3_SRC, "DeepSeek DeepThink Batch 2")
    
    merged = {**b1_icons, **b2_icons}
    print(f"Total merged icons across both sets: {len(merged)}")
    
    for filename, svg_body in merged.items():
        (ICONS_DIR / filename).write_text(svg_body, encoding="utf-8")
    
    print(f"Successfully saved {len(merged)} SVG files to {ICONS_DIR}")

if __name__ == "__main__":
    main()
