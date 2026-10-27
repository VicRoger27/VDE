#!/usr/bin/env python3
"""
VDE Design Token Compiler
Reads tokens/theme.json and generates:
1. astal-shell/style/tokens.scss (for Astal GTK4/SCSS)
2. qt-launcher/tokens/ThemeTokens.qml (for Qt6 QML singleton)
"""

import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
THEME_FILE = ROOT_DIR / "tokens" / "theme.json"
SCSS_OUT = ROOT_DIR / "astal-shell" / "style" / "tokens.scss"
QML_OUT = ROOT_DIR / "qt-launcher" / "tokens" / "ThemeTokens.qml"

def compile_tokens():
    with open(THEME_FILE, "r", encoding="utf-8") as f:
        theme = json.load(f)

    # 1. Generate SCSS
    SCSS_OUT.parent.mkdir(parents=True, exist_ok=True)
    scss_lines = [
        "// Auto-generated from tokens/theme.json. DO NOT EDIT DIRECTLY.",
        ""
    ]

    dark_c = theme["colors"]["dark"]
    scss_lines.append("// Dark Surface Colors")
    for k, v in dark_c["surface"].items():
        scss_lines.append(f"$surface-{k}: {v};")

    scss_lines.append("\n// Dark Border Colors")
    for k, v in dark_c["border"].items():
        scss_lines.append(f"$border-{k}: {v};")

    scss_lines.append("\n// Dark Text Colors")
    for k, v in dark_c["text"].items():
        scss_lines.append(f"$text-{k}: {v};")

    scss_lines.append("\n// Dark Accent Colors")
    for k, v in dark_c["accent"].items():
        scss_lines.append(f"$accent-{k}: {v};")

    scss_lines.append("\n// Dark Status Indicators")
    for k, v in dark_c["status"].items():
        scss_lines.append(f"$status-{k}: {v};")

    scss_lines.append("\n// Radii")
    for k, v in theme["radii"].items():
        scss_lines.append(f"$radius-{k}: {v};")

    scss_lines.append("\n// Typography")
    scss_lines.append(f"$font-family: {theme['typography']['fontFamily']};")
    for k, v in theme["typography"]["fontSizes"].items():
        scss_lines.append(f"$font-size-{k}: {v};")

    scss_lines.append("\n// Layout Dimensions")
    for k, v in theme["layout"].items():
        scss_lines.append(f"$layout-{k}: {v}px;")

    scss_lines.append("\n// Transitions")
    for k, v in theme["transitions"].items():
        scss_lines.append(f"$transition-{k}: {v};")

    with open(SCSS_OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(scss_lines) + "\n")
    print(f"Generated SCSS tokens at: {SCSS_OUT}")

    # 2. Generate QML Singleton
    QML_OUT.parent.mkdir(parents=True, exist_ok=True)
    font_family_clean = theme['typography']['fontFamily'].split(',')[0].replace("'", "").strip()
    qml_lines = [
        "// Auto-generated from tokens/theme.json. DO NOT EDIT DIRECTLY.",
        "pragma Singleton",
        "import QtQuick",
        "",
        "QtObject {",
        "    id: root",
        "",
        f'    readonly property string fontFamily: "{font_family_clean}"',
        "",
        "    // Layout Dimensions"
    ]

    for k, v in theme["layout"].items():
        qml_lines.append(f"    readonly property int {k}: {v}")

    qml_lines.append("\n    // Radii")
    for k, v in theme["radii"].items():
        val = int(v.replace("px", "")) if "px" in v else 9999
        qml_lines.append(f"    readonly property int radius_{k}: {val}")

    qml_lines.append("\n    // Dark Surface Colors")
    for k, v in dark_c["surface"].items():
        qml_lines.append(f"    readonly property color surface_{k}: \"{v}\"")

    qml_lines.append("\n    // Dark Border Colors")
    for k, v in dark_c["border"].items():
        qml_lines.append(f"    readonly property color border_{k}: \"{v}\"")

    qml_lines.append("\n    // Dark Text Colors")
    for k, v in dark_c["text"].items():
        qml_lines.append(f"    readonly property color text_{k}: \"{v}\"")

    qml_lines.append("\n    // Dark Accent Colors")
    for k, v in dark_c["accent"].items():
        qml_lines.append(f"    readonly property color accent_{k}: \"{v}\"")

    qml_lines.append("\n    // Dark Status Indicators")
    for k, v in dark_c["status"].items():
        qml_lines.append(f"    readonly property color status_{k}: \"{v}\"")

    qml_lines.append("}")

    with open(QML_OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(qml_lines) + "\n")
    print(f"Generated QML tokens at: {QML_OUT}")

if __name__ == "__main__":
    compile_tokens()
