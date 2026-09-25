## 2026-09-25 (auto) -- windows-11-arm 20260920.174

* Previous<https://github.com/LeonarddeR/nvda/actions/runs/35206978828>n; served 7/10 arm suites on 2026-09-09 while still flagged prerelease=True)
* Per-suite arm results (image served): chrome_annotations FAIL(20260906.161), startupShutdown FAIL(20260906.161), chrome_table FAIL(20260914.169), chrome_misc_aria FAIL(20260914.169), chrome_roleDescription FAIL(20260906.161), installer FAIL(20260914.169), chrome_list FAIL(20260906.161), chrome_language FAIL(20260906.161), chrome_link FAIL(20260906.161), chrome_misc FAIL(20260906.161), l10n CANCELLED

*
*

*# 2026-09<https://github.com/LeonarddeR/nvda/actions/runs/34375777935>
*

* NOTE: MIXED POOL despite the rollout gate — 7 of 10 suites actually served 20260906.161 (the release still flagged prerelease=True at trigger time and remained prerelease=True after the run), only 3 served the targeted 20260830.155. This is the first time the prerelease flag has visibly LAGGED actual pool rollout rather than leading it; treat prerelease=False as sufficient-but-not-necessary evidence of rollout going forward, not a strict gate — a still-prerelease image can already be partially live.
* Per-suit<https://github.com/LeonarddeR/nvda/actions/runs/33167538282> startupShutdown FAIL(20260830.155), chrome_annotations FAIL(20260906.161), chrome_table FAIL(20260906.161), chrome_misc FAIL(20260830.155), chrome_misc_aria FAIL(20260830.155), chrome_roleDescription FAIL(20260906.161), chrome_list FAIL(20260906.161), chrome_language FAIL(20260906.161), chrome_link FAIL(20260906.161)
*
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on BOTH served images: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (startupShutdown job, 20260830.155, 2026-09-09T16:35:24Z) and "Specific speech did not occur before timeout: NVDA Launcher" (installer job, 20260906.161, 2026-09-09T16:37:05Z)

* UPCOMING<https://github.com/LeonarddeR/nvda/actions/runs/33167538282>6 arm64 image between 2026-09-21 and 2026-09-30 (actions/runner-images issue #14602) — that swap is the next likely point for behaviour to change.


* Previous<https://github.com/LeonarddeR/nvda/actions/runs/33167538282>
* Release status at trigger time: prerelease=False, published 2026-08-24 14:10:51 UTC (3.89 days old at detection)

*

* Branch u<https://github.com/LeonarddeR/nvda/actions/runs/31881422116>ean log); merged origin/master (advanced, 32 commits; brought in a new 11th arm suite: l10n)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/33167538282>
*

* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL, l10n PASS

* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (e.g. startupShutdown job, 2026-08-28T11:53:05Z)
*

*# 2026-08<https://github.com/LeonarddeR/nvda/actions/runs/31881422116> rollout age guard)

* Previous<https://github.com/LeonarddeR/nvda/actions/runs/31363577205>ol was MIXED: 7 suites on 20260727.122, 3 on 20260804.129)

* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/31881422116>

* Result: <https://github.com/LeonarddeR/nvda/actions/runs/31363577205>
* NOTE: all 10 runners SERVED image 20260809.134 — rollout completed in ~3.3 days, faster than the assumed 4-5 days. The 4-day age guard was too conservative here; this was a real test on the new image.

* NOTE: th<https://github.com/LeonarddeR/nvda/actions/runs/31085283637>s on 20260727.122, 3 on 20260804.129). Sampling a single arm job to determine "last tested image" is unreliable during rollout — sample all arm jobs.
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
*
* Assessme<https://github.com/LeonarddeR/nvda/actions/runs/31363577205>heft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
*

* Previous<https://github.com/LeonarddeR/nvda/actions/runs/31085283637>
* Branch update: merged origin/master (advanced); merged leonard/try-testOnArm (prek auto-fix, kept clean log)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/31363577205>
*
* NOTE: runners SERVED image 20260804.129 — the new image HAS now rolled out (previous 2026-08-06 run still got 20260727.122). This is the first real test on 20260804.129.

* Per-suit<https://github.com/LeonarddeR/nvda/actions/runs/31085283637>_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
*# 2026-08<https://github.com/LeonarddeR/nvda/actions/runs/30566465513>
* Previously tested image: 20260727.122
*

* Branch update: merged origin/master (advanced); merged leonard/try-testOnArm (prek auto-fix, kept clean log)
*

* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/31085283637>
* Per-suit<https://github.com/LeonarddeR/nvda/actions/runs/30517046822>3>_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"


*# 2026-07-31 18:37 — windows-11-arm 20260727.122 (retry 2 — rollout lag)

*

* Previously tested image: 20260719.114 (both 2026-07-30 runs for 20260727.122 still got the old image; retrying again)
* Branch update: merged origin/master (advanced); merged leonard/try-testOnArm (prek auto-fix, kept clean log)
* Result: <https://github.com/LeonarddeR/nvda/actions/runs/30517046822>3>

* NOTE: runners served image 20260727.122 — the new image HAS rolled out; this is the first real test on it (both 2026-07-30 runs got 20260719.114 due to rollout lag).

* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL

* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
*

*# 2026-07<https://github.com/LeonarddeR/nvda/actions/runs/29953208083>g)

* Previously tested image: 20260719.114 (runs on 2026-07-30 morning for 20260727.122 still got the old image; retrying now that rollout may have completed)

* Branch u<https://github.com/LeonarddeR/nvda/actions/runs/30084982840>m (prek auto-fix), kept full log
* Result: failure (all 10 windows-11-arm suites failed)

* NOTE: runners STILL served image 20260719.114 — release 20260727.122 (published 2026-07-27) had not rolled out to the hosted win11-arm64 pool as of 2026-07-30 evening. Effectively another re-test on the previous image.

*
* Assessme<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>heft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"


* Previously tested image: 20260719.114
* Branch u<https://github.com/LeonarddeR/nvda/actions/runs/30084982840>ll log) and origin/master (advanced)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/30517046822>

* NOTE: runners served image 20260719.114 — release 20260727.122 (published 2026-07-27) had NOT rolled out to the hosted win11-arm64 pool at run time. Effectively a re-test on the previous image.

* Assessme<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>heft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"

*# 2026-07-24 12:05 — windows-11-arm 20260719.114

* Previous<https://github.com/LeonarddeR/nvda/actions/runs/29953208083>
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/30084982840>
* Result: failure (all 10 windows-11-arm suites failed)

* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
* Branch update: merged leonard/try-testOnArm (prek auto-fix) and origin/master (advanced)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/29953208083>
* Result: failure (6 arm suites failed, 4 cancelled by fail-fast)
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL; chrome_annotations/chrome_language/chrome_roleDescription/chrome_table CANCELLED

* Previously tested image: 20260714.109
* Branch update: merged origin/master (advanced)
* Result: failure (all 10 windows-11-arm suites failed)
* NOTE: runners still served image 20260714.109 — release 20260719.114 exists in actions/runner-images but had not rolled out to the hosted pool at run time. Effectively a re-test on the old image.
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; failures show the known focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
