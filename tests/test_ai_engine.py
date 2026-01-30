from voice_agent.services.ai_engine import AIEngine
from voice_agent.persona import load_persona_from_dict


def sample_persona_dict():
    return {
        "id": "p1",
        "name": "Listing Concierge",
        "type": "listing_concierge",
        "voice_settings": {"provider": "openai", "voice_id": "alloy", "speed": 1.0},
        "personality": {"tone": "warm", "formality": "professional", "verbosity": "concise", "empathy_level": "high"},
        "system_prompt": "You are helpful.",
        "greeting": "Hi there!",
        "capabilities": ["answer_property_questions"],
        "channels_enabled": ["voice"],
        "qualification_questions": [],
        "fair_housing_enabled": True,
        "recording_disclosure": True,
        "escalation_triggers": ["speak to agent", "human"]
    }


def test_greeting_uses_persona():
    persona = load_persona_from_dict(sample_persona_dict())
    engine = AIEngine(persona)
    assert engine.get_greeting() == "Hi there!"


def test_escalation_detection():
    persona = load_persona_from_dict(sample_persona_dict())
    engine = AIEngine(persona)
    resp = engine.process("I want to speak to a human now")
    assert "escalate_to_human" in resp.actions


def test_schedule_detection():
    persona = load_persona_from_dict(sample_persona_dict())
    engine = AIEngine(persona)
    resp = engine.process("Can I schedule a showing for this property?")
    assert "schedule_showing" in resp.actions
