from pathlib import Path

from voice_agent.services.persona_service import PersonaService


def test_persona_service_load_and_get(tmp_path: Path):
    # Copy sample persona into tmp dir to simulate data/personas
    personas_dir = tmp_path / "personas"
    personas_dir.mkdir(parents=True)

    sample = {
        "id": "test_persona",
        "name": "Test Persona",
        "type": "listing_concierge",
        "voice_settings": {"provider": "openai", "voice_id": "alloy", "speed": 1.0},
        "personality": {"tone": "warm", "formality": "professional", "verbosity": "concise", "empathy_level": "high"},
        "system_prompt": "Prompt",
        "greeting": "Hello",
        "capabilities": ["answer_property_questions"],
        "channels_enabled": ["voice"],
        "qualification_questions": [],
        "fair_housing_enabled": True,
        "recording_disclosure": True,
        "escalation_triggers": []
    }

    pfile = personas_dir / "test_persona.json"
    # write actual JSON
    import json
    pfile.write_text(json.dumps(sample))

    svc = PersonaService(data_dir=personas_dir)
    all_personas = svc.load_all()
    assert "test_persona" in all_personas

    p = svc.get("test_persona")
    assert p is not None
    assert p.id == "test_persona"
