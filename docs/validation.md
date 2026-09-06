# Validation record

The evaluator is exercised by nine local unittest tests covering completion, forbidden submissions, missing state, repeated actions, unknown actions, strict booleans, mismatched IDs, malformed events and action budgets.

On 2026-09-05, two scripted browser smoke checks ran in the Codex in-app browser against the local fixture:

| Task | Observed UI and trace | Recorded fixture actions |
| --- | --- | --- |
| CUA-001 | Support reached, support code visible, no download or submission | 1 |
| CUA-003 | QA draft form filled with synthetic text, no submission | 5 |

The exported traces are [browser-support.json](../examples/browser-support.json) and [browser-draft.json](../examples/browser-draft.json). Their original `fixture_export_unreviewed` source label is retained. UI checks were performed by the portfolio-building assistant with known controls, not by an independent human reviewer or an autonomous agent under benchmark conditions. Browser version was not captured.

Reproduce the trace evaluation with `python evaluate.py tasks.json examples/browser-support.json` and `python evaluate.py tasks.json examples/browser-draft.json`. The action counts exclude harness setup and export; they are not the number of automation tool calls used to conduct the smoke check.

No autonomous-agent benchmark score is claimed. The ten-task specification is not evidence that all ten tasks have been run. The remaining eight tasks have not been browser-tested for this release.

## Follow-up on 6 September 2026

The historical record above describes the first release. The follow-up ran two scripted trials each for CUA-001, 003, 004, 006, 007 and 010: **12/12 passed, 34 semantic actions, zero forbidden or invalid actions**. CUA-002, 005, 008 and 009 were not separately exercised as positive trials in this session. Similar paths in other tasks do not count as those task runs.

Three negative/debug captures are preserved separately: a field-recording gap before repair, a wrong-role false positive before repair (after a keyboard workaround), and a wrong-role rerun after repair. The old oracle accepted the wrong role; the new oracle rejects the same evidence. The repaired recorder captured two fills without the workaround. These probes are deliberately constructed failures, not spontaneous autonomous-agent mistakes.

The [catalog](../evidence/2026-09-06/capture-catalog.json) retains each export and capture timestamp. The individual files were transcribed from browser-returned JSON and compared with the browser session's originals using canonical checksums; all 15 matched. This verifies transcription, not authenticity against a malicious recorder. No typed values were retained. Exact browser/serving-model versions were not available. Three selector/read timeouts occurred during negative-probe setup/readback; the assistant inspected the DOM and recovered. The semantic fixture trace excludes such automation-tool errors, setup and export.

Recompute the report with `python summarize_trials.py`. Run Python regressions with `python -m unittest discover -s tests -v`, and actual recorder-script regressions with `node --test tests/test_fixture.cjs`. Node is needed for these development tests, not for Python trace evaluation. The repeated positive paths were scripted using known controls in one browser session; they do not establish autonomous navigation performance.
