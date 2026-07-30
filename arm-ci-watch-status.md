## 2026-07-30 19:32 — windows-11-arm 20260727.122 (retry — rollout lag)

*<https://github.com/LeonarddeR/nvda/actions/runs/30084982840>
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
*
* Result: <https://github.com/LeonarddeR/nvda/actions/runs/29953208083>

* Per-suit<https://github.com/LeonarddeR/nvda/actions/runs/29953208083>_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL

* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
<<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>>>

*



<<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>>>>>
*# 2026-07<https://github.com/LeonarddeR/nvda/actions/runs/29953208083>g)

* Previously tested image: 20260714.109 (run on 2026-07-20 for 20260719.114 still got the old image; retrying now that rollout may have completed)
*<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>>>>>>
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/29953208083>



* Result: failure (6 arm suites failed, 4 cancelled by fail-fast)
*<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>>>>
* NOTE: runners AGAIN served image 20260714.109 — release 20260719.114 (published 2026-07-19) still not rolled out to the hosted win11-arm64 pool as of 2026-07-22.
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL; chrome_annotations/chrome_language/chrome_roleDescription/chrome_table CANCELLED
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
*# 2026-07-20 19:58 — windows-11-arm 20260719.114



* Previously tested image: 20260714.109
* Branch update: merged origin/master (advanced)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/29764022234>
* Result: failure (all 10 windows-11-arm suites failed)
* NOTE: runners still served image 20260714.109 — release 20260719.114 exists in actions/runner-images but had not rolled out to the hosted pool at run time. Effectively a re-test on the old image.
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; failures show the known focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"

