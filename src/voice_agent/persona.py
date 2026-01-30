from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class PersonaType(str, Enum):
    LISTING_CONCIERGE = "listing_concierge"
    LEAD_QUALIFIER = "lead_qualifier"
    SHOWING_SCHEDULER = "showing_scheduler"
    FOLLOW_UP_AGENT = "follow_up_agent"
    OPEN_HOUSE_HOST = "open_house_host"
    LISTING_ASSISTANT = "listing_assistant"
    RENTAL_AGENT = "rental_agent"


class VoiceSettings(BaseModel):
    provider: str = "openai"
    voice_id: str = "alloy"
    speed: float = 1.0


class Personality(BaseModel):
    tone: str = "warm"
    formality: str = "professional"
    verbosity: str = "concise"
    empathy_level: str = "high"


class QualificationQuestion(BaseModel):
    key: str
    question: str
    required: bool = True
    options: Optional[List[str]] = None


class Persona(BaseModel):
    id: str
    name: str
    type: PersonaType
    description: Optional[str] = None

    voice_settings: VoiceSettings
    personality: Personality

    system_prompt: str
    greeting: str

    capabilities: List[str]
    channels_enabled: List[str]

    qualification_questions: List[QualificationQuestion]

    fair_housing_enabled: bool = True
    recording_disclosure: bool = True

    escalation_triggers: List[str] = []


def load_persona_from_dict(data: dict) -> Persona:
    """Create a `Persona` from a plain dict (e.g., parsed JSON/YAML)."""
    return Persona.model_validate(data)


def load_persona_from_json_file(path: str) -> Persona:
    import json

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return load_persona_from_dict(data)
