# Victorious Desktop Environment (VDE)

An ultra-lightweight, privacy-centric Linux desktop environment capturing modern Windows 11 aesthetics, dark Mica/acrylic styling, sub-500 MB idle RAM consumption, and zero telemetry.

---

## ⚡ 1-Command Terminal Installation

### 🟢 Inside "Try Ubuntu" (Live USB / Live Session)
Boot any standard Ubuntu live USB/ISO ("Try Ubuntu"), open a terminal, and run:
```bash
curl -sSL https://raw.githubusercontent.com/VicRoger27/VDE/main/install.sh | sudo bash
```
Once it finishes, type `vde` in your terminal or double-click the **Launch VDE** icon created on your desktop!

---

### 🔄 On Installed Systems: Clean Replace (Wipe Old Desktop / GNOME / Bloat)
Purges GNOME, GDM, and Canonical telemetry bloat, and replaces it with VDE:
```bash
curl -sSL https://raw.githubusercontent.com/VicRoger27/VDE/main/install.sh | sudo bash -s -- --replace
```

---

### 📦 Coexist (Install Alongside Existing Desktop)
```bash
curl -sSL https://raw.githubusercontent.com/VicRoger27/VDE/main/install.sh | sudo bash
```

Alternatively, clone the repository and run locally:
```bash
git clone https://github.com/VicRoger27/VDE.git
cd VDE
sudo ./install.sh --replace
```

---

## 🚀 Launching VDE

Once installed, you can enter VDE in two ways:

1. **Directly from Any Terminal or TTY**:
   ```bash
   vde
   ```
2. **From Your Login Display Manager**:
   Select **`Victorious Desktop Environment (VDE)`** from your session chooser on GDM, SDDM, LightDM, or greetd.

---

## 🏛️ Core Architecture

- **Compositor**: Labwc (Wayland `wlroots` layer-shell with 1px border snapping).
- **Taskbar & Flyout (`vde-bar`)**: Built with Astal & GTK4, featuring centered pinned icons and a modular Quick Settings flyout.
- **Start Menu Runner (`vde-launcher`)**: Hardware-accelerated Qt6 / QML with inotify `.desktop` indexing and local llama.cpp MiniCPM-V 4.7 vision client.
- **Settings Hub (`crossings`)**: Native two-pane interactive Card architecture for system customization and telemetry-free privacy toggles.
- **Memory Footprint**: Target < 500 MB idle RAM (under 250 MB on minimal Ubuntu Server base).

---

## 📜 License & Privacy

VDE is licensed under the MIT License. Designed with zero cloud telemetry, zero remote tracking, and strictly local AI inference.
