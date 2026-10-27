# Changelog 38: Built-in Terminal Fallback, Wofi Start Menu & Super Key Integration

## Summary
Eliminated non-functioning desktop shortcuts and uninstalled tool dependencies:
1. **Guaranteed Terminal Availability (`rc.xml`, `menu.xml`, `install.sh`)**:
   - Bundled and installed both `foot` and `xterm` to ensure that clicking "Open Terminal" or pressing `Super + Return` never fails.
   - Configured cascade fallback: `foot || xterm || alacritty || x-terminal-emulator`.
2. **Native Dark Mica Start Menu (`vde-launcher`, `wofi_style.css`)**:
   - Replaced dead `qdbus` signals with the native Wayland `wofi` runner styled with VDE dark Mica theme (`#18181b` frosted glass, rounded borders, accent focus).
   - Bound directly to `Super` / `Super_L` and `Super + Space` in `rc.xml`.
3. **Menu Action Hardening (`compositor/menu.xml`)**:
   - Replaced unresolvable commands in the desktop root menu with verified installed binaries.
