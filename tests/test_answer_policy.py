from src.agent.answer_policy import select_evidence
from src.rag.chunker import Chunk


def make_chunk(
    filename: str,
    heading: str,
) -> Chunk:

    return Chunk(
        chunk_id="test:0",
        document_filename=filename,
        metadata={
            "heading": heading,
        },
        content="test content",
    )


def test_standard_return_is_preferred_without_membership():

    results = [
        (
            make_chunk(
                "09-trailplus-membership.md",
                "Return window",
            ),
            0.95,
        ),
        (
            make_chunk(
                "01-returns-policy-current.md",
                "Standard return window",
            ),
            0.90,
        ),
    ]

    selected = select_evidence(
        "Can I return this after 20 days?",
        results,
    )

    assert len(selected) == 1

    assert (
        selected[0][0].document_filename
        == "01-returns-policy-current.md"
    )


def test_trailplus_return_is_preferred_for_trailplus_member():

    results = [
        (
            make_chunk(
                "01-returns-policy-current.md",
                "Standard return window",
            ),
            0.95,
        ),
        (
            make_chunk(
                "09-trailplus-membership.md",
                "Return window",
            ),
            0.90,
        ),
    ]

    selected = select_evidence(
        "Can I return this after 40 days?",
        results,
        membership_tier="trailplus",
    )

    assert len(selected) == 1

    assert (
        selected[0][0].document_filename
        == "09-trailplus-membership.md"
    )


def test_non_return_question_keeps_results():

    results = [
        (
            make_chunk(
                "05-domestic-shipping.md",
                "Delivery times",
            ),
            0.90,
        ),
        (
            make_chunk(
                "06-international-shipping.md",
                "Canada",
            ),
            0.80,
        ),
    ]

    selected = select_evidence(
        "How long does shipping take?",
        results,
    )

    assert len(selected) == 2