#!/usr/bin/env python3
"""
Generates the interactive desktop visual preview HTML artifact.
"""

from pathlib import Path

ARTIFACT_DIR = Path(r"C:\Users\Victor\.gemini\antigravity\brain\4aa0166f-e165-4662-8bfe-ab956574c3c4")
ICONS_DIR = Path("assets/icons")

def read_svg(name):
    p = ICONS_DIR / name
    if p.exists():
        content = p.read_text(encoding="utf-8").strip()
        # strip xml declaration if any
        if content.startswith("<?xml"):
            content = content.split("?>", 1)[1].strip()
        return content
    return f"<!-- {name} missing -->"

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>VDE Desktop Environment — Visual Prototype</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;500;600;700&display=swap');
    
    * {{
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
      user-select: none;
    }}

    .desktop-bg {{
      background: radial-gradient(circle at 50% 60%, #1e2638 0%, #0d1117 75%, #080a0f 100%);
      background-image: 
        radial-gradient(ellipse at 50% 40%, rgba(30, 75, 145, 0.35) 0%, transparent 60%),
        radial-gradient(circle at 75% 70%, rgba(20, 110, 180, 0.25) 0%, transparent 50%),
        radial-gradient(circle at 25% 70%, rgba(10, 45, 95, 0.35) 0%, transparent 50%);
    }}

    .acrylic-glass {{
      background: rgba(32, 32, 32, 0.82);
      backdrop-filter: blur(28px) saturate(125%);
      -webkit-backdrop-filter: blur(28px) saturate(125%);
      border: 1px solid rgba(255, 255, 255, 0.09);
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.45), 0 0 0 1px rgba(255, 255, 255, 0.05);
    }}

    .taskbar-glass {{
      background: rgba(32, 32, 32, 0.85);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    }}

    .tile-hover:hover {{
      background: rgba(255, 255, 255, 0.06);
    }}

    .tile-hover:active {{
      background: rgba(255, 255, 255, 0.04);
      transform: scale(0.96);
    }}

    .ai-active-glow {{
      box-shadow: 0 0 14px rgba(76, 194, 255, 0.45);
      border: 1px solid rgba(76, 194, 255, 0.4);
    }}
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col p-4 antialiased overflow-hidden select-none">

  <!-- Interactive Controls Bar -->
  <div class="mb-3 flex items-center justify-between bg-slate-900/80 border border-slate-800 rounded-xl px-4 py-2 text-xs">
    <div class="flex items-center gap-3">
      <span class="font-bold text-sky-400 tracking-wider">VDE SHELL SIMULATOR</span>
      <span class="text-slate-400">|</span>
      <span class="text-slate-300">Target Idle RAM: <strong class="text-emerald-400">~240 MB</strong> (Target &lt;500 MB)</span>
      <span class="text-slate-400">|</span>
      <span class="text-slate-300">Telemetry: <strong class="text-sky-400">0 KB/s (Offline)</strong></span>
    </div>
    
    <div class="flex items-center gap-2">
      <span class="text-slate-400 mr-1">AI Status Test:</span>
      <button onclick="setAiState('idle')" id="btn-idle" class="px-2.5 py-1 rounded-md bg-slate-800 border border-slate-700 text-slate-200 hover:bg-slate-700 transition">Idle</button>
      <button onclick="setAiState('active')" id="btn-active" class="px-2.5 py-1 rounded-md bg-sky-950/80 border border-sky-500/50 text-sky-300 hover:bg-sky-900 transition">Inference Active</button>
      <button onclick="setAiState('offline')" id="btn-offline" class="px-2.5 py-1 rounded-md bg-slate-800 border border-slate-700 text-slate-400 hover:bg-slate-700 transition">Offline</button>
      <div class="h-4 w-px bg-slate-800 mx-1"></div>
      <button onclick="toggleStartMenu()" class="px-3 py-1 rounded-md bg-sky-600 text-white font-medium hover:bg-sky-500 transition">Toggle Start</button>
      <button onclick="toggleQuickSettings()" class="px-3 py-1 rounded-md bg-slate-800 border border-slate-700 text-slate-200 hover:bg-slate-700 transition">Toggle Quick Settings</button>
    </div>
  </div>

  <!-- Simulated Desktop Viewport -->
  <div class="relative flex-1 rounded-2xl border border-slate-800/80 desktop-bg overflow-hidden flex flex-col justify-end p-3 shadow-2xl" style="min-height: 640px;">
    
    <!-- Desktop Sample Window (to demonstrate snapping & window decorations) -->
    <div class="absolute top-10 left-12 w-80 rounded-xl bg-slate-900/90 border border-white/10 shadow-xl overflow-hidden pointer-events-none opacity-85">
      <div class="h-8 bg-[#202020] px-3 flex items-center justify-between border-b border-white/5">
        <div class="flex items-center gap-2">
          <span class="w-4 h-4 flex items-center justify-center">{read_svg('app-files-dark.svg')}</span>
          <span class="text-xs font-medium text-slate-200">File Explorer</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="w-3.5 h-3.5 text-slate-400">{read_svg('window-minimize-dark.svg')}</span>
          <span class="w-3.5 h-3.5 text-slate-400">{read_svg('window-maximize-dark.svg')}</span>
          <span class="w-3.5 h-3.5 text-slate-400">{read_svg('window-close-dark.svg')}</span>
        </div>
      </div>
      <div class="p-4 text-xs text-slate-400 space-y-1">
        <div>Home / Victor / Documents</div>
        <div class="h-px bg-white/5 my-2"></div>
        <div class="flex items-center gap-2 text-slate-300">📁 Projects</div>
        <div class="flex items-center gap-2 text-slate-300">📁 Downloads</div>
        <div class="flex items-center gap-2 text-slate-300">📁 Pictures</div>
      </div>
    </div>

    <!-- START MENU FLYOUT (Qt6 / QML Drawer Mockup) -->
    <div id="start-menu" class="absolute bottom-16 left-1/2 -translate-x-1/2 w-[540px] acrylic-glass rounded-2xl p-5 z-20 flex flex-col gap-4 transition-all duration-200">
      
      <!-- 1. Search Box -->
      <div class="w-full h-10 rounded-full bg-[#242424] border border-white/10 px-4 flex items-center gap-3 focus-within:border-sky-400 focus-within:ring-1 focus-within:ring-sky-400 transition">
        <div class="w-4 h-4 text-slate-400 flex items-center justify-center">
          {read_svg('search-dark.svg')}
        </div>
        <input type="text" placeholder="Type here to search apps, files, or images..." class="bg-transparent text-xs text-slate-100 placeholder:text-slate-500 outline-none w-full" />
      </div>

      <!-- 2. Pinned Header -->
      <div class="flex items-center justify-between px-1">
        <span class="text-xs font-semibold text-slate-100">Pinned</span>
        <button class="text-xs text-slate-400 hover:text-sky-400 transition flex items-center gap-1">All apps &gt;</button>
      </div>

      <!-- 3. Pinned Apps Grid (6x2) -->
      <div class="grid grid-cols-6 gap-2">
        <!-- App 1: Explorer -->
        <div class="flex flex-col items-center p-2 rounded-lg tile-hover cursor-pointer transition">
          <div class="w-9 h-9 flex items-center justify-center mb-1">{read_svg('app-files-dark.svg')}</div>
          <span class="text-[11px] text-slate-200 text-center leading-tight">Explorer</span>
        </div>
        <!-- App 2: Browser -->
        <div class="flex flex-col items-center p-2 rounded-lg tile-hover cursor-pointer transition">
          <div class="w-9 h-9 flex items-center justify-center mb-1">{read_svg('app-browser-dark.svg')}</div>
          <span class="text-[11px] text-slate-200 text-center leading-tight">Browser</span>
        </div>
        <!-- App 3: Editor -->
        <div class="flex flex-col items-center p-2 rounded-lg tile-hover cursor-pointer transition">
          <div class="w-9 h-9 flex items-center justify-center mb-1">{read_svg('app-editor-dark.svg')}</div>
          <span class="text-[11px] text-slate-200 text-center leading-tight">Editor</span>
        </div>
        <!-- App 4: Terminal -->
        <div class="flex flex-col items-center p-2 rounded-lg tile-hover cursor-pointer transition">
          <div class="w-9 h-9 flex items-center justify-center mb-1">{read_svg('settings-dark.svg')}</div>
          <span class="text-[11px] text-slate-200 text-center leading-tight">Terminal</span>
        </div>
        <!-- App 5: Settings -->
        <div class="flex flex-col items-center p-2 rounded-lg tile-hover cursor-pointer transition">
          <div class="w-9 h-9 flex items-center justify-center mb-1">{read_svg('settings-dark.svg')}</div>
          <span class="text-[11px] text-slate-200 text-center leading-tight">Settings</span>
        </div>
        <!-- App 6: AI Vision Search -->
        <div class="flex flex-col items-center p-2 rounded-lg tile-hover cursor-pointer transition bg-sky-950/20 border border-sky-500/20">
          <div class="w-9 h-9 flex items-center justify-center mb-1 text-sky-400">{read_svg('start-active-dark.svg')}</div>
          <span class="text-[11px] text-sky-300 text-center leading-tight font-medium">Vision AI</span>
        </div>
      </div>

      <div class="h-px bg-white/5 my-0.5"></div>

      <!-- 4. Footer User Profile & Power -->
      <div class="flex items-center justify-between pt-1">
        <div class="flex items-center gap-2.5 px-1 py-1 rounded-lg tile-hover cursor-pointer">
          <div class="w-7 h-7 rounded-full bg-sky-700 text-white font-bold text-xs flex items-center justify-center shadow-inner">V</div>
          <span class="text-xs font-medium text-slate-200">Victor</span>
        </div>

        <div class="flex items-center gap-1">
          <button title="Sleep" class="p-1.5 rounded-lg tile-hover text-slate-300 transition w-7 h-7 flex items-center justify-center">{read_svg('power-sleep-dark.svg')}</button>
          <button title="Restart" class="p-1.5 rounded-lg tile-hover text-slate-300 transition w-7 h-7 flex items-center justify-center">{read_svg('power-restart-dark.svg')}</button>
          <button title="Shut Down" class="p-1.5 rounded-lg tile-hover hover:bg-rose-900/50 text-slate-300 hover:text-rose-200 transition w-7 h-7 flex items-center justify-center">{read_svg('power-shutdown-dark.svg')}</button>
        </div>
      </div>
    </div>

    <!-- QUICK SETTINGS FLYOUT (Astal Shell Mockup) -->
    <div id="quick-settings" class="absolute bottom-16 right-4 w-80 acrylic-glass rounded-2xl p-4 z-20 flex flex-col gap-3.5 transition-all duration-200">
      
      <!-- 2x2 Toggle Grid -->
      <div class="grid grid-cols-2 gap-2">
        <!-- Wi-Fi Active -->
        <div class="bg-sky-600 rounded-xl p-2.5 flex items-center gap-3 cursor-pointer shadow-sm">
          <div class="w-5 h-5 flex items-center justify-center text-white">{read_svg('wifi-dark.svg')}</div>
          <div class="flex flex-col">
            <span class="text-xs font-semibold text-white leading-tight">Wi-Fi</span>
            <span class="text-[11px] text-sky-100">Connected</span>
          </div>
        </div>

        <!-- Bluetooth -->
        <div class="bg-[#2d2d2d] border border-white/5 rounded-xl p-2.5 flex items-center gap-3 cursor-pointer tile-hover">
          <div class="w-5 h-5 flex items-center justify-center text-slate-300">{read_svg('bluetooth-dark.svg')}</div>
          <div class="flex flex-col">
            <span class="text-xs font-semibold text-slate-200 leading-tight">Bluetooth</span>
            <span class="text-[11px] text-slate-400">Off</span>
          </div>
        </div>

        <!-- Dark Theme -->
        <div class="bg-sky-600 rounded-xl p-2.5 flex items-center gap-3 cursor-pointer shadow-sm">
          <div class="w-5 h-5 flex items-center justify-center text-white">{read_svg('theme-switch-dark.svg')}</div>
          <div class="flex flex-col">
            <span class="text-xs font-semibold text-white leading-tight">Theme</span>
            <span class="text-[11px] text-sky-100">Dark Mica</span>
          </div>
        </div>

        <!-- Flight Mode -->
        <div class="bg-[#2d2d2d] border border-white/5 rounded-xl p-2.5 flex items-center gap-3 cursor-pointer tile-hover">
          <div class="w-5 h-5 flex items-center justify-center text-slate-300">{read_svg('airplane-dark.svg')}</div>
          <div class="flex flex-col">
            <span class="text-xs font-semibold text-slate-200 leading-tight">Airplane</span>
            <span class="text-[11px] text-slate-400">Off</span>
          </div>
        </div>
      </div>

      <!-- Sliders -->
      <div class="flex flex-col gap-2.5 pt-1">
        <!-- Volume -->
        <div class="flex items-center gap-2.5">
          <div class="w-4 h-4 text-slate-300 flex items-center justify-center">{read_svg('volume-dark.svg')}</div>
          <input type="range" min="0" max="100" value="70" class="flex-1 accent-sky-400 h-1.5 bg-slate-700 rounded-lg cursor-pointer" />
        </div>
      </div>

      <div class="h-px bg-white/5 my-0.5"></div>

      <!-- Battery & Power -->
      <div class="flex items-center justify-between text-xs text-slate-300 pt-0.5">
        <div class="flex items-center gap-2">
          <div class="w-4 h-4 text-slate-300 flex items-center justify-center">{read_svg('battery-dark.svg')}</div>
          <span class="font-medium text-slate-200">85% Battery</span>
        </div>
        <div class="flex items-center gap-1.5">
          <button class="w-7 h-7 rounded-lg tile-hover flex items-center justify-center text-slate-300">{read_svg('power-shutdown-dark.svg')}</button>
        </div>
      </div>
    </div>

    <!-- MAIN FLOATING TASKBAR (Astal Layer-Shell Dock) -->
    <div class="w-full flex items-center justify-between taskbar-glass rounded-xl h-12 px-3 z-30 shadow-lg">
      
      <!-- Left: Widgets / Workspace indicator -->
      <div class="flex items-center gap-2">
        <button class="w-8 h-8 rounded-lg tile-hover flex items-center justify-center text-slate-300" title="Task View (Win+Tab)">
          <div class="w-4 h-4">{read_svg('all-apps-dark.svg')}</div>
        </button>
      </div>

      <!-- Center: Windows 11 Centered Dock Items -->
      <div class="flex items-center gap-1">
        <!-- Start Button -->
        <button id="start-btn" onclick="toggleStartMenu()" class="w-10 h-9 rounded-lg tile-hover flex items-center justify-center transition p-1" title="Start">
          <div id="start-icon" class="w-6 h-6 flex items-center justify-center">
            {read_svg('start-idle-dark.svg')}
          </div>
        </button>

        <!-- Search Lens -->
        <button onclick="toggleStartMenu()" class="w-10 h-9 rounded-lg tile-hover flex flex-col items-center justify-center transition p-1" title="Search">
          <div class="w-5 h-5 flex items-center justify-center text-slate-200">{read_svg('search-dark.svg')}</div>
          <div class="w-1 h-1 rounded-full bg-transparent mt-0.5"></div>
        </button>

        <!-- Pinned Explorer -->
        <button class="w-10 h-9 rounded-lg tile-hover flex flex-col items-center justify-center transition p-1" title="File Explorer">
          <div class="w-5 h-5 flex items-center justify-center">{read_svg('app-files-dark.svg')}</div>
          <!-- Running indicator dot -->
          <div class="w-1 h-1 rounded-full bg-sky-400 mt-0.5"></div>
        </button>

        <!-- Pinned Browser (Focused window indicator) -->
        <button class="w-10 h-9 rounded-lg bg-white/5 flex flex-col items-center justify-center transition p-1" title="Web Browser (Active)">
          <div class="w-5 h-5 flex items-center justify-center">{read_svg('app-browser-dark.svg')}</div>
          <!-- Focused indicator underline bar -->
          <div class="w-3.5 h-0.5 rounded-full bg-sky-400 mt-0.5"></div>
        </button>

        <!-- Pinned Editor -->
        <button class="w-10 h-9 rounded-lg tile-hover flex flex-col items-center justify-center transition p-1" title="Text Editor">
          <div class="w-5 h-5 flex items-center justify-center">{read_svg('app-editor-dark.svg')}</div>
          <div class="w-1 h-1 rounded-full bg-transparent mt-0.5"></div>
        </button>

        <!-- Terminal -->
        <button class="w-10 h-9 rounded-lg tile-hover flex flex-col items-center justify-center transition p-1" title="Terminal">
          <div class="w-5 h-5 flex items-center justify-center">{read_svg('settings-dark.svg')}</div>
          <div class="w-1 h-1 rounded-full bg-sky-400 mt-0.5"></div>
        </button>
      </div>

      <!-- Right: System Tray & Quick Settings Pill & Clock -->
      <div class="flex items-center gap-1.5">
        <!-- Grouped Quick Settings Pill -->
        <button onclick="toggleQuickSettings()" class="flex items-center gap-2 px-2.5 py-1.5 rounded-lg tile-hover transition" title="Quick Settings">
          <div class="w-3.5 h-3.5 flex items-center justify-center text-slate-300">{read_svg('wifi-dark.svg')}</div>
          <div class="w-3.5 h-3.5 flex items-center justify-center text-slate-300">{read_svg('volume-dark.svg')}</div>
          <div class="w-3.5 h-3.5 flex items-center justify-center text-slate-300">{read_svg('battery-dark.svg')}</div>
        </button>

        <!-- Clock & Date -->
        <button onclick="toggleStartMenu()" class="flex flex-col items-end px-2 py-1 rounded-lg tile-hover transition">
          <span class="text-xs font-medium text-slate-100 leading-tight">12:45 PM</span>
          <span class="text-[10px] text-slate-400 leading-tight">10/27/2026</span>
        </button>

        <!-- Show Desktop strip -->
        <div class="w-1 h-6 rounded-sm hover:bg-white/20 transition cursor-pointer ml-1" title="Show Desktop"></div>
      </div>
    </div>
  </div>

  <script>
    const idleSvg = `{read_svg('start-idle-dark.svg')}`;
    const activeSvg = `{read_svg('start-active-dark.svg')}`;
    const offlineSvg = `{read_svg('start-offline-dark.svg')}`;

    function toggleStartMenu() {{
      const el = document.getElementById('start-menu');
      el.classList.toggle('hidden');
    }}

    function toggleQuickSettings() {{
      const el = document.getElementById('quick-settings');
      el.classList.toggle('hidden');
    }}

    function setAiState(state) {{
      const icon = document.getElementById('start-icon');
      const btn = document.getElementById('start-btn');
      
      // Update icon
      if (state === 'active') {{
        icon.innerHTML = activeSvg;
        btn.classList.add('ai-active-glow');
      }} else if (state === 'offline') {{
        icon.innerHTML = offlineSvg;
        btn.classList.remove('ai-active-glow');
      }} else {{
        icon.innerHTML = idleSvg;
        btn.classList.remove('ai-active-glow');
      }}
    }}
  </script>
</body>
</html>
"""

ARTIFACT_PATH = ARTIFACT_DIR / "vde_desktop_preview.html"
ARTIFACT_PATH.write_text(html_content, encoding="utf-8")
print(f"Created visual preview artifact at: {ARTIFACT_PATH}")
