import json
from pathlib import Path
import yaml
ROOT=Path(__file__).parent
def main():
 s=json.loads((ROOT/'dext_operator_state.json').read_text(encoding='utf-8'))
 v=yaml.safe_load((ROOT/'dext_operator_test_vectors.yaml').read_text(encoding='utf-8'))
 assert s['status']=='FORMALIZATION' and s['canonical_promotion'] is False
 for k in ['continuation','outgoing','exhaustion','boundary','regime_transition','candidate_common_carrier']:
  assert k in s['structures']
 assert s['source_mapping']['exhaustion']=='Out_R(P3)=empty_set'
 assert s['source_mapping']['transition']=='P3 --J_R--> P4'
 assert len(v['cases'])==10
 assert sum(x['expected']=='REJECT' for x in v['cases'])>=6
 print('DEXT OPERATOR VALIDATION: PASS')
if __name__=='__main__': main()