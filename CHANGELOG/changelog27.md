# Changelog 27: Trademark Decoupling, Fluent Nomenclature & Legal Disclaimer Safeguards

## Summary
Proactively sanitized all references to third-party proprietary trademarks across the codebase, documentation, and install manifests:
1. **Trademark Decoupling**:
   - Replaced proprietary references with generic descriptive terms ("Fluent Ergonomics", "Quadrant Snap Tiling", "Dark Mica Acrylic Styling", and "Interactive Task Switcher").
   - Replaced distribution brand references with generic technical terminology ("telemetry bloat", "default desktop bloat", "sandboxed snap daemon").
2. **Legal Trademark Disclaimer**:
   - Added standard open-source trademark disclaimer to `README.md` explicitly stating that all referenced trademarks belong to their respective owners and are used purely for identification and compatibility purposes.
3. **Configuration & Package Sanitization**:
   - Updated `compositor/rc.xml`, `compositor/themerc`, `astal-shell/package.json`, and `waybar_style.css` to adopt clean, neutral Fluent/Mica nomenclature.
