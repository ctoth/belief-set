from __future__ import annotations


def test_package_imports() -> None:
    import belief_set

    assert set(belief_set.__all__) == {
        "BOTTOM",
        "TOP",
        "Atom",
        "BeliefSet",
        "Formula",
        "RevisionOutcome",
        "RevisionTrace",
        "SpohnEpistemicState",
        "World",
        "conjunction",
        "disjunction",
        "equivalent",
        "expand",
        "full_meet_contract",
        "lexicographic_revise",
        "negate",
        "restrained_revise",
        "revise",
        "theory_subset",
    }
