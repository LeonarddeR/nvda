## 2026-07-22 21:58 — windows-11-arm 20260719.114 (retry — rollout lag)
- Previously tested image: 20260714.109 (run on 2026-07-20 for 20260719.114 still got the old image; retrying now that rollout may have completed)
- Branch update: merged leonard/try-testOnArm (prek auto-fix) and origin/master (advanced)
- CI run: <fill in after it starts>
- Result: pending
## 2026-07-20 19:58 — windows-11-arm 20260719.114
- Previously tested image: 20260714.109
- Branch update: merged origin/master (advanced)
- CI run: https://github.com/LeonarddeR/nvda/actions/runs/29764022234
- Result: failure (all 10 windows-11-arm suites failed)
- NOTE: runners still served image 20260714.109 — release 20260719.114 exists in actions/runner-images but had not rolled out to the hosted pool at run time. Effectively a re-test on the old image.
- Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
- Assessment: #14069 and #14264 STILL APPLY — both OPEN; failures show the known focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
