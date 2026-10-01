import json
from pathlib import Path
import yaml

ROOT = Path(__file__).parent

def main():
    state = json.loads((ROOT / 'dext_state.json').read_text(encoding='utf-8'))
    vectors = yaml.safe_load((ROOT / 'dext_test_vectors.yaml').read_text(encoding='utf-8'))
    required = ['id','revision_of','status','canonical_promotion','objects','source_basis','not_established','next_tests']
    missing = [k for k in required if k not in state]
    assert not missing, f'missing: {missing}'
    assert state['status'] == 'FORMALIZATION'
    assert state['canonical_promotion'] is False
    for key in ['continuation_set','exhaustion','frustration','regime_transition','boundary']:
        assert key in state['objects']
    assert vectors['suite'] == 'DEXT_EXHAUSTION_FORMALIZATION'
    assert len(vectors['cases']) == 10
    assert sum(c['expected'] == 'REJECT' for c in vectors['cases']) >= 6
    print('DEXT VALIDATION: PASS')

if __name__ == '__main__':
    main()