# Changelog 31: Single-Instance Taskbar Guard & GTK CSS Property Optimization

## Summary
Refined Waybar shell styling and lifecycle management based on live nested execution logs:
1. **GTK CSS Property Validation (`waybar_style.css`)**:
   - Removed the unsupported standard CSS `text-align` rule from the `#clock` selector to satisfy GTK 3/4 CSS parser requirements and eliminate runtime warnings.
2. **Single-Instance Shell Guard (`vde-bar` & `compositor/autostart`)**:
   - Added `pgrep -x waybar` lifecycle checks to ensure only one taskbar instance is initialized, preventing dual execution when launched via Labwc's `-s` startup argument and `autostart` script concurrently.
