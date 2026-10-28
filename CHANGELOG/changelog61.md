# Changelog 61 - Removal of Pre-Flight Display Manager Kill Command

### Highlights & Modifications
1. **Elimination of Pre-Flight Process Killing**:
   - Removed pre-flight `systemctl stop`, `systemctl mask --now`, and `pkill -9 -f gnome-shell|mutter` commands from the beginning of `install.sh`.
   - Running destructive kill commands prior to package installation aborted graphical terminal sessions (such as `gnome-terminal`) mid-execution, preventing the rest of the installer from executing.
2. **Safe Persistent Service Configuration**:
   - `systemctl disable` and `systemctl mask` are now configured at the end of the installation without `--now`, allowing the active terminal to complete cleanly without session disruption.
   - Background display managers are now stopped only when `vde` is explicitly launched or upon reboot.
