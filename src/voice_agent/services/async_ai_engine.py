from __future__ import annotations
from typing import List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from voice_agent.persona import Persona
from voice_agent.services.ai_engine import AIResponse


class SimpleConversationMemory:
    """Simple conversation memory that stores messages."""

    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.messages: List[BaseMessage] = []

    def add_message(self, message: BaseMessage):
        self.messages.append(message)
        # Keep only last N messages
        if len(self.messages) > self.window_size * 2:
            self.messages = self.messages[-self.window_size:]

    def get_messages(self) -> List[BaseMessage]:
        return self.messages.copy()

    def clear(self):
        self.messages = []


class AsyncAIEngine:
    """Async AI engine using LangChain + OpenAI GPT-4o-mini.

    This replaces the simple rule-based engine with real LLM inference,
    providing context-aware, personalized responses based on the Persona.
    """

    def __init__(
        self,
        persona: Persona,
        api_key: Optional[str] = None,
        conversation_history_window: int = 10,
        channel: str = "voice",
    ):
        from app.config import settings

        self.persona = persona
        self.channel = channel
        self.api_key = api_key or settings.OPENAI_API_KEY

        # Lazy initialize LLM (avoid requiring API key at instantiation)
        self.llm = None
        self._llm_initialized = False

        # Conversation memory
        self.memory = SimpleConversationMemory(window_size=conversation_history_window)

        # Build prompt template (will be used with invoke/ainvoke)
        self.prompt_template = self._build_prompt()

    def _build_prompt(self) -> ChatPromptTemplate:
        """Build the LLM prompt template with persona context."""
        system_prompt = self.persona.system_prompt

        # Add channel-specific instructions
        if self.channel == "voice":
            system_prompt += "\n\nIMPORTANT: Keep responses brief (1-2 sentences) for natural conversation."
        elif self.channel == "chat":
            system_prompt += "\n\nYou can use rich formatting and suggest quick reply buttons when appropriate."

        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ])

    def _ensure_llm(self):
        """Lazy initialize the LLM on first use."""
        if self._llm_initialized:
            return
        try:
            self.llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.7,
                max_tokens=150 if self.channel == "voice" else 500,
                api_key=self.api_key,
            )
            self._llm_initialized = True
        except Exception as e:
            print(f"Failed to initialize LLM: {e}")
            raise

    def _should_escalate(self, user_input: str) -> bool:
        """Check if user wants human agent."""
        lower = user_input.lower()
        return any(trigger in lower for trigger in self.persona.escalation_triggers)

    def _detect_actions(self, user_input: str, response_text: str) -> List[str]:
        """Detect actionable intents from user input and response."""
        combined = f"{user_input} {response_text}".lower()
        actions: List[str] = []

        if any(w in combined for w in ["schedule", "showing", "tour", "visit", "see it"]):
            actions.append("schedule_showing")
        if any(w in combined for w in ["price", "cost", "how much"]):
            actions.append("provide_pricing")
        if any(w in combined for w in ["photo", "picture", "image"]):
            actions.append("send_photos")

        return actions

    async def get_greeting(self) -> str:
        """Return the persona's greeting."""
        return self.persona.greeting

    async def process(self, user_input: str) -> AIResponse:
        """Process user input and return an AI response using LangChain."""
        # Check for escalation triggers
        if self._should_escalate(user_input):
            return AIResponse(
                text="I'm connecting you to a human agent now.",
                actions=["escalate_to_human"],
            )

        try:
            self._ensure_llm()
            # Build chain and invoke with history
            chain = self.prompt_template | self.llm
            history = self.memory.get_messages()

            result = await chain.ainvoke({"input": user_input, "history": history})
            response_text = result.content if hasattr(result, 'content') else str(result)

            # Add to memory
            self.memory.add_message(HumanMessage(content=user_input))
            self.memory.add_message(AIMessage(content=response_text))
        except Exception as e:
            print(f"AsyncAIEngine error: {e}")
            response_text = "I'm having trouble processing that. Please try again."

        # Detect actions
        actions = self._detect_actions(user_input, response_text)

        return AIResponse(text=response_text, actions=actions)

    def add_to_memory(self, role: str, content: str):
        """Manually add a message to conversation memory."""
        if role == "user":
            self.memory.add_message(HumanMessage(content=content))
        else:
            self.memory.add_message(AIMessage(content=content))

    def clear_memory(self):
        """Clear conversation history."""
        self.memory.clear()
