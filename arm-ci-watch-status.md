## 2026-10-30 13:52 (auto) -- windows-11-arm 20261026.197 (win11-vs2026-arm64 family)

* Per-suite arm results (image served noted per suite): installer FAIL (20261021.192), chrome_table FAIL (20261021.192), chrome_annotations FAIL (20261021.192), chrome_list FAIL (20261021.192), chrome_language FAIL (20261022.194), startupShutdown FAIL (20261021.192), chrome_roleDescription FAIL (20261021.192), chrome_link FAIL (20261022.194), chrome_misc_aria FAIL (20261021.192), chrome_misc FAIL (20261021.192), l10n CANCELLED (20261021.192)

*# 2026-10-16 (auto) -- windows-11-arm 20261013.183 (win11-vs2026-arm64 family)
* Release status at trigger time: prerelease=False, published 2026-10-14 10:24:42 UTC (2.08 days old at detection) -- flag already flipped to rolled-out; no override needed. Flipped faster than the previously observed 3.3-5 day range (worth noting, not blocking, since a False flag has never been observed to lag rollout -- only True has lagged).
* Also not<https://github.com/LeonarddeR/nvda/actions/runs/38900233524>.188, also prerelease=False, published same day (2026-10-14) -- not the family windows-11-arm has actually served since the 2026-09-25 VS2026 swap, so not targeted here.
* Assessment: #14069 and #14264 STILL APPLY -- both OPEN; same focus-theft signature persists on the new image 20261013.183: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (startupShutdown job, 2026-10-16T12:41:53Z). No change -- the VS2026 arm64 image line continues to carry the same underlying focus-theft problem across releases.
* Previously tested image: 20260924.168 (confirmed prod, served all 11 jobs cleanly on 2026-10-02 run 37052401873)
* Release <https://github.com/LeonarddeR/nvda/actions/runs/37959306044>05 16:18:37 UTC (3.81 days old at detection) -- normally gates per the age/prerelease heuristic, but OVERRIDDEN: this log has now recorded the prerelease flag lagging actual hosted-pool rollout on at least two prior occasions (2026-09-09: new image already serving 7/10 suites while still prerelease=True; 2026-09-17: new image already serving 3/10 suites at only 1.75 days old, still prerelease=True) against a fastest-observed full rollout of 3.3 days. At 3.81 days old, 20261004.176 is already past that fastest-case mark, so waiting on the flag risked sitting on stale data another week. User confirmed this override live in chat on 2026-10-09.

* Also noted: win11-arm64/20261004.186 (plain arm64 family) published same day, also still prerelease=True -- not the family the windows-11-arm label has actually been serving since the 2026-09-25 VS2026 swap, so not targeted here.

* Branch update: merged leonard/try-testOnArm (prek auto-fix mangled the log again; restored clean version); merged origin/master (advanced, 19 commits incl. brlapi bindings update, CLI loglevel fix)
*<https://github.com/LeonarddeR/nvda/actions/runs/36131144605>>959306044>

* Result: failure (9 of 10 windows-11-arm suites failed; chrome_annotations and l10n cancelled)
*<https://github.com/LeonarddeR/nvda/actions/runs/36131144605>>61004.176 for all 11 jobs): installer FAIL, chrome_link FAIL, startupShutdown FAIL, chrome_misc_aria FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_table FAIL, chrome_language FAIL, chrome_roleDescription FAIL, chrome_annotations CANCELLED, l10n CANCELLED
<https://github.com/LeonarddeR/nvda/actions/runs/36131144605>>
* Assessment: #14069 and #14264 STILL APPLY -- both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (startupShutdown job, 2026-10-09T16:49:48Z). No change -- the VS2026 arm64 image line continues to carry the same underlying focus-theft problem across releases.

*

*<https://github.com/LeonarddeR/nvda/actions/runs/36131144605>>052401873>26-arm64 family, post label-swap)
<https://github.com/LeonarddeR/nvda/actions/runs/36131144605>>

* Previously tested image: 20260920.164 (win11-vs2026-arm64; confirmed prod, served all 10 arm suites in the 2026-09-25 run)

* Release status at trigger time: prerelease=False, published 2026-09-29 10:20:37 UTC (3.37 days old at detection)
* Branch update: merged leonard/try-testOnArm (prek auto-fix mangled the log again; restored clean version); merged origin/master (advanced, large commit batch incl. word comment reporting fix)
*<https://github.com/LeonarddeR/nvda/actions/runs/36131144605>>
*<https://github.com/LeonarddeR/nvda/actions/runs/36131144605>>052401873>
* Result: failure (10 of 10 windows-11-arm suites failed; l10n cancelled)

* Per-suite arm results (image served: win11-vs2026-arm64/20260924.168 for all 11 jobs, clean rollout, no mixed pool): installer FAIL, chrome_annotations FAIL, startupShutdown FAIL, chrome_list FAIL, chrome_roleDescription FAIL, chrome_misc FAIL, chrome_language FAIL, chrome_misc_aria FAIL, chrome_link FAIL, chrome_table FAIL, l10n CANCELLED
* Assessment: #14069 and #14264 STILL APPLY -- both OPEN; same focus-theft signature persists on the new VS2026 arm64 image 20260924.168: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (startupShutdown job, 2026-10-02T19:32:39Z). No change from the 2026-09-25 run on 20260920.164/174 -- the VS2026 arm64 label swap has not affected the underlying focus-theft problem.


*<https://github.com/LeonarddeR/nvda/actions/runs/36131144605>>
*# 2026-09-25 (auto) -- windows-11-arm 20260920.174

* Previously tested image: 20260906.161 (confirmed prod, majority of last run); 20260914.169 partially served (3/10) under manual override, not yet confirmed as prod on its own
* Release status at trigger time: prerelease=False, published 2026-09-21 12:51:45 UTC (3.95 days old at detection)
* Branch u<https://github.com/LeonarddeR/nvda/actions/runs/35206978828>the log again; restored clean version); merged origin/master (advanced, security.md change)
*

* Result: failure (10 of 10 windows-11-arm suites failed; l10n cancelled)


* Per-suite arm results (image served: win11-vs2026-arm64/20260920.164 for all): installer FAIL, chrome_annotations FAIL, startupShutdown FAIL, chrome_list FAIL, chrome_misc_aria FAIL, chrome_link FAIL, chrome_language FAIL, chrome_misc FAIL, chrome_table FAIL, chrome_roleDescription FAIL, l10n CANCELLED
* Assessment: #14069 and #14264 STILL APPLY -- both OPEN; same focus-theft signature persists even on the new VS2026 arm64 image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (startupShutdown job, 2026-09-25T12:15:28Z). The image family swap did not fix the underlying focus-theft problem.

*

*# 2026-09-17 11:46 -- windows-11-arm 20260914.169 (manual override -- prerelease flag known to lag rollout)

* Release <https://github.com/LeonarddeR/nvda/actions/runs/34375777935>15 15:22 UTC (1.75 days old at detection) -- normally gates, but OVERRIDDEN per user direction: last week proved the prerelease flag can lag actual hosted-pool rollout (20260906.161 was already serving 7/10 suites while still flagged prerelease=True)
*


* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/35206978828>

* Result: failure (10 of 10 windows-11-arm suites failed; l10n cancelled)
* Per-suite arm results (image served): chrome_annotations FAIL(20260906.161), startupShutdown FAIL(20260906.161), chrome_table FAIL(20260914.169), chrome_misc_aria FAIL(20260914.169), chrome_roleDescription FAIL(20260906.161), installer FAIL(20260914.169), chrome_list FAIL(20260906.161), chrome_language FAIL(20260906.161), chrome_link FAIL(20260906.161), chrome_misc FAIL(20260906.161), l10n CANCELLED


* UPCOMING: GitHub is switching the windows-11-arm label to the VS2026 arm64 image between 2026-09-21 and 2026-09-30 (actions/runner-images issue #14602) -- that swap is the next likely point for behaviour to change; it is close now, watch for it next run.

* Release status at trigger time: prerelease=False, published 2026-09-01 12:13:50 UTC (rolled out; a newer release 20260906.161 also existed, still marked prerelease=True, 1.3 days old, published 2026-09-08 - skipped per rollout gate)

*
* Branch update: merged leonard/try-testOnArm (prek auto-fix mangled the log again; restored clean version); merged origin/master (advanced, 28 commits)

* Per-suit<https://github.com/LeonarddeR/nvda/actions/runs/33167538282> startupShutdown FAIL(20260830.155), chrome_annotations FAIL(20260906.161), chrome_table FAIL(20260906.161), chrome_misc FAIL(20260830.155), chrome_misc_aria FAIL(20260830.155), chrome_roleDescription FAIL(20260906.161), chrome_list FAIL(20260906.161), chrome_language FAIL(20260906.161), chrome_link FAIL(20260906.161)
* Assessme<https://github.com/LeonarddeR/nvda/actions/runs/31881422116>heft signature on BOTH served images: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA" (startupShutdown job, 20260830.155, 2026-09-09T16:35:24Z) and "Specific speech did not occur before timeout: NVDA Launcher" (installer job, 20260906.161, 2026-09-09T16:37:05Z)
*<https://github.com/LeonarddeR/nvda/actions/runs/30566465513>>

*

* Previously tested image: 20260809.134
* Release status at trigger time: prerelease=False, published 2026-08-24 14:10:51 UTC (3.89 days old at detection)
* Branch update: merged leonard/try-testOnArm (prek auto-fix, kept clean log); merged origin/master (advanced, 32 commits; brought in a new 11th arm suite: l10n)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/33167538282>
* Result: <https://github.com/LeonarddeR/nvda/actions/runs/31363577205>6>10n suite added by the origin/master merge passed)
* NOTE: all 11 windows-11-arm jobs SERVED image 20260823.149 (clean rollout, no mixed pool) — confirms the prerelease flag flipped to false around 2026-08-27/28, roughly 3.9 days after publication (2026-08-24), consistent with the 3.3-5 day rollout window observed previously.

*# 2026-08-15 13:11 — windows-11-arm 20260809.134 (manual override of rollout age guard)

* Previously tested image: 20260727.122 / 20260804.129 (2026-08-10 pool was MIXED: 7 suites on 20260727.122, 3 on 20260804.129)

* Branch update: merged leonard/try-testOnArm (prek auto-fix, kept clean log); merged origin/master (advanced)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/31363577205>6>
* Result: failure (all 10 windows-11-arm suites failed)
<<https://github.com/LeonarddeR/nvda/actions/runs/30566465513>>>
* NOTE: the 2026-08-10 run (31363577205) ran on a MIXED pool (7 suites on 20260727.122, 3 on 20260804.129). Sampling a single arm job to determine "last tested image" is unreliable during rollout — sample all arm jobs.

* Assessme<https://github.com/LeonarddeR/nvda/actions/runs/30647864308>heft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"

*



* NOTE: runners SERVED image 20260804.129 — the new image HAS now rolled out (previous 2026-08-06 run still got 20260727.122). This is the first real test on 20260804.129.

* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature on the new image: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"
*

*# 2026-08<https://github.com/LeonarddeR/nvda/actions/runs/30647864308>

* Previously tested image: 20260727.122
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/31085283637>
* Result: <https://github.com/LeonarddeR/nvda/actions/runs/30517046822>

* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL

* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"

* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/30647864308>

* NOTE: runners served image 20260727.122 — the new image HAS rolled out; this is the first real test on it (both 2026-07-30 runs got 20260719.114 due to rollout lag).

*

*# 2026-07<https://github.com/LeonarddeR/nvda/actions/runs/29953208083>g)

* Previously tested image: 20260719.114 (runs on 2026-07-30 morning for 20260727.122 still got the old image; retrying now that rollout may have completed)

* Result: failure (all 10 windows-11-arm suites failed)
* Per-suit<https://github.com/LeonarddeR/nvda/actions/runs/30084982840>_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessme<https://github.com/LeonarddeR/nvda/actions/runs/29764022234>heft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"

*
* Branch update: merged leonard/try-testOnArm (prek auto-fix, kept full log) and origin/master (advanced)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/30517046822>
* Result: failure (all 10 windows-11-arm suites failed)
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; same focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"

*

* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/30084982840>
* NOTE: runners served image 20260719.114 — the new image HAS rolled out; this is the first real test on it (previous two runs got 20260714.109 due to rollout lag).
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL

## 2026-07-22 21:58 — windows-11-arm 20260719.114 (retry — rollout lag)

* Previously tested image: 20260714.109 (run on 2026-07-20 for 20260719.114 still got the old image; retrying now that rollout may have completed)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/29953208083>
* Result: failure (6 arm suites failed, 4 cancelled by fail-fast)
## 2026-07-20 19:58 — windows-11-arm 20260719.114

* Previously tested image: 20260714.109
* Branch update: merged origin/master (advanced)
* CI run: <https://github.com/LeonarddeR/nvda/actions/runs/29764022234>
* Result: failure (all 10 windows-11-arm suites failed)
* Per-suite arm results: startupShutdown FAIL, installer FAIL, chrome_annotations FAIL, chrome_language FAIL, chrome_link FAIL, chrome_list FAIL, chrome_misc FAIL, chrome_misc_aria FAIL, chrome_roleDescription FAIL, chrome_table FAIL
* Assessment: #14069 and #14264 STILL APPLY — both OPEN; failures show the known focus-theft signature: "Timed out waiting Welcome to NVDA to focus" / "Specific speech did not occur before timeout: Welcome to NVDA"