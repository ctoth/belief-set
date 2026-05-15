from __future__ import annotations


def test_package_imports() -> None:
    import belief_set

    assert set(belief_set.__all__) == {
        "AlphabetBudgetExceeded",
        "BOTTOM",
        "TOP",
        "Atom",
        "BeliefSet",
        "EnumerationExceeded",
        "EpistemicEntrenchment",
        "Formula",
        "ICMergeOperator",
        "ICMergeOutcome",
        "ICMergeProfileMemberInconsistent",
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
        "merge_belief_profile",
        "negate",
        "restrained_revise",
        "revise",
        "theory_subset",
    }


def test_package_exports_are_importable_from_root() -> None:
    from belief_set import (  # noqa: PLC0415
        AlphabetBudgetExceeded,
        EnumerationExceeded,
        EpistemicEntrenchment,
        ICMergeOperator,
        ICMergeOutcome,
        ICMergeProfileMemberInconsistent,
        merge_belief_profile,
    )

    assert AlphabetBudgetExceeded.__name__ == "AlphabetBudgetExceeded"
    assert EnumerationExceeded.__name__ == "EnumerationExceeded"
    assert EpistemicEntrenchment.__name__ == "EpistemicEntrenchment"
    assert ICMergeOperator.SIGMA == "sigma"
    assert ICMergeOperator.MAX == "max"
    assert ICMergeOutcome.__name__ == "ICMergeOutcome"
    assert ICMergeProfileMemberInconsistent.__name__ == "ICMergeProfileMemberInconsistent"
    assert callable(merge_belief_profile)


def test_cn_is_extensional_closure_identity() -> None:
    from belief_set import Atom, BeliefSet, conjunction  # noqa: PLC0415

    p = Atom("p")
    q = Atom("q")
    belief_set = BeliefSet.from_formula(frozenset({"p", "q"}), conjunction(p, q))

    assert belief_set.cn() is belief_set
    assert belief_set.cn().equivalent(belief_set)
    assert belief_set.cn().cn() is belief_set
