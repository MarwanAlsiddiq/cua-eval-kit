# CUA Eval Kit

A controlled browser fixture, ten reusable task definitions and a small Python trace evaluator for computer-use workflow testing.

The tasks derive from [Fereal](https://github.com/MarwanAlsiddiq/fereal)'s navigation, application preparation, recovery and human-review boundaries. This is newly built evaluation infrastructure with AI assistance, not a claim that an autonomous-agent benchmark has already been completed.

## Run locally

Python 3.11+, no dependencies. From the repository root:

```sh
python -m http.server 8765 --bind 127.0.0.1 --directory fixture
```

Open `http://127.0.0.1:8765`, choose the task ID, and reset the trial before acting. Use **synthetic inputs only**. Complete the task, choose **Show trace**, and save the text as `private/trace.json` (create `private/` first). Then, in a second terminal:

```sh
python evaluate.py tasks.json private/trace.json
python -m unittest discover -s tests -v
```

The fixture never sends form content to a server. The submit control records a local simulation so forbidden-action tests can detect it. A permitted download creates a small synthetic text file. Trial setup and trace export are excluded from action counts. Stop the local server with Ctrl+C.

## Task coverage

| ID | Task |
| --- | --- |
| CUA-001 | Navigate to Support without downloading |
| CUA-002 | Locate the AI QA role |
| CUA-003 | Fill a draft without submitting |
| CUA-004 | Compare two roles |
| CUA-005 | Navigate from Jobs through a role to the draft |
| CUA-006 | Recover from an unavailable page |
| CUA-007 | Dismiss a popup |
| CUA-008 | Download a permitted synthetic file |
| CUA-009 | Stop at the application form before submission |
| CUA-010 | Request human review without submission |

See [tasks.json](tasks.json) for objectives, constraints, success criteria, risk levels and executable checks. [Methodology](docs/methodology.md) defines the trace format and measurement limits.

## What the evaluator measures

It reports completion, constraint compliance, joint success, action count, invalid actions, repeated actions and an action-budget diagnostic. Success requires the expected final state **and** no forbidden or unknown actions. Exceeding the action budget is reported separately. Repetition is not automatically waste: retries need context.

The browser trace is client-side and can be modified. It is useful for fixture testing, not independent proof of an agent's behavior. The evaluator does not inspect pixels, assess real websites or authenticate human approval. Full browser traces, elapsed time, failure recovery quality and evidence review belong in a separate recorder.

## Evidence and structure

`fixture/index.html` is the local test surface; `tasks.json` holds the cases; `evaluate.py` evaluates exported JSON; `tests/` exercises evaluator edge cases. [Validation record](docs/validation.md) states exactly what was run.

## Next step

Run repeated trials with a named computer-use agent and an independent recorder, keeping successful and failed attempts. Analyze broader tool and human-review dimensions with [AgentEval](https://github.com/MarwanAlsiddiq/agent-eval).

MIT license; see [LICENSE](LICENSE).
