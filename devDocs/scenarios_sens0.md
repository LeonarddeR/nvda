# Handy Tech Actilino — ATC scenarios at MINIMUM sensitivity (0%)

Companion to `scenarios.md` (which was captured at **100%** sensitivity).
Run the **exact same 11 scenarios** here, but first set ATC sensitivity to the
**lowest** value (0% in the display UI, = sensitivity 0 in the driver).

Why: the round-2 heuristic depends on report **cadence** and on a resting finger
emitting a 2nd end-zone report (14<->15 micro-movement). At low sensitivity the
device needs more pressure to register a read, so a light rest may emit far fewer
reports. This run tests whether:

* a genuine end-dwell still produces >=2 end-zone reports (vs looking like a tap),
* the ~0.8s dwell gap between "reverse" (sc3) and "rest" (sc1/5) still holds,
* forward slides still reach cell 15, or stall earlier,
* inter-packet gaps / silent periods get longer.

## Setup (do once)

1. **Restart NVDA** so the patched `handyTech.py` driver (with `ATCDBG` logging) is loaded.
2. In NVDA Braille Settings, set **ATC sensitivity to the LOWEST value (0%)** and
   confirm **ATC is enabled** for the Handy Tech driver.
3. Make sure the log shows **warnings**.
4. Open a document with a line **much wider than 16 cells**; position the braille
   window in the **middle** of a long line (text both before and after).

## How to run each scenario

* Use **only your finger(s) on the braille cells**. Do not press routing or scroll keys.
* Try to use your **normal reading pressure** — do NOT press extra hard to compensate
  for the low sensitivity. The point is to see what light/normal touch produces at 0%.
* Do each scenario **one at a time**; paste the log snippet under its heading.
* If a scenario produces no packets at all, note that explicitly (that itself is a result).

Cells are numbered 0-15. "The end" = the rightmost cell (15).

---

## Single-finger scenarios

**1. Forward slide to the end, then pause (~1s).** *(WANT scroll.)*

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:06.268) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9857.3166 type=0x55 numCells=16 raw=5502 rawPos=2
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:06.335) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9857.3836 type=0x55 numCells=16 raw=5503 rawPos=3
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:06.426) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9857.4747 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:06.492) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9857.5409 type=0x55 numCells=16 raw=5505 rawPos=5
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:06.514) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9857.5635 type=0x55 numCells=16 raw=5506 rawPos=6
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:06.628) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9857.6770 type=0x55 numCells=16 raw=5507 rawPos=7
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:06.718) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9857.7664 type=0x55 numCells=16 raw=5508 rawPos=8
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:06.831) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9857.8801 type=0x55 numCells=16 raw=5509 rawPos=9
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:06.876) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9857.9248 type=0x55 numCells=16 raw=550a rawPos=10
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:06.966) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9858.0145 type=0x55 numCells=16 raw=550b rawPos=11
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:07.032) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9858.0808 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:07.054) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9858.1034 type=0x55 numCells=16 raw=550d rawPos=13
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:07.167) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9858.2162 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:07.326) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9858.3745 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:07.416) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9858.4649 type=0x55 numCells=16 raw=55ff rawPos=255

**2. Forward slide, lift in the middle.** *(No scroll.)*

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:15.335) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9866.3839 type=0x55 numCells=16 raw=5503 rawPos=3
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:15.402) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9866.4513 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:15.470) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9866.5191 type=0x55 numCells=16 raw=5505 rawPos=5
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:15.583) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9866.6322 type=0x55 numCells=16 raw=5506 rawPos=6
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:15.673) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9866.7219 type=0x55 numCells=16 raw=5507 rawPos=7
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:15.786) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9866.8351 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:15.875) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9866.9240 type=0x55 numCells=16 raw=5508 rawPos=8
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:16.032) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9867.0815 type=0x55 numCells=16 raw=55ff rawPos=255

**3. Slide to the end, then reverse back.** *(No scroll.)*

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:23.931) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9874.9804 type=0x55 numCells=16 raw=5503 rawPos=3
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:23.976) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9875.0249 type=0x55 numCells=16 raw=5505 rawPos=5
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:24.021) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9875.0697 type=0x55 numCells=16 raw=5506 rawPos=6
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:24.065) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9875.1143 type=0x55 numCells=16 raw=5507 rawPos=7
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:24.111) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9875.1597 type=0x55 numCells=16 raw=5508 rawPos=8
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:24.179) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9875.2279 type=0x55 numCells=16 raw=5509 rawPos=9
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:24.268) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9875.3174 type=0x55 numCells=16 raw=550b rawPos=11
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:24.313) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9875.3618 type=0x55 numCells=16 raw=550c rawPos=12
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:24.358) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9875.4068 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:24.425) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9875.4742 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:24.583) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9875.6320 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:24.697) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9875.7459 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:25.033) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9876.0818 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:25.237) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9876.2859 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:25.281) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9876.3301 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:25.326) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9876.3750 type=0x55 numCells=16 raw=550c rawPos=12
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:25.371) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9876.4201 type=0x55 numCells=16 raw=550b rawPos=11
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:25.484) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9876.5326 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:25.506) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9876.5552 type=0x55 numCells=16 raw=5509 rawPos=9
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:25.573) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9876.6219 type=0x55 numCells=16 raw=5508 rawPos=8
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:25.618) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9876.6668 type=0x55 numCells=16 raw=5507 rawPos=7
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:25.663) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9876.7116 type=0x55 numCells=16 raw=5506 rawPos=6
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:25.709) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9876.7577 type=0x55 numCells=16 raw=5505 rawPos=5
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:25.776) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9876.8245 type=0x55 numCells=16 raw=5503 rawPos=3
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:25.866) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9876.9151 type=0x55 numCells=16 raw=5502 rawPos=2
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:25.979) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9877.0280 type=0x55 numCells=16 raw=5501 rawPos=1
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:26.068) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9877.1167 type=0x55 numCells=16 raw=5500 rawPos=0
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:26.225) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9877.2744 type=0x55 numCells=16 raw=55ff rawPos=255

**4. Direct tap on the rightmost cell, lift quickly.** *(No scroll.)*

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:56.490) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9907.5388 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:56.625) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9907.6743 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:56.781) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9907.8305 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:07:56.894) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9907.9428 type=0x55 numCells=16 raw=55ff rawPos=255

**5. Slide to the end, then hold ~2s.** *(Threshold-setting.)*

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:05.715) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9916.7644 type=0x55 numCells=16 raw=5500 rawPos=0
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:06.344) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9917.3933 type=0x55 numCells=16 raw=5508 rawPos=8
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:06.413) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9917.4618 type=0x55 numCells=16 raw=5509 rawPos=9
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:06.457) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9917.5057 type=0x55 numCells=16 raw=550b rawPos=11
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:06.615) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9917.6637 type=0x55 numCells=16 raw=550c rawPos=12
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:06.660) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9917.7091 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:06.750) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9917.7992 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:06.908) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9917.9570 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:07.065) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9918.1135 type=0x55 numCells=16 raw=55ff rawPos=255

**6. Backward read (rightmost -> start).** *(No scroll.)*

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:15.030) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9926.0788 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:15.480) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9926.5288 type=0x55 numCells=16 raw=550b rawPos=11
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:15.547) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9926.5960 type=0x55 numCells=16 raw=550a rawPos=10
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:15.637) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9926.6863 type=0x55 numCells=16 raw=5509 rawPos=9
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:15.682) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9926.7310 type=0x55 numCells=16 raw=5508 rawPos=8
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:15.727) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9926.7764 type=0x55 numCells=16 raw=5507 rawPos=7
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:15.774) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9926.8226 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:15.863) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9926.9120 type=0x55 numCells=16 raw=5506 rawPos=6
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:15.907) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9926.9563 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:15.930) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9926.9791 type=0x55 numCells=16 raw=5505 rawPos=5
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:16.020) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9927.0686 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:16.132) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9927.1811 type=0x55 numCells=16 raw=5503 rawPos=3
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:16.290) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9927.3386 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:16.334) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9927.3834 type=0x55 numCells=16 raw=5502 rawPos=2
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:16.492) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9927.5412 type=0x55 numCells=16 raw=5501 rawPos=1
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:16.515) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9927.5637 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:16.582) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9927.6312 type=0x55 numCells=16 raw=5501 rawPos=1
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:16.650) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9927.6991 type=0x55 numCells=16 raw=5500 rawPos=0
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:16.785) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9927.8337 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:16.875) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9927.9237 type=0x55 numCells=16 raw=5500 rawPos=0
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:16.943) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9927.9922 type=0x55 numCells=16 raw=55ff rawPos=255

---

## Two-handed scenarios

**7. Both hands slide together forward to the end.**

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:23.628) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9934.6766 type=0x55 numCells=16 raw=5500 rawPos=0
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:24.210) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9935.2591 type=0x55 numCells=16 raw=5506 rawPos=6
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:24.300) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9935.3489 type=0x55 numCells=16 raw=5507 rawPos=7
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:24.345) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9935.3939 type=0x55 numCells=16 raw=5508 rawPos=8
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:24.412) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9935.4612 type=0x55 numCells=16 raw=550b rawPos=11
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:24.435) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9935.4841 type=0x55 numCells=16 raw=550c rawPos=12
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:24.548) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9935.5973 type=0x55 numCells=16 raw=550a rawPos=10
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:24.616) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9935.6646 type=0x55 numCells=16 raw=550d rawPos=13
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:24.750) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9935.7992 type=0x55 numCells=16 raw=550c rawPos=12
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:24.863) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9935.9116 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:24.907) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9935.9564 type=0x55 numCells=16 raw=550d rawPos=13
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:24.997) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9936.0464 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:25.110) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9936.1591 type=0x55 numCells=16 raw=55ff rawPos=255

**8. Left finger anchors near the start, right finger reads forward to the end.**

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:32.626) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9943.6750 type=0x55 numCells=16 raw=5506 rawPos=6
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:32.738) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9943.7867 type=0x55 numCells=16 raw=5507 rawPos=7
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:32.828) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9943.8767 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:32.872) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9943.9215 type=0x55 numCells=16 raw=5508 rawPos=8
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:32.963) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9944.0118 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:33.075) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9944.1244 type=0x55 numCells=16 raw=550a rawPos=10
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:33.189) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9944.2378 type=0x55 numCells=16 raw=550b rawPos=11
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:33.279) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9944.3280 type=0x55 numCells=16 raw=550c rawPos=12
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:33.435) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9944.4844 type=0x55 numCells=16 raw=550d rawPos=13
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:33.548) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9944.5971 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:33.661) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9944.7099 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:33.863) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9944.9118 type=0x55 numCells=16 raw=55ff rawPos=255

**9. Left finger reads forward to the end while a right finger rests at the end.**

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:44.056) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9955.1047 type=0x55 numCells=16 raw=550b rawPos=11
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:44.124) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9955.1724 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:44.215) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9955.2635 type=0x55 numCells=16 raw=550d rawPos=13
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:44.326) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9955.3746 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:44.979) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9956.0281 type=0x55 numCells=16 raw=5501 rawPos=1
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:45.136) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9956.1848 type=0x55 numCells=16 raw=5502 rawPos=2
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:45.225) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9956.2745 type=0x55 numCells=16 raw=5503 rawPos=3
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:45.317) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9956.3655 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:45.340) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9956.3889 type=0x55 numCells=16 raw=5505 rawPos=5
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:45.385) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9956.4337 type=0x55 numCells=16 raw=5506 rawPos=6
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:45.451) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9956.5002 type=0x55 numCells=16 raw=5507 rawPos=7
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:45.519) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9956.5683 type=0x55 numCells=16 raw=5508 rawPos=8
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:45.631) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9956.6801 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:45.699) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9956.7474 type=0x55 numCells=16 raw=550a rawPos=10
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:45.788) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9956.8372 type=0x55 numCells=16 raw=550b rawPos=11
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:45.833) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9956.8820 type=0x55 numCells=16 raw=550c rawPos=12
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:45.924) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9956.9726 type=0x55 numCells=16 raw=550d rawPos=13
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:46.127) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9957.1757 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:46.329) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9957.3775 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:46.396) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9957.4445 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:46.531) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9957.5798 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:46.779) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9957.8281 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:46.981) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9958.0298 type=0x55 numCells=16 raw=55ff rawPos=255

---

## 14-vs-15 question

**10. Deliberately rest on the physical rightmost cell, three separate times.**

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:54.160) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9965.2089 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:54.226) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9965.2748 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:54.361) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9965.4103 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:54.430) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9965.4785 type=0x55 numCells=16 raw=550e rawPos=14
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:54.451) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9965.5002 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:55.936) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9966.9851 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:56.027) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9967.0757 type=0x55 numCells=16 raw=55ff rawPos=255
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:57.467) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9968.5160 type=0x55 numCells=16 raw=550f rawPos=15
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:08:57.579) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9968.6282 type=0x55 numCells=16 raw=55ff rawPos=255

---

## Quick-touch case to exclude

**11. Fast forward swipe to the end, then immediate lift.**

WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:09:03.766) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9974.8154 type=0x55 numCells=16 raw=5500 rawPos=0
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:09:03.857) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9974.9064 type=0x55 numCells=16 raw=5501 rawPos=1
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:09:03.971) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9975.0201 type=0x55 numCells=16 raw=5502 rawPos=2
WARNING - brailleDisplayDrivers.handyTech.BrailleDisplayDriver._handleInputStream (19:09:04.599) - hwIo.ioThread.IoThread (16876):
ATCDBG t=9975.6484 type=0x55 numCells=16 raw=55ff rawPos=255

---

# Sensitivity comparison (0% vs 100%) and revised design implication

Focal sequences at 0% (ff dropped):
  1  2,3,5,6,7,8,9,10,11,13,14,15            peak15; single 15 then SILENT (pause = 0 re-reports)
  2  3,5,6,7,8                               peak8
  3  3,5,6,7,8,9,11,12,14,15,15,14,12..0     peak15 then reverse; ~0.74s at end before reversing
  4  15,15                                   cold taps
  5  0,8,9,11,12,14,15                       peak15; single 15 then SILENT (2s hold = 0 re-reports)
  6  15,11,10,9,8,7,6,5,3,2,1,0              cold start at 15, descends
  7  0,6,7,8,11,12,10,13,12,13,14            peak14 (NEVER 15) two-hand slide stalled at 14
  8  6,7,8,10,11,12,13,14,15                 peak15; single 15 then SILENT
  9  11,13,14,1,2,3,5,6,7,8,10,11,12,13,15,14,15   peak15 with anchor-finger jumps (14->1->climb)
 10  15 / 15,14 / 15 / 15                    rests, mostly single report then silent
 11  0,1,2                                   STALLED at 2, never reached end (fast light swipe doesnt register)

## Decisive difference

At **100%**, a resting/held finger keeps emitting end-zone reports (14<->15 micro-movement),
so dwell is observable in the packet stream (>=2 reports over time).

At **0%**, a resting/held finger emits **one** end report and then goes **silent**.
Dwell is NOT observable. sc1 (slide+pause) and sc5 (slide+2s hold) are indistinguishable
from a quick lift by packet content alone.

=> The round-2 "fire on the 2nd end-zone report >=0.8s after entry" mechanism is
   NOT portable to low sensitivity. It only works while micro-movement re-reports exist.

## Other 0% findings

* Fast swipe (sc11) never reached the end (stalled at cell 2): light fast contact does
  not register at low sensitivity. "Quickly swiping to the end" is barely possible at 0%.
* Two-hand slide (sc7) stalled at cell 14, never 15: firing must accept end-zone >=14,
  not require exactly 15.
* Reverse hold time at the end is consistent (sc3: 0.56s @100%, 0.74s @0%).

## Revised design implication

The packet stream cannot separate "resting at end" from "lifted at end" at low
sensitivity, because a still finger is silent. Therefore dwell-by-re-reports must be
replaced by a **silence-tolerant timer**:

  On forward-arrival in the end zone (focal >= numCells-2, having travelled up from
  a low cell), arm a timer. If a reverse (focal drops well below the end zone) occurs
  within REVERSE_WINDOW (~0.8s), cancel. Otherwise, on timer expiry (finger still at
  end OR lifted-and-silent), scroll once.

This is robust to silence and works at both sensitivities. Trade-off: a *fast complete
forward swipe that reaches the last cell* (sc11 @100%) would scroll, because dwell can
no longer veto it. At 0% this is moot (fast swipes do not reach the end).

OPEN DECISION (needs user): should reaching the last cell *reading forward* always
scroll after the no-reverse window, or must the finger additionally linger (dwell),
accepting that lingering is undetectable at low sensitivity?
