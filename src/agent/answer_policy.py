from src.rag.chunker import Chunk


def is_return_question(query: str) -> bool:
    return "return" in query.lower()


def select_evidence(
    query: str,
    results: list[tuple[Chunk, float]],
    membership_tier: str | None = None,
) -> list[tuple[Chunk, float]]:

    if not results:
        return []

    query_lower = query.lower()

    # Return-policy questions need special handling because
    # TrailPlus and standard customers have different return windows.

    if not is_return_question(query):
        return results

    # Explicit TrailPlus mention in the current question should
    # take priority even if the session does not yet know the
    # customer's membership tier.
    if (
        membership_tier == "trailplus"
        or "trailplus" in query_lower
    ):
        preferred = [
            result
            for result in results
            if (
                "trailplus" in result[0].document_filename.lower()
                or "trailplus"
                in (result[0].metadata.get("heading") or "").lower()
            )
        ]

        if preferred:
            return preferred

    # If membership is unknown, prefer the current standard
    # return policy rather than assuming TrailPlus.
    standard = [
        result
        for result in results
        if (
            result[0].document_filename
            == "01-returns-policy-current.md"
            and "standard return window"
            in (
                result[0].metadata.get("heading") or ""
            ).lower()
        )
    ]

    if standard:
        return standard

    return results