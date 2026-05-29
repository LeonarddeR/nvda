# Handy Tech Actilino — ATC debugging scenarios

Goal: gather incoming ATC packet data to design an "auto-scroll forward at the
end of the display" heuristic that fires **only** when the user has genuinely
read forward to the end — not when reading backward, briefly touching the end,
or resting.

## Setup (do once)

1. **Restart NVDA** so the patched `handyTech.py` driver (with `ATCDBG` logging) is loaded.
2. In NVDA Braille Settings, confirm **ATC is enabled** for the Handy Tech driver.
3. Make sure the log shows **warnings** (the debug lines are logged at warning level).
4. Open a document with a line **much wider than 16 cells** (e.g. a long paragraph
   in Notepad). Position the braille window in the **middle** of a long line so
   there is text both before and after the visible 16 cells.

## How to run each scenario

* Use **only your finger(s) on the braille cells**. Do not press routing or scroll keys.
* Do each scenario **one at a time**.
* After each scenario, **copy the log snippet to the clipboard** and paste it back,
  **labeled with the scenario number**.
* If you make a mistake, just redo that one scenario.

Note: cells are numbered 0-15 (16 cells). "The end" = the rightmost cell.

---

## Single-finger scenarios

**1. Forward slide to the end, then pause.**
Slide one finger smoothly left -> right across all cells, rest on the rightmost
cell ~1 second, then lift. *(This is the case where we WANT to scroll.)*

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:31.299) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9102.3475 type=0x55 numCells=16 raw=5504 rawPos=4
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:31.342) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9102.3912 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:31.433) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9102.4824 type=0x55 numCells=16 raw=5507 rawPos=7
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:31.478) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9102.5270 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:31.546) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9102.5949 type=0x55 numCells=16 raw=5508 rawPos=8
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:31.567) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9102.6162 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:31.839) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9102.8875 type=0x55 numCells=16 raw=550c rawPos=12
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:32.062) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9103.1114 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:32.085) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9103.1336 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:32.287) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9103.3363 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:33.099) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9104.1476 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:33.548) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9104.5972 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:33.660) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9104.7092 type=0x55 numCells=16 raw=55ff rawPos=255

**2. Forward slide, lift in the middle.**
Slide from the left, lift around the middle — do not reach the end. *(No scroll.)*

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:42.346) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9113.3952 type=0x55 numCells=16 raw=5503 rawPos=3
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:42.390) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9113.4394 type=0x55 numCells=16 raw=5504 rawPos=4
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:42.435) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9113.4840 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:42.886) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9113.9354 type=0x55 numCells=16 raw=5508 rawPos=8
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:42.998) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9114.0467 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:43.449) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9114.4981 type=0x55 numCells=16 raw=5507 rawPos=7
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:43.899) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9114.9475 type=0x55 numCells=16 raw=5506 rawPos=6
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:54:43.989) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9115.0379 type=0x55 numCells=16 raw=55ff rawPos=255

**3. Slide to the end, then reverse back.**
Slide to the rightmost cell, then slide back toward the left, then lift. *(No scroll.)*

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:00.009) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9131.0584 type=0x55 numCells=16 raw=5501 rawPos=1
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:00.571) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9131.6204 type=0x55 numCells=16 raw=5506 rawPos=6
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:00.662) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9131.7106 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:00.865) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9131.9136 type=0x55 numCells=16 raw=5509 rawPos=9
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:00.909) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9131.9582 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:00.953) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9132.0023 type=0x55 numCells=16 raw=550b rawPos=11
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:01.111) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9132.1600 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:01.201) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9132.2503 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:01.247) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9132.2957 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:01.313) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9132.3624 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:01.471) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9132.5199 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:01.764) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9132.8126 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:01.854) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9132.9033 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:01.966) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9133.0149 type=0x55 numCells=16 raw=550c rawPos=12
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:02.101) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9133.1499 type=0x55 numCells=16 raw=550b rawPos=11
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:02.170) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9133.2186 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:02.191) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9133.2401 type=0x55 numCells=16 raw=5509 rawPos=9
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:02.304) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9133.3532 type=0x55 numCells=16 raw=5508 rawPos=8
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:02.372) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9133.4208 type=0x55 numCells=16 raw=5507 rawPos=7
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:02.462) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9133.5105 type=0x55 numCells=16 raw=5506 rawPos=6
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:02.551) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9133.6000 type=0x55 numCells=16 raw=5505 rawPos=5
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:02.618) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9133.6673 type=0x55 numCells=16 raw=5507 rawPos=7
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:02.641) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9133.6897 type=0x55 numCells=16 raw=5503 rawPos=3
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:02.867) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9133.9157 type=0x55 numCells=16 raw=5502 rawPos=2
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:03.001) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9134.0502 type=0x55 numCells=16 raw=5501 rawPos=1
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:03.114) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9134.1630 type=0x55 numCells=16 raw=5500 rawPos=0
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:03.361) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9134.4103 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:03.856) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9134.9050 type=0x55 numCells=16 raw=5500 rawPos=0
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:04.059) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9135.1079 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:04.126) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9135.1749 type=0x55 numCells=16 raw=5501 rawPos=1
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:04.171) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9135.2202 type=0x55 numCells=16 raw=55ff rawPos=255

**4. Direct tap on the rightmost cell.**
Without sliding, tap the rightmost cell directly and lift quickly. *(No scroll.)*

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:11.911) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9142.9602 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:12.002) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9143.0506 type=0x55 numCells=16 raw=55ff rawPos=255

**5. Slide to the end, then hold ~2 seconds.**
Slide to the rightmost cell and hold there ~2s before lifting. *(Threshold-setting.)*

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:18.640) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9149.6894 type=0x55 numCells=16 raw=5500 rawPos=0
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:18.685) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9149.7338 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:19.517) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9150.5663 type=0x55 numCells=16 raw=5506 rawPos=6
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:19.719) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9150.7680 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:19.877) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9150.9262 type=0x55 numCells=16 raw=5509 rawPos=9
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:20.012) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9151.0607 type=0x55 numCells=16 raw=550b rawPos=11
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:20.125) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9151.1742 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:20.216) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9151.2645 type=0x55 numCells=16 raw=550d rawPos=13
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:20.259) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9151.3082 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:20.327) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9151.3765 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:20.620) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9151.6688 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:21.678) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9152.7268 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:21.722) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9152.7706 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:22.218) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9153.2665 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:22.285) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9153.3339 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:22.307) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9153.3564 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:22.532) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9153.5808 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:22.667) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9153.7162 type=0x55 numCells=16 raw=55ff rawPos=255

**6. Backward read.**
Start on the rightmost cell and slide right -> left to the start, then lift. *(No scroll.)*

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:30.789) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9161.8383 type=0x55 numCells=16 raw=550d rawPos=13
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:30.834) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9161.8834 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:30.992) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9162.0412 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:31.262) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9162.3109 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:31.802) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9162.8510 type=0x55 numCells=16 raw=5507 rawPos=7
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:31.960) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9163.0090 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:32.208) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9163.2573 type=0x55 numCells=16 raw=5502 rawPos=2
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:32.387) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9163.4359 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:32.499) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9163.5484 type=0x55 numCells=16 raw=5502 rawPos=2
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:32.544) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9163.5933 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:32.590) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9163.6387 type=0x55 numCells=16 raw=5501 rawPos=1
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:32.837) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9163.8859 type=0x55 numCells=16 raw=5500 rawPos=0
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:33.445) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9164.4936 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:33.491) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9164.5396 type=0x55 numCells=16 raw=5500 rawPos=0
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:33.534) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9164.5834 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:33.648) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9164.6973 type=0x55 numCells=16 raw=5500 rawPos=0
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:34.142) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9165.1912 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:34.345) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9165.3943 type=0x55 numCells=16 raw=5500 rawPos=0
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:34.457) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9165.5061 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:34.502) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9165.5508 type=0x55 numCells=16 raw=5501 rawPos=1
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:34.548) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9165.5966 type=0x55 numCells=16 raw=55ff rawPos=255

---

## Two-handed scenarios (single-focal `0x55` behavior with two contact points)

**7. Both hands slide together forward to the end.**
Two fingers side by side, slide left edge -> right edge together, then lift.

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:47.126) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9178.1752 type=0x55 numCells=16 raw=5501 rawPos=1
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:47.171) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9178.2202 type=0x55 numCells=16 raw=5502 rawPos=2
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:47.261) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9178.3102 type=0x55 numCells=16 raw=5506 rawPos=6
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:47.328) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9178.3767 type=0x55 numCells=16 raw=5504 rawPos=4
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:47.530) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9178.5793 type=0x55 numCells=16 raw=5509 rawPos=9
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:47.576) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9178.6251 type=0x55 numCells=16 raw=550a rawPos=10
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:47.711) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9178.7599 type=0x55 numCells=16 raw=550c rawPos=12
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:47.913) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9178.9618 type=0x55 numCells=16 raw=550d rawPos=13
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:47.981) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9179.0301 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:48.161) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9179.2104 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:48.430) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9179.4791 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:48.521) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9179.5703 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:48.723) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9179.7716 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:49.376) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9180.4246 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:49.442) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9180.4914 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:49.713) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9180.7617 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:55:49.781) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9180.8302 type=0x55 numCells=16 raw=55ff rawPos=255

**8. Left finger anchors near the start, right finger reads forward to the end.**
Hold a left finger on an early cell; with the right finger read from the middle
forward to the rightmost cell; then lift both.

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:32.487) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9223.5357 type=0x55 numCells=16 raw=5500 rawPos=0
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:32.533) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9223.5819 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:33.230) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9224.2793 type=0x55 numCells=16 raw=5505 rawPos=5
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:33.387) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9224.4357 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:33.523) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9224.5715 type=0x55 numCells=16 raw=5507 rawPos=7
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:33.680) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9224.7294 type=0x55 numCells=16 raw=5508 rawPos=8
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:33.793) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9224.8417 type=0x55 numCells=16 raw=5509 rawPos=9
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:33.882) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9224.9308 type=0x55 numCells=16 raw=550a rawPos=10
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:33.972) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9225.0207 type=0x55 numCells=16 raw=550c rawPos=12
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:34.130) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9225.1793 type=0x55 numCells=16 raw=550d rawPos=13
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:34.198) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9225.2467 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:34.333) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9225.3818 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:34.534) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9225.5832 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:35.525) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9226.5741 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:35.570) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9226.6192 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:35.614) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9226.6633 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:35.682) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9226.7307 type=0x55 numCells=16 raw=5501 rawPos=1
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:35.772) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9226.8208 type=0x55 numCells=16 raw=55ff rawPos=255

**9. Left finger reads forward to the end while a right finger rests at the end.**
One finger already sitting on the rightmost cell while the other reads up to it.

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:44.367) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9235.4162 type=0x55 numCells=16 raw=5506 rawPos=6
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:44.570) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9235.6186 type=0x55 numCells=16 raw=5508 rawPos=8
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:44.661) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9235.7095 type=0x55 numCells=16 raw=5509 rawPos=9
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:44.773) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9235.8223 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:44.818) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9235.8670 type=0x55 numCells=16 raw=550b rawPos=11
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:44.975) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9236.0235 type=0x55 numCells=16 raw=550c rawPos=12
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:45.066) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9236.1146 type=0x55 numCells=16 raw=550d rawPos=13
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:45.267) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9236.3164 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:45.426) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9236.4749 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:45.516) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9236.5649 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:45.582) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9236.6310 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:45.762) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9236.8112 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:46.168) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9237.2169 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:46.775) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9237.8244 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:56:46.864) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9237.9135 type=0x55 numCells=16 raw=55ff rawPos=255

---

## Resolving the 14-vs-15 question

(In earlier runs, several "end" touches only registered as cell 14, not 15.)

**10. Deliberately rest on the physical rightmost cell, three separate times.**
Touch only the last cell, lift, repeat x3. Shows whether it reports 14 or 15
when you are truly on the last cell.

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:57:01.063) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9252.1116 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:57:01.108) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9252.1567 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:57:02.256) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9253.3045 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:57:02.345) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9253.3943 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:57:02.459) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9253.5075 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:57:02.548) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9253.5967 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:57:02.660) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9253.7092 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:57:02.864) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9253.9128 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:57:02.954) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9254.0025 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:57:03.651) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9254.7001 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:57:03.763) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9254.8118 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:57:03.853) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9254.9018 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:57:04.011) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9255.0604 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:57:04.056) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9255.1052 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:57:04.393) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9255.4418 type=0x55 numCells=16 raw=55ff rawPos=255

---

## The "quick touch" case to exclude

**11. Fast forward swipe to the end, then immediate lift.**
Slide left -> right quickly across the whole display and lift the instant you hit
the end — no pause. (Different from scenario 4''s cold tap: here there IS a
forward trajectory, but no dwell.)

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:57:15.645) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9266.6937 type=0x55 numCells=16 raw=5500 rawPos=0
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:57:16.273) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9267.3223 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (18:57:16.365) - hwIo.ioThread.IoThread (14972):
ATCDBG t=9267.4135 type=0x55 numCells=16 raw=55ff rawPos=255

What this decides: whether "forward arrival at the last cell" alone is enough to
scroll, or whether the finger must also *stay* at the end.

---

# Analysis & proposed auto-scroll heuristic (round 2)

Device: **Actilino** (16 cells, indices 0-15). Transport: HID. ATC packets are
**100% `0x55` (READING_POSITION)** — a single focal cell index, `0xFF` = no read.
**No `0x52` pressure-map packets are ever emitted**, so the heuristic has only the
focal cell + timing to work with.

## Hardware behavior learned from the captures

* `0xFF` is **not** a lift signal. It fires constantly *between* cells during a
  slide, and whenever the finger stops moving.
* A **still finger goes silent** (ATC reports reading motion, not presence).
  Mid-rest silent gaps up to ~1.35s were observed (sc5). So lift and still-rest
  are indistinguishable by silence alone -> never reset state on a no-touch timeout
  shorter than ~1.5s, or a genuine rest will be misread as a lift.
* A genuine rest at the end still produces **repeated** end-zone reports
  (micro-movement oscillating between cell 14 and 15 — sc10). A quick tap/lift
  produces exactly **one** end report (sc4, sc11). This is the signal that
  separates "resting at the end" from "brushed the end and left".
* Forward reads reliably reach cell **15** (the true last cell). Resting on the
  physical last cell oscillates 14<->15.
* Two-handed reading: the single focal tracks the **leading** finger and climbs
  monotonically; an anchored finger only surfaces as a focal *after* the reading
  finger lifts. No special handling needed.

## Scenario outcomes the heuristic must reproduce

SCROLL: 1, 5, 7, 8, 9    NO-SCROLL: 2, 3, 4, 6, 10, 11

## Three necessary signals (each justified by >=1 scenario)

1. Forward approach   — excludes sc10 (cold rests on last cell), sc4 (cold tap).
2. Dwell >= ~0.8s end  — excludes sc11 (fast swipe, 1 report, 90ms), sc4.
3. No reverse         — excludes sc3, sc6.

Key timing gap: sc3 (reverse, no-scroll) holds the end only ~0.56s before
reversing; scroll cases produce a qualifying end report at ~1.0-1.5s. A dwell
threshold of ~0.8s sits cleanly between them.

## Proposed heuristic (packet-driven, no timer)

Constants (tunable; could later be tied to a sensitivity setting):
  LAST            = numCells - 1                # 15
  END_ZONE        = focal >= numCells - 2       # {14, 15}
  TRAVEL_FLOOR    = numCells - 4                # <=12  => "came from far enough"
  REVERSE_FLOOR   = numCells - 4                # focal <=12 after end => left/reversed
  DWELL_THRESHOLD = 0.8  seconds
  STATE_RESET     = 1.5  seconds of no-touch    # clear stale session (> max rest gap)

Per-session state:
  minFocal           # lowest focal seen this session
  reachedLast        # focal == LAST seen this episode
  endZoneEntryTime   # perf_counter when focal first entered END_ZONE (None if outside)
  fired              # already scrolled this episode

On each 0x55 packet:
  if rawPos == 0xFF:                # no read; do NOT reset (still finger looks like this)
      record time of last no-touch; if sustained >= STATE_RESET, clear all state
      return
  focal = rawPos
  minFocal = min(minFocal, focal)
  if focal == LAST: reachedLast = True

  if focal in END_ZONE:
      if endZoneEntryTime is None:          # entering the end zone
          endZoneEntryTime = now
      forwardApproached = (minFocal <= TRAVEL_FLOOR)   # travelled up from a low cell
      dwell = now - endZoneEntryTime
      if (not fired) and forwardApproached and reachedLast and dwell >= DWELL_THRESHOLD:
          scroll_forward()
          fired = True
  elif focal <= REVERSE_FLOOR:              # left the end going down = reverse / new read
      endZoneEntryTime = None               # reset dwell + suppression for this region
      fired = False
      # (minFocal stays; a sustained reverse simply never re-qualifies)

Notes:

* Fires **once per end-dwell episode** (suppressed by `fired` until the finger
  leaves the end zone downward, or the session resets).
* After a scroll the window content changes; the finger is typically still at the
  old end zone — suppression prevents repeat scrolling until they move/lift.
* No wx timer required: a genuine rest always yields a 2nd end-zone report >=0.8s
  after entry; a quick lift yields only one and never qualifies.

## Validation against all 11 scenarios

  1 SCROLL  fwd(min4) reachedLast, 2nd end report @1.02s >=0.8, no reverse
  2 no      never reaches END_ZONE
  3 no      reaches end but reverses at 0.76s; no end report >=0.8s before reverse
  4 no      cold (min=14, not <=12) and single report
  5 SCROLL  fwd(min0) reachedLast, end report @1.35s
  6 no      starts high, reverses to 0; treated as reverse
  7 SCROLL  fwd two-hand slide, end report @1.39s
  8 SCROLL  fwd, end report @1.32s -> fires before anchor-jump to cell 1
  9 SCROLL  fwd, end report @1.51s
 10 no      every touch cold on last cell (minFocal never <=12) -> forwardApproached False
 11 no      fwd but single end report, 90ms -> dwell < 0.8s

## Open tuning decisions

* DWELL_THRESHOLD (0.8s): conservative gap is 0.56s..1.0s. Lower = snappier but
  risks catching a slow reverse; higher = safer but laggier. Candidate for a
  user setting.
* END_ZONE width: last two cells (14,15) for dwell detection, but firing also
  requires reachedLast (15) at least once, so a finger that only ever hits 14
  will not scroll.
* sc8 (two-handed anchor) scrolls under this design (fires during the end dwell,
  before the focal jumps back to the anchor finger). If that is unwanted, it is
  the one case that would need extra handling.
