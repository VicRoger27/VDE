# Victorious Desktop Environment (VDE)

An ultra-lightweight, privacy-centric Linux desktop environment capturing modern fluent acrylic aesthetics, dark Mica styling, sub-500 MB idle RAM consumption, and zero telemetry.

---

## ⚡ 1-Command Quick Install

### 🟢 Universal One-Liner (vopple.uk)
Open a terminal (or switch to a virtual console via `Ctrl + Alt + F3`) and run:

```bash
wget -qO- https://vopple.uk/install.sh | sudo bash
```
*or using curl:*
```bash
curl -sSL https://vopple.uk/install.sh | sudo bash
```

> **Fallback Mirror**: `wget -qO- https://raw.githubusercontent.com/i2qq/VDE/main/install.sh | sudo bash`

---

### 🛠️ Installation Options

| Mode | Command | Description |
| :--- | :--- | :--- |
| **Clean Replace (Default)** | `wget -qO- https://vopple.uk/install.sh \| sudo bash` | Purges background `snapd`, telemetry services (`whoopsie`, `apport`, `ubuntu-report`), and default desktop bloat, installing clean VDE. |
| **Coexist Mode** | `wget -qO- https://vopple.uk/install.sh \| sudo bash -s -- --keep-gnome` | Installs VDE alongside your existing desktop without removing existing components. |

Alternatively, install from source:
```bash
git clone https://github.com/i2qq/VDE.git
cd VDE
sudo ./install.sh
```

---

## 🚀 Launching VDE

Once installed, launch VDE anytime:

1. **Directly from Terminal or TTY Console**:
   ```bash
   vde
   ```
2. **From Login Display Managers**:
   Select **`Victorious Desktop Environment (VDE)`** from your session menu on GDM, SDDM, LightDM, or greetd.

---

## ⌨️ Fluent Ergonomics & Shortcuts

| Shortcut | Action |
| :--- | :--- |
| <kbd>Super</kbd> / <kbd>Super</kbd> + <kbd>Space</kbd> | Toggle Start Menu (`vde-launcher`) |
| <kbd>Super</kbd> + <kbd>Return</kbd> | Open Fast Terminal (`foot`) |
| <kbd>Super</kbd> + <kbd>←</kbd> / <kbd>→</kbd> | Snap Window Left / Right Half |
| <kbd>Super</kbd> + <kbd>↑</kbd> | Maximize Window |
| <kbd>Super</kbd> + <kbd>↓</kbd> | Minimize / Restore Window |
| <kbd>Super</kbd> + <kbd>Alt</kbd> + <kbd>Arrows</kbd> | 4-Corner Quadrant Snap (Top-Left, Top-Right, Bottom-Left, Bottom-Right) |
| <kbd>Alt</kbd> + <kbd>Tab</kbd> | Interactive Task Switcher |
| <kbd>Alt</kbd> + <kbd>F4</kbd> | Close Active Window |
| <kbd>Super</kbd> + <kbd>E</kbd> | Open File Explorer |
| <kbd>Super</kbd> + <kbd>L</kbd> | Lock Screen |
| <kbd>PrintScreen</kbd> | Interactive Area Screenshot to Clipboard (`grim` + `slurp`) |
| **Right-Click Desktop** | Open VDE Context Menu (Apps, Settings, Terminal, Window Controls) |

---

## 🏛️ Core Architecture

- **Compositor**: [Labwc](https://github.com/labwc/labwc) — Lightweight stacking Wayland compositor built on `wlroots` with sub-millisecond layer-shell rendering, GLES2 acceleration, and Pixman software fallback.
- **Taskbar & Shell (`vde-bar`)**: Built with Astal & GTK4, with automated dark Mica Waybar fallback featuring centered taskbar items, start menu button, system tray, audio flyout, and clock.
- **Start Menu Runner (`vde-launcher`)**: Hardware-accelerated Qt6 / QML with real-time inotify `.desktop` indexing and local llama.cpp vision client.
- **Settings Hub (`crossings`)**: Two-pane interactive card-based customization center for theme accents, display scaling, and privacy controls.
- **Memory Footprint**: Target < 500 MB idle RAM (under 250 MB on minimal server base).

---

## 📜 License & Privacy

VDE is licensed under the **VPL License**. 

Designed strictly with **zero cloud telemetry**, **zero remote tracking**, and exclusively **local on-device processing**.

---

## ⚖️ Trademark Disclaimer

All product names, logos, brands, and registered trademarks mentioned or referenced are the property of their respective owners. All company, product, and service names used in this project are strictly for identification, reference, and compatibility purposes only. Use of these names, logos, and brands does not imply endorsement, affiliation, or sponsorship.

---

## ❗Warranty Disclaimer

Please view **NOTICE.md** for all warranty
