from dataclasses import dataclass


@dataclass
class SearchQuery:
    original_query: str
    search_query: str
    membership_context: str | None


def build_search_query(
    query: str,
    membership_tier: str | None = None,
) -> SearchQuery:

    query_lower = query.lower()

    # Explicit TrailPlus context.
    if (
        membership_tier == "trailplus"
        or "trailplus" in query_lower
    ):
        return SearchQuery(
            original_query=query,
            search_query="TrailPlus return window membership return policy",
            membership_context="trailplus",
        )

    # Explicit standard context.
    if (
        membership_tier == "standard"
        or "standard plan" in query_lower
    ):
        return SearchQuery(
            original_query=query,
            search_query="standard return window returns policy",
            membership_context="standard",
        )

    # No membership information was provided.
    # Keep the query broad rather than assuming membership status.
    if "return" in query_lower:
        return SearchQuery(
            original_query=query,
            search_query="return eligibility return window",
            membership_context=None,
        )

    return SearchQuery(
        original_query=query,
        search_query=query,
        membership_context=None,
    )