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
