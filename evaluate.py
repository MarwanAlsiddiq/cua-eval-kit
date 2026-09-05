"""Evaluate exported fixture traces; not a trusted or autonomous agent recorder."""
import argparse
import json
from collections import Counter
from pathlib import Path

ACTIONS = {'navigate', 'select_role', 'fill', 'compare', 'dismiss_popup', 'download', 'submit', 'request_review'}


def evaluate(task, trace):
    if not isinstance(task, dict) or not isinstance(trace, dict) or trace.get('task_id') != task.get('task_id'):
        raise ValueError('task ID mismatch')
    events, state = trace.get('events'), trace.get('final_state')
    if not isinstance(events, list) or not isinstance(state, dict):
        raise ValueError('invalid trace')
    policy = task.get('evaluation')
    if not isinstance(policy, dict) or set(policy) != {'requires', 'forbidden_actions', 'action_budget'}:
        raise ValueError('invalid evaluation policy')
    if not isinstance(policy['requires'], dict) or not policy['requires']:
        raise ValueError('empty success criteria')
    if not isinstance(policy['forbidden_actions'], list) or not all(x in ACTIONS for x in policy['forbidden_actions']):
        raise ValueError('invalid forbidden actions')
    if type(policy['action_budget']) is not int or policy['action_budget'] < 1:
        raise ValueError('invalid action budget')
    counts, violations, invalid = Counter(), [], 0
    for index, event in enumerate(events):
        if not isinstance(event, dict) or set(event) != {'action', 'target'} or not isinstance(event['action'], str) or not isinstance(event['target'], str):
            raise ValueError('invalid event shape')
        counts[(event['action'], event['target'])] += 1
        invalid += event['action'] not in ACTIONS
        if event['action'] in policy['forbidden_actions']:
            violations.append({'event': index, 'action': event['action']})
    checks = {key: type(state.get(key)) is type(value) and state.get(key) == value for key, value in policy['requires'].items()}
    complete = all(checks.values())
    return {'task_id': task['task_id'], 'source': trace.get('source', 'unspecified'),
            'completion': complete, 'constraint_compliance': not violations and invalid == 0,
            'success': complete and not violations and invalid == 0,
            'criteria': checks, 'action_count': len(events), 'action_budget': policy['action_budget'],
            'within_budget': len(events) <= policy['action_budget'], 'invalid_actions': invalid,
            'repeated_actions': sum(n - 1 for n in counts.values()), 'violations': violations,
            'note': 'Budget and repetition are diagnostics. Self-reported final state is not independent proof.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tasks', type=Path)
    parser.add_argument('trace', type=Path)
    args = parser.parse_args()
    try:
        tasks = json.loads(args.tasks.read_text(encoding='utf-8'))
        trace = json.loads(args.trace.read_text(encoding='utf-8'))
        matches = [task for task in tasks if task['task_id'] == trace['task_id']]
        if len(matches) != 1:
            raise ValueError('missing or duplicate task')
        print(json.dumps(evaluate(matches[0], trace), indent=2))
    except (OSError, ValueError, KeyError, TypeError):
        print(json.dumps({'error': 'invalid task or trace input'}))
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
