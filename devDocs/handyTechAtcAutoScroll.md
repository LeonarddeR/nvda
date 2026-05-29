# Handy Tech ATC auto-scroll-forward heuristic

This note documents the design for automatically scrolling the braille display
forward when a user reads to the end of the display using Active Tactile Control
(ATC) on Handy Tech displays, and the packet-level evidence behind it.

Driver: `source/brailleDisplayDrivers/handyTech.py`.

## Goal

Scroll the display forward only when the user has genuinely **read forward to the
end**. Do not scroll when reading backward, when briefly tapping the end, or when
resting on the last cell without having read into it.

## ATC packet behavior (measured on an Actilino, 16 cells)

Validated by logging incoming packets at two ATC sensitivities (0% and 100%),
running 11 reading scenarios at each (22 traces total).

* ATC reports arrive as `HT_EXTPKT_READING_POSITION` (`0x55`): a single byte
  holding the 0-based focal cell index, or `0xFF` for "no read". The Actilino
  emits **only** `0x55`; it never sends the `HT_EXTPKT_ATC_INFO` (`0x52`)
  per-cell pressure map. The heuristic therefore relies solely on the focal cell
  index over time.
* `0xFF` is **not** a finger-lift signal. It is emitted continuously between
  cells during a slide and whenever finger motion stops.
* ATC reports reading **motion**, not mere presence. At low sensitivity a still
  or resting finger goes **silent** (one report, then nothing), so a dwell/linger
  at the end is **undetectable** from the packet stream at low sensitivity. At
  high sensitivity a resting finger keeps re-reporting (micro-movement oscillating
  between the last two cells), but this cannot be relied upon.
* A fast, light swipe does not register every cell at low sensitivity and may
  never reach the end; deliberate reads still reach the last cell.
* Two-handed reading: the single focal index tracks the **leading** reading
  finger and climbs monotonically; an anchored finger only surfaces as a focal
  index after the reading finger lifts. The focal may top out at the
  second-to-last cell rather than the last cell, so the "end zone" is the last
  **two** cells.

## Design decisions

Because dwell is undetectable at low sensitivity, the heuristic does **not**
require the finger to linger. Triggering is based on **forward arrival at the end
with no subsequent reverse**, which is robust to silence and behaves identically
at all sensitivities. A consequence accepted by design: a fast complete forward
swipe that reaches the last cell will scroll.

## Heuristic

Constants (tunable):

| Name | Value | Meaning |
| --- | --- | --- |
| `END_ZONE` | `focal >= numCells - 2` | last two cells (e.g. 14, 15) |
| `TRAVEL_FLOOR` | `numCells - 4` | forward approach requires `minFocal <= TRAVEL_FLOOR` |
| `REVERSE_FLOOR` | `numCells - 4` | focal dropping to `<= REVERSE_FLOOR` after arming = reverse |
| `CONFIRM_WINDOW` | `1.0 s` | must exceed worst observed reverse-hold (0.9 s) |
| `STATE_RESET` | `1.5 s` of continuous no-touch | clears stale session state |

Per-session state: `minFocal` (lowest focal seen), `armed`, `fired`.

On each `0x55` report:

```
if rawPos == 0xFF:
    note no-touch time; if no touch for >= STATE_RESET: reset minFocal and fired
    return
focal = rawPos
minFocal = min(minFocal, focal)
forwardApproached = (minFocal <= TRAVEL_FLOOR)

if (not fired) and (not armed) and (focal >= END_ZONE) and forwardApproached:
    armed = True
    start timer(CONFIRM_WINDOW) -> on expiry: scrollForward(); fired = True; armed = False
elif armed and (focal <= REVERSE_FLOOR):     # reversed before the window elapsed
    cancel timer; armed = False              # may re-arm if the finger climbs back to the end
```

Notes:

* The timer fires whether the finger stays at the end or has lifted; silence is
  expected and fine.
* A reverse is the only veto once armed.
* `forwardApproached` excludes cold taps, rests on the last cell, and pure
  backward reads — none of them travelled up from a low cell.
* `fired` suppresses repeat scrolls until the session resets or the finger leaves
  and re-enters the end zone in a fresh forward read.
* The `0x55` packets are handled on the `hwIo` I/O thread. The confirmation timer
  and the scroll action must run on NVDA's main thread (e.g. via `wx.CallLater`).
  The scroll itself is the same action bound to `braille_scrollForward`.

## Validation against all 22 traces

`SCROLL` = scenarios 1, 5, 7, 8, 9 at both sensitivities, plus the fast-swipe
scenario (11) at 100% (by decision). `NO SCROLL` = scenarios 2, 3, 4, 6, 10 at
both sensitivities, plus scenario 11 at 0% (the fast swipe physically never
reaches the end). All outcomes match intent.

Representative cases:

* Slide forward to end then pause/hold (1, 5): forward-approached, no reverse,
  timer fires even though the rest is silent at low sensitivity.
* Slide to end then reverse (3): armed on arrival, focal drops below
  `REVERSE_FLOOR` at ~0.76 s (100%) / ~0.9 s (0%), within `CONFIRM_WINDOW` =
  cancelled.
* Cold tap on last cell (4) and rest on last cell (10): `minFocal` never
  `<= TRAVEL_FLOOR`, so never armed.
* Backward read (6): cold start at/near the end, not forward-approached.
* Two-handed read with anchor finger (8, 9): timer fires during the forward read
  before the focal jumps back to the anchor finger; an anchor jump that arrives
  first cancels and the subsequent climb re-arms.

## Tuning notes and risks

* The `CONFIRM_WINDOW` margin over the worst reverse-hold (0.9 s at 0%) is only
  ~100 ms. If reverse false-negatives appear in the field, raise the window
  (adds latency) or detect reverse earlier via "focal dropped at least 3 below
  the episode peak" instead of an absolute floor. Do **not** cancel on a single
  one-cell step down: a genuine forward read shows that as the finger settles or
  lifts at the end.
* `TRAVEL_FLOOR = numCells - 4` requires reading up from at least 4 cells before
  the end. A forward read that starts within the last few cells will not scroll;
  lower this if too strict.
* `CONFIRM_WINDOW` could be exposed as a setting or scaled with ATC sensitivity.
