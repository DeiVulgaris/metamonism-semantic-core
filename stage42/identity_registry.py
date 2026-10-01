"""Stage 42: explicit identity and continuity registry."""

from dataclasses import dataclass, field

RELATIONS = {
    "IDENTITY_EQUIVALENCE", "ALIAS", "VERSION_CONTINUATION",
    "DERIVATION", "FORK", "MERGE", "UNRESOLVED_IDENTITY",
}
STATUSES = {"PROPOSED", "ASSERTED", "REJECTED", "UNRESOLVED"}

@dataclass(frozen=True)
class IdentityMapping:
    mapping_id: str
    left_ref: str
    right_ref: str
    relation_type: str
    assertion_status: str
    scope: str
    evidence: list[str] = field(default_factory=list)
    provenance: dict[str, str] = field(default_factory=dict)
    derived_from: list[str] = field(default_factory=list)
    notes: str = ""

class IdentityRegistry:
    """Append-only registry. It never infers identity from labels."""

    def __init__(self):
        self._mappings = {}

    def register(self, mapping: IdentityMapping):
        if mapping.mapping_id in self._mappings:
            raise ValueError("mapping_id already exists")
        self._validate(mapping)
        self._mappings[mapping.mapping_id] = mapping

    @staticmethod
    def _validate(m):
        if not m.left_ref or not m.right_ref:
            raise ValueError("identity references are required")
        if m.relation_type not in RELATIONS:
            raise ValueError("invalid identity relation")
        if m.assertion_status not in STATUSES:
            raise ValueError("invalid assertion status")
        for key in ("repository", "path", "ref", "locator"):
            if not m.provenance.get(key):
                raise ValueError("incomplete provenance")
        if m.assertion_status == "ASSERTED":
            if not m.evidence or not m.derived_from:
                raise ValueError("asserted identity requires evidence and derived_from")
        if m.relation_type == "UNRESOLVED_IDENTITY" and m.assertion_status == "ASSERTED":
            raise ValueError("unresolved identity cannot be asserted")

    def resolve(self, ref, asserted_only=True):
        return [
            m for m in self._mappings.values()
            if ref in (m.left_ref, m.right_ref)
            and (not asserted_only or m.assertion_status == "ASSERTED")
        ]

    def unresolved(self, ref):
        return bool(self.resolve(ref, asserted_only=False)) and not bool(self.resolve(ref))

    def all(self):
        return list(self._mappings.values())
