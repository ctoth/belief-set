from __future__ import annotations

import math
from collections.abc import MutableMapping
from typing import cast

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from belief_set import SpohnEpistemicState, World
from belief_set.core import BeliefSet


def test_spohn_state_ranks_are_read_only_after_construction() -> None:
    alphabet = frozenset({"p"})
    state = SpohnEpistemicState.from_ranks(
        alphabet,
        {
            frozenset(): 0,
            frozenset({"p"}): 1,
        },
    )

    with pytest.raises(TypeError):
        cast(MutableMapping[World, int | float], state.ranks)[frozenset()] = 99


def test_spohn_state_rejects_negative_ranks() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        SpohnEpistemicState.from_ranks(
            frozenset({"p"}),
            {
                frozenset(): -1,
                frozenset({"p"}): 0,
            },
        )


def test_spohn_state_rejects_nan_ranks() -> None:
    with pytest.raises(ValueError, match="NaN"):
        SpohnEpistemicState.from_ranks(
            frozenset({"p"}),
            {
                frozenset(): math.nan,
                frozenset({"p"}): 0,
            },
        )


def test_spohn_state_rejects_missing_worlds() -> None:
    with pytest.raises(ValueError, match="cover every world"):
        SpohnEpistemicState.from_ranks(
            frozenset({"p"}),
            {
                frozenset(): 0,
            },
        )


@pytest.mark.property
@given(
    st.dictionaries(
        st.sampled_from(tuple(BeliefSet.all_worlds(frozenset({"p", "q"})))),
        st.integers(min_value=0, max_value=9),
        min_size=4,
        max_size=4,
    ),
)
@settings(deadline=None)
def test_finite_spohn_state_normalization_preserves_zero_minimum(
    ranks: dict[World, int],
) -> None:
    state = SpohnEpistemicState.from_ranks(frozenset({"p", "q"}), ranks)

    assert min(state.ranks.values()) == 0
