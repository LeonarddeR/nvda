# Handy Tech ATC auto-scroll — reverse-engineered from Handy Tech's own driver

This note documents the **actual** ATC ("Active Tactile Control") reading-analysis and
auto-scroll algorithm as implemented in Handy Tech / Help Tech's own braille driver,
recovered by reverse engineering the binary. It is the authoritative counterpart to the
heuristic-based design in [`handyTechAtcAutoScroll.md`](./handyTechAtcAutoScroll.md),
which was derived from packet observation alone.

The goal: implement the auto-scroll behaviour natively in
`source/brailleDisplayDrivers/handyTech.py` without bringing back the old COM server.

## Source binaries

Provided by Handy Tech (stored outside the repo, under `C:\Sources\HT`):

| File | Arch | Role |
| --- | --- | --- |
| `jaws/handy.jlb` | x86-64 | **JAWS braille driver, 2023 — newest, the analysis target.** |
| `jaws/sbsupport.dll` | x86-64 | Dealer/service dialog support (not ATC). |
| `NVDA/HtBrailleDriverServer.dll` | x86 | The old NVDA COM server (≤ NVDA 2017.1). Same logic, older. |
| `NVDA/sbsupport.dll` | x86 | Dealer/service dialog support (not ATC). |

`handy.jlb` is a C++ DLL built with MSVC and retains full **RTTI**, so all class names
survive. The auto-scroll logic is *not* in `sbsupport.dll` (that only handles the
dealer/"service bytes" config dialog).

### Tooling

No disassembler was installed. Rizin was used (`winget install Rizin.Rizin`,
binaries under `C:\Program Files (x86)\Rizin\bin`, e.g. `rz-bin`, `rizin`). Raw
disassembly dumps live under `C:\Sources\HT\re\` (`decider.asm` is the main function).
There is no decompiler plugin, so analysis is from x64 assembly.

## Class architecture (from RTTI)

All classes are in namespace `BrlDriver`. Relevant ones:

* `AtcActionProcessor` — owns a worker thread (3 `CreateEventW` events + 2 critical
  sections, object size 184 bytes). Actions are **enqueued** to it; its thread fires the
  host callback `onAtcActionEvent(%d,%d,%d,%d,%d)`.
* `AtcBrailleNavigator` / `AtcLineInfo` — model of the current braille line (length,
  start, end cell).
* `AtcAction` base class with one subclass per action type (each is a 82-byte
  constructor that logs `[ATC Action %u]: <name>`):
  `AtcCharacterSaying`, `AtcSpelling`, `AtcWordSaying`, `AtcBrailleLineSaying`,
  `AtcHighSignal`, `AtcLowSignal`, `AtcLineEndSignal`, `AtcNextBrailleLine`,
  `AtcPrevBrailleLine`, `AtcSayLineGoNextLine`, `AtcReadAloud`, `AtcSayAttribute`,
  `AtcSayAttributeChanged`, `AtcRouteCursor`, `AtcNoAction`.
* `AtcMonitor` — mirrors display + ATC state to a *separate* monitor/visualiser window
  (the `atcWindowRegistrationString` window). Irrelevant to scrolling; ignore.
* `JawsInputProcessor` / `InputProcessor` — receive device packets and drive the above.

## The decision function

Everything below is one function (`fcn.1800382c0` in `handy.jlb`, ~6.3 KB, 215 basic
blocks), called from `JawsInputProcessor::virtual_56` once per ATC **reading-position**
report. This is the analogue of the `0x55 HT_EXTPKT_READING_POSITION` packet handler.

Signature (recovered): `process(this, int pos, void* geometry)`

* `this` (called `S` below) is the ATC analysis-state object; it embeds the
  `AtcBrailleNavigator`/line model at offset `+0x430`.
* `pos` is the **focal cell index** (0-based) just reported by ATC.

### State object field map (`S`)

| Offset | Meaning |
| --- | --- |
| `+0x270` | device/display handle (passed to every action constructor) |
| `+0x380` | signal observer (gets `vtbl+0x10` "signal" callbacks) |
| `+0x3b8` | computed average reading speed (cells/s) |
| `+0x3c0` | configured action code for state **1 (fast forward)** |
| `+0x3c4` | configured action code for state **2 (slow forward)** |
| `+0x3c8` | configured action code for state **3 (dwell)** |
| `+0x3cc` | configured action code for state **4 (backward)** |
| `+0x3d0` | **speed threshold** (cells/s): fast vs. slow |
| `+0x3d4` | **dwell-time threshold** (ms) |
| `+0x3d8` | extra arg passed to most action constructors (signal level / sensitivity) |
| `+0x3df` | setting: **auto-next-line (NextBrailleLine) enabled** (bool) |
| `+0x3e0` | **base delay** (ms) for the scheduled NextBrailleLine |
| `+0x3e4` | setting: **LineEndSignal enabled** (bool) |
| `+0x3e8` | the `AtcActionProcessor` (action queue) the actions are enqueued onto |
| `+0x3f0` | current reading-state (0–4) |
| `+0x3f4` | previous reading-state |
| `+0x3f8` | "fresh start" flag (first report after an idle/timeout reset) |
| `+0x3f9` | **auto-scroll arm** — one-shot latch, set when a new line is loaded, consumed on fire |
| `+0x3fc` | last position |
| `+0x400` | last timestamp (`GetTickCount`) |
| `+0x404` | accumulated dwell/elapsed time |
| `+0x408` | timestamp of last NextBrailleLine fire |
| `+0x40c` | "recently fired" lock flag |
| `+0x410` | last emitted action code |
| `+0x418` | per-line "line-saying already done" flag |
| `+0x419` | "did a forward read this episode" flag |
| `+0x420` | pointer to a per-cell **touched** bool array |
| `+0x428` | **count of distinct cells touched** |
| `+0x430` | `AtcBrailleNavigator`/line model: `[+0x1c]`=line length, `[+0x20]`=start cell, `[+0x24]`=**end cell** |
| `+0x478`, `+0x47c` | display position bounds (range guard) |
| `+0x488` | 5×`double` sliding speed-sample buffer (40 bytes) |

### Constants (verified in the binary)

| Constant | Value | Use |
| --- | --- | --- |
| idle/timeout reset | **2000 ms** (`0x7d0`) | resets accumulators; also the post-fire re-fire lock window |
| coverage threshold | **0.25** (`float 0x3e800000` @ `0x1800df91c`) | fraction of the line's cells that must be touched |
| near-end window | **3 cells** | `lineEnd - pos < 3` |
| speed window | **5 samples** (`double 5.0` @ `0x1800df920`) | sliding average |
| speed scale | **1000.0** (`double` @ `0x1800df928`) | `speed = Δcells × 1000 / Δms` → cells/s |
| per-cell scroll delay | **200 ms** (`0xc8`) | `delay = (lineEnd − pos) × 200 + base` |
| fast hysteresis band | **3** | stay "fast" if `avg ≥ threshold − 3` and threshold > 3 |

## Algorithm (distilled)

Per reading-position report `pos`:

1. **Range guard.** If `pos` is outside the display window bounds (`+0x478`/`+0x47c`),
   return.
2. **Idle reset.** If the post-fire lock (`+0x40c`) is set and `now − lastFire > 2000 ms`,
   clear the accumulator and set the fresh-start flag.
3. **Mark coverage.** If `touched[pos] == 0`, set it and increment the distinct-cell
   counter `+0x428`. This is how the driver measures "how much of the line was read",
   built incrementally from the focal index — it does **not** need the `0x52` per-cell
   pressure map.
4. **Classify reading state** (`+0x3f0`) from the position delta `Δpos = pos − lastPos`
   and time delta `Δt`:
   * `Δpos < 0` → state **4 (backward)**; reset accumulator + speed buffer.
   * `Δpos == 0` → dwell: accumulate `Δt`; if `accum > dwellThreshold (+0x3d4)` →
     state **3 (dwell)**, else keep previous state (no new action this report).
   * `Δpos > 0` → forward: push `speed = Δcells×1000/accum` (cells/s) into the 5-sample
     ring, average it (`+0x3b8`). If `avg < speedThreshold (+0x3d0)` → state **2 (slow)**,
     else state **1 (fast)** (with a 3-unit hysteresis band so a previously-fast reader
     isn't bumped to "slow" by one slow sample). Set the "did-forward-read" flag `+0x419`.
   * On a fresh start, state is forced to **0 (no action)** if the previous action was a
     NextBrailleLine, otherwise **2**.
5. **Reading-assistant action.** Map the reading state → a configured **action code**
   (`+0x3c0`/`+0x3c4`/`+0x3c8`/`+0x3cc` for fast/slow/dwell/backward), fire the matching
   signal callback, then construct and **enqueue** the corresponding `AtcAction`:

   | action code | class | constructor |
   | --- | --- | --- |
   | 1 | `AtcCharacterSaying` | `fcn.18000c070` |
   | 2 | `AtcWordSaying` / `AtcSpelling` (with word-boundary nav) | `fcn.18000c340` / `fcn.18000c1b0` |
   | 3 | `AtcBrailleLineSaying` | `fcn.18000c480` |
   | 4 | `AtcHighSignal` | `fcn.18000c710` |
   | 5 | `AtcLowSignal` | `fcn.18000c5c0` |
   | 6 | `AtcSayLineGoNextLine` | `fcn.18000cc30` |
   | 7 | `AtcReadAloud` | `fcn.18000cd70` |
   | 8 | `AtcSayAttribute` | `fcn.18000ceb0` |
   | 9 | `AtcSayAttributeChanged` | `fcn.18000cff0` |
   | 0xa | `AtcRouteCursor` | `fcn.18000d130` |
   | other | `AtcNoAction` | `fcn.18000d270` |

   These are the user-configurable "ATC assistant" behaviours and are **separate** from
   auto-scroll.

6. **Auto-scroll (the part we care about).** After step 5, on every qualifying report:

   ```
   readEnough = touchedCount / lineLength >= 0.25        # coverage ≥ 25% of the line
   nearEnd    = (lineEnd - pos) < 3                       # within 3 cells of the line end
   if not readEnough: return
   if not didForwardRead(+0x419):                         # never read forward this episode…
       if lineStart != lineEnd: return                   # …only allowed on a degenerate line
   if not nearEnd: return
   if not armed(+0x3f9): return                           # one-shot per line
   armed = 0                                              # consume the latch

   if lineEndSignalEnabled(+0x3e4):
       enqueue AtcLineEndSignal(pos, display, 0)          # tactile/audio "end of line" cue

   if not autoNextLineEnabled(+0x3df): return
   delay = (lineEnd - pos) * 200ms + baseDelay(+0x3e0)
   enqueue AtcNextBrailleLine(pos, display, delay)        # SCHEDULED scroll-forward
   ```

### Key takeaways

* **Auto-scroll = `AtcNextBrailleLine`**, enqueued only when the reader has *covered ≥ 25 %
  of the line's cells* **and** *is within 3 cells of the line end* **and** the per-line
  arm latch is still set. It is gated by two independent settings: a "line-end signal" cue
  and the "auto next line" action itself.
* The scroll is **scheduled with a delay**, not immediate:
  `delay = (lineEnd − pos) × 200 ms + base`. Being right at the end fires after just the
  base delay; being a few cells short waits longer (≈ time to read those cells). A new
  reading report supersedes the state, so reading on/backward within the delay effectively
  cancels/reschedules.
* Coverage is tracked from the **single focal-cell index** by marking each visited cell —
  so this works on the Actilino's `0x55`-only stream. The `0x52` per-cell pressure map is
  **not** required (contrary to the pessimistic note in the heuristic doc).
* `AtcSayLineGoNextLine` (action code 6) is the *combined* "read the whole line aloud then
  go to next line" assistant action — a different feature from the silent auto-scroll, and
  configured as one of the reading-state actions.
* There is a separate **arm latch** (`+0x3f9`) set when a new line is loaded (in another
  function, ~`0x1800359c3`): each displayed line can auto-scroll **once**.
* A **2000 ms** idle window resets the analysis and re-arms; a post-fire lock suppresses an
  immediate second scroll.

## The `0x52` pressure-map path (Modular Evolution / older protocol)

The `0x55` reading-position packet (single focal cell) is only one of the two ATC input
formats. The older `HT_EXTPKT_ATC_INFO` (`0x52`) packet carries a **per-cell pressure
map**. Crucially, **both formats feed the exact same auto-scroll decider** — the `0x52`
path just has an extra front-end that reduces the pressure map to one focal cell.

That front-end is `JawsInputProcessor::virtual_48` (the "ATC Pressures" handler,
`0x180035d50` in `handy.jlb`). Per `0x52` packet it:

1. **Integrates pressure over time.** `accum[i] += pressure[i]` into `S[+0x3a0]` for each
   cell with `pressure > 0`; a cell whose pressure drops to `≤ 0` is **reset to 0**. So a
   resting finger builds up; a lifted finger clears.
2. **Smooths spatially.** Convolves the accumulated map with a fixed 5-tap kernel
   `[1, 4, 4, 4, 1]` (at `0x180108098`, half-width `N = 2` at `0x1801080ac`) into
   `S[+0x3a8]`.
3. **Finds the focal cell** = `argmax` of the smoothed map, searched outward from the
   previous focal (`S[+0x3b4]`), clamped to the current line's start/end
   (`fcn.180039c80`/`c70`) and validity (`fcn.180039cf0`). Stored in `S[+0x3b0]`.
   A direction flag `S[+0x398]` records forward vs. backward vs. the previous focal.
4. **Calls the reading-position handler with that focal cell** — `this->vtbl[+0x38]`,
   which is `virtual_56`, i.e. the **same** `0x55` handler that runs the decider
   (`fcn.1800382c0`).

So the auto-scroll heuristic (25 % coverage + within-3-of-end + delay etc.) is
**identical** for Modular Evolution / `0x52` devices; only the focal-cell derivation
differs:

* `0x55` (Active family, e.g. Actilino): focal cell comes straight from the device.
* `0x52` (Modular Evolution, older): focal cell = peak of the time-integrated,
  `[1,4,4,4,1]`-smoothed pressure map, clamped to line bounds.

Implication for NVDA: the design only needs **one** auto-scroll implementation. For `0x52`
devices, reduce the pressure map to a focal cell (NVDA's `_parseAtcInfo` already exposes
per-cell pressures, and `AtcGesture` already derives a focal point) and feed it through the
same gate. The current spec scoping auto-scroll to `0x55`-only Active-family displays is a
*deliberate simplification*, not a protocol limitation — Handy Tech's own driver supports
both with shared logic. (The old x86 COM server `NVDA/HtBrailleDriverServer.dll` is the
same architecture, older; it can be cross-checked the same way if needed, but the JAWS
binary already contains both paths.)

## Reconciliation with the heuristic in `handyTechAtcAutoScroll.md`

| Aspect | Own heuristic (packet-derived) | Handy Tech's actual driver |
| --- | --- | --- |
| End zone | last 2 cells (`>= numCells-2`) | within 3 of `lineEnd` (`lineEnd - pos < 3`) |
| "Genuinely read" test | forward approach from `<= numCells-4` (min focal) | **coverage ≥ 25 % of line cells** (distinct touched) + a forward-read flag |
| Trigger timing | fixed 1.0 s confirm window, fires on silence | **delay = (lineEnd−pos)×200 ms + base**, recomputed per report |
| Reverse veto | drop below `numCells-4` cancels | a backward Δpos resets state; reading back re-runs the gate |
| Re-fire suppression | `fired` flag + 1.5 s no-touch reset | per-line **arm latch** + 2000 ms post-fire lock + 2000 ms idle reset |
| Speed/dwell | not modelled (dwell undetectable at low sensitivity) | 5-sample cells/s average + dwell-time accumulator (drives assistant actions, not the scroll gate) |
| Input needed | focal index only | focal index only (coverage built incrementally) |

The two designs agree on the spirit (forward read to the end → scroll, backward cancels)
but differ on the **evidence** for "really read" (coverage fraction vs. travel-from-low)
and on **timing** (proportional delay vs. fixed confirm window).

## Recommended native implementation (NVDA `handyTech.py`)

Match Handy Tech's behaviour so it feels identical to their JAWS/COM driver:

1. On each `HT_EXTPKT_READING_POSITION` (`0x55`) report, on the `hwIo` thread, update:
   * a per-cell `touched` set for the current braille window (mark `focal`),
   * `lastPos`, `lastTime`, and the backward/forward determination.
2. Maintain a per-line **arm** flag, set whenever the braille window content/region
   changes (NVDA already knows when it pans/scrolls — hook the same place that updates the
   window), reset to "armed" for each new line.
3. Gate the scroll with HT's three conditions, reusing their constants:
   * `len(touched) / numCells >= 0.25`,
   * `(lastCellIndex - focal) < 3`,
   * armed, and the user has auto-scroll enabled.
4. Schedule the scroll with `delay = (lastCellIndex - focal) * 0.2 + base` seconds via
   `wx.CallLater`/`core.callLater` (timer + action on the **main** thread; packets arrive
   on the I/O thread). A subsequent report that moves backward or to a new line cancels the
   pending timer.
5. The scroll action itself is the existing `braille_scrollForward` binding.
6. Expose at least the on/off toggle (mirror `+0x3df`); optionally the base delay
   (`+0x3e0`) and the "line-end signal" cue (`+0x3e4`). The 25 % coverage, 3-cell window,
   200 ms/cell and 2000 ms reset can start as the same hard-coded constants HT uses.

Scope, per the existing spec, is Active-family displays (Actilino etc.) using the `0x55`
reading-position stream — not Modular Evolution's `0x52` pressure map.

> Note: the reading-state classifier (fast/slow/dwell/backward → configurable
> say-character / say-word / say-line / read-aloud / signal actions) is the broader "ATC
> assistant" feature set. It is out of scope for auto-scroll but documented above because
> it shares the same per-report pipeline, and Handy Tech may want it later.
