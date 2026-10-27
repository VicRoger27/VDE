# Changelog 26: Documentation Revision, VPL License Alignment & Shortcut Reference

## Summary
Revised and updated the project `README.md` to reflect recent installation, architectural, and licensing enhancements:
1. **VPL License Alignment**: Retained and highlighted the user-defined VPL (Victorious Public License) terms and privacy guarantees.
2. **Reliable `wget` One-Liner**: Replaced sandboxed `curl` commands with native `wget -qO- ... | sudo bash` to guarantee execution on live USB and server environments without snap-confine errors.
3. **Keyboard Ergonomics Table**: Added a comprehensive shortcut table documenting Windows 11 snapping (half-screen, 4-corner quadrants), terminal launcher (`Super + Enter`), Start launcher, and desktop right-click menu.
4. **Architectural Transparency**: Documented Labwc wlroots GLES2/Pixman graphics pipeline, Astal/Waybar fallback taskbar layer, and zero-telemetry architecture.
