import json
from pathlib import Path
import yaml
ROOT=Path(__file__).parent
def main():
 s=json.loads((ROOT/'common_carrier_state.json').read_text(encoding='utf-8'))
 v=yaml.safe_load((ROOT/'common_carrier_test_vectors.yaml').read_text(encoding='utf-8'))
 assert s['status']=='FORMALIZATION' and s['canonical_promotion'] is False
 assert s['carrier']['definition'].startswith('W = Span_F')
 assert 'J_R|P3,R>=|P4,R>' in s['operators']['J']
 assert 'undefined' in s['critical_result']
 assert len(v['cases'])==10
 assert sum(c['expected']=='REJECT' for c in v['cases'])>=7
 print('COMMON CARRIER VALIDATION: PASS')
if __name__=='__main__': main()