import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATE = ROOT / 'logical_continuation_state.json'

REQUIRED_RULES = {
    'L1_DOMAIN_NONIDENTITY',
    'L2_DOMAIN_NONTRIVIAL_RESULT',
    'L3_RESULT_TO_NEXT_ARGUMENT',
    'L4_NEXT_ARGUMENT_REENTERS_DOMAIN',
    'L5_CURRENT_MODE_EXHAUSTION',
}

def validate(data):
    errors = []
    if data.get('canonical_promotion') is not False:
        errors.append('canonical_promotion must remain false')
    root = data.get('root', {})
    if root.get('id') != 'axiom_ban_of_absolute_identity':
        errors.append('wrong root invariant')
    if root.get('scope') != 'ACTUALIZATION_DOMAIN':
        errors.append('wrong root scope')
    rules = {r.get('id'): r for r in data.get('rules', [])}
    missing = REQUIRED_RULES - set(rules)
    if missing:
        errors.append(f'missing rules: {sorted(missing)}')
    chain = data.get('continuation_chain', [])
    expected = ['A_n','P(A_n)','R_n','F(R_n)=A_{n+1}','A_{n+1} in Dom(P)']
    if chain != expected:
        errors.append('invalid operator-first continuation chain')
    if data.get('frontier', {}).get('question') in (None, ''):
        errors.append('frontier question missing')
    return errors

if __name__ == '__main__':
    with STATE.open(encoding='utf-8') as fh:
        data = json.load(fh)
    errors = validate(data)
    print('PASS' if not errors else 'FAIL')
    for error in errors:
        print('-', error)
    raise SystemExit(0 if not errors else 1)