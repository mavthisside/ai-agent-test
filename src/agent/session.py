from dataclasses import dataclass, field


@dataclass
class Message:
    role: str
    content: str


@dataclass
class SessionState:
    messages: list[Message] = field(default_factory=list)

    # Useful context that can carry between turns.
    active_order_id: str | None = None
    membership_tier: str | None = None
    current_topic: str | None = None
    current_country: str | None = None

    def add_message(self, role: str, content: str) -> None:
        self.messages.append(
            Message(
                role=role,
                content=content,
            )
        )

    def recent_messages(self, limit: int = 6) -> list[Message]:
        return self.messages[-limit:]