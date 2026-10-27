# Changelog 14: Ubuntu Server Backbone ISO Generator & Packaging

## Summary
Created the standalone ISO generator toolchain [`builder/make_vde_iso.py`](file:///c:/Users/Victor/Antigravity%20Projects/Other/DEs/VDE/builder/make_vde_iso.py) that packages the complete Victorious Desktop Environment (VDE) onto the official Ubuntu Server (Noble minimal) backbone, outputting `vde-live-amd64.iso` to `C:\Users\Victor\ISO\Test\vde-live-amd64.iso`.

## Key Changes
1. **Ubuntu Server (uS) Backbone Builder (`builder/make_vde_iso.py`)**:
   - Uses `C:\Users\Victor\ISO\ubuntu-26.04.1-live-server-amd64.iso` as the immutable base template.
   - Stages the full VDE desktop shell:
     - Astal floating centered taskbar & Quick Settings (`/usr/share/vde/astal-shell/`)
     - Qt6/QML Start Menu runner (`/usr/share/vde/qt-launcher/`)
     - Crossings settings hub (`/usr/share/vde/apps/crossings/`)
     - Labwc compositor rules and theming (`/etc/xdg/labwc/`)
     - Design tokens and icons (`/usr/share/vde/tokens/`, `/usr/share/vde/assets/`)
   - Configures systemd tty1 autologin override and automated session startup.
   - Compresses overlay via high-density zstd SquashFS.
   - Injects the overlay directly into the Ubuntu Server ISO `/casper/` tree via `pycdlib`.
   - Customizes GRUB menu with branded entries ("Victorious Desktop Environment (VDE) - Live on Ubuntu Server").

2. **Output Artifact**:
   - Generated bootable hybrid ISO: `C:\Users\Victor\ISO\Test\vde-live-amd64.iso` (2,792.27 MB / 2.92 GB).
   - Compatible with VirtualBox, VMware, QEMU, and bare-metal USB flashing (Ventoy/Rufus).
