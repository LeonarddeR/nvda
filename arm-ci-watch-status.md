## 2026-11-21 09:41 (auto) -- windows-11-arm 20261115.219 (win11-vs2026-arm64 family)


*


*# 2026-11<https://github.com/LeonarddeR/nvda/actions/runs/42248974511>26-arm64 family)

* Result: failure (10 of 10 windows-11-arm suites failed; l10n cancelled)
* Image se<https://github.com/LeonarddeR/nvda/actions/runs/41058653164>clean rollout, no mixed pool, no anomaly -- matched the targeted release exactly)
*
* Per-suite arm results: chrome_list FAIL, chrome_language FAIL, chrome_annotations FAIL, installer FAIL, chrome_table FAIL, chrome_misc_aria FAIL, startupShutdown FAIL, chrome_misc FAIL, chrome_roleDescription FAIL, chrome_link FAIL, l10n CANCELLED

* Assessme<https://github.com/LeonarddeR/nvda/actions/runs/41058653164>theft signature persists on the new image 20261101.203: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (startupShutdown job, 2026-11-06T16:22:48Z onward). No change -- the VS2026 arm64 image line continues to carry the same underlying focus-theft problem across this newest release.

*# 2026-10-30 13:52 (auto) -- windows-11-arm 20261026.197 (win11-vs2026-arm64 family)
* Previous<https://github.com/LeonarddeR/nvda/actions/runs/41058653164>onfirmed on 2026-10-24 run 40076803794: 8 of 10 suites + l10n served 20261021.192, 2 of 10 served 20261022.194; both now prerelease=False)
* Release status at trigger time: prerelease=False, published 2026-10-27 08:31:56 UTC (3.18 days old at detection) -- already flagged as rolled out, no override needed

*
* Branch update: merged leonard/try-testOnArm (prek auto-fix mangled the log again; restored clean version); merged origin/master (advanced, 19 commits)

* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/40076803794>4>
*
<https://github.com/LeonarddeR/nvda/actions/runs/37959306044>>


* Per-suit<https://github.com/LeonarddeR/nvda/actions/runs/40076803794>6 for all 10 jobs): chrome_list FAIL, startupShutdown FAIL, chrome_annotations FAIL, installer FAIL, chrome_table FAIL, chrome_roleDescription FAIL, chrome_language FAIL, chrome_link FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, l10n CANCELLED
* Assessment: #14069 and #14264 STILL APPLY -- both OPEN; same focus-theft signature persists on the new (unreleased-but-served) image 20261025.196: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (startupShutdown job, 2026-10-30T13:12:38Z / 13:13:10Z). No change -- the VS2026 arm64 image line continues to carry the same underlying focus-theft problem.
*

<<https://github.com/LeonarddeR/nvda/actions/runs/37959306044>>>
*# 2026-10-24 (auto, manual override -- user requested this run live despite image still prerelease) -- windows-11-arm 20261022.194
*


* Release status at trigger time: prerelease=True, published 2026-10-23 15:44:44 UTC (0.68 days old at detection) -- far below the ~3.3-day mark this log has used to justify overriding the prerelease flag before; normally this would gate (skip). OVERRIDDEN ANYWAY: user explicitly asked live in chat to run now rather than wait for rollout. Risk flagged: at well under a day old this image is very likely still deploying, so the hosted pool may still serve the old 20261013.183 image instead -- watch the served-image sample closely.
*

* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/38900233524>4> (first attempt 2026-10-24T08:07 failed at Build NVDA / Install Python step with an unrelated runner infra flake before any arm system tests ran -- re-ran failed jobs only via `gh run rerun --failed`, same run id, same commit; no new commit needed)

* Result: failure (10 of 10 windows-11-arm suites failed; l10n cancelled) -- MIXED POOL: 2 of 10 ran suites served the brand-new 20261022.194 (0.68 days old at trigger, still prerelease=True), the other 8 (plus the cancelled l10n job) served 20261021.192 (1.9 days old at trigger, also still prerelease=True). CONFIRMS THE OVERRIDE WAS RIGHT (4th such confirmation, after 2026-09-09/09-17/10-09): both of the newest VS2026 arm64 releases were already live on the hosted pool well before their prerelease flag flipped to false -- 20261021.192 at under 2 days old, 20261022.194 at under 1 day old. The gap between "prerelease=True" and "actually serving" keeps shrinking; treat the flag as unreliable going forward rather than a hard gate, per user's live override this run.
* Per-suite arm results (image served noted per suite): installer FAIL (20261021.192), chrome_table FAIL (20261021.192), chrome_annotations FAIL (20261021.192), chrome_list FAIL (20261021.192), chrome_language FAIL (20261022.194), startupShutdown FAIL (20261021.192), chrome_roleDescription FAIL (20261021.192), chrome_link FAIL (20261022.194), chrome_misc_aria FAIL (20261021.192), chrome_misc FAIL (20261021.192), l10n CANCELLED (20261021.192)
*<https://github.com/LeonarddeR/nvda/actions/runs/37959306044>>e focus-theft signature persists on BOTH newly-served images (20261021.192 and 20261022.194): "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (startupShutdown job, 20261021.192, 2026-10-24T08:26:41Z). No change -- the VS2026 arm64 image line continues to carry the same underlying focus-theft problem across the two newest releases.
*<https://github.com/LeonarddeR/nvda/actions/runs/37959306044>>>>


*# 2026-10<https://github.com/LeonarddeR/nvda/actions/runs/38900233524>64 family)
*<https://github.com/LeonarddeR/nvda/actions/runs/37959306044>>

* Branch update: merged leonard/try-testOnArm (prek auto-fix mangled the log again; restored clean version); merged origin/master (advanced, incl. UIAHandler/comInterfaces TOM2 change, braille display gesture priority fix, winBindings icu test)

* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/38900233524>
* Result: <https://github.com/LeonarddeR/nvda/actions/runs/37052401873>led)
* Per-suite arm results (image served: win11-vs2026-arm64/20261013.183 for all 11 jobs, clean rollout, no mixed pool): installer FAIL, chrome_list FAIL, chrome_table FAIL, chrome_misc FAIL, startupShutdown FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_roleDescription FAIL, chrome_link FAIL, chrome_misc_aria FAIL, l10n CANCELLED
*




*<https://github.com/LeonarddeR/nvda/actions/runs/37959306044>>
*
* Branch update: merged leonard/try-testOnArm (prek auto-fix mangled the log again; restored clean version); merged origin/master (advanced, 19 commits incl. brlapi bindings update, CLI loglevel fix)


*
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/37959306044>

* Result: failure (9 of 10 windows-11-arm suites failed; chrome_annotations and l10n cancelled)
* CONFIRMS THE OVERRIDE WAS RIGHT: all 11 windows-11-arm jobs served 20261004.176 cleanly (no mixed pool) despite the release still being flagged prerelease=True (3.85 days old at trigger, age climbed to ~4.2 days by run completion) in the GitHub API at trigger time -- the hosted pool had already fully rolled out. This is now the THIRD time the prerelease flag has lagged real rollout (also 2026-09-09, 2026-09-17); it should no longer be treated as a hard gate once an image clears ~3.3 days old -- check empirically instead of waiting for the flag to flip.
* Assessme<https://github.com/LeonarddeR/nvda/actions/runs/36131144605>theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (startupShutdown job, 2026-10-09T16:49:48Z). No change -- the VS2026 arm64 image line continues to carry the same underlying focus-theft problem across releases.
*# 2026-10-02 21:10 (auto) -- windows-11-arm 20260924.168 (win11-vs2026-arm64 family, post label-swap)
*

* Previously tested image: 20260920.164 (win11-vs2026-arm64; confirmed prod, served all 10 arm suites in the 2026-09-25 run)
* Release status at trigger time: prerelease=False, published 2026-09-29 10:20:37 UTC (3.37 days old at detection)

* Branch update: merged leonard/try-testOnArm (prek auto-fix mangled the log again; restored clean version); merged origin/master (advanced, large commit batch incl. word comment reporting fix)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/37052401873>

* Result: <https://github.com/LeonarddeR/nvda/actions/runs/36131144605>led)
*

*# 2026-09-25 (auto) -- windows-11-arm 20260920.174
*
* Previously tested image: 20260906.161 (confirmed prod, majority of last run); 20260914.169 partially served (3/10) under manual override, not yet confirmed as prod on its own
*

* Release status at trigger time: prerelease=False, published 2026-09-21 12:51:45 UTC (3.95 days old at detection)

* Branch update: merged leonard/try-testOnArm (prek auto-fix mangled the log again; restored clean version); merged origin/master (advanced, security.md change)
* Result: <https://github.com/LeonarddeR/nvda/actions/runs/35206978828>led)
* Per-suit<https://github.com/LeonarddeR/nvda/actions/runs/33167538282>5>4 for all): installer FAIL, chrome_annotations FAIL, startupShutdown FAIL, chrome_list FAIL, chrome_misc_aria FAIL, chrome_link FAIL, chrome_language FAIL, chrome_misc FAIL, chrome_table FAIL, chrome_roleDescription FAIL, l10n CANCELLED
* NOTE: this run falls inside the announced windows-11-arm -> VS2026 arm64 label swap window (2026-09-21 to 2026-09-30, actions/runner-images #14602). Watch the served image string closely -- it may report a win11-vs2026-arm64 release instead of win11-arm64 if the swap has already landed.
*

*# 2026-09-17 11:46 -- windows-11-arm 20260914.169 (manual override -- prerelease flag known to lag rollout)

*
* Previously tested image: 20260906.161 (confirmed prod as of this run; served 7/10 arm suites on 2026-09-09 while still flagged prerelease=True)

* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/35206978828>
* Result: <https://github.com/LeonarddeR/nvda/actions/runs/33167538282>5>led)
* CONFIRMS THE OVERRIDE WAS RIGHT: pool was already MIXED at 1.75-2 days old and still prerelease=True -- 3 of 10 suites served the new 20260914.169, 7 of 10 still served 20260906.161. This is the second consecutive week the prerelease flag has visibly lagged actual pool rollout (also seen 2026-09-09). Treat prerelease as a soft signal only -- worth checking a fresh release even while still marked prerelease=True, not waiting for the flag to flip.
* Assessment: #14069 and #14264 STILL APPLY -- both OPEN; same focus-theft signature on BOTH served images: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (startupShutdown job, 20260906.161, 2026-09-17T10:03:45Z) and "Specific speech did not occur before timeout: NVDA Launcher" (installer job, 20260914.169, 2026-09-17T10:04:12Z)

*

*<https://github.com/LeonarddeR/nvda/actions/runs/31363577205>

* Release <https://github.com/LeonarddeR/nvda/actions/runs/31881422116>-01 12:13:50 UTC (rolled out; a newer release 20260906.161 also existed, still marked prerelease=True, 1.3 days old, published 2026-09-08 - skipped per rollout gate)
* Branch update: merged leonard/try-testOnArm (prek auto-fix mangled the log again; restored clean version); merged origin/master (advanced, 28 commits)



* Per-suit<https://github.com/LeonarddeR/nvda/actions/runs/31085283637> startupShutdown FAIL(20260830.155), chrome_annotations FAIL(20260906.161), chrome_table FAIL(20260906.161), chrome_misc FAIL(20260830.155), chrome_misc_aria FAIL(20260830.155), chrome_roleDescription FAIL(20260906.161), chrome_list FAIL(20260906.161), chrome_language FAIL(20260906.161), chrome_link FAIL(20260906.161)
*
* UPCOMING: GitHub is switching the windows-11-arm label to the VS2026 arm64 image between 2026-09-21 and 2026-09-30 (actions/runner-images issue #14602) — that swap is the next likely point for behaviour to change.
*<https://github.com/LeonarddeR/nvda/actions/runs/31363577205>

*# 2026-08-28 13:32 — windows-11-arm 20260823.149
* Branch update: merged leonard/try-testOnArm (prek auto-fix, kept clean log); merged origin/master (advanced, 32 commits; brought in a new 11th arm suite: l10n)
*
* Result: failure (10 of 10 known windows-11-arm suites failed; new l10n suite added by the origin/master merge passed)
* NOTE: all 11 windows-11-arm jobs SERVED image 20260823.149 (clean rollout, no mixed pool) — confirms the prerelease flag flipped to false around 2026-08-27/28, roughly 3.9 days after publication (2026-08-24), consistent with the 3.3-5 day rollout window observed previously.
* Assessme<https://github.com/LeonarddeR/nvda/actions/runs/30566465513>heft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (e.g. startupShutdown job, 2026-08-28T11:53:05Z)
*
*

* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/30647864308>6>
* Result: <https://github.com/LeonarddeR/nvda/actions/runs/30517046822>
*
* NOTE: all 10 runners SERVED image 20260809.134 — rollout completed in ~3.3 days, faster than the assumed 4-5 days. The 4-day age guard was too conservative here; this was a real test on the new image.
* NOTE: the 2026-08-10 run (31363577205) ran on a MIXED pool (7 suites on 20260727.122, 3 on 20260804.129). Sampling a single arm job to determine "last tested image" is unreliable during rollout — sample all arm jobs.

*

*# 2026-08<https://github.com/LeonarddeR/nvda/actions/runs/30084982840>3>

* Branch update: merged origin/master (advanced); merged leonard/try-testOnArm (prek auto-fix, kept clean log)
*

* Per-suit<https://github.com/LeonarddeR/nvda/actions/runs/29953208083>8>_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessme<https://github.com/LeonarddeR/nvda/actions/runs/30517046822>heft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
*# 2026-08-06 10:31 — windows-11-arm 20260804.129
*

*
* NOTE: ru<https://github.com/LeonarddeR/nvda/actions/runs/30084982840>3>9 (published 2026-08-04) had not rolled out to the hosted win11-arm64 pool as of 2026-08-06. Effectively another re-test on the previous image.
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL

* Previously tested image: 20260719.114 (both 2026-07-30 runs for 20260727.122 still got the old image; retrying again)
* Branch update: merged origin/master (advanced); merged leonard/try-testOnArm (prek auto-fix, kept clean log)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/29953208083>8>
* NOTE: runners served image 20260727.122 — the new image HAS rolled out; this is the first real test on it (both 2026-07-30 runs got 20260719.114 due to rollout lag).

* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL


* Branch update: no origin/master change; merged leonard/try-testOnArm (prek auto-fix), kept full log
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/30084982840>3>
* NOTE: runners STILL served image 20260719.114 — release 20260727.122 (published 2026-07-27) had not rolled out to the hosted win11-arm64 pool as of 2026-07-30 evening. Effectively another re-test on the previous image.
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL

* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"

* Previously tested image: 20260719.114
* Branch u<https://github.com/LeonarddeR/nvda/actions/runs/29953208083>ll log) and origin/master (advanced)


*# 2026-07-24 12:05 — windows-11-arm 20260719.114
* Previous<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
* Previously tested image: 20260714.109 (run on 2026-07-20 for 20260719.114 still got the old image; retrying now that rollout may have completed)
* Result: failure (6 arm suites failed, 4 cancelled by fail-fast)
* NOTE: runners AGAIN served image 20260714.109 — release 20260719.114 (published 2026-07-19) still not rolled out to the hosted win11-arm64 pool as of 2026-07-22.
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL; chrome_annotations/chrome_language/chrome_roleDescription/chrome_table CANCELLED
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"

## 2026-07-20 19:58 — windows-11-arm 20260719.114

* Previously tested image: 20260714.109
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/29764022234>
* Result: failure (all 10 windows-11-arm suites failed)
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL