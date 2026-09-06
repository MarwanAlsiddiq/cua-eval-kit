"""Recompute per-trial browser evidence and before/after oracle results."""
import json
from pathlib import Path
from evaluate import evaluate


def build():
    root=Path(__file__).resolve().parent
    base=root/'evidence/2026-09-06'
    tasks={t['task_id']:t for t in json.loads((root/'tasks.json').read_text(encoding='utf-8'))}
    catalog=json.loads((base/'capture-catalog.json').read_text(encoding='utf-8'))
    results=[]
    for row in catalog:
        # Cross-check the catalog against the separately inspectable original export.
        trace=json.loads((base/(row['name']+'.json')).read_text(encoding='utf-8'))
        if trace != row['trace']: raise ValueError('capture mismatch')
        if row['kind']=='scripted_browser_trial':
            results.append({'run':row['name'],'captured_at':row['captured_at'],**evaluate(tasks[trace['task_id']],trace)})
    negative=json.loads((base/'wrong-role-after.json').read_text(encoding='utf-8'))
    return {'protocol':'Two scripted trials for each of six tasks; known controls; same session; not autonomous benchmark.',
            'completion':{'passed':sum(r['success'] for r in results),'total':len(results)},
            'forbidden_or_invalid_runs':sum(not r['constraint_compliance'] for r in results),
            'actions':sum(r['action_count'] for r in results),
            'results':results,'wrong_role_after':evaluate(tasks['CUA-003'],negative),
            'limitations':'Client-side semantic events, not complete browser-tool traces. Setup and export excluded. Exact browser/model versions not captured. Three selector/read timeouts occurred during negative-probe setup/readback and were recovered; they are not fixture actions.'}


if __name__=='__main__':
    print(json.dumps(build(),indent=2))
