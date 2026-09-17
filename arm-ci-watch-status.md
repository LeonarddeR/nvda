## 2026-09-17 11:46 -- windows-11-arm 20260914.169 (manual override -- prerelease flag known to lag rollout)

* Per-suite arm results (image served): installer FAIL(20260906.161), startupShutdown FAIL(20260830.155), chrome_annotations FAIL(20260906.161), chrome_table FAIL(20260906.161), chrome_misc FAIL(20260830.155), chrome_misc_aria FAIL(20260830.155), chrome_roleDescription FAIL(20260906.161), chrome_list FAIL(20260906.161), chrome_language FAIL(20260906.161), chrome_link FAIL(20260906.161)

*
*

*# 2026-08<https://github.com/LeonarddeR/nvda/actions/runs/33167538282>
*

* Result: failure (10 of 10 known windows-11-arm suites failed; new l10n suite added by the origin/master merge passed)
* NOTE: al<https://github.com/LeonarddeR/nvda/actions/runs/31881422116>ollout, no mixed pool) — confirms the prerelease flag flipped to false around 2026-08-27/28, roughly 3.9 days after publication (2026-08-24), consistent with the 3.3-5 day rollout window observed previously.
*<https://github.com/LeonarddeR/nvda/actions/runs/31363577205>>
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL, l10n PASS
* Assessme<https://github.com/LeonarddeR/nvda/actions/runs/31881422116>heft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (e.g. startupShutdown job, 2026-08-28T11:53:05Z)
*

*<https://github.com/LeonarddeR/nvda/actions/runs/31363577205>>rride of rollout age guard)


* Previous<https://github.com/LeonarddeR/nvda/actions/runs/31881422116>ol was MIXED: 7 suites on 20260727.122, 3 on 20260804.129)
*<https://g>github.com/LeonarddeR/nvda/actions/runs/31363577205>> kept clean log); merged origin/master (advanced)
*<https://github.com/LeonarddeR/nvda/actions/runs/31363577205>>

* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/31881422116>


* Result: failure (all 10 windows-11-arm suites failed)

* NOTE: all 10 runners SERVED image 20260809.134 — rollout completed in ~3.3 days, faster than the assumed 4-5 days. The 4-day age guard was too conservative here; this was a real test on the new image.
* NOTE: the 2026-08-10 run (31363577205) ran on a MIXED pool (7 suites on 20260727.122, 3 on 20260804.129). Sampling a single arm job to determine "last tested image" is unreliable during rollout — sample all arm jobs.
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
*<https://g><https://github.com/LeonarddeR/nvda/actions/runs/31085283637>
*


*# 2026-08-10 08:51 — windows-11-arm 20260804.129


* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/31085283637>5>
*

* NOTE: ru<https://github.com/LeonarddeR/nvda/actions/runs/30647864308>led out (previous 2026-08-06 run still got 20260727.122). This is the first real test on 20260804.129.
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
*

* Assessme<https://github.com/LeonarddeR/nvda/actions/runs/31085283637>heft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
*

* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/31085283637>
* Result: failure (all 10 windows-11-arm suites failed)
* NOTE: runners STILL served image 20260727.122 — release 20260804.129 (published 2026-08-04) had not rolled out to the hosted win11-arm64 pool as of 2026-08-06. Effectively another re-test on the previous image.

* Per-suit<https://github.com/LeonarddeR/nvda/actions/runs/30647864308>_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
*# 2026-07<https://github.com/LeonarddeR/nvda/actions/runs/30517046822>lag)
* Previously tested image: 20260719.114 (both 2026-07-30 runs for 20260727.122 still got the old image; retrying again)
*
* Branch update: merged origin/master (advanced); merged leonard/try-testOnArm (prek auto-fix, kept clean log)
*
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/30647864308>
* NOTE: ru<https://github.com/LeonarddeR/nvda/actions/runs/30566465513>out; this is the first real test on it (both 2026-07-30 runs got 20260719.114 due to rollout lag).
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"


*# 2026-07-30 19:32 — windows-11-arm 20260727.122 (retry — rollout lag)
*

* Previously tested image: 20260719.114 (runs on 2026-07-30 morning for 20260727.122 still got the old image; retrying now that rollout may have completed)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/29953208083>3>

* NOTE: runners STILL served image 20260719.114 — release 20260727.122 (published 2026-07-27) had not rolled out to the hosted win11-arm64 pool as of 2026-07-30 evening. Effectively another re-test on the previous image.

* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"

*
*
* Previously tested image: 20260719.114

* Branch u<https://github.com/LeonarddeR/nvda/actions/runs/29953208083>ll log) and origin/master (advanced)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/30084982840>2>
* Result: failure (all 10 windows-11-arm suites failed)
* NOTE: runners served image 20260719.114 — release 20260727.122 (published 2026-07-27) had NOT rolled out to the hosted win11-arm64 pool at run time. Effectively a re-test on the previous image.
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"

*# 2026-07<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>

* Previously tested image: 20260714.109
* Branch u<https://github.com/LeonarddeR/nvda/actions/runs/29953208083>
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/30084982840>
* NOTE: runners served image 20260719.114 — the new image HAS rolled out; this is the first real test on it (previous two runs got 20260714.109 due to rollout lag).
* Previous<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>19.114 still got the old image; retrying now that rollout may have completed)
* Branch update: merged leonard/try-testOnArm (prek auto-fix) and origin/master (advanced)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/29953208083>
* Result: failure (6 arm suites failed, 4 cancelled by fail-fast)
* NOTE: runners AGAIN served image 20260714.109 — release 20260719.114 (published 2026-07-19) still not rolled out to the hosted win11-arm64 pool as of 2026-07-22.
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL; chrome_annotations/chrome_language/chrome_roleDescription/chrome_table CANCELLED
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
## 2026-07-20 19:58 — windows-11-arm 20260719.114
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/29764022234>
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; failures show the known focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
