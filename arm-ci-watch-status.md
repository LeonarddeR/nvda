## 2026-07-30 07:35 — windows-11-arm 20260727.122
- Previously tested image: 20260719.114
- Branch update: merged leonard/try-testOnArm (prek auto-fix, kept full log) and origin/master (advanced)
- CI run: <fill in after it starts>
- Result: pending
## 2026-07-24 12:05 — windows-11-arm 20260719.114
- Previously tested image: 20260714.109
- Branch update: merged origin/master (advanced)
- CI run: https://github.com/LeonarddeR/nvda/actions/runs/30084982840
- Result: failure (all 10 windows-11-arm suites failed)
- NOTE: runners served image 20260719.114 — the new image HAS rolled out; this is the first real test on it (previous two runs got 20260714.109 due to rollout lag).
- Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
- Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
## 2026-07-22 21:58 — windows-11-arm 20260719.114 (retry — rollout lag)
- Previously tested image: 20260714.109 (run on 2026-07-20 for 20260719.114 still got the old image; retrying now that rollout may have completed)
- Branch update: merged leonard/try-testOnArm (prek auto-fix) and origin/master (advanced)
- CI run: https://github.com/LeonarddeR/nvda/actions/runs/29953208083
- Result: failure (6 arm suites failed, 4 cancelled by fail-fast)
- NOTE: runners AGAIN served image 20260714.109 — release 20260719.114 (published 2026-07-19) still not rolled out to the hosted win11-arm64 pool as of 2026-07-22.
- Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL; chrome_annotations/chrome_language/chrome_roleDescription/chrome_table CANCELLED
- Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
## 2026-07-20 19:58 — windows-11-arm 20260719.114
- Previously tested image: 20260714.109
- Branch update: merged origin/master (advanced)
- CI run: https://github.com/LeonarddeR/nvda/actions/runs/29764022234
- Result: failure (all 10 windows-11-arm suites failed)
- NOTE: runners still served image 20260714.109 — release 20260719.114 exists in actions/runner-images but had not rolled out to the hosted pool at run time. Effectively a re-test on the old image.
- Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
- Assessment: #14069 and #14264 STILL APPLY — both OPEN; failures show the known focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
