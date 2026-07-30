## 2026-07-30 07:35 — windows-11-arm 20260727.122

*<https://github.com/LeonarddeR/nvda/actions/runs/29953208083>

* NOTE: runners AGAIN served image 20260714.109 — release 20260719.114 (published 2026-07-19) still not rolled out to the hosted win11-arm64 pool as of 2026-07-22.


*# 2026-07<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>

* Previously tested image: 20260714.109
* Branch update: merged origin/master (advanced)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/29764022234>
* Result: failure (all 10 windows-11-arm suites failed)
* NOTE: runners still served image 20260714.109 — release 20260719.114 exists in actions/runner-images but had not rolled out to the hosted pool at run time. Effectively a re-test on the old image.
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; failures show the known focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
