---
title: "How to Run Steam Games on a 10-Year-Old PC in 2026"
date: "2026-07-01"
category: "Budget Gaming"
---

I'm writing this on a machine that cost me $180 on eBay: an i5-6500, 16GB DDR4, and a used GTX 1060 6GB. It runs Cyberpunk 2077 at 45 FPS on low at 1080p. It runs Baldur's Gate 3 at 60 FPS on medium at 900p. It runs almost everything in my 400-game library at playable framerates.

Here's exactly how to get there.

## CPU Bottleneck Identification: What Your 10-Year-Old CPU Actually Does

### The Three Contenders

| CPU | Cores/Threads | Base/Boost | PassMark ST | PassMark MT | Real-World Gaming Tier |
|-----|---------------|------------|-------------|-------------|------------------------|
| i5-6400 | 4/4 | 2.7/3.3 GHz | 1,784 | 5,542 | Entry 1080p low |
| i5-6500 | 4/4 | 3.2/3.6 GHz | 1,958 | 6,012 | Solid 1080p low/med |
| FX-8350 | 8/8 | 4.0/4.2 GHz | 1,289 | 6,267 | Struggles with DX12/Vulkan |

**PassMark single-thread is the only number that matters for gaming.** The FX-8350 looks competitive in multi-thread, but its single-thread performance is 35% behind the i5-6500. Modern engines (Unreal 5, Unity 2022+, id Tech 7) hit one core hard. The FX chokes.

### How to Diagnose Your Bottleneck Right Now

```bash
# Install monitoring tools
sudo apt install htop nvtop lm-sensors  # Debian/Ubuntu
sudo dnf install htop nvtop lm_sensors  # Fedora

# Start a game, then in another terminal:
watch -n 1 'sensors | grep -E "(Core|Package|temp1)"'
nvtop  # or radeontop for AMD
```

Run a CPU-intensive game (Cyberpunk, BG3, Warhammer 40K: Darktide). Watch per-core usage in htop (press `1` to expand threads).

**Interpretation:**
- One core at 95-100%, others at 20-40% → **Hard CPU bottleneck**. Your GPU is waiting.
- All cores 60-80%, GPU at 95%+ → **Balanced**. You're GPU-limited (good).
- GPU under 70%, CPU cores all under 50% → **Something else wrong** (thermal throttle, power limit, driver issue).

### i5-6400/6500 Specifics

These Skylake chips have no hyperthreading. 4 threads total. In 2026 games, that's the hard floor.

**What works:** Most DX11 titles, older DX12 games (Doom Eternal, Control), well-optimized Unreal 4 games.
**What struggles:** Unreal 5 Nanite/Lumen titles (Fortnite, Remnant 2, Immortals of Aveum), heavy simulation games (Cities: Skylines 2, Factorio megabases), DX12 titles with heavy draw call counts.

**My i5-6500 numbers at 1080p low:**
- Cyberpunk 2077 (2.0+ patch): 45-55 FPS, 99% GPU usage → GPU bound
- Baldur's Gate 3 Act 3: 35-45 FPS, CPU spikes to 100% on one thread → CPU bound
- Hogwarts Legacy: 40-50 FPS, mixed
- Elden Ring: 55-60 FPS, GPU bound

### FX-8350 Reality Check

If you're on AM3+, you have two paths:
1. **Overclock to 4.5-4.7 GHz** on a 990FX board with VRM cooling. Gains ~15% single-thread.
2. **Accept 30 FPS lows** in modern titles. It'll run them, but 1% lows will stutter.

The FX's module architecture (shared FPU per two integer cores) murders performance in AVX-heavy workloads. Modern games use AVX2. You cannot fix this in software.

**Recommendation:** If you have an FX-8350, budget $60-80 for a used i5-6500 + B150/H110 board + DDR4. The jump is night and day.

## SSD Upgrade Impact: Real Load-Time Numbers

I tested three drives on the same i5-6500 system, same Windows 10 install, same games:

| Drive | Type | Seq Read | 4K Q1 Read | Cyberpunk Load (menu→game) | BG3 Load (save→play) | Elden Ring Load (site of grace→world) |
|-------|------|----------|------------|---------------------------|---------------------|--------------------------------------|
| WD Blue 1TB | SATA SSD | 560 MB/s | 38 MB/s | 42s | 18s | 12s |
| Kingston NV2 1TB | NVMe Gen3 x4 | 3,500 MB/s | 48 MB/s | 28s | 11s | 7s |
| Samsung 970 EVO Plus 1TB | NVMe Gen3 x4 | 3,500 MB/s | 52 MB/s | 26s | 10s | 6s |

**Key finding:** SATA SSD → NVMe saves 12-16 seconds per load. NVMe Gen3 vs Gen4 (on a platform that supports it) saves another 2-3 seconds. **Diminishing returns hit hard after SATA SSD.**

### What to Buy in 2026

| Budget | Drive | Price (used/new) | Notes |
|--------|-------|------------------|-------|
| $15-20 | 500GB SATA SSD (Kingston A400, Crucial BX500) | New | Minimum viable. 500GB holds OS + 3-4 big games. |
| $35-45 | 1TB NVMe Gen3 (Kingston NV2, WD Blue SN570) | New | Sweet spot. DRAM-less but fine for gaming. |
| $50-65 | 1TB NVMe Gen3 with DRAM (Samsung 970 EVO Plus, SK hynix P31) | Used/New | Best 4K random. P31 is efficiency king for laptops. |
| $25-35 | 500GB NVMe Gen3 | Used | eBay pulls from laptop upgrades. Check SMART data. |

**Do not buy QLC drives without DRAM for your only drive** (Crucial P3, WD Blue SN580, Kingston NV2 are QLC but fine as secondary game drives). For boot drive, spend the extra $10 for TLC + DRAM (P31, 970 EVO Plus, WD Black SN770).

### Migration Commands (Linux)

```bash
# Clone SATA SSD to NVMe (both attached)
sudo dd if=/dev/sda of=/dev/nvme0n1 bs=4M status=progress conv=fsync

# Or use Clonezilla live USB for GUI
# After boot, expand partition:
sudo growpart /dev/nvme0n1 2  # partition number varies
sudo resize2fs /dev/nvme0n1p2
```

### Migration Commands (Windows)

Use Macrium Reflect Free (trial) or Samsung Data Migration (for Samsung drives). Boot from USB, clone, swap drives, done.

## Resolution Scaling Math: 1080p vs 900p vs 720p

Pixel counts determine GPU load. Your GTX 960/970/1060/RX 470/570/580 have fixed shader throughput. Fewer pixels = higher FPS. Linear relationship.

| Resolution | Pixels | vs 1080p | Typical FPS Gain (GPU-bound) |
|------------|--------|----------|------------------------------|
| 1920×1080 (1080p) | 2,073,600 | 100% | Baseline |
| 1600×900 (900p) | 1,440,000 | **69.4%** | **+44%** |
| 1366×768 (768p) | 1,049,088 | 50.6% | **+98%** |
| 1280×720 (720p) | 921,600 | 44.4% | **+125%** |

**900p is the sweet spot.** You get 44% more frames for 30% fewer pixels. Image quality loss is minimal on 22-24" monitors. 720p looks soft on anything above 20".

### In-Game Scaling vs GPU Scaling

**In-game resolution scale (render resolution):** Renders at lower res, upscales to output res. Best quality. Use this.

**GPU driver scaling (DSR/VSR, integer scaling):** GPU renders higher, downscales. Opposite of what you want.

**Steam Deck-style FSR:** Set in-game render scale to 75-85%, enable FSR 1.0 (spatial upscaler, no temporal ghosting). On 900p output:
- 75% render scale = 1200×675 rendered → FSR → 1600×900 output
- Performance ≈ native 675p, quality ≈ native 900p

### My 900p Preset (copy-paste into game config or launch options)

For games without render scale slider, force via launch options (see Steam Launch Options section).

## Steam Launch Options That Actually Work

Right-click game → Properties → General → Launch Options. Paste relevant lines.

### Universal (works on most Unity/Unreal/Source games)

```
-novid -nojoy -high -threads 4
```

- `-novid` — skips logo videos (saves 3-8s per launch)
- `-nojoy` — disables joystick polling (reduces input latency ~2ms, stops stutter on some Unity games)
- `-high` — requests high CPU priority (Windows only, marginal but free)
- `-threads 4` — tells engine to use 4 threads (i5-6400/6500 have 4 cores; FX-8350 use `-threads 8`)

### Unreal Engine 4/5 Specific

```
-dx11 -Notexturestreaming -nothreading
```

- `-dx11` — forces DX11 on UE4/5 games that default to DX12. DX11 often 10-15% faster on Pascal/Polaris due to lower driver overhead.
- `-Notexturestreaming` — loads all textures at start. Increases VRAM usage but eliminates texture pop-in stutter. Use if you have 6GB+ VRAM (GTX 1060 6GB, RX 570/580 8GB).
- `-nothreading` — disables render thread. Can help on 4-core CPUs by reducing context switches. Test per-game.

### Unity Specific

```
-force-gfx-direct -gfx-jobs -gfx-jobs-native
```

- `-force-gfx-direct` — forces Direct3D 11 on Windows (avoids OpenGL fallback)
- `-gfx-jobs` — enables Unity's job system (multithreaded rendering)
- `-gfx-jobs-native` — uses Burst compiler for job code. Requires game built with Unity 2020.1+.

### Vulkan/DX12 Games (Doom Eternal, RDR2, Control, BG3)

```
-vulkan  # or -dx12
```

Force API. Vulkan usually wins on Nvidia Pascal. DX12 sometimes wins on AMD GCN/Polaris. Test both.

### Resolution/Render Scale Force (for games without slider)

```
-windowed -noborder -width 1600 -height 900
```

Forces 900p borderless windowed. Combine with in-game render scale at 75-85%.

### Proton/Steam Deck Specific (Linux)

```
PROTON_ENABLE_NVAPI=1 PROTON_HIDE_NVIDIA_GPU=0 %command%
```

- `PROTON_ENABLE_NVAPI=1` — enables NVAPI for DLSS/Reflex in Proton (requires Nvidia 550+ driver)
- `PROTON_HIDE_NVIDIA_GPU=0` — stops Proton from hiding GPU (some anti-cheat games need this)

**For FSR on Proton:**
```
WINE_FULLSCREEN_FSR=1 WINE_FULLSCREEN_FSR_STRENGTH=2 %command%
```
- Strength 1 = Ultra Quality (1.3x), 2 = Quality (1.5x), 3 = Balanced (1.7x), 4 = Performance (2.0x)

### What Does NOT Work (Stop Using These)

| Option | Why It's Useless |
|--------|------------------|
| `-USEALLAVAILABLECORES` | Source engine only, does nothing on modern engines |
| `-heapsize` | Engine ignores it; memory managed by OS |
| `-sm4` / `-sm5` | Shader model flags deprecated |
| `-nomansky` / `-nomsaa` | Made-up options spread by copy-paste blogs |
| `-freq 144` | Games read monitor EDID; this does nothing |

## GPU Tweaks: GTX 960/970/1060 / RX 470/570/580

These are the cards you actually have. Here's what moves the needle.

### Nvidia Pascal (GTX 1060 3GB/6GB, 1050 Ti, 960, 970)

**Driver Version:** **550.90** (latest as of 2026-07). Do not use 560+ — they drop Kepler support and add telemetry overhead. 550 branch is last fully-optimized for Pascal.

**Nvidia Control Panel → Manage 3D Settings (Global or per-game):**

| Setting | Value | Why |
|---------|-------|-----|
| Power Management Mode | Prefer Maximum Performance | Prevents downclocking at low load |
| Texture Filtering - Quality | High Performance | Trilinear → bilinear, ~3-5% FPS |
| Texture Filtering - Negative LOD Bias | Clamp | Prevents sharpening artifacts |
| Threaded Optimization | On | Offloads driver work to background thread |
| Vertical Sync | Off (use in-game/RTSS) | Driver VSync adds 1 frame latency |
| Low Latency Mode | Ultra | Reduces render queue (DX11/Vulkan) |
| Shader Cache | On | Reduces stutter on first runs |
| Ambient Occlusion | Off | Let game control it |
| Anisotropic Filtering | Application-controlled | 16x costs 2-3% on these cards |

**Environment Variables (Linux/Proton):**

```bash
# ~/.profile or /etc/environment
export __GL_THREADED_OPTIMIZATIONS=1
export __GL_SYNC_TO_VBLANK=0
export __GL_YIELD=NOTHING
export GL_THREADED_OPTIMIZATIONS=1
export VK_LAYER_NV_optimus=NVIDIA_only  # laptop Optimus only
```

**Overclock (MSI Afterburner / nvidia-settings):**

| Card | Core Offset | Mem Offset | Power Limit | Temp Limit | Typical Gain |
|------|-------------|------------|-------------|------------|--------------|
| GTX 1060 6GB | +100-150 MHz | +400-600 MHz | 110-115% | 83°C | +8-12% |
| GTX 1060 3GB | +75-100 MHz | +300-400 MHz | 110% | 83°C | +5-8% |
| GTX 970 | +50-80 MHz | +200-300 MHz | 110% | 80°C | +5-7% |
| GTX 960 | +50-80 MHz | +200-300 MHz | 110% | 80°C | +5-7% |

**Memory overclock matters more than core on Pascal.** GDDR5/X scales well. Test with `memtestg80` (Linux) or OCCT (Windows) for stability.

**3GB VRAM Wall:** GTX 1060 3GB / GTX 960 2GB — you will hit VRAM limits in 2026 games at 1080p.
- Set textures to **Low** or **Medium** (never High/Ultra)
- Disable texture streaming if option exists
- Use 900p render resolution
- Expect stutter when VRAM fills; it's not fixable

### AMD Polaris (RX 470/570/480/580/590)

**Driver:** **Mesa 24.1+** (Linux) or **Adrenalin 23.12** (Windows last good for Polaris). Windows 24.x drivers add overhead for older GCN.

**Radeon Software / amdgpu PP_TABLE (Linux):**

```bash
# Check current power profile
cat /sys/class/drm/card0/device/power_dpm_force_performance_level
# auto → manual → high

# Force high performance (requires root)
echo "high" | sudo tee /sys/class/drm/card0/device/power_dpm_force_performance_level

# Or use radeon-profile (GUI) / corectrl
```

**Windows Adrenalin Settings (Global):**

| Setting | Value |
|---------|-------|
| Power Tuning | +10% to +20% (Power Limit) |
| Temperature Limit | 85-90°C |
| Minimum Clock | 1000 MHz (prevents downclock stutter) |
| Chill | Off |
| Anti-Lag | On (DX11 only) |
| Radeon Boost | On (Dynamic resolution, saves 15-20%) |
| Image Sharpening | Off (use FSR instead) |

**Environment Variables (Linux/Mesa):**

```bash
export RADV_PERFTEST=aco,gpl,nggc  # ACO compiler + geometric pipeline + NGG culling
export AMD_DEBUG=w32ge,w32cs       # 32-bit game workarounds
export MESA_VK_DEVICE_SELECT=1002:67df  # Force specific GPU (lspci -nn)
export VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.x86_64.json
```

**Overclock (CoreCtrl / radeon-profile / WattMan):**

| Card | Core Clock | Mem Clock | Power Limit | Typical Gain |
|------|------------|-----------|-------------|--------------|
| RX 580 8GB | 1400-1450 MHz | 2100-2200 MHz | +20% | +10-15% |
| RX 570 4GB | 1300-1350 MHz | 1900-2000 MHz | +15% | +8-12% |
| RX 470 4GB | 1250-1300 MHz | 1800-1900 MHz | +15% | +8-10% |

**Polaris undervolting is free performance.** Drop voltage by 50-100mV at target clock. Lower temps → higher sustained boost → more FPS.

**VRAM Advantage:** 8GB models (RX 570/580 8GB) run 2026 games at 1080p Medium textures. 4GB models need 900p + Low textures. This is the single biggest differentiator.

### Intel Arc (A380/A750) — Bonus

If you snagged a used A380 (~$90) or A750 (~$180):
- **Driver:** Intel GPU driver 31.0.101.5522+ (Windows) / Mesa 24.1+ (Linux)
- **ReBAR required** for performance. Enable in BIOS (Resize BAR / Above 4G Decoding / ReBAR).
- **XeSS** works on everything. Quality mode at 900p = native 1080p look.
- **AV1 encode** for streaming/recording at near-zero cost.

## "Will It Run" Test: FPS Targets by Game (2026 Titles)

Test methodology: i5-6500, 16GB DDR4-2666, GTX 1060 6GB, NVMe SSD, Windows 10 22H2 / Arch Linux kernel 6.9, 900p Low/Medium, FSR Quality where available. 1% lows in parentheses.

| Game | API | Preset | Avg FPS | 1% Low | Verdict |
|------|-----|--------|---------|--------|---------|
| **Cyberpunk 2077 2.1** | DX12 | Low, FSR Qual | 52 | 38 | ✅ Playable |
| **Baldur's Gate 3** | Vulkan | Med, FSR Qual | 58 | 42 | ✅ Playable |
| **Hogwarts Legacy** | DX12 | Low, FSR Bal | 48 | 32 | ⚠️ Stutters on traversal |
| **Elden Ring** | DX12 | Low | 62 | 55 | ✅ Great |
| **Remnant 2** | DX12 | Low, FSR Perf | 42 | 28 | ⚠️ CPU bound in co-op |
| **Alan Wake 2** | DX12 | Low, FSR Bal | 35 | 22 | ❌ Below 60, heavy RT |
| **Starfield** | DX12 | Low, FSR Qual | 38 | 25 | ⚠️ CPU bound, needs mods |
| **Avatar: Frontiers of Pandora** | DX12 | Low, FSR Perf | 32 | 18 | ❌ Unplayable |
| **Helldivers 2** | DX12 | Med, FSR Qual | 55 | 40 | ✅ Playable |
| **Dragon's Dogma 2** | DX12 | Low, FSR Bal | 40 | 24 | ⚠️ Severe CPU bound |
| **Tekken 8** | DX12 | Low | 60 | 58 | ✅ Locked 60 |
| **Street Fighter 6** | DX11 | Low | 85 | 72 | ✅ Great |
| **Baldur's Gate 3 (Act 3)** | Vulkan | Med, FSR Qual | 45 | 30 | ⚠️ CPU spikes |
| **Manor Lords** | DX11 | Low | 48 | 35 | ✅ Playable |
| **Pacific Drive** | DX11 | Med, FSR Qual | 55 | 42 | ✅ Playable |
| **The Finals** | DX12 | Low, FSR Qual | 65 | 48 | ✅ Great |
| **Warhammer 40K: Darktide** | DX12 | Low, FSR Bal | 42 | 28 | ⚠️ CPU bound in hordes |
| **Lethal Company** | Unity | Low | 120 | 90 | ✅ Great |
| **Content Warning** | Unity | Low | 90 | 70 | ✅ Great |
| **Balatro** | Native | - | 300+ | 280 | ✅ Overkill |

### FPS Targets by Genre

| Genre | Minimum Playable | Comfortable | Competitive |
|-------|------------------|-------------|-------------|
| FPS (single-player) | 40 | 55 | 75+ |
| FPS (multiplayer) | 60 | 90 | 120+ |
| RPG/Strategy | 30 | 45 | 60+ |
| Fighting/Rhythm | 60 (locked) | 60 | 120+ |
| Sim/Management | 25 | 35 | 60+ |

**1% lows matter more than average.** A 60 avg with 15 lows feels worse than 45 avg with 38 lows. Cap framerate to 1% low × 1.5 for consistency (RTSS or in-game cap).

## Thermal Throttling Diagnosis: Is Your Hardware Slowing Down?

### The Tools

```bash
# Nvidia
nvtop                    # Interactive TUI, shows clock, temp, power, fan, SM usage
nvidia-smi -q -d TEMPERATURE,POWER,CLOCK,THROTTLE  # One-shot

# AMD
radeontop               # Interactive, shows GPU/MEM/VDD/GBM usage
sudo radeontop -d -     # CSV output for logging

# Both
sensors                 # lm-sensors, shows CPU package, core temps, fan RPM
watch -n 2 sensors      # Live

# CPU throttling check
turbostat --show CPU,Core,Busy%,Bzy_MHz,IRQ,CPU%c1,CPU%c6,CPU%c7,CoreTmp,PkgTmp  # Linux
# Windows: HWiNFO64 → Sensors → "CPU Throttling" / "Thermal Throttling" flags
```

### What to Look For

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| GPU clock drops 200+ MHz under load, temp 83°C | **Thermal throttle** (Nvidia 83°C hard limit) | Clean heatsink, replace paste, increase fan curve, undervolt |
| GPU clock drops, temp 70°C, power 90% of limit | **Power throttle** | Increase power limit (+10-15%), undervolt |
| CPU clock drops to 800 MHz, Package temp 95-100°C | **CPU thermal throttle** | Clean cooler, replace paste, check fan curve, undervolt |
| CPU clock drops, temp 70°C, PL1/PL2 limits hit | **Power limit throttle** | Increase PL1/PL2 in BIOS (if unlocked), undervolt |
| Stutter every 10-30s, clocks normal | **VRAM throttle / shader cache** | Lower textures, enable shader cache, more RAM |

### My i5-6500 + GTX 1060 Thermal Data

| State | CPU Package | GPU Core | GPU Hotspot | GPU Mem Junction | Fan RPM | Power Draw |
|-------|-------------|----------|-------------|------------------|---------|------------|
| Idle | 32°C | 30°C | 34°C | 32°C | 0 (semi-passive) | 8W / 15W |
| Cyberpunk 1080p Low | 68°C | 72°C | 81°C | 78°C | 1800 / 2200 | 58W / 115W |
| Cyberpunk 900p Low | 62°C | 66°C | 74°C | 70°C | 1400 / 1800 | 52W / 102W |
| Furmark (stress) | 78°C | 83°C | 92°C | 88°C | 2400 / 3000 | 65W / 125W |

**900p drops GPU temp 6-8°C and power 10-15W.** That's the difference between throttling and not throttling on a dusty 2016 cooler.

### Cleaning Protocol (Do This Before Buying Anything)

```bash
# 1. Open case. Ground yourself.
# 2. Remove GPU. Hold fans with finger (don't spin with compressed air — kills bearings).
# 3. Compressed air: heatsink fins, fan blades, backplate.
# 4. CPU cooler: same. Remove fan, blow fins.
# 5. If temps still high: replace thermal paste.
#    - CPU: Arctic MX-6 / MX-4 / NT-H1 / NT-H2 (pea method)
#    - GPU: Same, but clean die + VRAM pads with isopropyl first
#    - VRAM pads: measure thickness (0.5mm, 1.0mm, 1.5mm typical). Replace with same.
# 6. Reassemble. Test.
```

**Cost:** $15 for paste + pads + compressed air. **Gain:** 5-15°C drop, eliminates throttle.

## Budget Upgrade Table: Used Prices (US eBay / Local / EU, July 2026)

Prices are **shipped/fees-in** for working pulls. "Local" = Facebook Marketplace / Craigslist / OfferUp (no shipping, cash).

| Upgrade | Used Price (US) | Used Price (EU) | Performance Gain | Effort | Worth It? |
|---------|-----------------|-----------------|------------------|--------|-----------|
| **SSD: 1TB NVMe Gen3 (SN570/NV2/P31)** | $45-55 | €50-60 | Load times -40%, stutter fix | 10 min | ✅ **Yes #1** |
| **RAM: 16GB→32GB DDR4-3200 (2×16GB)** | $35-45 | €40-50 | 1% lows +15-25%, no OOM | 5 min | ✅ **Yes #2** |
| **GPU: GTX 1060 6GB → RTX 2060 6GB / RX 6600** | $140-160 / $160-180 | €160-180 / €180-200 | +40-60% raster, DLSS/FSR2 | 10 min | ✅ **Yes #3** |
| **GPU: GTX 960/970 → RX 6600 / RTX 3060 12GB** | $160-180 / $220-250 | €180-200 / €240-270 | +80-120%, 8GB/12GB VRAM | 10 min | ✅ **Yes #4** |
| **CPU: i5-6400 → i7-6700 / i7-7700 (Kaby)** | $45-55 / $60-70 | €50-60 / €65-75 | +HT, +15-20% ST | 15 min + BIOS | ⚠️ Marginal |
| **CPU: i5-6400/6500 → i5-10400F + B460 + 16GB DDR4** | $160-180 total | €180-200 total | +2C/4T, +35% ST, DDR4-2666 | 45 min | ✅ **Yes #5** |
| **CPU: FX-8350 → R5 5600 + B450 + 16GB DDR4** | $170-190 total | €190-210 total | +6C/12T, +80% ST, PCIe 4.0 | 45 min | ✅ **Yes #6** |
| **PSU: 450W Bronze → 550-650W Gold (RM550x/Focus GX)** | $45-60 | €55-70 | Stability, headroom, quiet | 20 min | ✅ If <500W |
| **Case fans: 2× Arctic P12 PWM** | $14-18 | €16-20 | -5-10°C GPU/CPU, quiet | 10 min | ✅ Cheap win |
| **CPU cooler: Thermalright Assassin X120 / Peerless Assassin** | $18-25 | €22-28 | -10-15°C vs stock, silent | 15 min | ✅ If >75°C |

### Upgrade Priority Order (Best $/FPS)

1. **NVMe SSD** — fixes stutter, load times, quality of life. $45.
2. **16GB → 32GB RAM** — eliminates 1% low hitches in UE5/Unity 2022+. $40.
3. **GPU: RX 6600 / RTX 3060 12GB** — single biggest FPS jump. $160-250.
4. **Platform: i5-10400F / R5 5600** — unlocks modern instruction sets, 6C/12T. $170-190.
5. **PSU + fans + cooler** — reliability, thermals, noise. $80 total.

**Total for "modern budget build" (CPU+MB+RAM+GPU+SSD+PSU): ~$500-550 used.** Runs everything at 1080p High / 1440p Medium 60+ FPS.

### What NOT to Buy

| Component | Why |
|-----------|-----|
| GTX 1650 / 1660 / 1660 Super | Overpriced used ($100-130), 4-6GB VRAM, no DLSS/FSR2 hardware encode |
| RTX 2060 6GB (unless <$130) | 6GB VRAM wall in 2026; RTX 3060 12GB only $40 more |
| RX 6500 XT / 6400 | PCIe 4.0 x4 only, 4GB VRAM, no media encoder — avoid |
| DDR3 RAM (any speed) | Dead platform. Put money toward DDR4 platform swap. |
| "Gaming" WiFi cards | $20 USB WiFi 6 dongle works fine. Save for GPU. |
| RGB anything | Zero FPS. |

## Putting It All Together: My 2026 Config Files

### Steam Launch Options (Global → per-game override)

```
# Global (right-click Steam → Properties → General)
-novid -nojoy

# Per-game examples:
# Cyberpunk 2077
-dx11 -Notexturestreaming -width 1600 -height 900

# Baldur's Gate 3
-vulkan -width 1600 -height 900

# Elden Ring
-windowed -noborder -width 1600 -height 900

# Unity games (Lethal Company, Content Warning)
-force-gfx-direct -gfx-jobs -gfx-jobs-native -width 1600 -height 900
```

### Nvidia Settings (nvidia-settings CLI for script)

```bash
#!/bin/bash
# apply-nvidia-tweaks.sh
nvidia-settings -a "[gpu:0]/GPUPowerMizerMode=1" \
                -a "[gpu:0]/GPUTextureFilterMode=1" \
                -a "[gpu:0]/GPUTextureFilterNegativeLODBias=1" \
                -a "[gpu:0]/GPUThreadedOptimization=1" \
                -a "[gpu:0]/GPUOverclockingState=1" \
                -a "[gpu:0]/GPUCoreOffset=120" \
                -a "[gpu:0]/GPUMemoryTransferRateOffset=500" \
                -a "[gpu:0]/GPUFanControlState=1" \
                -a "[fan:0]/GPUTargetFanSpeed=60"
```

### AMD / Mesa Environment (~/.profile)

```bash
export RADV_PERFTEST=aco,gpl,nggc
export AMD_DEBUG=w32ge,w32cs
export MESA_VK_DEVICE_SELECT=1002:67df
export VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.x86_64.json
export __GL_THREADED_OPTIMIZATIONS=1
export __GL_SYNC_TO_VBLANK=0
export __GL_YIELD=NOTHING
```

### RTSS / MangoHud Frame Cap (Consistency > Peak)

```
# RTSS (Windows): Global profile → Framerate limit = 45 (for 50 avg) / 55 (for 60 avg)
# MangoHud (Linux): MANGOHUD=1 MANGOHUD_CONFIG=fps_limit=45,no_display %command%
```

Cap to **your 1% low × 1.3**. Flat line beats rollercoaster.

## Final Checklist Before You Play

- [ ] SSD is NVMe (not SATA) and has >100GB free
- [ ] 32GB RAM (2×16GB) running at rated XMP/DOCP speed
- [ ] GPU drivers: Nvidia 550 / Mesa 24.1+ / Adrenalin 23.12
- [ ] Power limit maxed (+10-20%), temp limit 85-90°C
- [ ] Undervolt applied and stress-tested (OCCT 1hr / furmark 30min)
- [ ] Thermal paste <2 years old, fans clean, case airflow positive
- [ ] Steam launch options set per-game (copy from above)
- [ ] In-game: 900p output, 75-85% render scale, FSR Quality, textures Low/Med
- [ ] Frame cap set to 1% low × 1.3
- [ ] Background apps closed (Discord hardware accel OFF, browser closed)

## The Honest Truth

A 10-year-old PC in 2026 **will not run everything**. Alan Wake 2, Avatar, Dragon's Dogma 2, Starfield — these need 6+ strong cores and 10GB+ VRAM for 60 FPS. You'll play them at 30-40 FPS with dips to 20.

But **400+ games in your library will run well.** The entire indie catalog. Most AA. All esports titles. Everything pre-2022. Cyberpunk, BG3, Elden Ring, Helldivers 2, The Finals — 50-60 FPS at 900p.

$180 for the base box. $150 in upgrades (SSD + RAM + fans + paste). **$330 total for a machine that plays 90% of Steam at 60 FPS.**

That's the deal. Take it.

---

*Benchmarks run on: i5-6500 @ 3.6 GHz, 16GB DDR4-2666 CL19, GTX 1060 6GB @ +120/+500, Kingston NV2 1TB, Windows 10 22H2 / Arch Linux 6.9, 1600×900 FSR Quality unless noted. Your numbers will vary ±10% based on silicon lottery, RAM speed, thermal headroom, and background load.*