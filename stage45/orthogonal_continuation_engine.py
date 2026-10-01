from dataclasses import dataclass
from typing import Callable, Iterable, Optional


@dataclass(frozen=True)
class ConstrainedState:
    state_id: str
    regime: str
    need_continue: bool = True


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    regime: str


@dataclass(frozen=True)
class ResolutionCandidate:
    candidate_id: str
    from_state: str
    new_regime: str
    orthogonal_resolution: bool
    orientation_before: Optional[str] = None
    orientation_after: Optional[str] = None


def d_perp(
    state: ConstrainedState,
    candidates: Iterable[Candidate],
    continue_predicate: Callable[[ConstrainedState, Candidate], bool],
    orthogonality_predicate: Callable[[ConstrainedState, Candidate], bool],
) -> list[Candidate]:
    """Return candidates satisfying both continuation and orthogonality."""
    return [
        candidate
        for candidate in candidates
        if candidate.regime == state.regime
        and continue_predicate(state, candidate)
        and orthogonality_predicate(state, candidate)
    ]


def is_exhausted(feasible_candidates: Iterable[Candidate]) -> bool:
    return len(list(feasible_candidates)) == 0


def is_frustrated(
    state: ConstrainedState,
    feasible_candidates: Iterable[Candidate],
) -> bool:
    return state.need_continue and is_exhausted(feasible_candidates)


def validate_resolution(candidate: ResolutionCandidate) -> list[str]:
    errors: list[str] = []

    if not candidate.orthogonal_resolution:
        errors.append("resolution is not marked as orthogonal")

    if candidate.orientation_before is not None or candidate.orientation_after is not None:
        if candidate.orientation_before != "+n" or candidate.orientation_after != "-n":
            errors.append("source-grounded P3->P4 orientation pattern must be +n -> -n")

    if candidate.from_state != "P3":
        errors.append("this demonstrator validates the Chapter 3 P3 -> P4 pattern only")

    if candidate.new_regime == "":
        errors.append("new_regime must be explicit")

    return errors


def demonstrate_p3_constraint(
    candidates: Iterable[Candidate],
    continue_predicate: Callable[[ConstrainedState, Candidate], bool],
    orthogonality_predicate: Callable[[ConstrainedState, Candidate], bool],
) -> dict:
    state = ConstrainedState("P3", "R_old", True)
    feasible = d_perp(state, candidates, continue_predicate, orthogonality_predicate)
    return {
        "state": state.state_id,
        "regime": state.regime,
        "D_perp": [x.candidate_id for x in feasible],
        "exhausted": len(feasible) == 0,
        "frustrated": state.need_continue and len(feasible) == 0,
    }
