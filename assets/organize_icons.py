#!/usr/bin/env python3
"""
Synchronizes and organizes all SVG sets:
- artifacts/SVG/1.txt & 3.txt -> assets/icons/dseek/ (DeepSeek with DeepThink)
- artifacts/SVG/2.txt & 4.txt -> assets/icons/glm/   (GLM 5.3 Flash Effort Max - PRIMARY)
- Top-level assets/icons/ is populated with the complete GLM production set.
"""

import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
S1_SRC = ROOT_DIR / "artifacts" / "SVG" / "1.txt"
S2_SRC = ROOT_DIR / "artifacts" / "SVG" / "2.txt"
S3_SRC = ROOT_DIR / "artifacts" / "SVG" / "3.txt"
S4_SRC = ROOT_DIR / "artifacts" / "SVG" / "4.txt"

DSEEK_DIR = ROOT_DIR / "assets" / "icons" / "dseek"
GLM_DIR = ROOT_DIR / "assets" / "icons" / "glm"
PRIMARY_DIR = ROOT_DIR / "assets" / "icons"

def extract_named_svgs(filepath):
    if not filepath.exists():
        return {}
    content = filepath.read_text(encoding="utf-8")
    pattern = re.compile(r'<!--\s*([a-zA-Z0-9\-_.]+\.svg)\s*-[^>]*-->\s*(<svg[\s\S]*?</svg>)', re.MULTILINE)
    return dict(pattern.findall(content))

def main():
    DSEEK_DIR.mkdir(parents=True, exist_ok=True)
    GLM_DIR.mkdir(parents=True, exist_ok=True)
    PRIMARY_DIR.mkdir(parents=True, exist_ok=True)

    # 1. DeepSeek sets (1.txt and 3.txt)
    dseek_b2 = extract_named_svgs(S3_SRC)
    print(f"DeepSeek Batch 2: {len(dseek_b2)} icons")
    for f, body in dseek_b2.items():
        (DSEEK_DIR / f).write_text(body.strip() + "\n", encoding="utf-8")

    # 2. GLM sets (2.txt and 4.txt)
    glm_b1 = extract_named_svgs(S2_SRC)
    glm_b2 = extract_named_svgs(S4_SRC)
    print(f"GLM Batch 1: {len(glm_b1)} icons")
    print(f"GLM Batch 2: {len(glm_b2)} icons")

    glm_combined = {**glm_b1, **glm_b2}
    print(f"Total GLM Production Icons: {len(glm_combined)}")

    for f, body in glm_combined.items():
        (GLM_DIR / f).write_text(body.strip() + "\n", encoding="utf-8")
        (PRIMARY_DIR / f).write_text(body.strip() + "\n", encoding="utf-8")

    print(f"Done! All {len(glm_combined)} GLM icons deployed to {PRIMARY_DIR}")

if __name__ == "__main__":
    main()
