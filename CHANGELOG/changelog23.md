# Changelog 23: Display Guard Protection, Runtime Dir Provisioning & Session Hardening

## Summary
Hardened `install.sh` and session launchers against abrupt GUI terminal termination during GNOME desktop uninstallation and ensured standard Wayland runtime environment variables:
1. **Display Server Guard (`install.sh`)**: Conditioned display manager termination (`gdm3`, `gnome-shell`) on whether the installer is running from a virtual console (TTY) or an active graphical session, preventing self-termination of the terminal window mid-purge.
2. **Wayland Runtime Directory Management (`vde-session`)**: Added automatic discovery and permission provisioning for `XDG_RUNTIME_DIR` (`/run/user/<uid>`) to guarantee Wayland compositors (`labwc`) and clients start properly from any TTY context without permission errors.
3. **D-Bus Session Hardening**: Guarded `dbus-launch` invocations and added `dbus-x11` to the apt dependency suite for headless and minimal live session environments.
4. **Clean Session Takeover**: Enables direct transition from Linux TTY into VDE via `vde` or `vde-session`.
