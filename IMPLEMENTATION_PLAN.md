# VDE (Victorious Desktop Environment) — Architectural Blueprint & Implementation Plan

> **Codename:** VDE (Windows 11 Ergonomics & Visual Familiarity for Linux)  
> **Target Idle RAM:** Sub-500 MB (Entire desktop session: compositor + shell daemons)  
> **Telemetry & Bloat:** Zero (Decoupled from web search widgets, telemetry daemons, and cloud recall)  
> **Status:** Pending Architecture Approval (Zero Code Execution Phase)

---

## 1. System Architecture Overview

```
                         +----------------------------------------------+
                         |           Labwc Wayland Compositor           |
                         |   (wlroots-based, sub-60 MB idle RAM)        |
                         |   rc.xml: Snap Hotkeys, Themes, Decor Rules   |
                         +----------------------+-----------------------+
                                                |
               +--------------------------------+--------------------------------+
               | wlr-layer-shell                                                 | wlr-layer-shell
               v                                                                 v
+-------------------------------+                               +-------------------------------+
|     Astal Shell Daemon        |                               |   Qt6 / QML Start Menu Daemon |
| (AGS v2 / TypeScript + SCSS)  |                               |   (C++ / QML, sub-40 MB RAM)  |
|                               |                               |                               |
| * Centered Taskbar            |                               | * Native App Indexer (<10ms)  |
| * Active Window Indicators    |     Session D-Bus Interface   | * On-Demand Fuzzy File Search |
| * Quick Settings Flyout       |<=============================>| * MiniCPM-V 4.7 Image Search  |
| * Notification Center & Tray  |      org.vde.Shell / Launcher | * Hardware-accelerated Acrylic|
| * Dynamic Start AI Indicator  |                               | * Strict Minimalist Layout    |
+---------------+---------------+                               +---------------+---------------+
                |                                                               |
                |                                       HTTP / OpenAI Endpoint  | (localhost:8080)
                |                                                               v
                |                                               +-------------------------------+
                |                                               | llama.cpp In-Memory Server    |
                |                                               | (MiniCPM-V 4.7 GGUF 1B Dense) |
                |                                               | Local Multimodal Vision Model |
                +-----------------------+-----------------------+-------------------------------+
                                        |
                                        v
                        +-------------------------------+
                        |   Design Token Engine         |
                        |   tokens/theme.json           |
                        |   -> SCSS / QML Sync          |
                        +-------------------------------+
```

---

## 2. Memory & Footprint Budget (<500 MB Total Session Idle)

| Component | Technology | Target Idle RAM | Role |
| :--- | :--- | :--- | :--- |
| **Compositor** | Labwc (wlroots) | 45 – 65 MB | Wayland compositor, window management, snapping, borders |
| **Panel & Flyouts** | Astal (AGS v2 / GJS) | 90 – 130 MB | Centered floating taskbar, tray, Quick Settings, PipeWire/NM |
| **Start Launcher** | Qt6 / QML + C++ | 35 – 55 MB | Fast app launcher, file query, acrylic blur, thumbnail grid |
| **Theme / IPC Bus** | D-Bus Session Daemon | ~5 MB | Low-overhead IPC coordinator (`org.vde.Shell`) |
| **Core Daemons** | PipeWire, WirePlumber | 35 – 50 MB | Low-latency audio and screen-share infrastructure |
| **Total Baseline Idle** | | **~210 – 300 MB** | **Well under the 500 MB ceiling (~40% headroom)** |
| *Local Vision AI (opt)* | llama.cpp (MiniCPM-V) | Offloaded to VRAM / Swapped when idle | Natural language visual search on local images |

---

## 3. Core Subsystems & Technical Scope

### 3.1 Compositor: Labwc
- **Protocol Support:** `wlr-layer-shell-unstable-v1`, `wlr-foreign-toplevel-management-unstable-v1`, `ext-workspace-v1`.
- **Window Snapping & Grid Layouts:** Windows 11 style snapping via `rc.xml` keybinds:
  - `Super + Left / Right`: Snap half screen.
  - `Super + Up`: Maximize or snap top half.
  - `Super + Down`: Restore or minimize.
  - `Super + Alt + Arrows`: Corner quadrant snapping.
- **Decorations:** Border radius with smooth sub-pixel anti-aliasing matching Windows 11 window curves.

### 3.2 Shell Modules (Astal / AGS v2)
1. **Centered Taskbar (`vde-bar`):**
   - Floating pill or dock mode with configurable padding and margins.
   - Pinned launchers with active window badges (running dot indicator, focus underline pill).
   - Window preview thumbnails on hover using `wlr-foreign-toplevel-management`.
   - Start Button: Dynamic AI indicator state:
     - `Idle`: Clean monochrome Windows 11-inspired geometric emblem.
     - `Inference Active`: Subtle pulsing accent dot/glow.
     - `Offline / Standby`: Dimmed opacity (50%).
     - Right-click context menu: Quick power actions, local AI daemon status, and VRAM usage.
2. **Quick Settings Flyout (`vde-quicksettings`):**
   - Windows 11 control center layout: Wi-Fi picker, Bluetooth toggles, Volume & Brightness sliders, Dark/Light mode switch, Battery saver.
   - Separate Notification Center with inline calendar widget.

### 3.3 Start Menu Runner (Qt6 / QML + C++)
1. **Application & Document Search:**
   - **XDG Desktop Indexer:** C++ inotify watcher caching `/usr/share/applications` and `~/.local/share/applications` on startup. Launch latency `< 10ms`.
   - **On-Demand Fuzzy Matcher:** Multi-threaded Smith-Waterman / Levenshtein matching on user document directories without running persistent background database crawlers.
2. **Local Multimodal Search (MiniCPM-V 4.7):**
   - Connects directly to local `llama.cpp` server (OpenAI-compatible `/v1/chat/completions` or embedding endpoint).
   - Zero Ollama dependency. Queries return matched local image paths rendered into QML thumbnail grids.
3. **Ergonomics & Visual Design:**
   - Acrylic blur background via custom GLSL fragment shader (`QQuickFramebufferObject` or Qt Quick Effects).
   - Pinned apps grid (6x3) with "All Apps" vertical scroll drawer.
   - Minimalist footer: User avatar and power flyout (Restart, Sleep, Shut Down). All debug banners removed.

---

## 4. Inter-Process Communication (IPC) Protocol

### D-Bus Interface: `org.vde.Shell` & `org.vde.Launcher`

```xml
<node>
  <!-- Shell Controller exposed by Astal -->
  <interface name="org.vde.Shell">
    <method name="ToggleQuickSettings" />
    <method name="ToggleCalendar" />
    <method name="SetTheme">
      <arg name="mode" type="s" direction="in"/> <!-- "dark" or "light" -->
    </method>
    <signal name="ThemeChanged">
      <arg name="mode" type="s"/>
    </signal>
  </interface>

  <!-- Launcher Controller exposed by Qt6 Daemon -->
  <interface name="org.vde.Launcher">
    <method name="Toggle" />
    <method name="Show" />
    <method name="Hide" />
    <signal name="VisibilityChanged">
      <arg name="visible" type="b"/>
    </signal>
    <signal name="InferenceStateChanged">
      <arg name="state" type="s"/> <!-- "idle", "active", "offline" -->
      <arg name="model" type="s"/>
    </signal>
  </interface>
</node>
```

---

## 5. Design Tokens & Styling Architecture

Shared token definition in `tokens/theme.json`:
- **Palette (Dark/Light):** Windows 11 Mica and Acrylic surfaces (`#202020` / `#F3F3F3`), border accents (`rgba(255,255,255,0.08)`), accent blues (`#0067C0` / `#0078D4`).
- **Radii:** Standard `8px` for buttons, `12px` for flyout cards, `6px` for inner badges.
- **Typography:** `Segoe UI Variable` / `Inter` / `Cantarell` fallback stack.
- **Sync Mechanism:** Build script generates `astal/style/tokens.scss` and `qt6/tokens/ThemeTokens.qml` whenever `theme.json` is modified.

---

## 6. Asset & Visual Generation Pipeline

Strict adherence to the user's asset pipeline rules:
1. **Zero Inline Art Generation:** No autonomous inline SVG generation, raw artwork, or raster icons will be created in code.
2. **Manifest Specification (`assets/asset_manifest.json`):**
   - Every needed icon or graphic asset will be appended to `assets/asset_manifest.json` with:
     - `asset_id`: Unique identifier (e.g., `icon-start-button`, `tray-wifi-connected`, `bg-acrylic-noise`).
     - `canvas_dimensions`: e.g., `24x24`, `32x32`, `256x256`.
     - `stroke_weight`: e.g., `1.5px`, `2.0px`.
     - `style_tokens`: Accent colors, fill rules, border radii.
     - `visual_description`: Detailed prompt for GLM 5.3 (vectors) or Flux 1 schnell / Flux 2/3 klein (textures/graphics).
3. **Layout Placeholders:**
   - The shell UI layouts will strictly use standard CSS/QML placeholder rectangles with bounding-box debug outlines until user-rendered assets are placed in `assets/`.

---

## 7. Phased Implementation Roadmap

### Phase 1: Environment & Token Baseline
- Define directory structure (`compositor/`, `astal-shell/`, `qt-launcher/`, `tokens/`, `assets/`).
- Initialize `assets/asset_manifest.json` with required core icons.
- Create `tokens/theme.json` with dark/light mode definitions.

### Phase 2: Compositor Configuration (Labwc)
- Configure `rc.xml` for Windows 11 snap keybindings (`Super+Arrows`), window margins, and layer-shell rules.
- Set up systemd user services for clean startup and shutdown lifecycles (`vde-session.target`).

### Phase 3: Astal Shell (Taskbar & Quick Settings)
- Implement centered taskbar with pinned launchers and active running indicators.
- Build system tray and Quick Settings flyout (audio slider, network toggle, theme switch).
- Implement D-Bus client listener for Start Menu trigger and dynamic AI status badge.

### Phase 4: Qt6 Start Menu & Search Runner
- Implement C++ XDG `.desktop` fast file watcher and parser (<10ms indexing).
- Build QML drawer with hardware-accelerated acrylic blur shader and smooth entry/exit animations.
- Implement HTTP client for local `llama.cpp` MiniCPM-V 4.7 vision queries.
- Connect D-Bus interface `org.vde.Launcher` to Astal taskbar.

### Phase 5: Polishing, Benchmarking & Validation
- Profile idle memory footprint under `valgrind` / `ps_mem` to verify `<500 MB` target.
- Validate telemetry scrubbing (confirm zero network traffic to external servers on launch and query).
