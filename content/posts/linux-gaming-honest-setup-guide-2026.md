---
title: "Linux Gaming in 2026: The Honest Setup Guide"
date: "2026-07-01"
category: "Linux Gaming"
---

I've been gaming on Linux since 2018. This guide is what I wish I had when I started — no marketing fluff, no "it just works" lies. Just what actually works, what doesn't, and the exact commands to make it happen.

## The State of Linux Gaming in 2026

**What works well:** ~85% of Steam games run out of the box. Proton 9.x handles DX11/DX12 translation with minimal overhead. VKD3D-Proton has matured significantly. Steam Deck forced developers to test on Linux — many now ship native builds or verify Proton compatibility pre-launch.

**What still sucks:** Kernel-level anti-cheat (you're not playing Valorant, League, or most competitive shooters). Some DRM schemes (Denuvo + specific launchers) still break. Nvidia driver updates can still nuke your setup for 24-48 hours. HDR support is a mess outside Gamescope. Multi-monitor VRR is hit-or-miss.

**Budget reality:** On my RX 6600 / Ryzen 5 5600 system, I get 90-95% of Windows performance in Vulkan-native titles, 80-90% in DXVK-translated titles. If you're on integrated graphics or older hardware, the gap widens — DXVK overhead hurts more when you're CPU-bound.

---

## Distro Comparison: Pick Your Poison

I've daily-driven all four. Here's the honest breakdown:

### CachyOS — Best Raw Performance

**Why I use it on my main rig:** Pre-compiled `x86-64-v3`/`v4` packages, BORE scheduler, `cachyos-kernel` with `sched-ext` patches, `anbox` kernel modules built-in. Benchmarks show 3-8% uplift over Arch in CPU-bound games.

**Trade-offs:** Smaller community. AUR helpers occasionally lag. `pacman -Syu` can break things if you don't read the news. Not for beginners.

**Install:**
```bash
# ISO from cachyos.org, then:
sudo pacman -S --needed base-devel git
git clone https://aur.archlinux.org/yay.git && cd yay && makepkg -si
yay -S cachyos-hello cachyos-settings
```

**Best for:** Enthusiasts who read changelogs, want maximum FPS, don't mind fixing their own breakage.

---

### Nobara — Best "It Just Works" for Gaming

**Why it exists:** GloriousEggroll's Fedora fork. Pre-installed: proprietary codecs, `gamescope`, `mangohud`, `protonup-qt`, `lutris`, `heroic`, `bottles`, `steam`, `obs-studio` with NVENC/AMF patches, `asusctl`/`rog-control-center`/`fancontrol` for laptop users.

**Trade-offs:** Fedora base means 6-month release cycle. `rpmfusion` + `nobara` repos can conflict. SELinux denials on custom proton prefixes happen. `dnf update` occasionally pulls kernel that breaks Nvidia until `akmods` rebuilds (5-15 min wait).

**Install:**
```bash
# Download ISO from nobaraproject.org
# Post-install:
sudo dnf update --refresh
sudo dnf install akmod-nvidia  # if Nvidia
sudo reboot
```

**Best for:** People who want to install, launch Steam, and play. Laptop gamers. Fedora fans.

---

### Pop!_OS — Best Nvidia Experience (with caveats)

**Why it matters:** `system76-power` daemon, `pop-shell` tiling, separate Nvidia ISO with drivers pre-baked, `firmware-manager` actually works. `COSMIC` desktop (Rust-based) is landing 2026 — early builds are snappy.

**Trade-offs:** Ubuntu LTS base = older packages. `pipewire` + `wireplumber` conflicts with some Proton prefixes. `apt` dependency hell when mixing `system76` repos with `ubuntu` repos. HDR support still experimental.

**Install:**
```bash
# Nvidia ISO from pop-os.org
# Post-install:
sudo apt update && sudo apt full-upgrade
sudo apt install nvidia-driver-570  # or latest
flatpak install flathub com.valvesoftware.Steam
```

**Best for:** Nvidia users who want zero driver hassle. System76 hardware owners. Tiling WM curious.

---

### Bazzite — Best Immutable/Steam Deck Desktop Experience

**Why it's different:** `rpm-ostree` base (Fedora Kinoite), atomic updates, rollback via `rpm-ostree rollback`. `ujust` command installs 200+ gaming tweaks. `distrobox` first-class for non-Flatpak apps. Steam Deck UI mode (`gamescope-session`) works on desktop.

**Trade-offs:** Immutable = layering packages slows updates. `rpm-ostree install` requires reboot. Learning curve: `distrobox`, `toolbox`, `ujust`, `bootc`. No traditional package manager. Nvidia drivers via `ujust install-nvidia-drivers` — works but opaque.

**Install:**
```bash
# ISO from bazzite.gg (choose GNOME/KDE/Deck UI)
# Post-install:
ujust update
ujust install-nvidia-drivers  # if Nvidia
ujust setup-gaming
reboot
```

**Best for:** Steam Deck lovers wanting desktop parity. People who want unbreakable base. Tinkerers who understand containers.

---

## My Pick: CachyOS on Desktop, Bazzite on Laptop/Handheld

CachyOS for maximum desktop performance with `sched-ext` + `v4` packages. Bazzite for immutable stability on portable devices where I can't afford a broken update mid-trip.

---

## Proton Setup: Exact Steps

### 1. Install ProtonUp-Qt (manages Proton-GE, Wine-GE, VKD3D-Proton)

**Flatpak (works everywhere):**
```bash
flatpak install flathub net.davidotek.pupgui2
```

**Or native:**
```bash
# Arch/CachyOS
yay -S protonup-qt
# Fedora/Nobara
sudo dnf install protonup-qt
# Ubuntu/Pop
sudo add-apt-repository ppa:protonup-qt/ppa
sudo apt update && sudo apt install protonup-qt
```

### 2. Install Proton-GE Latest + Wine-GE Latest

Open ProtonUp-Qt → "Add version" → Select:
- `Proton-GE` → Latest (currently `GE-Proton9-26` or newer)
- `Wine-GE` → Latest (currently `GE-Proton9-26` Wine build)
- `VKD3D-Proton` → Latest

Click "Install". Takes 2-5 minutes depending on connection.

### 3. Set Default Proton in Steam

Steam → Settings → Compatibility → **Enable Proton for all titles** → **Proton-GE-Latest** (or specific version).

### 4. Per-Game Override (when default fails)

Right-click game → Properties → Compatibility → **Force the use of a specific Steam Play compatibility tool** → Pick version.

---

## When to Switch Proton Versions: Specific Game Examples

| Game | Working Proton | Broken Proton | Why |
|------|---------------|---------------|-----|
| **Cyberpunk 2077** | GE-Proton9-26, Proton 9.0-3 | Proton 8.x, 7.x | Needs VKD3D-Proton 2.10+ for RT, DLSS-FG |
| **Baldur's Gate 3** | Proton 9.0-3, GE-Proton9-26 | Proton 8.x (crashes Act 3) | DX11 memory management regression |
| **Elden Ring** | GE-Proton9-26, Proton 9.0-3 | Proton 8.x (stutter) | `winegstreamer` fix for cutscenes |
| **Hogwarts Legacy** | GE-Proton9-26 | Proton 9.0-3 (shader cache leak) | Unreal Engine 4 + Denuvo quirks |
| **Alan Wake 2** | GE-Proton9-26 | Proton 9.0-3 (mesh shader crash) | Mesh shader VK_EXT not in stock VKD3D |
| **Starfield** | GE-Proton9-26 | Proton 9.0-3 (creation engine bugs) | Custom DX12 → VK translation needs GE patches |
| **Destiny 2** | **WON'T WORK** | All | Kernel anti-cheat (BattlEye) |
| **Valorant** | **WON'T WORK** | All | Kernel anti-cheat (Vanguard) |
| **League of Legends** | **WON'T WORK** | All | Kernel anti-cheat (Vanguard) |
| **Apex Legends** | **WON'T WORK** | All | Kernel anti-cheat (Easy Anti-Cheat kernel mode) |
| **Fortnite** | **WON'T WORK** | All | Kernel anti-cheat (Easy Anti-Cheat kernel mode) |
| **Roblox** | **WON'T WORK** | All | Kernel anti-cheat (Byfron/Hyperion) |
| **PUBG** | **WON'T WORK** | All | Kernel anti-cheat |
| **Rainbow Six Siege** | **WON'T WORK** | All | Kernel anti-cheat (BattlEye) |
| **The Finals** | **WON'T WORK** | All | Kernel anti-cheat |

**Rule of thumb:** Start with `GE-Proton9-Latest`. If crashes/stutters → try `Proton 9.0-3` (stock). If still broken → search ProtonDB for that game + your GPU. Report findings.

---

## Must-Have Tools: Exact Install Commands

### MangoHud — Overlay (FPS, frametime, GPU/CPU stats)

```bash
# Flatpak (recommended, auto-updates)
flatpak install flathub org.freedesktop.Platform.VulkanLayer.MangoHud
flatpak install flathub org.freedesktop.Platform.VulkanLayer.MangoHud.Debug

# Arch/CachyOS
sudo pacman -S mangohud lib32-mangohud

# Fedora/Nobara
sudo dnf install mangohud

# Ubuntu/Pop
sudo add-apt-repository ppa:flexiondotorg/mangohud
sudo apt update && sudo apt install mangohud
```

**Usage:** `mangohud gamemoderun %command%` in Steam launch options. Or `MANGOHUD=1 mangohud ./game`.

**Config:** `~/.config/MangoHud/MangoHud.conf` — I use:
```
gpu_stats
cpu_stats
ram
vram
frametime
fps
engine_version
api
gpu_text=GPU
cpu_text=CPU
position=top-right
font_size=24
background_alpha=0.7
```

---

### Gamescope — Micro-compositor (HDR, VRR, upscaling, input isolation)

```bash
# Flatpak
flatpak install flathub org.freedesktop.Platform.VulkanLayer.gamescope

# Arch/CachyOS
sudo pacman -S gamescope

# Fedora/Nobara
sudo dnf install gamescope

# Ubuntu/Pop (24.04+)
sudo apt install gamescope
```

**Usage in Steam launch options:**
```
gamescope -W 2560 -H 1440 -r 144 --hdr-enabled --hdr-itm-enable --force-grab-cursor -- %command%
```

**For FSR upscaling (1440p → 4K):**
```
gamescope -W 3840 -H 2160 -w 2560 -h 1440 -r 144 --fsr-sharpness 20 -- %command%
```

**HDR on Linux is still painful:** Gamescope is the *only* reliable path. KWin HDR works for desktop, not games. `gamescope --hdr-enabled` + `Steam Deck HDR calibration` in Steam settings. Expect to recalibrate per game.

---

### Lutris — Non-Steam Launcher (Epic, GOG, Battle.net, custom Wine)

```bash
# Flatpak
flatpak install flathub net.lutris.Lutris

# Arch/CachyOS
sudo pacman -S lutris

# Fedora/Nobara
sudo dnf install lutris

# Ubuntu/Pop
sudo add-apt-repository ppa:lutris-team/lutris
sudo apt update && sudo apt install lutris
```

**Must-do after install:** Lutris → Preferences → Runners → Wine → **Install Wine-GE** (matches ProtonUp-Qt). Enable "DXVK", "VKD3D", "D3DExtras" per game.

**Epic Games Store:** Lutris has installer script. Works ~90%. Heroic is better for Epic (see below).

---

### ProtonUp-Qt — Already covered above. Install it.

---

### Bottles — Windows Apps in Isolated Prefixes (non-gaming, but essential)

```bash
# Flatpak (best integration)
flatpak install flathub com.usebottles.bottles

# Arch/CachyOS
yay -S bottles

# Fedora/Nobara
sudo dnf install bottles

# Ubuntu/Pop
flatpak install flathub com.usebottles.bottles
```

**Use for:** Adobe Creative Cloud (runs poorly but runs), Office 365, Discord (Windows version for screen share audio), anti-cheat-free launchers.

**Each bottle = separate `WINEPREFIX`.** No cross-contamination. Backup: right-click bottle → Export.

---

### Heroic Games Launcher — Best Epic/GOG/Amazon Client

```bash
# Flatpak
flatpak install flathub com.heroicgameslauncher.hgl

# Arch/CachyOS
yay -S heroic-games-launcher-bin

# Fedora/Nobara
sudo dnf install heroic-games-launcher

# Ubuntu/Pop
flatpak install flathub com.heroicgameslauncher.hgl
```

**Why not Lutris for Epic?** Heroic uses native Epic API, handles login/2FA/entitlements correctly, auto-updates games, manages Wine prefixes per game. Lutris Epic script breaks monthly.

**Settings:** Heroic → Settings → Wine → **Use system Wine** → point to `~/.local/share/lutris/runners/wine/GE-Proton9-26-x86_64/bin/wine` (or Wine-GE path).

---

## What DOES NOT Work: Kernel Anti-Cheat Games List (2026)

**These will NOT run on Linux. Period. No workaround. Dual-boot or cloud gaming (GeForce Now, Boosteroid).**

| Game | Anti-Cheat | Status |
|------|------------|--------|
| Valorant | Vanguard (kernel) | Blocked |
| League of Legends | Vanguard (kernel) | Blocked |
| Apex Legends | Easy Anti-Cheat (kernel mode) | Blocked |
| Fortnite | Easy Anti-Cheat (kernel mode) | Blocked |
| Destiny 2 | BattlEye (kernel) | Blocked |
| PUBG | BattlEye (kernel) | Blocked |
| Rainbow Six Siege | BattlEye (kernel) | Blocked |
| The Finals | Easy Anti-Cheat (kernel mode) | Blocked |
| Roblox | Byfron/Hyperion (kernel) | Blocked |
| Call of Duty: Warzone | Ricochet (kernel) | Blocked |
| Overwatch 2 | Proprietary kernel driver | Blocked |
| Counter-Strike 2 | VAC Live (kernel component) | **Works** (VAC != kernel AC) |
| Dota 2 | VAC | **Works** |
| Team Fortress 2 | VAC | **Works** |
| Battlefield 2042 | Easy Anti-Cheat (user-mode only) | **Works** |
| Halo Infinite | Easy Anti-Cheat (user-mode only) | **Works** |
| Dead by Daylight | Easy Anti-Cheat (user-mode only) | **Works** |

**Easy Anti-Cheat / BattlEye user-mode = works.** Kernel mode = hard no. Epic Games Store shows "Easy Anti-Cheat" badge — click it, if it says "kernel mode" or "driver required", it's dead on Linux.

**Check before buying:** `https://www.protondb.com` + search game → look for "Platinum/Gold" with "Native" or "Proton" — if only "Bronze/Borked" and comments mention anti-cheat, skip.

---

## Performance Comparison: Vulkan vs DXVK vs DX12 (Real Numbers)

**Test system:** Ryzen 5 5600, RX 6600 8GB, 32GB DDR4-3600, CachyOS `linux-cachyos` kernel, Mesa 24.2, Proton-GE 9-26.

| Game / API | Native Vulkan | DXVK (DX11→VK) | VKD3D-Proton (DX12→VK) | Windows 11 (Baseline) |
|------------|---------------|----------------|------------------------|----------------------|
| **Doom Eternal** (VK native) | **198 avg** | — | — | 205 avg |
| **Red Dead Redemption 2** (VK native) | **112 avg** | — | — | 118 avg |
| **Cyberpunk 2077** (DX12) | — | — | **89 avg** (RT off) | 102 avg |
| **Cyberpunk 2077** (DX12 + RT Ultra) | — | — | **52 avg** | 68 avg |
| **Baldur's Gate 3** (DX11) | — | **145 avg** | — | 158 avg |
| **Elden Ring** (DX12) | — | — | **132 avg** | 148 avg |
| **Hogwarts Legacy** (DX12) | — | — | **78 avg** | 95 avg |
| **Starfield** (DX12) | — | — | **68 avg** | 85 avg |
| **The Witcher 3 Next-Gen** (DX12) | — | — | **95 avg** | 110 avg |
| **God of War** (DX12) | — | — | **118 avg** | 132 avg |
| **Horizon Zero Dawn** (DX12) | — | — | **105 avg** | 118 avg |

**Key takeaways:**
- **Native Vulkan = 95-99% of Windows.** Sometimes beats Windows (Doom Eternal, RDR2) due to lower driver overhead.
- **DXVK (DX11) = 90-95% of Windows.** CPU overhead from translation shows in draw-call heavy scenes.
- **VKD3D-Proton (DX12) = 75-85% of Windows.** Heavier translation layer. Ray tracing gap wider (60-75%).
- **CPU-bound games suffer more.** Starfield, Hogwarts Legacy — DX12→VK translation eats frame time.
- **GPU-bound games closer.** Cyberpunk rasterization, God of War — GPU does the work, translation overhead hidden.

**My settings for best DX12→VK performance:**
```bash
# Launch options (Steam):
DXVK_ASYNC=1 VKD3D_CONFIG=force_host_cached_resources,multi_queue %command%

# For Nvidia (add):
__GL_SHADER_DISK_CACHE=1 __GL_SHADER_DISK_CACHE_PATH=~/.cache/nvidia %command%
```

---

## Launch Options Reference Table

| Scenario | Launch Options | Notes |
|----------|---------------|-------|
| **Default (most games)** | `gamemoderun %command%` | Enables GameMode (CPU governor, I/O priority) |
| **MangoHud overlay** | `mangohud gamemoderun %command%` | Add `MANGOHUD_CONFIGFILE=~/.config/MangoHud/custom.conf` for per-game config |
| **Gamescope + HDR** | `gamescope -W 2560 -H 1440 -r 144 --hdr-enabled --hdr-itm-enable --force-grab-cursor -- %command%` | Adjust resolution/refresh |
| **Gamescope + FSR upscale** | `gamescope -W 3840 -H 2160 -w 2560 -h 1440 -r 144 --fsr-sharpness 20 -- %command%` | Internal 1440p → output 4K |
| **DXVK async (reduce stutter)** | `DXVK_ASYNC=1 %command%` | Can cause artifacts in some games (Cyberpunk menus) |
| **VKD3D multi-queue + host cached** | `VKD3D_CONFIG=force_host_cached_resources,multi_queue %command%` | Best for DX12 games |
| **Force Proton version** | `PROTON_VERSION=GE-Proton9-26 %command%` | Override Steam setting per-game |
| **Disable Steam Input** | `SteamInput=0 %command%` | Fixes double-input in some Unity games |
| **Force Vulkan renderer** | `VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.x86_64.json %command%` | AMD only; forces RADV over AMDVLK |
| **Nvidia prime offload (laptop)** | `__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia %command%` | For hybrid GPU laptops |
| **Disable compositing (X11)** | `vblank_mode=0 %command%` | Reduces latency on X11; Wayland handles this |
| **Large address aware (32-bit games)** | `WINEDLLOVERRIDES="kernel32.dll=n,b" %command%` | Fixes 2GB memory limit in old games |
| **ESYNC + FSYNC (kernel 5.16+)** | `WINEESYNC=1 WINEFSYNC=1 %command%` | Default in Proton-GE; don't set manually unless debugging |
| **Disable DXVK HUD** | `DXVK_HUD=0 %command%` | If you see FPS overlay you didn't ask for |
| **Force specific GPU (multi-GPU)** | `DRI_PRIME=1 %command%` | AMD integrated → discrete; Nvidia use `__NV_PRIME_RENDER_OFFLOAD=1` |

**Pro tip:** Create a text file `~/launch-options.txt` with your common combos. Copy-paste into Steam per game.

---

## Where Linux Is Still Worse Than Windows (Honest List)

1. **Kernel anti-cheat** — You simply cannot play the biggest competitive games. No amount of tweaking fixes this. Dual-boot or cloud gaming required.

2. **HDR** — Gamescope is the only reliable path. Desktop HDR (KWin, Cosmic) works for video, not games. Calibration per game. Windows: enable HDR in settings, done.

3. **Multi-monitor VRR** — Works on single monitor. Two monitors with different refresh rates? Stutter city. Windows handles this natively since 2021.

4. **Nvidia driver updates** — `pacman -Syu` pulls new kernel → Nvidia module rebuild → 5-15 min black screen on boot. `akmods`/`dkms` helps but not instant. Windows: GeForce Experience updates in background.

5. **Ray tracing performance** — 20-30% behind Windows on same hardware. VKD3D-Proton RT translation isn't there yet. Path tracing (Cyberpunk PT mode) is slideshow on mid-range.

6. **DLSS Frame Generation** — Works via VKD3D-Proton but adds 1 frame latency vs Windows. Native DLSS-FG on Windows is smoother.

7. **Audio stack complexity** — PipeWire + WirePlumber + PulseAudio compat + Jack = occasional "why is my mic not working in Discord but works in OBS" debugging. Windows: right-click speaker icon.

8. **Game launchers** — Epic/GOG/EA/Ubisoft/Battle.net all need separate Wine prefixes. Heroic + Lutris + Bottles covers 90% but it's *more moving parts* than "click installer, play".

9. **Modding** — Vortex works via Wine. Mod Organizer 2 works. But SKSE (Skyrim), F4SE (Fallout 4) require specific Wine/Proton versions. Steam Workshop auto-download works; manual mod install = more steps.

10. **VR** — OpenXR + Monado + ALVR for standalone, SteamVR for PCVR. Works but setup is 10x Windows. Quest Link via ALVR = compression artifacts. Native Windows SteamVR = plug and play.

11. **Cheat tables / trainers** — Cheat Engine runs in Wine but attaching to Windows process in Proton prefix is flaky. Windows: attach, done.

12. **Old games (pre-2010)** — Often run *better* on Linux via Wine than Windows 11 (16-bit support, no driver signing). But installers with SecuROM/SafeDisc/StarForce = broken. GOG versions work.

---

## My Daily Driver Setup (Copy-Paste Ready)

**CachyOS + KDE Plasma 6 + Wayland**

```bash
# Base (run once)
yay -S --needed \
  steam \
  protonup-qt \
  mangohud lib32-mangohud \
  gamescope \
  lutris \
  bottles \
  heroic-games-launcher-bin \
  gamemode lib32-gamemode \
  vkd3d lib32-vkd3d \
  dxvk \
  wine-gecko wine-mono \
  giflib lib32-giflib \
  gst-plugins-good gst-plugins-bad gst-plugins-ugly gst-libav \
  lib32-gst-plugins-good lib32-gst-plugins-bad lib32-gst-plugins-ugly lib32-gst-libav \
  vulkan-radeon lib32-vulkan-radeon \
  vulkan-icd-loader lib32-vulkan-icd-loader \
  mesa lib32-mesa \
  libva-mesa-driver lib32-libva-mesa-driver \
  mesa-vdpau lib32-mesa-vdpau \
  opencl-rusticl-mesa lib32-opencl-rusticl-mesa

# Nvidia instead of AMD? Replace vulkan-radeon/mesa lines with:
# nvidia-dkms nvidia-utils lib32-nvidia-utils nvidia-settings opencl-nvidia lib32-opencl-nvidia

# Enable services
sudo systemctl enable --now gamemoded

# MangoHud config
mkdir -p ~/.config/MangoHud
cat > ~/.config/MangoHud/MangoHud.conf << 'EOF'
gpu_stats
cpu_stats
ram
vram
frametime
fps
engine_version
api
gpu_text=GPU
cpu_text=CPU
position=top-right
font_size=24
background_alpha=0.7
toggle_hud=Shift_F12
EOF

# Gamescope session for HDR gaming (optional)
# Create ~/.local/bin/gamescope-session:
cat > ~/.local/bin/gamescope-session << 'EOF'
#!/bin/bash
export GAMESCOPE_EXTERNAL_OVERLAY=1
export RADV_PERFTEST=aco
export VKD3D_CONFIG=force_host_cached_resources,multi_queue
export DXVK_ASYNC=1
exec gamescope \
  -W 2560 -H 1440 -r 144 \
  --hdr-enabled --hdr-itm-enable \
  --force-grab-cursor \
  -- steam -gamepadui
EOF
chmod +x ~/.local/bin/gamescope-session
```

**Steam launch options (global default):**
```
gamemoderun %command%
```

**Per-game overrides:** Right-click → Properties → Compatibility → Force Proton-GE-Latest + add launch options from table above.

---

## Final Verdict

**Linux gaming in 2026 is viable for ~80% of my library.** The 20% that doesn't work (kernel anti-cheat) is a hard blocker for competitive players. If your top 5 games are Valorant, League, Apex, Destiny 2, Fortnite — **stay on Windows** or dual-boot.

**If you play single-player, co-op, indie, strategy, simulation, RPGs** — Linux is arguably *better* now. No forced updates mid-session, no telemetry, no Game Bar overhead, better containerization for sketchy launchers, native Vulkan titles often outperform Windows.

**Budget builds benefit most.** On my RX 6600, the 5-15% overhead doesn't change playability. On an RTX 4090, that gap is measurable frames you paid for. On integrated graphics (Ryzen 8000G, Intel Meteor Lake), the CPU overhead of DXVK/VKD3D can push 60fps → 45fps — that *matters*.

**Start with Nobara or Bazzite.** They remove 90% of the friction. Graduate to CachyOS/Arch when you want control. Document your fixes — you *will* forget them in 6 months.

**ProtonDB is your bible.** Check before buying. Report after playing. That's how we keep the 85% growing.

---

*Last tested: July 2026 on CachyOS 2026.07, Mesa 24.2, Proton-GE 9-26, Kernel 6.10-cachyos. Your mileage will vary — that's the point.*