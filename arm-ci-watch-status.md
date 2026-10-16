## 2026-10-16 (auto) -- windows-11-arm 20261013.183 (win11-vs2026-arm64 family)

* CONFIRMS THE OVERRIDE WAS RIGHT: all 11 windows-11-arm jobs served 20261004.176 cleanly (no mixed pool) despite the release still being flagged prerelease=True (3.85 days old at trigger, age climbed to ~4.2 days by run completion) in the GitHub API at trigger time -- the hosted pool had already fully rolled out. This is now the THIRD time the prerelease flag has lagged real rollout (also 2026-09-09, 2026-09-17); it should no longer be treated as a hard gate once an image clears ~3.3 days old -- check empirically instead of waiting for the flag to flip.

* Per-suite arm results (image served: win11-vs2026-arm64/20261004.176 for all 11 jobs): installer FAIL, chrome_link FAIL, startupShutdown FAIL, chrome_misc_aria FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_table FAIL, chrome_language FAIL, chrome_roleDescription FAIL, chrome_annotations CANCELLED, l10n CANCELLED

*# 2026-10<https://github.com/LeonarddeR/nvda/actions/runs/37052401873>26-arm64 family, post label-swap)
* Release <https://github.com/LeonarddeR/nvda/actions/runs/37052401873>-29 10:20:37 UTC (3.37 days old at detection)
*
* Per-suite arm results (image served: win11-vs2026-arm64/20260924.168 for all 11 jobs, clean rollout, no mixed pool): installer FAIL, chrome_annotations FAIL, startupShutdown FAIL, chrome_list FAIL, chrome_roleDescription FAIL, chrome_misc FAIL, chrome_language FAIL, chrome_misc_aria FAIL, chrome_link FAIL, chrome_table FAIL, l10n CANCELLED
*# 2026-09-25 (auto) -- windows-11-arm 20260920.174

<https://github.com/LeonarddeR/nvda/actions/runs/34375777935>>

* Release status at trigger time: prerelease=False, published 2026-09-21 12:51:45 UTC (3.95 days old at detection)

*<https://github.com/LeonarddeR/nvda/actions/runs/34375777935>>mangled the log again; restored clean version); merged origin/master (advanced, security.md change)


*<https://github.com/LeonarddeR/nvda/actions/runs/34375777935>> VS2026 arm64 label swap window (2026-09-21 to 2026-09-30, actions/runner-images #14602). Watch the served image string closely -- it may report a win11-vs2026-arm64 release instead of win11-arm64 if the swap has already landed.
*

*<https://github.com/LeonarddeR/nvda/actions/runs/34375777935>>206978828>- prerelease flag known to lag rollout)
* Previously tested image: 20260906.161 (confirmed prod as of this run; served 7/10 arm suites on 2026-09-09 while still flagged prerelease=True)

* Release status at trigger time: prerelease=True, published 2026-09-15 15:22 UTC (1.75 days old at detection) -- normally gates, but OVERRIDDEN per user direction: last week proved the prerelease flag can lag actual hosted-pool rollout (20260906.161 was already serving 7/10 suites while still flagged prerelease=True)

*<https://github.com/LeonarddeR/nvda/actions/runs/34375777935>>

* Per-suite arm results (image served): chrome_annotations FAIL(20260906.161), startupShutdown FAIL(20260906.161), chrome_table FAIL(20260914.169), chrome_misc_aria FAIL(20260914.169), chrome_roleDescription FAIL(20260906.161), installer FAIL(20260914.169), chrome_list FAIL(20260906.161), chrome_language FAIL(20260906.161), chrome_link FAIL(20260906.161), chrome_misc FAIL(20260906.161), l10n CANCELLED

* Assessment: #14069 and #14264 STILL APPLY -- both OPEN; same focus-theft signature on BOTH served images: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (startupShutdown job, 20260906.161, 2026-09-17T10:03:45Z) and "Specific speech did not occur before timeout: NVDA Launcher" (installer job, 20260914.169, 2026-09-17T10:04:12Z)

*<https://github.com/LeonarddeR/nvda/actions/runs/34375777935>>
*# 2026-09-09 18:16 — windows-11-arm 20260830.155

* Branch update: merged leonard/try-testOnArm (prek auto-fix mangled the log again; restored clean version); merged origin/master (advanced, 28 commits)


* Result: failure (10 of 10 windows-11-arm suites failed; l10n cancelled)

* NOTE: MIXED POOL despite the rollout gate — 7 of 10 suites actually served 20260906.161 (the release still flagged prerelease=True at trigger time and remained prerelease=True after the run), only 3 served the targeted 20260830.155. This is the first time the prerelease flag has visibly LAGGED actual pool rollout rather than leading it; treat prerelease=False as sufficient-but-not-necessary evidence of rollout going forward, not a strict gate — a still-prerelease image can already be partially live.

* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on BOTH served images: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (startupShutdown job, 20260830.155, 2026-09-09T16:35:24Z) and "Specific speech did not occur before timeout: NVDA Launcher" (installer job, 20260906.161, 2026-09-09T16:37:05Z)
* UPCOMING<https://github.com/LeonarddeR/nvda/actions/runs/33167538282>6 arm64 image between 2026-09-21 and 2026-09-30 (actions/runner-images issue #14602) — that swap is the next likely point for behaviour to change.
*
*# 2026-08-28 13:32 — windows-11-arm 20260823.149

* Previous<https://github.com/LeonarddeR/nvda/actions/runs/31881422116>
* Release status at trigger time: prerelease=False, published 2026-08-24 14:10:51 UTC (3.89 days old at detection)


* Result: failure (10 of 10 known windows-11-arm suites failed; new l10n suite added by the origin/master merge passed)

* Per-suit<https://github.com/LeonarddeR/nvda/actions/runs/31881422116>_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL, l10n PASS
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (e.g. startupShutdown job, 2026-08-28T11:53:05Z)

*<https://github.com/LeonarddeR/nvda/actions/runs/31363577205>
*# 2026-08-15 13:11 — windows-11-arm 20260809.134 (manual override of rollout age guard)
* Rollout age: release 20260809.134 published 2026-08-11 10:48 UTC (3.3 days) — below the 4-day guard; run requested explicitly by the user

* Branch update: merged leonard/try-testOnArm (prek auto-fix, kept clean log); merged origin/master (advanced)
* Result: failure (all 10 windows-11-arm suites failed)
* NOTE: al<https://github.com/LeonarddeR/nvda/actions/runs/31085283637>5>in ~3.3 days, faster than the assumed 4-5 days. The 4-day age guard was too conservative here; this was a real test on the new image.
*<https://github.com/LeonarddeR/nvda/actions/runs/30084982840>>(7 suites on 20260727.122, 3 on 20260804.129). Sampling a single arm job to determine "last tested image" is unreliable during rollout — sample all arm jobs.
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL

* Previously tested image: 20260727.122
* Branch u<https://github.com/LeonarddeR/nvda/actions/runs/30647864308>testOnArm (prek auto-fix, kept clean log)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/31085283637>5>
* Result: failure (all 10 windows-11-arm suites failed)
*<https://github.com/LeonarddeR/nvda/actions/runs/30084982840>>>> now rolled out (previous 2026-08-06 run still got 20260727.122). This is the first real test on 20260804.129.

* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL


*
* Branch u<https://github.com/LeonarddeR/nvda/actions/runs/30647864308>testOnArm (prek auto-fix, kept clean log)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/31085283637>
* Result: failure (all 10 windows-11-arm suites failed)
<<https://github.com/LeonarddeR/nvda/actions/runs/30084982840>>>
* NOTE: runners STILL served image 20260727.122 — release 20260804.129 (published 2026-08-04) had not rolled out to the hosted win11-arm64 pool as of 2026-08-06. Effectively another re-test on the previous image.

* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
*

* Branch update: merged origin/master (advanced); merged leonard/try-testOnArm (prek auto-fix, kept clean log)

* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/30647864308>
* Result: failure (all 10 windows-11-arm suites failed)
* NOTE: runners served image 20260727.122 — the new image HAS rolled out; this is the first real test on it (both 2026-07-30 runs got 20260719.114 due to rollout lag).
*<https://github.com/LeonarddeR/nvda/actions/runs/30084982840>>>>
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
*

* NOTE: runners STILL served image 20260719.114 — release 20260727.122 (published 2026-07-27) had not rolled out to the hosted win11-arm64 pool as of 2026-07-30 evening. Effectively another re-test on the previous image.
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"

*<https://github.com/LeonarddeR/nvda/actions/runs/30084982840>>
*# 2026-07-30 07:35 — windows-11-arm 20260727.122

* Previously tested image: 20260719.114
* Branch u<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>ll log) and origin/master (advanced)

*# 2026-07-24 12:05 — windows-11-arm 20260719.114
* Branch update: merged origin/master (advanced)

* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/30084982840>
* Result: failure (all 10 windows-11-arm suites failed)
* NOTE: runners served image 20260719.114 — the new image HAS rolled out; this is the first real test on it (previous two runs got 20260714.109 due to rollout lag).
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
*

* Previously tested image: 20260714.109
* Branch update: merged origin/master (advanced)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/29764022234>
* Result: failure (all 10 windows-11-arm suites failed)
* NOTE: runners still served image 20260714.109 — release 20260719.114 exists in actions/runner-images but had not rolled out to the hosted pool at run time. Effectively a re-test on the old image.
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; failures show the known focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
