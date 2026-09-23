from src.agent.session import SessionState


def test_session_stores_messages():
    session = SessionState()

    session.add_message(
        "user",
        "Where is my order?",
    )

    session.add_message(
        "assistant",
        "Please provide your order ID.",
    )

    assert len(session.messages) == 2
    assert session.messages[0].content == "Where is my order?"
    assert session.messages[1].role == "assistant"


def test_session_stores_order_context():
    session = SessionState()

    session.active_order_id = "ORD-1007"

    assert session.active_order_id == "ORD-1007"


def test_session_stores_topic_context():
    session = SessionState()

    session.current_topic = "international_shipping"
    session.current_country = "Canada"

    assert session.current_topic == "international_shipping"
    assert session.current_country == "Canada"


def test_recent_messages_limits_history():
    session = SessionState()

    for number in range(10):
        session.add_message(
            "user",
            f"message {number}",
        )

    recent = session.recent_messages(limit=3)

    assert len(recent) == 3
    assert recent[0].content == "message 7"
    assert recent[-1].content == "message 9"