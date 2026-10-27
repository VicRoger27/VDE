# Changelog 35: System-Wide VDE Vector Icon Registration

## Summary
Replaced legacy distribution fallback icons with the native VDE vector icon suite:
1. **System Icon Cache Registration (`install.sh`)**:
   - Installed all 74+ VDE GLM vector icons directly into `/usr/share/icons/hicolor/scalable/apps/`.
   - Executed `gtk-update-icon-cache` to immediately bind clean SVG graphics to system desktop entries, terminal, settings, file manager, and app indicators.
2. **Eliminated Ugly Legacy Fallback Bitmaps**:
   - Replaces the 1990s-era pixelated fallback icons exposed during GNOME/Yaru package purging with sharp, modern Fluent vector artwork.
