# Methodology and trace schema

Each task has `task_id`, `objective`, `constraints` (list), `success_criteria` (list), `risk_level`, and `evaluation`. Evaluation requires exact final-state values, a forbidden-action list and a positive action budget.

A trace is an object with `task_id`, `source`, `events` and `final_state`. Every event has exactly `action` and `target`, both strings. Accepted action names are `navigate`, `select_role`, `fill`, `compare`, `dismiss_popup`, `download`, `submit` and `request_review`. The fixture logs a completed field edit on the `change` event; blur a field before exporting. Typed values are omitted from the trace.

Final state is exported by the fixture. A value such as `form_filled: true` means both synthetic inputs were nonempty, not that their content was correct. Download state means the download was initiated; verify the resulting file independently when testing a real agent. A review request flag does not prove a human responded.

## Trial protocol

1. Choose one task, reset and record browser/agent versions and initial conditions.
2. Give the objective and constraints to the agent. Do not provide selectors or the solution when measuring autonomous performance.
3. Record actions independently where possible. Preserve failures and manual interventions.
4. Verify the final UI and side effects, then export the fixture trace.
5. Evaluate and review the report. A report produced successfully is not necessarily a successful trial.
6. Repeat with a fixed trial count chosen in advance. Report per-task denominators and failure categories.

For this release, browser smoke tests are explicitly scripted through known UI controls. They validate the fixture, not autonomous navigation ability. There is no claimed cross-site benchmark or long-horizon success rate.

## Extending the benchmark

Use an owned test surface and synthetic records. Add new actions to the evaluator deliberately; unknown actions fail compliance. Bind destructive operations to a sandbox. Record task completion and constraint violations separately so a forbidden submission cannot be hidden by a completed form.
