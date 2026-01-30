import pytest
from voice_agent.services.async_ai_engine import AsyncAIEngine
from voice_agent.persona import load_persona_from_dict
import os


def sample_persona_dict():
    return {
        "id": "p1",
        "name": "Listing Concierge",
        "type": "listing_concierge",
        "voice_settings": {"provider": "openai", "voice_id": "alloy", "speed": 1.0},
        "personality": {"tone": "warm", "formality": "professional", "verbosity": "concise", "empathy_level": "high"},
        "system_prompt": "You are a helpful real estate assistant. Help answer questions about properties.",
        "greeting": "Hi! How can I help with your property search?",
        "capabilities": ["answer_property_questions"],
        "channels_enabled": ["voice"],
        "qualification_questions": [],
        "fair_housing_enabled": True,
        "recording_disclosure": True,
        "escalation_triggers": ["speak to agent", "human"]
    }


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OpenAI API key not set")
@pytest.mark.asyncio
async def test_async_greeting():
    persona = load_persona_from_dict(sample_persona_dict())
    engine = AsyncAIEngine(persona, api_key=os.getenv("OPENAI_API_KEY"))
    greeting = await engine.get_greeting()
    assert greeting == "Hi! How can I help with your property search?"


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OpenAI API key not set")
@pytest.mark.asyncio
async def test_async_process_escalation():
    persona = load_persona_from_dict(sample_persona_dict())
    engine = AsyncAIEngine(persona, api_key=os.getenv("OPENAI_API_KEY"))
    resp = await engine.process("I want to speak to a human")
    assert "escalate_to_human" in resp.actions


@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OpenAI API key not set")
@pytest.mark.asyncio
async def test_async_process_schedule_detection():
    persona = load_persona_from_dict(sample_persona_dict())
    engine = AsyncAIEngine(persona, api_key=os.getenv("OPENAI_API_KEY"))
    resp = await engine.process("Can I schedule a showing?")
    assert "schedule_showing" in resp.actions
