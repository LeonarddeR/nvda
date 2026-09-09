## 2026-09-09 18:16 — windows-11-arm 20260830.155

*# 2026-08-28 13:32 — windows-11-arm 20260823.149

* Previous<https://github.com/LeonarddeR/nvda/actions/runs/33167538282>

*


*# 2026-08<https://github.com/LeonarddeR/nvda/actions/runs/31881422116> rollout age guard)

* Previously tested image: 20260727.122 / 20260804.129 (2026-08-10 pool was MIXED: 7 suites on 20260727.122, 3 on 20260804.129)
* Rollout <https://github.com/LeonarddeR/nvda/actions/runs/31881422116>.3 days) — below the 4-day guard; run requested explicitly by the user

* Branch update: merged leonard/try-testOnArm (prek auto-fix, kept clean log); merged origin/master (advanced)


* Result: failure (all 10 windows-11-arm suites failed)

*

<https://github.com/LeonarddeR/nvda/actions/runs/31085283637>>

* NOTE: al<https://github.com/LeonarddeR/nvda/actions/runs/31363577205>in ~3.3 days, faster than the assumed 4-5 days. The 4-day age guard was too conservative here; this was a real test on the new image.
*<https://github.com/LeonarddeR/nvda/actions/runs/31085283637>>(7 suites on 20260727.122, 3 on 20260804.129). Sampling a single arm job to determine "last tested image" is unreliable during rollout — sample all arm jobs.


*<https://g><https://github.com/LeonarddeR/nvda/actions/runs/31363577205>_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
<https://github.com/LeonarddeR/nvda/actions/runs/31085283637>>


* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"


<https://github.com/LeonarddeR/nvda/actions/runs/31085283637>>


*<https://g><https://github.com/LeonarddeR/nvda/actions/runs/31363577205>
<https://github.com/LeonarddeR/nvda/actions/runs/31085283637>>


* Previously tested image: 20260727.122


*<https://github.com/LeonarddeR/nvda/actions/runs/31085283637>>

* Branch update: merged origin/master (advanced); merged leonard/try-testOnArm (prek auto-fix, kept clean log)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/31363577205>
*<https://g>failure (all 10 windows-11-arm suites failed)
*<https://github.com/LeonarddeR/nvda/actions/runs/31085283637>>

* NOTE: runners SERVED image 20260804.129 — the new image HAS now rolled out (previous 2026-08-06 run still got 20260727.122). This is the first real test on 20260804.129.
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL

* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
*<https://g><https://github.com/LeonarddeR/nvda/actions/runs/30647864308>
*

*# 2026-08-06 10:31 — windows-11-arm 20260804.129

* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/30647864308>7>

*

* Result: failure (all 10 windows-11-arm suites failed)
* NOTE: ru<https://github.com/LeonarddeR/nvda/actions/runs/30566465513>9 (published 2026-08-04) had not rolled out to the hosted win11-arm64 pool as of 2026-08-06. Effectively another re-test on the previous image.
*

*# 2026-07-31 18:37 — windows-11-arm 20260727.122 (retry 2 — rollout lag)

* Previous<https://github.com/LeonarddeR/nvda/actions/runs/30566465513>60727.122 still got the old image; retrying again)
* Branch update: merged origin/master (advanced); merged leonard/try-testOnArm (prek auto-fix, kept clean log)
*<https://github.com/LeonarddeR/nvda/actions/runs/30517046822>
* Result: failure (all 10 windows-11-arm suites failed)

*
* NOTE: runners served image 20260727.122 — the new image HAS rolled out; this is the first real test on it (both 2026-07-30 runs got 20260719.114 due to rollout lag).

*<https://github.com/LeonarddeR/nvda/actions/runs/30517046822>


*# 2026-07<https://github.com/LeonarddeR/nvda/actions/runs/30084982840>g)

* Previously tested image: 20260719.114 (runs on 2026-07-30 morning for 20260727.122 still got the old image; retrying now that rollout may have completed)
*

* Branch update: no origin/master change; merged leonard/try-testOnArm (prek auto-fix), kept full log
*

* NOTE: ru<https://github.com/LeonarddeR/nvda/actions/runs/30517046822>2 (published 2026-07-27) had not rolled out to the hosted win11-arm64 pool as of 2026-07-30 evening. Effectively another re-test on the previous image.

* Per-suit<https://github.com/LeonarddeR/nvda/actions/runs/29953208083>0>_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL


* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
*

*# 2026-07-30 07:35 — windows-11-arm 20260727.122
*

* Branch update: merged leonard/try-testOnArm (prek auto-fix, kept full log) and origin/master (advanced)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/29764022234>2>


* Result: <https://github.com/LeonarddeR/nvda/actions/runs/29953208083>0>
* NOTE: runners served image 20260719.114 — release 20260727.122 (published 2026-07-27) had NOT rolled out to the hosted win11-arm64 pool at run time. Effectively a re-test on the previous image.
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
*

*# 2026-07-24 12:05 — windows-11-arm 20260719.114

* Previously tested image: 20260714.109
* Branch u<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/29953208083>0>
* Result: failure (all 10 windows-11-arm suites failed)
* NOTE: runners served image 20260719.114 — the new image HAS rolled out; this is the first real test on it (previous two runs got 20260714.109 due to rollout lag).
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"


*# 2026-07-22 21:58 — windows-11-arm 20260719.114 (retry — rollout lag)
* Branch u<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>gin/master (advanced)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/29953208083>
* Result: failure (6 arm suites failed, 4 cancelled by fail-fast)
* NOTE: runners AGAIN served image 20260714.109 — release 20260719.114 (published 2026-07-19) still not rolled out to the hosted win11-arm64 pool as of 2026-07-22.
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL; chrome_annotations/chrome_language/chrome_roleDescription/chrome_table CANCELLED
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"


## 2026-07-20 19:58 — windows-11-arm 20260719.114

* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/29764022234>
* Result: failure (all 10 windows-11-arm suites failed)
* NOTE: runners still served image 20260714.109 — release 20260719.114 exists in actions/runner-images but had not rolled out to the hosted pool at run time. Effectively a re-test on the old image.
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; failures show the known focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
