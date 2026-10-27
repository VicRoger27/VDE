# Changelog 24: Universal Wayland Graphics Backend & Labwc XML Schema Alignment

## Summary
Resolved the `unable to create renderer: render:vulkan device ... "vkInitialize"` crash and eliminated all Labwc XML syntax warnings:
1. **Universal Renderer Fallback (`WLR_RENDERER=gles2`)**:
   - Eliminated the Vulkan initialization crash by enforcing OpenGL ES 2 (`WLR_RENDERER=gles2`) with software llvmpipe rasterization support (`WLR_RENDERER_ALLOW_SOFTWARE=1`) and software cursor rendering (`WLR_NO_HARDWARE_CURSORS=1`).
   - Added automatic secondary fallback to the CPU Pixman renderer (`WLR_RENDERER=pixman`) if GLES2 is unavailable.
   - Purged `mesa-vulkan-drivers` and installed `libgl1-mesa-dri` to ensure direct Mesa DRI hardware/software drivers.
2. **Labwc rc.xml Schema Alignment**:
   - Migrated `<snapping><range>10</range>` to `<snapping><range inner="10" outer="10"/>`.
   - Fixed `serverDecoration="none"` to boolean `serverDecoration="no"` for `vde-bar`, `vde-launcher`, and `vde-quicksettings`.
   - Removed obsolete dialog action tags without criteria.
