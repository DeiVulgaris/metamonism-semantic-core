from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

R = TypeVar("R")
A = TypeVar("A")

@dataclass(frozen=True)
class ContinuationResult(Generic[A]):
    next_argument: A
    in_domain: bool
    canonical_root_preserved: bool

def continuation_step(
    result: R,
    build_next_argument: Callable[[R], A],
    is_in_domain: Callable[[A], bool],
    root_preserved: Callable[[R, A], bool],
) -> ContinuationResult[A]:
    next_argument = build_next_argument(result)
    return ContinuationResult(
        next_argument=next_argument,
        in_domain=is_in_domain(next_argument),
        canonical_root_preserved=root_preserved(result, next_argument),
    )
