# Changelog 46: Native TTY1 Direct PAM Autologin & Direct VDE Command Polish

## Summary
Refined the startup architecture so VDE boots automatically into the desktop with full PAM seat0 DRM permissions, eliminating the need to manually switch TTYs or type commands:

1. **Seamless TTY1 Direct PAM Autologin**:
   - Replaced conflicting systemd unit with standard `getty@tty1` autologin and PAM logind seat registration.
   - When the system boots or GDM is masked, `getty@tty1` automatically logs in the target user via PAM (allocating `seat0` hardware DRM master and input permissions).
   - `/etc/profile.d/99-vde-login.sh` automatically executes `vde-session` on TTY1 to load the desktop directly without manual user intervention.

2. **Streamlined `vde` Executable**:
   - Cleaned `compositor/vde` to directly release DRM from zombie processes and execute `vde-session` cleanly on any terminal without querying inactive service state.

3. **End-to-End Test Suite**:
   - 100% verified across all 12 native applications, compositor XMLs, Waybar configuration, and installer scripts.
