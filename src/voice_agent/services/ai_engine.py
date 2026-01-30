from __future__ import annotations
from typing import List, Optional

from voice_agent.persona import Persona


class AIResponse:
    def __init__(self, text: str, rich_content: Optional[dict] = None, actions: Optional[List[str]] = None):
        self.text = text
        self.rich_content = rich_content or {}
        self.actions = actions or []


class AIEngine:
    """Minimal AI engine stub that uses a `Persona` to generate greetings and
    rule-based responses. This is intentionally small and synchronous to
    facilitate unit testing and local dev without external LLMs.
    """

    def __init__(self, persona: Persona):
        self.persona = persona

    def get_greeting(self) -> str:
        # Personalize greeting if persona provides it
        try:
            return self.persona.greeting
        except Exception:
            return "Hello. How can I help?"

    def _should_escalate(self, user_input: str) -> bool:
        lower = user_input.lower()
        return any(trigger in lower for trigger in self.persona.escalation_triggers)

    def _detect_actions(self, user_input: str, response_text: str) -> List[str]:
        combined = f"{user_input} {response_text}".lower()
        actions: List[str] = []
        if any(w in combined for w in ["schedule", "showing", "tour", "visit", "see it"]):
            actions.append("schedule_showing")
        if any(w in combined for w in ["price", "cost", "how much", "price of"]):
            actions.append("provide_pricing")
        return actions

    def process(self, user_input: str) -> AIResponse:
        # Escalation check
        if self._should_escalate(user_input):
            return AIResponse(
                text="I'm connecting you to a human agent now.",
                actions=["escalate_to_human"],
            )

        # Simple echo-like reply using persona tone
        text = f"{self.persona.name}: "
        if isinstance(self.persona, Persona) and self.persona.personality.verbosity == "concise":
            text += (user_input if len(user_input.split()) < 10 else user_input.split(" ")[:10])
            if isinstance(text, list):
                text = " ".join(text)
        else:
            text += f"Thanks for your message. {user_input}"

        actions = self._detect_actions(user_input, text)

        return AIResponse(text=text, actions=actions)
