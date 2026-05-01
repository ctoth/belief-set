from __future__ import annotations


def test_package_imports() -> None:
    import belief_set

    assert belief_set.__all__ == []
