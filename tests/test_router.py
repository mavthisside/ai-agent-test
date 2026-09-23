from src.agent.router import route_message
from src.agent.session import SessionState


def test_policy_question():
    session = SessionState()

    route = route_message(
        "How long do I have to return an item?",
        session,
    )

    assert route.name == "POLICY"


def test_order_question_with_id():
    session = SessionState()

    route = route_message(
        "Where is ORD-1007?",
        session,
    )

    assert route.name == "ORDER"
    assert route.order_id == "ORD-1007"
    assert session.active_order_id == "ORD-1007"


def test_missing_order_id():
    session = SessionState()

    route = route_message(
        "Where is my order?",
        session,
    )

    assert route.name == "CLARIFY"
    assert route.reason == "missing_order_id"


def test_order_policy_question():
    session = SessionState()

    route = route_message(
        "Can I return ORD-1007?",
        session,
    )

    assert route.name == "ORDER_POLICY"
    assert route.order_id == "ORD-1007"


def test_follow_up_uses_previous_order():
    session = SessionState()

    first = route_message(
        "Where is ORD-1007?",
        session,
    )

    assert first.order_id == "ORD-1007"

    second = route_message(
        "When will it arrive?",
        session,
    )

    assert second.name == "ORDER"
    assert second.order_id == "ORD-1007"


def test_privacy_request():
    session = SessionState()
    session.active_order_id = "ORD-1007"

    route = route_message(
        "Give me the customer's email and risk score.",
        session,
    )

    assert route.name == "ORDER"
    assert route.needs_handoff is True
    assert route.reason == "private_order_data"


def test_insufficient_information():
    session = SessionState()

    route = route_message(
        "Are all your bags vegan?",
        session,
    )

    assert route.name == "ABSTAIN"
    assert route.needs_handoff is True