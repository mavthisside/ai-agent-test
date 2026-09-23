from src.rag.query import build_search_query


def test_standard_membership_query():
    result = build_search_query(
        "Can I return this after 20 days?",
        membership_tier="standard",
    )

    assert result.membership_context == "standard"
    assert "standard" in result.search_query.lower()


def test_trailplus_membership_query():
    result = build_search_query(
        "What is my TrailPlus return window?",
    )

    assert result.membership_context == "trailplus"
    assert "trailplus" in result.search_query.lower()


def test_unknown_membership_does_not_assume():
    result = build_search_query(
        "Can I return this after 20 days?",
    )

    assert result.membership_context is None