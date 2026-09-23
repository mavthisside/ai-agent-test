import json

from src.agent.agent import Agent
from src.rag.document_loader import load_knowledge_base
from src.rag.chunker import chunk_documents


def create_agent():

    documents = load_knowledge_base(
        "knowledge-base"
    )

    chunks = chunk_documents(
        documents
    )

    return Agent(chunks)


def check_contains(
    response: str,
    required: list[str],
) -> list[str]:

    response_lower = response.lower()

    return [
        item
        for item in required
        if item.lower() not in response_lower
    ]


def check_forbidden(
    response: str,
    forbidden: list[str],
) -> list[str]:

    response_lower = response.lower()

    return [
        item
        for item in forbidden
        if item.lower() in response_lower
    ]


def check_sources(
    response: str,
    required_sources: list[str],
) -> list[str]:

    return [
        source
        for source in required_sources
        if source not in response
    ]


def evaluate_case(case: dict) -> dict:

    agent = create_agent()

    responses = []

    # Run every message in the case through
    # the SAME agent so multi-turn memory works.
    for message in case["messages"]:

        if message["role"] != "user":
            continue

        response = agent.handle_message(
            message["content"]
        )

        responses.append(response)

    full_response = "\n".join(responses)

    expect = case["expect"]

    missing = check_contains(
        full_response,
        expect.get("must_include", []),
    )

    forbidden = check_forbidden(
        full_response,
        expect.get("must_not_include", []),
    )

    missing_sources = check_sources(
        full_response,
        expect.get("required_sources", []),
    )

    expected_tool = expect.get("tool")
    expected_handoff = expect.get("handoff")

    actual_tool = agent.last_trace["tool_called"]
    actual_handoff = agent.last_trace["handoff"]

    if expected_tool is None:
        tool_pass = True

    elif expected_tool in {
        "not_called",
        "not_called_without_id",
    }:
        tool_pass = actual_tool is False

    elif expected_tool == "order_lookup":
        tool_pass = actual_tool is True

    elif expected_tool in {
        "optional",
        "optional_sanitized_lookup",
    }:
        tool_pass = True

    else:
        tool_pass = False

    handoff_pass = (
        expected_handoff is None
        or expected_handoff == actual_handoff
    )

    passed = (
        not missing
        and not forbidden
        and not missing_sources
        and tool_pass
        and handoff_pass
    )

    return {
        "id": case["id"],
        "passed": passed,
        "missing": missing,
        "forbidden": forbidden,
        "missing_sources": missing_sources,
        "expected_tool": expected_tool,
        "actual_tool": actual_tool,
        "expected_handoff": expected_handoff,
        "actual_handoff": actual_handoff,
        "route": agent.last_trace["route"],
        "response": full_response,
    }


def main():

    with open(
        "evaluation/visible-cases.json",
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    cases = data["cases"]

    results = []

    for case in cases:

        result = evaluate_case(case)

        results.append(result)

        status = (
            "PASS"
            if result["passed"]
            else "FAIL"
        )

        print(
            f"{status:4} | {result['id']}"
        )

    passed = sum(
        result["passed"]
        for result in results
    )

    total = len(results)

    print()
    print("=" * 60)
    print(f"RESULT: {passed}/{total}")
    print("=" * 60)

    print()

    for result in results:

        if result["passed"]:
            continue

        print(f"\n❌ {result['id']}")

        if result["missing"]:
            print(
                "   Missing:",
                result["missing"],
            )

        if result["forbidden"]:
            print(
                "   Forbidden:",
                result["forbidden"],
            )

        if result["missing_sources"]:
            print(
                "   Missing sources:",
                result["missing_sources"],
            )

        if (
            result["expected_tool"]
            not in (None, "optional")
        ):
            print(
                "   Tool:",
                result["expected_tool"],
                "→",
                result["actual_tool"],
            )

        if result["expected_handoff"] is not None:
            print(
                "   Handoff:",
                result["expected_handoff"],
                "→",
                result["actual_handoff"],
            )


if __name__ == "__main__":
    main()