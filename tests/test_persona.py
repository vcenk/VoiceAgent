from voice_agent.persona import (
    Persona,
    PersonaType,
    VoiceSettings,
    Personality,
    QualificationQuestion,
    load_persona_from_dict,
)


def make_sample_persona_dict() -> dict:
    return {
        "id": "listing_concierge_default",
        "name": "Listing Concierge",
        "type": "listing_concierge",
        "description": "Handles inbound property inquiries",
        "voice_settings": {"provider": "openai", "voice_id": "alloy", "speed": 1.0},
        "personality": {"tone": "warm", "formality": "professional", "verbosity": "concise", "empathy_level": "high"},
        "system_prompt": "You are a helpful agent.",
        "greeting": "Hi! How can I help?",
        "capabilities": ["answer_property_questions", "schedule_showings"],
        "channels_enabled": ["voice", "chat", "whatsapp"],
        "qualification_questions": [
            {"key": "working_with_agent", "question": "Are you working with an agent?", "required": True, "options": ["Yes", "No"]}
        ],
        "fair_housing_enabled": True,
        "recording_disclosure": True,
        "escalation_triggers": ["speak to agent", "talk to human"]
    }


def test_persona_parse_and_fields():
    d = make_sample_persona_dict()
    persona = load_persona_from_dict(d)

    assert isinstance(persona, Persona)
    assert persona.id == d["id"]
    assert persona.type == PersonaType.LISTING_CONCIERGE
    assert persona.voice_settings.voice_id == "alloy"
    assert persona.personality.tone == "warm"
    assert len(persona.qualification_questions) == 1
