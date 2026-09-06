import copy
import json
import unittest
from pathlib import Path
from evaluate import evaluate
from summarize_trials import build

ROOT=Path(__file__).resolve().parents[1]


class ObservedRegressions(unittest.TestCase):
    def test_captured_trial_report_is_reproducible(self):
        self.assertEqual(build(),json.loads((ROOT/'evidence/2026-09-06/metrics.json').read_text(encoding='utf-8')))

    def test_observed_wrong_role_rejected_after_policy_fix(self):
        trace=json.loads((ROOT/'evidence/2026-09-06/wrong-role-before.json').read_text(encoding='utf-8'))
        old=json.loads((ROOT/'evidence/2026-09-06/baseline-tasks.json').read_text(encoding='utf-8'))[2]
        new=json.loads((ROOT/'tasks.json').read_text(encoding='utf-8'))[2]
        self.assertTrue(evaluate(old,trace)['success'])
        self.assertFalse(evaluate(new,trace)['success'])
        self.assertFalse(evaluate(new,trace)['criteria']['selected_role'])

    def test_stop_at_qa_form_also_requires_correct_role(self):
        trace=json.loads((ROOT/'evidence/2026-09-06/wrong-role-before.json').read_text(encoding='utf-8'))
        trace['task_id']='CUA-009'
        task=json.loads((ROOT/'tasks.json').read_text(encoding='utf-8'))[8]
        self.assertFalse(evaluate(task,trace)['success'])
        trace['final_state']['selected_role']='qa'
        self.assertTrue(evaluate(task,trace)['success'])
