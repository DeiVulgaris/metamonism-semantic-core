# Selection Policy Specification

The selector operates only on already generated READY tasks.

USER_SELECTED requires an explicit task ID.

DEPENDENCY_FIRST chooses the lowest externally supplied dependency_depth.

BLOCKER_FIRST chooses the greatest externally supplied blocker_reduction.

CHEAPEST_TEST_FIRST chooses the lowest externally supplied estimated_cost among TEST tasks.

INFORMATION_GAIN chooses the greatest externally supplied expected_information_gain.

PARALLEL_BRANCHING selects all tasks explicitly marked eligible_for_parallel_branching.

The metrics are policy inputs, not semantic conclusions. If a required metric is absent, selection is blocked rather than guessed.

Tie-breaking is lexicographic task ID.

Selection never changes epistemic status, frontier state, task meaning, or competing candidates.
