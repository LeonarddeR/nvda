## 2026-10-02 21:10 (auto) -- windows-11-arm 20260924.168 (win11-vs2026-arm64 family, post label-swap)


*


*# 2026-09<https://github.com/LeonarddeR/nvda/actions/runs/35206978828>- prerelease flag known to lag rollout)

* Result: failure (10 of 10 windows-11-arm suites failed; l10n cancelled)
*
* CONFIRMS THE OVERRIDE WAS RIGHT: pool was already MIXED at 1.75-2 days old and still prerelease=True -- 3 of 10 suites served the new 20260914.169, 7 of 10 still served 20260906.161. This is the second consecutive week the prerelease flag has visibly lagged actual pool rollout (also seen 2026-09-09). Treat prerelease as a soft signal only -- worth checking a fresh release even while still marked prerelease=True, not waiting for the flag to flip.
* Per-suit<https://github.com/LeonarddeR/nvda/actions/runs/34375777935>906.161), startupShutdown FAIL(20260906.161), chrome_table FAIL(20260914.169), chrome_misc_aria FAIL(20260914.169), chrome_roleDescription FAIL(20260906.161), installer FAIL(20260914.169), chrome_list FAIL(20260906.161), chrome_language FAIL(20260906.161), chrome_link FAIL(20260906.161), chrome_misc FAIL(20260906.161), l10n CANCELLED

*
* Assessment: #14069 and #14264 STILL APPLY -- both OPEN; same focus-theft signature on BOTH served images: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (startupShutdown job, 20260906.161, 2026-09-17T10:03:45Z) and "Specific speech did not occur before timeout: NVDA Launcher" (installer job, 20260914.169, 2026-09-17T10:04:12Z)
* UPCOMING<https://github.com/LeonarddeR/nvda/actions/runs/34375777935>6 arm64 image between 2026-09-21 and 2026-09-30 (actions/runner-images issue #14602) -- that swap is the next likely point for behaviour to change; it is close now, watch for it next run.

*# 2026-09-09 18:16 — windows-11-arm 20260830.155
<https://github.com/LeonarddeR/nvda/actions/runs/31881422116>>

* Previous<https://github.com/LeonarddeR/nvda/actions/runs/34375777935>
* Release status at trigger time: prerelease=False, published 2026-09-01 12:13:50 UTC (rolled out; a newer release 20260906.161 also existed, still marked prerelease=True, 1.3 days old, published 2026-09-08 - skipped per rollout gate)
* Branch update: merged leonard/try-testOnArm (prek auto-fix mangled the log again; restored clean version); merged origin/master (advanced, 28 commits)

*<https://github.com/LeonarddeR/nvda/actions/runs/31881422116>>
*<https://github.com/LeonarddeR/nvda/actions/runs/31881422116>>167538282>5>

* NOTE: MIXED POOL despite the rollout gate — 7 of 10 suites actually served 20260906.161 (the release still flagged prerelease=True at trigger time and remained prerelease=True after the run), only 3 served the targeted 20260830.155. This is the first time the prerelease flag has visibly LAGGED actual pool rollout rather than leading it; treat prerelease=False as sufficient-but-not-necessary evidence of rollout going forward, not a strict gate — a still-prerelease image can already be partially live.
*

<https://github.com/LeonarddeR/nvda/actions/runs/31881422116>>
*<https://github.com/LeonarddeR/nvda/actions/runs/31881422116>>167538282> startupShutdown FAIL(20260830.155), chrome_annotations FAIL(20260906.161), chrome_table FAIL(20260906.161), chrome_misc FAIL(20260830.155), chrome_misc_aria FAIL(20260830.155), chrome_roleDescription FAIL(20260906.161), chrome_list FAIL(20260906.161), chrome_language FAIL(20260906.161), chrome_link FAIL(20260906.161)

<https://github.com/LeonarddeR/nvda/actions/runs/31881422116>>

* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on BOTH served images: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (startupShutdown job, 20260830.155, 2026-09-09T16:35:24Z) and "Specific speech did not occur before timeout: NVDA Launcher" (installer job, 20260906.161, 2026-09-09T16:37:05Z)
* UPCOMING: GitHub is switching the windows-11-arm label to the VS2026 arm64 image between 2026-09-21 and 2026-09-30 (actions/runner-images issue #14602) — that swap is the next likely point for behaviour to change.

<https://github.com/LeonarddeR/nvda/actions/runs/31881422116>>

*<https://github.com/LeonarddeR/nvda/actions/runs/31881422116>>167538282>

*<https://github.com/LeonarddeR/nvda/actions/runs/31881422116>>

* Previously tested image: 20260809.134
* Branch update: merged leonard/try-testOnArm (prek auto-fix, kept clean log); merged origin/master (advanced, 32 commits; brought in a new 11th arm suite: l10n)
*<https://github.com/LeonarddeR/nvda/actions/runs/31881422116>>167538282>



* Result: failure (10 of 10 known windows-11-arm suites failed; new l10n suite added by the origin/master merge passed)
* NOTE: all 11 windows-11-arm jobs SERVED image 20260823.149 (clean rollout, no mixed pool) — confirms the prerelease flag flipped to false around 2026-08-27/28, roughly 3.9 days after publication (2026-08-24), consistent with the 3.3-5 day rollout window observed previously.
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL, l10n PASS
* Assessme<https://github.com/LeonarddeR/nvda/actions/runs/31363577205>heft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (e.g. startupShutdown job, 2026-08-28T11:53:05Z)
*
*# 2026-08-15 13:11 — windows-11-arm 20260809.134 (manual override of rollout age guard)

* Previously tested image: 20260727.122 / 20260804.129 (2026-08-10 pool was MIXED: 7 suites on 20260727.122, 3 on 20260804.129)



*<https://github.com/LeonarddeR/nvda/actions/runs/31085283637>
* Result: failure (all 10 windows-11-arm suites failed)
* NOTE: all 10 runners SERVED image 20260809.134 — rollout completed in ~3.3 days, faster than the assumed 4-5 days. The 4-day age guard was too conservative here; this was a real test on the new image.

* NOTE: the 2026-08-10 run (31363577205) ran on a MIXED pool (7 suites on 20260727.122, 3 on 20260804.129). Sampling a single arm job to determine "last tested image" is unreliable during rollout — sample all arm jobs.
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
*<https://github.com/LeonarddeR/nvda/actions/runs/31085283637>
*# 2026-08<https://github.com/LeonarddeR/nvda/actions/runs/30647864308>



* Branch update: merged origin/master (advanced); merged leonard/try-testOnArm (prek auto-fix, kept clean log)
*

* NOTE: ru<https://github.com/LeonarddeR/nvda/actions/runs/31085283637>led out (previous 2026-08-06 run still got 20260727.122). This is the first real test on 20260804.129.

* Per-suit<https://github.com/LeonarddeR/nvda/actions/runs/30566465513>8>_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL


*
*

*<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>>

* Branch update: merged origin/master (advanced); merged leonard/try-testOnArm (prek auto-fix, kept clean log)

* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/30517046822>7>

* Result: <https://github.com/LeonarddeR/nvda/actions/runs/30566465513>8>
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"

*

*<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>>>>
*


*# 2026-07<https://github.com/LeonarddeR/nvda/actions/runs/30084982840>lag)

* Previously tested image: 20260719.114 (both 2026-07-30 runs for 20260727.122 still got the old image; retrying again)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/30566465513>8>
* NOTE: runners served image 20260727.122 — the new image HAS rolled out; this is the first real test on it (both 2026-07-30 runs got 20260719.114 due to rollout lag).
*<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>>>>, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
*
* Assessme<https://github.com/LeonarddeR/nvda/actions/runs/29953208083>heft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
*


*


*# 2026-07<https://github.com/LeonarddeR/nvda/actions/runs/30084982840>g)

* Result: failure (all 10 windows-11-arm suites failed)
*

*

*# 2026-07-30 07:35 — windows-11-arm 20260727.122


* Previous<https://github.com/LeonarddeR/nvda/actions/runs/30084982840>
* Branch update: merged leonard/try-testOnArm (prek auto-fix, kept full log) and origin/master (advanced)


*<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>>
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Previously tested image: 20260714.109
* Result: failure (all 10 windows-11-arm suites failed)

* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
*<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>>
* Previously tested image: 20260714.109 (run on 2026-07-20 for 20260719.114 still got the old image; retrying now that rollout may have completed)
* Branch update: merged leonard/try-testOnArm (prek auto-fix) and origin/master (advanced)

* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/29953208083>
* Result: failure (6 arm suites failed, 4 cancelled by fail-fast)
* NOTE: runners AGAIN served image 20260714.109 — release 20260719.114 (published 2026-07-19) still not rolled out to the hosted win11-arm64 pool as of 2026-07-22.
## 2026-07-20 19:58 — windows-11-arm 20260719.114

* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; failures show the known focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"