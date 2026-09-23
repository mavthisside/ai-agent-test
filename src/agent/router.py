import re
from dataclasses import dataclass
from src.agent.session import SessionState


@dataclass
class Route:
    name: str
    order_id: str | None = None
    needs_handoff: bool = False
    reason: str | None = None


ORDER_ID_PATTERN = re.compile(r"\bORD-\d{4}\b", re.IGNORECASE)


def extract_order_id(text: str) -> str | None:
    match = ORDER_ID_PATTERN.search(text)
    if match:
        return match.group(0).upper()
    return None


def route_message(message: str, session: SessionState) -> Route:
    text = message.lower()
    order_id = extract_order_id(message)

    if order_id:
        session.active_order_id = order_id

    privacy_terms = [
        "email",
        "address",
        "internal note",
        "risk score",
        "fraud review",
    ]

    if any(term in text for term in privacy_terms):
        if session.active_order_id or order_id:
            return Route(
                name="ORDER",
                order_id=session.active_order_id,
                needs_handoff=True,
                reason="private_order_data",
            )

    order_terms = [
        "order",
        "tracking",
        "where is",
        "arrive",
        "delivery",
        "shipped",
        "carrier",
        "status",
    ]

    mentions_order = (
        order_id is not None
        or any(
            re.search(rf"\b{re.escape(term)}\b", text)
            for term in order_terms
        )
    )

    if mentions_order:
        if session.active_order_id is None:
            return Route(
                name="CLARIFY",
                reason="missing_order_id",
            )

        policy_terms = [
            "return",
            "refund",
            "warranty",
            "cancel",
            "eligible",
            "policy",
        ]

        if any(term in text for term in policy_terms):
            return Route(
                name="ORDER_POLICY",
                order_id=session.active_order_id,
            )

        return Route(
            name="ORDER",
            order_id=session.active_order_id,
        )

    insufficient_terms = [
        "vegan",
        "vegan guarantee",
        "material certification",
    ]

    if any(term in text for term in insufficient_terms):
        return Route(
            name="ABSTAIN",
            needs_handoff=True,
            reason="insufficient_information",
        )

    return Route(name="POLICY")