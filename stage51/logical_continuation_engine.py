from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class Atom:
    predicate: str
    args: tuple[str, ...] = ()

@dataclass(frozen=True)
class Rule:
    rule_id: str
    premises: tuple[Atom, ...]
    conclusion: Atom
    status: str
    provenance: str

@dataclass(frozen=True)
class Proof:
    conclusion: Atom
    premises: tuple[Atom, ...]
    rule_id: str
    status: str

RULES = {
    'L1_DOMAIN_NONIDENTITY': Rule('L1_DOMAIN_NONIDENTITY',
        (Atom('NonIdentity', ('D','I')),),
        Atom('InDomain', ('P','(D,I)')),
        'SOURCE_FORMALIZATION', 'Chapter1'),
    'L2_DOMAIN_NONTRIVIAL_RESULT': Rule('L2_DOMAIN_NONTRIVIAL_RESULT',
        (Atom('InDomain', ('P','A')),),
        Atom('NonTrivialResult', ('P','A')),
        'SOURCE_FORMALIZATION', 'Chapter1'),
    'L3_RESULT_TO_NEXT_ARGUMENT': Rule('L3_RESULT_TO_NEXT_ARGUMENT',
        (Atom('Actualized', ('R_n',)), Atom('Continue', ('R_n',))),
        Atom('ExistsNextArgument', ('A_{n+1}',)),
        'SOURCE_SUPPORTED_FORMALIZATION', 'Chapter2'),
    'L4_NEXT_ARGUMENT_REENTERS_DOMAIN': Rule('L4_NEXT_ARGUMENT_REENTERS_DOMAIN',
        (Atom('ExistsNextArgument', ('A_{n+1}',)),),
        Atom('InDomain', ('P','A_{n+1}')),
        'SOURCE_SUPPORTED_FORMALIZATION', 'Chapter2'),
    'L5_CURRENT_MODE_EXHAUSTION': Rule('L5_CURRENT_MODE_EXHAUSTION',
        (Atom('CurrentModeExhausted', ('A_n',)), Atom('NeedContinue', ('A_n',))),
        Atom('OrthogonalResolutionRequired', ('A_n',)),
        'SOURCE_FORMALIZATION', 'Chapter2'),
}

def infer(rule_id: str, facts: Iterable[Atom]) -> Proof:
    rule = RULES[rule_id]
    fact_set = set(facts)
    missing = [p for p in rule.premises if p not in fact_set]
    if missing:
        raise ValueError(f'missing premises for {rule_id}: {missing}')
    return Proof(rule.conclusion, rule.premises, rule.rule_id, 'PROVED_WITH_REGISTERED_RULES')