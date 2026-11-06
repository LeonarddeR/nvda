## 2026-11-06 16:03 (auto) -- windows-11-arm 20261101.203 (win11-vs2026-arm64 family)

*
* Per-suite arm results (image served: win11-vs2026-arm64/20261025.196 for all 10 jobs): chrome_list FAIL, startupShutdown FAIL, chrome_annotations FAIL, installer FAIL, chrome_table FAIL, chrome_roleDescription FAIL, chrome_language FAIL, chrome_link FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, l10n CANCELLED
*
* Also not<https://github.com/LeonarddeR/nvda/actions/runs/40076803794> still prerelease=True and skipped in favor of testing the newest release.
* Branch update: merged leonard/try-testOnArm (prek auto-fix mangled the log again; restored clean version); merged origin/master (advanced, incl. installer "ask to end running copies" changes, NVDAHelper UTF-8 compile flag, MathCAT speech fix, voice settings panel tests)
*

* Assessment: #14069 and #14264 STILL APPLY -- both OPEN; same focus-theft signature persists on BOTH newly-served images (20261021.192 and 20261022.194): "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (startupShutdown job, 20261021.192, 2026-10-24T08:26:41Z). No change -- the VS2026 arm64 image line continues to carry the same underlying focus-theft problem across the two newest releases.
*<https://github.com/LeonarddeR/nvda/actions/runs/38900233524>

*# 2026-10-16 (auto) -- windows-11-arm 20261013.183 (win11-vs2026-arm64 family)

* Previously tested image: 20261004.176 (confirmed prod, served all 11 jobs cleanly on 2026-10-09 run 37959306044)

* Release <https://github.com/LeonarddeR/nvda/actions/runs/38900233524>-14 10:24:42 UTC (2.08 days old at detection) -- flag already flipped to rolled-out; no override needed. Flipped faster than the previously observed 3.3-5 day range (worth noting, not blocking, since a False flag has never been observed to lag rollout -- only True has lagged).
*

* Also noted: win11-arm64 (plain, pre-swap family) latest is 20261006.188, also prerelease=False, published same day (2026-10-14) -- not the family windows-11-arm has actually served since the 2026-09-25 VS2026 swap, so not targeted here.

*<https://github.com/LeonarddeR/nvda/actions/runs/37052401873>>900233524>

*


* Result: failure (10 of 10 windows-11-arm suites failed; l10n cancelled)
*<https://github.com/LeonarddeR/nvda/actions/runs/37052401873>>959306044>3 for all 11 jobs, clean rollout, no mixed pool): installer FAIL, chrome_list FAIL, chrome_table FAIL, chrome_misc FAIL, startupShutdown FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_roleDescription FAIL, chrome_link FAIL, chrome_misc_aria FAIL, l10n CANCELLED
<https://github.com/LeonarddeR/nvda/actions/runs/37052401873>>

*<https://github.com/LeonarddeR/nvda/actions/runs/37052401873>>
<https://github.com/LeonarddeR/nvda/actions/runs/37052401873>>
*<https://github.com/LeonarddeR/nvda/actions/runs/37052401873>>rically lags rollout) -- windows-11-arm 20261004.176


* Previous<https://github.com/LeonarddeR/nvda/actions/runs/37959306044>1 jobs cleanly on 2026-10-02 run 37052401873)
*<https://github.com/LeonarddeR/nvda/actions/runs/37052401873>>
*<https://github.com/LeonarddeR/nvda/actions/runs/37052401873>>2026-10-05 16:18:37 UTC (3.81 days old at detection) -- normally gates per the age/prerelease heuristic, but OVERRIDDEN: this log has now recorded the prerelease flag lagging actual hosted-pool rollout on at least two prior occasions (2026-09-09: new image already serving 7/10 suites while still prerelease=True; 2026-09-17: new image already serving 3/10 suites at only 1.75 days old, still prerelease=True) against a fastest-observed full rollout of 3.3 days. At 3.81 days old, 20261004.176 is already past that fastest-case mark, so waiting on the flag risked sitting on stale data another week. User confirmed this override live in chat on 2026-10-09.
*<https://github.com/LeonarddeR/nvda/actions/runs/37052401873>>ublished same day, also still prerelease=True -- not the family the windows-11-arm label has actually been serving since the 2026-09-25 VS2026 swap, so not targeted here.
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/37959306044>
*<https://github.com/LeonarddeR/nvda/actions/runs/37052401873>>
*<https://github.com/LeonarddeR/nvda/actions/runs/37052401873>>me_annotations and l10n cancelled)
* CONFIRMS THE OVERRIDE WAS RIGHT: all 11 windows-11-arm jobs served 20261004.176 cleanly (no mixed pool) despite the release still being flagged prerelease=True (3.85 days old at trigger, age climbed to ~4.2 days by run completion) in the GitHub API at trigger time -- the hosted pool had already fully rolled out. This is now the THIRD time the prerelease flag has lagged real rollout (also 2026-09-09, 2026-09-17); it should no longer be treated as a hard gate once an image clears ~3.3 days old -- check empirically instead of waiting for the flag to flip.
* Per-suit<https://github.com/LeonarddeR/nvda/actions/runs/36131144605>6 for all 11 jobs): installer FAIL, chrome_link FAIL, startupShutdown FAIL, chrome_misc_aria FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_table FAIL, chrome_language FAIL, chrome_roleDescription FAIL, chrome_annotations CANCELLED, l10n CANCELLED
*
* Assessment: #14069 and #14264 STILL APPLY -- both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (startupShutdown job, 2026-10-09T16:49:48Z). No change -- the VS2026 arm64 image line continues to carry the same underlying focus-theft problem across releases.

*# 2026-10-02 21:10 (auto) -- windows-11-arm 20260924.168 (win11-vs2026-arm64 family, post label-swap)

* Previously tested image: 20260920.164 (win11-vs2026-arm64; confirmed prod, served all 10 arm suites in the 2026-09-25 run)
* Release <https://github.com/LeonarddeR/nvda/actions/runs/36131144605>-29 10:20:37 UTC (3.37 days old at detection)

*
* Branch update: merged leonard/try-testOnArm (prek auto-fix mangled the log again; restored clean version); merged origin/master (advanced, large commit batch incl. word comment reporting fix)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/35206978828>3>
* Result: failure (10 of 10 windows-11-arm suites failed; l10n cancelled)

* Per-suite arm results (image served: win11-vs2026-arm64/20260924.168 for all 11 jobs, clean rollout, no mixed pool): installer FAIL, chrome_annotations FAIL, startupShutdown FAIL, chrome_list FAIL, chrome_roleDescription FAIL, chrome_misc FAIL, chrome_language FAIL, chrome_misc_aria FAIL, chrome_link FAIL, chrome_table FAIL, l10n CANCELLED

* Assessme<https://github.com/LeonarddeR/nvda/actions/runs/36131144605>theft signature persists on the new VS2026 arm64 image 20260924.168: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (startupShutdown job, 2026-10-02T19:32:39Z). No change from the 2026-09-25 run on 20260920.164/174 -- the VS2026 arm64 label swap has not affected the underlying focus-theft problem.
*

*# 2026-09-25 (auto) -- windows-11-arm 20260920.174

* Previous<https://github.com/LeonarddeR/nvda/actions/runs/35206978828>last run); 20260914.169 partially served (3/10) under manual override, not yet confirmed as prod on its own

* Release status at trigger time: prerelease=False, published 2026-09-21 12:51:45 UTC (3.95 days old at detection)
* Branch u<https://github.com/LeonarddeR/nvda/actions/runs/34375777935>the log again; restored clean version); merged origin/master (advanced, security.md change)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/36131144605>
* Result: failure (10 of 10 windows-11-arm suites failed; l10n cancelled)

*

* Per-suite arm results (image served: win11-vs2026-arm64/20260920.164 for all): installer FAIL, chrome_annotations FAIL, startupShutdown FAIL, chrome_list FAIL, chrome_misc_aria FAIL, chrome_link FAIL, chrome_language FAIL, chrome_misc FAIL, chrome_table FAIL, chrome_roleDescription FAIL, l10n CANCELLED

* NOTE: this run falls inside the announced windows-11-arm -> VS2026 arm64 label swap window (2026-09-21 to 2026-09-30, actions/runner-images #14602). Watch the served image string closely -- it may report a win11-vs2026-arm64 release instead of win11-arm64 if the swap has already landed.
*
*# 2026-09<https://github.com/LeonarddeR/nvda/actions/runs/34375777935>- prerelease flag known to lag rollout)

* Previously tested image: 20260906.161 (confirmed prod as of this run; served 7/10 arm suites on 2026-09-09 while still flagged prerelease=True)
* Release <https://github.com/LeonarddeR/nvda/actions/runs/33167538282>15 15:22 UTC (1.75 days old at detection) -- normally gates, but OVERRIDDEN per user direction: last week proved the prerelease flag can lag actual hosted-pool rollout (20260906.161 was already serving 7/10 suites while still flagged prerelease=True)

* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/35206978828>


* Result: failure (10 of 10 windows-11-arm suites failed; l10n cancelled)
* CONFIRMS THE OVERRIDE WAS RIGHT: pool was already MIXED at 1.75-2 days old and still prerelease=True -- 3 of 10 suites served the new 20260914.169, 7 of 10 still served 20260906.161. This is the second consecutive week the prerelease flag has visibly lagged actual pool rollout (also seen 2026-09-09). Treat prerelease as a soft signal only -- worth checking a fresh release even while still marked prerelease=True, not waiting for the flag to flip.

*

*# 2026-09-09 18:16 — windows-11-arm 20260830.155
*
*


<https://github.com/LeonarddeR/nvda/actions/runs/30647864308>>

* Result: <https://github.com/LeonarddeR/nvda/actions/runs/31363577205>led)
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on BOTH served images: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (startupShutdown job, 20260830.155, 2026-09-09T16:35:24Z) and "Specific speech did not occur before timeout: NVDA Launcher" (installer job, 20260906.161, 2026-09-09T16:37:05Z)
* UPCOMING: GitHub is switching the windows-11-arm label to the VS2026 arm64 image between 2026-09-21 and 2026-09-30 (actions/runner-images issue #14602) — that swap is the next likely point for behaviour to change.


*# 2026-08<https://github.com/LeonarddeR/nvda/actions/runs/31085283637>
<https://github.com/LeonarddeR/nvda/actions/runs/30647864308>>


* Release status at trigger time: prerelease=False, published 2026-08-24 14:10:51 UTC (3.89 days old at detection)

* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/31881422116>2>
* Result: failure (10 of 10 known windows-11-arm suites failed; new l10n suite added by the origin/master merge passed)
*<https://github.com/LeonarddeR/nvda/actions/runs/30647864308>>
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (e.g. startupShutdown job, 2026-08-28T11:53:05Z)
*


*<https://github.com/LeonarddeR/nvda/actions/runs/30647864308>>085283637> rollout age guard)

* Previously tested image: 20260727.122 / 20260804.129 (2026-08-10 pool was MIXED: 7 suites on 20260727.122, 3 on 20260804.129)


*
* NOTE: all 10 runners SERVED image 20260809.134 — rollout completed in ~3.3 days, faster than the assumed 4-5 days. The 4-day age guard was too conservative here; this was a real test on the new image.


*<https://github.com/LeonarddeR/nvda/actions/runs/30647864308>>

* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL

*<https://github.com/LeonarddeR/nvda/actions/runs/30647864308>> focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"

*# 2026-08<https://github.com/LeonarddeR/nvda/actions/runs/31085283637>

* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/31363577205>
* Result: <https://github.com/LeonarddeR/nvda/actions/runs/30566465513>

* NOTE: ru<https://github.com/LeonarddeR/nvda/actions/runs/30084982840>led out (previous 2026-08-06 run still got 20260727.122). This is the first real test on 20260804.129.

* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL

* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
*
*<https://github.com/LeonarddeR/nvda/actions/runs/30647864308>>
*# 2026-08-06 10:31 — windows-11-arm 20260804.129

* Previously tested image: 20260727.122
* Branch u<https://github.com/LeonarddeR/nvda/actions/runs/30517046822>testOnArm (prek auto-fix, kept clean log)
* Result: failure (all 10 windows-11-arm suites failed)

* NOTE: runners STILL served image 20260727.122 — release 20260804.129 (published 2026-08-04) had not rolled out to the hosted win11-arm64 pool as of 2026-08-06. Effectively another re-test on the previous image.


*

*# 2026-07<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>0>lag)

*


* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/30647864308>

* Result: failure (all 10 windows-11-arm suites failed)
* NOTE: runners served image 20260727.122 — the new image HAS rolled out; this is the first real test on it (both 2026-07-30 runs got 20260719.114 due to rollout lag).
*
*# 2026-07-30 19:32 — windows-11-arm 20260727.122 (retry — rollout lag)


* Branch update: no origin/master change; merged leonard/try-testOnArm (prek auto-fix), kept full log
* NOTE: ru<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>0>2 (published 2026-07-27) had not rolled out to the hosted win11-arm64 pool as of 2026-07-30 evening. Effectively another re-test on the previous image.

* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
* Result: <https://github.com/LeonarddeR/nvda/actions/runs/29953208083>
* NOTE: runners served image 20260719.114 — release 20260727.122 (published 2026-07-27) had NOT rolled out to the hosted win11-arm64 pool at run time. Effectively a re-test on the previous image.
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"

*

## 2026-07-24 12:05 — windows-11-arm 20260719.114
* Previously tested image: 20260714.109
* Branch update: merged origin/master (advanced)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/29764022234>0>
* Result: failure (all 10 windows-11-arm suites failed)
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
## 2026-07-22 21:58 — windows-11-arm 20260719.114 (retry — rollout lag)

* Result: failure (6 arm suites failed, 4 cancelled by fail-fast)
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL; chrome_annotations/chrome_language/chrome_roleDescription/chrome_table CANCELLED
## 2026-07-20 19:58 — windows-11-arm 20260719.114

* Previously tested image: 20260714.109
* Branch update: merged origin/master (advanced)
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; failures show the known focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
