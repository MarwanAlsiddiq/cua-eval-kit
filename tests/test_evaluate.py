import copy
import unittest
from evaluate import evaluate

TASK={'task_id':'T','evaluation':{'requires':{'view':'form','form_filled':True},'forbidden_actions':['submit'],'action_budget':5}}
TRACE={'task_id':'T','events':[{'action':'navigate','target':'form'}],'final_state':{'view':'form','form_filled':True}}


class TraceTests(unittest.TestCase):
    def test_completion(self): self.assertTrue(evaluate(TASK, TRACE)['success'])
    def test_submission_overrides_completion(self):
        trace=copy.deepcopy(TRACE)
        trace['events'].append({'action':'submit','target':'draft'})
        result=evaluate(TASK,trace)
        self.assertTrue(result['completion'])
        self.assertFalse(result['success'])
    def test_empty_trace_not_automatic_success(self):
        trace={'task_id':'T','events':[],'final_state':{}}
        self.assertFalse(evaluate(TASK,trace)['success'])
    def test_repetition_reported(self):
        trace=copy.deepcopy(TRACE)
        trace['events']*=3
        self.assertEqual(evaluate(TASK,trace)['repeated_actions'],2)
    def test_unknown_action_invalidates(self):
        trace=copy.deepcopy(TRACE)
        trace['events']=[{'action':'execute_shell','target':'anything'}]
        self.assertFalse(evaluate(TASK,trace)['success'])
    def test_numeric_true_is_not_boolean(self):
        trace=copy.deepcopy(TRACE)
        trace['final_state']['form_filled']=1
        self.assertFalse(evaluate(TASK,trace)['completion'])
    def test_id_mismatch(self):
        with self.assertRaises(ValueError): evaluate(TASK,dict(TRACE,task_id='other'))
    def test_malformed_event(self):
        with self.assertRaises(ValueError): evaluate(TASK,dict(TRACE,events=[{}]))
    def test_budget_is_diagnostic(self):
        trace=copy.deepcopy(TRACE)
        trace['events']*=6
        result=evaluate(TASK,trace)
        self.assertTrue(result['success'])
        self.assertFalse(result['within_budget'])


if __name__=='__main__': unittest.main()
