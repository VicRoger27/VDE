# Changelog 65: Root Menu Action Spec Fix, Fluent Button Proportions & Win Key Nomenclature

1. **Labwc & Openbox Context Menu Action Fix (`compositor/menu.xml`)**:
   - Replaced invalid XML attribute syntax `<action name="Execute" command="..." />` with standard compliant sub-node hierarchy `<action name="Execute"><command>...</command></action>`.
   - Updated across `compositor/menu.xml`, `builder/vde_overlay/etc/xdg/labwc/menu.xml`, and `builder/vde_overlay/usr/share/vde/compositor/menu.xml` to ensure right-click desktop menu launches all 12 VDE native applications, reload, reconfigure, and terminal without failing.

2. **Windows 11 Fluent Button Proportions (`apps/crossings/crossings_gui.py`)**:
   - Refined `button.card-btn` CSS with explicit `min-height: 28px`, `padding: 4px 12px`, and `font-size: 12px` to eliminate oversized default GTK button scaling.
   - Updated action card layout and power buttons to match Windows 11 Fluent ergonomics.

3. **User-Centric Key Nomenclature (`Win` vs `Super`)**:
   - Converted Linux-internal `Super` keyboard shortcut labels (`Super+L`, `Super+P`, `Super+Shift+S`, `Super+I`) to intuitive Windows key notation (`Win+L`, `Win+P`, `Win+Shift+S`, `Win+I`) across Crossings, Crossnip, and Waybar tooltips.

4. **Graphics Driver Safety in Installer Wipe (`install.sh`)**:
   - Preserved `mesa-vulkan-drivers` during desktop bloatware purge to prevent accidental removal of hardware acceleration drivers.
