---
title: "Best Games for Intel UHD Graphics in 2026: What Actually Runs at 30+ FPS"
date: "2026-07-03"
category: "Budget Gaming"
---

You've got a laptop with Intel UHD Graphics. Maybe it's an i5-8250U with UHD 620. Maybe a 12th-gen desktop with UHD 770. Either way, someone told you "integrated graphics can't game" and now you're wondering if your $400 machine is just a glorified typewriter.

It's not. You can game on Intel integrated graphics — you just need to pick the right games and apply the right settings. I've tested dozens of titles across three generations of Intel iGPUs. Here's what actually works, what doesn't, and how to squeeze playable framerates out of a GPU that shares memory with your system RAM.

## The Intel iGPU Tier List: Know What You Have

Before you pick games, know your chip. The performance gap between Intel iGPU generations is bigger than you'd think.

| Chip | Found In | EU Count | Rough Discrete Equivalent | Practical Ceiling |
|------|----------|----------|---------------------------|-------------------|
| UHD 620 | 8th gen laptops (i5-8250U, i7-8550U) | 24 | ~GT 920M-930M | 720p low for most 3D games |
| UHD 630 | 8th-10th gen desktops (i3-8100 through i9-10900K) | 24 | ~GT 730-1030 | 720p-1080p low for older titles |
| Iris Xe (80 EU) | 11th-12th gen laptops (i5-1135G7, i5-1235U) | 80 | ~GT 1030 / MX 350 | 1080p low for indies, 720p low for AA |
| Iris Xe (96 EU) | 11th-12th gen higher-end laptops (i7-1165G7) | 96 | ~MX 450 (lightly) | 1080p low-medium for most indies |
| UHD 770 | 12th gen desktops (i5-12600K through i9-12900K) | 32 | ~GT 1030-1030 slightly above | 1080p low for modern, medium for older |

**RAM speed matters more than you think.** Intel iGPUs have no dedicated VRAM — they steal system RAM. If you have single-channel DDR4-2400, you're leaving 15-25% performance on the table versus dual-channel DDR4-3200. Always run RAM in dual-channel mode. This is the single biggest free performance upgrade for integrated graphics.

## Games That Genuinely Run at 30+ FPS on UHD 620/630

The entry-level chips. These are the 24-EU units with roughly GT 920M-level performance. You're not playing Cyberpunk here. You're playing games built for hardware from an era when integrated graphics were assumed.

### Tier 1: Runs Smoothly at 720p Low

| Game | Resolution | Settings | Expected FPS | Notes |
|------|------------|----------|--------------|-------|
| Terraria | 1080p | Maxed | 60 | 2D sprite game, runs on anything with a screen |
| Stardew Valley | 1080p | Maxed | 60 | Same — Unity 2D, negligible GPU load |
| Into the Breach | 1080p | Maxed | 60 | Turn-based tactics, practically zero GPU requirement |
| Vampire Survivors | 1080p | Maxed (cap at 60) | 60 | Can overwhelm late-game with particles — cap FPS |
| Slay the Spire | 1080p | Maxed | 60 | Card game, zero GPU stress |
| Portal 2 | 1080p | Medium | 45-60 | Source engine loves low-end hardware |
| Half-Life 2 | 1080p | High | 60 | Same Source engine, even smoother |
| Counter-Strike 2 (CSGO) | 720p | Low, FPS config | 40-60 | Needs `autoexec.cfg` tweaks — see below |
| Left 4 Dead 2 | 1080p | Medium | 45-60 | Source engine, handles hordes fine |
| Team Fortress 2 | 1080p | Medium-high | 50-60 | Valve still optimizes for potato PCs |
| Hotline Miami 2 | 1080p | Maxed | 60 | Top-down 2D, gorgeous, zero GPU stress |
| Celeste | 1080p | Maxed | 60 | Pixel art platformer, perfect for iGPUs |
| Hollow Knight | 1080p | Maxed | 60 | Hand-drawn 2D, low system requirements |
| Hades | 1080p | Low-medium | 50-60 | UE4 but optimized for low specs — suprisingly smooth |
| Undertale | 1080p | Maxed | 60 | 2D RPG, could run on a calculator |

### Tier 2: Playable but Needs Tweaks (30 FPS Target)

| Game | Resolution | Settings | Expected FPS | Required Tweaks |
|------|------------|----------|--------------|-----------------|
| GTA V | 720p | Normal, population density low, extended distance scaling off | 35-45 | Disable advanced graphics, FXAA on, MSAA off |
| Skyrim Special Edition | 720p | Low | 30-40 | BethINI low preset, disable god rays |
| Fallout 4 | 720p | Low | 25-35 | Borderline — use Creation Engine INI tweaks, god rays off |
| CS2 (Counter-Strike 2) | 1280x960 stretched | Low + FPS config | 40-60 | Launch: `-novid -threads 4 -high -freq 144` |
| The Witcher 3 | 720p | Low, hairworks off, foliage visibility low | 25-35 | Borderline. Apply FSR 2 mod if comfortable modding |
| Sekiro | 720p | Low | 20-30 | Barely playable. Skip unless you're patient. |

## Games That Run Well on Iris Xe / UHD 770

These chips are a step up. The 80-96 EU Iris Xe in 11th/12th gen laptops and the 32-EU UHD 770 in 12th gen desktops have roughly GT 1030 / MX 350 performance. That opens up a broader game library at 720p-1080p.

| Game | Resolution | Settings | Expected FPS | Notes |
|------|------------|----------|--------------|-------|
| Valorant | 1080p | Low | 80-120 | Designed for low specs, runs beautifully on Iris Xe |
| League of Legends | 1080p | Medium | 60-90 | Very well optimized, runs on anything |
| Dota 2 | 1080p | Low-medium | 50-70 | Source 2, well optimized |
| GTA V | 1080p | Normal | 40-55 | Big step up from UHD 620 |
| The Witcher 3 | 1080p | Low, hairworks off | 30-40 | Actually decent on Iris Xe with FSR mod |
| Elden Ring | 720p | Low | 25-35 | Struggles but playable with patience. Shader stutters on first load |
| Dark Souls 3 | 1080p | Low | 30-45 | Surprisingly smooth after shader cache fills |
| Resident Evil 2 Remake | 720p | Low, FSR 2 Quality | 30-40 | RE Engine scales down beautifully with FSR |
| Devil May Cry 5 | 720p | Low | 35-45 | RE Engine again — great optimization |
| Forza Horizon 4 | 720p | Low, dynamic optimization on | 35-45 | Turn 10's engine handles iGPUs better than most |
| DOOM (2016) | 1080p | Low | 40-55 | id Tech 6 is a miracle — Vulkan path runs smooth |
| DOOM Eternal | 720p | Low | 35-50 | Same id Tech magic, honestly the best big game for iGPUs |
| No Man's Sky | 720p | Low, FSR 2 Quality | 30-40 | Had a massive optimization pass — surprisingly doable now |
| Halo: MCC | 1080p | Low | 45-60 | Individual games scale well; CE and Reach run best |
| Mass Effect Legendary Edition | 1080p | Low-medium | 40-55 | BioWare's remaster is lighter than you'd expect |

## The Settings That Change Everything

Before you launch anything, set these up. They're more impactful than any in-game setting.

### Intel Graphics Command Center (Windows)

Download from the Microsoft Store. Then:

```
Display → Color → Disable "Energy Efficient" mode (sets to "Maximum performance")
System → Power → Plan: "Maximum Performance" (prevents thermal throttling on laptops)
Gaming → Game Mode → Enable for each game in your library
```

The two settings that bite hardest: **Energy Efficient mode** and **Power Plan**. On laptops, Intel aggressively downclocks the iGPU to save battery and because it shares the die with the CPU. You'll lose 20-30% FPS in both modes left at defaults.

### RAM Allocation (BIOS)

Some laptops let you set how much system RAM is dedicated to the iGPU. Look for "DVMT Pre-Allocated Memory" or "UMA Frame Buffer Size" in BIOS:

```
BIOS → Advanced → Chipset Configuration → DVMT Pre-Allocated Memory
Set to 512MB minimum (default is often 64MB-128MB on cheap laptops)
```

This doesn't give the GPU faster VRAM (it's still system RAM), but it ensures the driver doesn't have to negotiate memory during gameplay, which causes microstutter.

### Dual-Channel RAM: The Free Upgrade

If your laptop shipped with a single 8GB stick, adding a second 8GB stick in matching speed is the single best performance upgrade you can make. Dual-channel memory roughly doubles memory bandwidth, and on iGPUs, memory bandwidth = GPU performance.

Expect a 15-30% FPS uplift across the board. A $20 RAM stick turns a 25 FPS experience into a 32-35 FPS one. Nothing else comes close for the price.

## Linux-Side Tweaks: Mesa and DXVK

If you're on Linux (or running Windows games through Proton/Bottles), you have options Windows users don't:

```bash
# Ubuntu/Debian — install latest Mesa from kisak-mesa PPA
sudo add-apt-repository ppa:kisak/turtle
sudo apt update && sudo apt upgrade -y

# Fedora — Mesa is already current
sudo dnf install mesa-vulkan-drivers mesa-dri-drivers

# Set environment variables for Intel on Linux
export MESA_GL_DEFAULT_OVERRIDE=mesa_glthread
export INTEL_DEBUG=bat  # Debug only — leave off for gaming
export RADV_PERFTEST=aco  # Not for Intel but good to know
```

The big one: **mesa_glthread**. It enables a separate thread for GL calls, reducing CPU overhead. On Intel iGPUs where the CPU and GPU share a die, this matters more than anywhere.

If you're running games through Proton (Steam Play) or Bottles (standalone Wine prefix), DXVK replaces DirectX 9/10/11 calls with Vulkan. For Intel iGPUs, DXVK is often faster than native Windows drivers because the Vulkan path is better optimized:

```bash
# In Steam: set launch options per game
PROTON_USE_WINED3D=0 %command%  # Use DXVK (default, but be explicit)
DXVK_HUD=fps %command%          # Show FPS overlay to verify performance
```

## FSR: The Cheat Code for Modern Games

AMD FidelityFX Super Resolution (FSR) works on any GPU, including Intel integrated. If a game supports FSR, enable it at Quality or Balanced. This is the single biggest win for modern games on iGPUs.

- **AMD FSR 1.0**: Native to most games. Upscales the render resolution. Costs ~5% of games' visual fidelity for a 20-40% FPS boost. Set to "Quality" (77% render scale) or "Balanced" (59%).
- **AMD FSR 2.0/2.1**: Better image quality, small performance cost over FSR 1. Worth it for solo games where frame-time consistency matters.
- **FSR Mods (Lossless Scaling, Lossless.scaling)**: For games that don't natively support FSR, you can inject it. **Lossless Scaling** on Steam ($4) adds FSR 2/XeSS/LS1 upscaling to any game. For Intel Iris Xe, try **XeSS** first — Intel's own upscaler is tuned for their hardware.

## Games to Avoid (or Approach With Patience)

Some games look like they should work but won't:

- **Cyberpunk 2077**: Even at 720p low, UHD 620 cangs. Shader compilation stutters make it unplayable. Iris Xe hits 20-28 FPS with crippling stutters. Skip.
- **Baldur's Gate 3**: Act 1 runs at 30 FPS on Iris Xe, Act 3 doesn't. City scenes drop to 12-15 FPS. Wait for Larian's future optimizations or play on a real GPU.
- **Alan Wake 2**: Path-tracing required ssd level hardware. Don't attempt.
- **Starfield**: The Creation Engine 2 is significantly heavier than Fallout 4. 15-25 FPS on Iris Xe, unplayable on UHD 620/630.
- **Dragon's Dogma 2**: CPU-bound even on high-end hardware. iGPUs don't stand a chance.
- **Tekken 8**: UE5, shader stutters on first load. Borderline on Iris Xe, unplayable on UHD 620.

The common thread: modern Unreal Engine 5 games and CPU-bound titles are the wrong target. Stick to Source, RE Engine, id Tech, or 2D Unity games.

## The Bottom Line

Intel integrated graphics aren't good. They're also not useless. The trick is matching expectations to hardware:

- **UHD 620/630**: 2D indies, 2005-2015 3D classics at 720p low, Source engine games. That's a library of hundreds of great games.
- **Iris Xe / UHD 770**: Everything above, plus 2015-2022 AA games at 720p low with FSR. Valorant, LoL, Dota, Halo MCC, DOOM, Resident Evil remakes, Mass Effect Legendary. You're playing real games — just not the latest AAA.

The free wins are always the same: dual-channel RAM, DVMT at 512MB+, power plan at maximum, DXVK on Linux, and FSR wherever a game supports it. Do those four things and you'll be surprised what a $400 laptop can actually run.
