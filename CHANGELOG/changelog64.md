# Changelog 64 - Dynamic Desktop Environment Detection & Comprehensive Purge

### Highlights & Modifications
1. **Dynamic Installed Package Discovery**:
   - The desktop environment purge in `install.sh` previously supplied a static list containing packages from multiple distributions (e.g. `gdm` vs `gdm3`, `unity`, `kde-standard`), which caused `apt-get` to abort on unlocatable packages before removing GNOME.
   - Refactored purge logic to dynamically query `dpkg -s` for installed desktop packages (`gnome-shell`, `gnome-session`, `gdm3`, `ubuntu-desktop`, `mutter`, etc.) before purging.
2. **Complete Legacy Desktop Removal**:
   - Accurately targets and purges all installed GNOME, KDE, XFCE, LXQt, Budgie, MATE, and Cinnamon packages, followed by clean autoremove.
