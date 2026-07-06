---
title: "Proton GE vs Proton Experimental vs Proton: Which One Should You Actually Use?"
date: "2026-07-06"
category: "Linux Gaming"
---

You installed Steam on Linux. You enabled Steam Play. Now you're staring at a dropdown listing six different "Proton" options and wondering which one is supposed to make your game work. Proton. Proton Experimental. GE-Proton11-1. Proton 9.0. Proton Hotfix. What's the difference, and does picking the wrong one matter?

Yes, it matters. Picking the right one can be the difference between a game that crashes on launch and one that runs at 60 FPS. But the good news is the decision tree is simpler than the dropdown makes it look. Here's what each one is, what they're built for, and the actual rules for choosing.

## The Three You Actually Need to Know

There are more than three Proton variants kicking around, but 90% of the time you're choosing between these:

**Proton (the numbered version).** This is Valve's stable, officially-supported compatibility tool. As of mid-2026 it sits at Proton 9.0-x. It's the one Steam installs by default when you flip on Steam Play for a title. It's the most tested, the least likely to break, and the one you should reach for first. Valve promotes fixes out of Experimental and into numbered Proton releases once they're stable. When in doubt, use this.

**Proton Experimental.** Valve's bleeding-edge branch. This is where new fixes live before they graduate to a numbered Proton release. It updates frequently — sometimes multiple times a week — and includes work that isn't fully vetted yet. In January 2026, the bleeding-edge build string hit `experimental-bleeding-edge-10.-294104-20260113`, pushing the version to 10.0. There's also a "Bleeding Edge" beta branch you can opt into via Steam's properties for Proton Experimental if you want the absolute cutting edge. The wiki is blunt about it: it can eat your game prefix and saves. Use it when a game has a known fix that's landed in Experimental but not yet in numbered Proton.

**GE-Proton (Proton GE).** A community-maintained fork, built by GloriousEggroll, a Red Hat engineer. The current version is **GE-Proton11-1**, released June 24, 2026. It's rebased on top of Proton 11 bleeding-edge, and it folds in patches and fixes that Valve hasn't merged yet — or won't, because of upstream policy. GE is also where media foundation and video playback fixes tend to land first.

## What Makes GE-Proton Different

GE-Proton isn't a different engine. It's Valve's Proton with extra stuff bolted on. Specifically, it tracks the latest bleeding-edge Wine, DXVK, VKD3D-Proton, and DXVK-NVAPI git versions, plus a set of community patches:

- **Media Foundation / video playback fixes.** The headline feature. Games with FMV cutscenes, embedded video, or DirectShow-based playback often need GE. Valve re-encodes some videos to work around the problem; GE implements upstream fixes.
- **Game-specific protonfixes.** Controller fixes for DualShock 4 in BioShock 2 Remastered and Dragon's Dogma: Dark Arisen, a libglesv2 patch for Duet Night Abyss under Wayland, a save-game fix for Dark Earth.
- **New in GE-Proton11-1:** d7vk (DirectX 7 to Vulkan), a Discord bridge, optiscaler support, winealsa channel/speaker overrides, Star Citizen patches, VRChat webcam face tracking, and a native rsx3d library so older games like Tex Murphy no longer need third-party winetricks.
- **The big rework:** GE-Proton11-1 gutted all gstreamer libraries and converted the quartz video path to use `quartz->winedmo->ffmpeg` instead. This is a 4-month effort that fixed video playback for roughly 80% of the games on the video-rework list — mostly Visual Novels and older titles that use DirectShow, ASF, or MPEG playback paths.

That gstreamer-to-ffmpeg conversion is the reason GE-Proton11 is a generational jump, not just a version bump. If you had broken cutscenes on GE-Proton10, GE-Proton11-1 is worth installing now.

## The Decision Tree

Stop guessing. Here's the order to try:

1. **Start with Proton 9.0 (or whatever the latest numbered Proton is).** It's the stable default. If it works, you're done. Don't "optimize" by trying other versions — stable and working beats experimental and slightly faster.
2. **If Proton 9.0 doesn't work, check ProtonDB.** Search the game at protondb.com. The top-reported fix almost always tells you which Proton version other people used and what launch options or protontricks they needed.
3. **Try Proton Experimental.** If there's a recent fix that hasn't shipped in numbered Proton yet, Experimental has it. This is the safest "I need something newer" move.
4. **Switch to GE-Proton11-1 if the game has:** broken FMV/cutscenes, media foundation errors, audio desync in pre-rendered video, a known GE-only protonfix, or a report on ProtonDB specifically recommending GE.
5. **Don't use GE-Proton as your daily driver.** It's a compatibility tool for specific games, not a blanket upgrade. Install it, apply it per-game, leave Proton 9.0 as your global default. GE versions don't get the same QA as Valve's, and a new GE release can regress something that worked on the previous one.

The counterintuitive part: GE-Proton is *not* "Proton but faster." On most games, numbered Proton and GE-Proton perform within a frame or two of each other because they're built on the same Wine/DXVK foundation. GE's value is compatibility, not speed.

## How to Install GE-Proton11-1

Two paths. The easy one first.

### Method 1: ProtonUp-Qt

If you want a GUI and you want updates handled for you:

```
flatpak install flathub net.davidotek.pupgui2
```

Launch ProtonUp-Qt, pick Steam, choose "GE-Proton" from the version dropdown, and click install. Restart Steam. GE-Proton11-1 will now show up in the per-game compatibility tool list.

ProtonUp-Qt also handles Lutris Wine-GE and Luxtorpeda versions, so it's worth keeping around.

### Method 2: Manual install

If you're not using Flatpak, or you want a specific build:

```
mkdir -p ~/.steam/root/compatibilitytools.d
cd /tmp
wget https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton11-1/GE-Proton11-1.tar.gz
tar -xf GE-Proton11-1.tar.gz -C ~/.steam/root/compatibilitytools.d/
```

Restart Steam. The version appears under the game's Properties → Compatibility → "Force the use of a specific Steam Play compatibility tool."

If `compatibilitytools.d` doesn't exist, create it — that's where Steam looks for third-party Proton builds.

On Steam Deck, the path is `~/.steam/root/compatibilitytools.d/` in Desktop Mode. Reboot or relaunch Steam in Gaming Mode after installing.

## Games That Specifically Need GE

Concrete examples, as of mid-2026:

- **Persona 4 Arena Ultimax** — extensionless ASF video files. Fixed natively in GE-Proton11-1 via the new quartz RenderFile path.
- **The Medium** — previously needed audio hacks; GE-Proton11-1 removed the hacks and implemented a non-breaking solution.
- **Metal Gear Solid V** — same story, audio fixes replaced with proper implementations.
- **Darksiders Warmastered Edition** — video playback fixed from scratch in GE-Proton11-1.
- **Tex Murphy: Overseer** — needs d7vk and the new native rsx3d library, both in GE-Proton11-1. Enables `PROTON_USE_D7VK=1` via protonfix.
- **Nukitashi 2** — fixed from scratch, one of the harder cases.
- **Arknights Endfield** — anti-cheat fix landed in GE-Proton10-29's protonfixes.
- **Star Citizen** — ongoing patches maintained in GE only.
- **VRChat** (non-Steam) — webcam face tracking patch in GE-Proton11-1.
- A large bucket of Visual Novels sharing the same few engines — fixing one or two fixed the rest.

The pattern: if a game has pre-rendered video, Japanese VN-style FMV, or an anti-cheat quirk that's been in the GE protonfixes list, GE is the answer. If it's a mainstream AAA title from the last few years that runs fine on Proton 9.0, GE won't buy you anything.

## When to Also Try Proton Experimental

Proton Experimental is the right move when a game was broken six months ago and you're not sure if the fix landed. Valve's experimental branch absorbs upstream Wine and DXVK commits faster than numbered Proton ships them. If a recent Wine commit fixes your game, Experimental has it before numbered Proton does.

The catch: Experimental is a moving target. A fix lands today, a regression lands next week. If you switch a game to Experimental and it works, fine — but check back. Bugs introduced in Experimental can break things that worked on numbered Proton. Don't set-and-forget Experimental across your whole library.

## The Short Version

- **Default:** Proton 9.0. Always start here.
- **Need a newer fix not yet in 9.0:** Proton Experimental.
- **FMV cutscene problems, media foundation errors, or a GE-specific protonfix:** GE-Proton11-1.
- **Don't blanket-apply GE or Experimental to everything.** Treat both as targeted tools, not global upgrades.
- **Always check ProtonDB first** when something breaks. Someone has already solved your problem and posted the exact Proton version + launch options.

The dropdown looks like a menu because it is. Most of your library runs on the stable default. The rest is a small set of per-game overrides you'll set once and forget.

Install ProtonUp-Qt, keep GE-Proton11-1 around for the problem titles, and stop overthinking it.
