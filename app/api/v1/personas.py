from fastapi import APIRouter, HTTPException
from typing import Dict
from voice_agent.services.persona_service import PersonaService

router = APIRouter()

# Use PersonaService to load personas from data/personas/
_svc = PersonaService()


@router.get("/{persona_id}", response_model=Dict)
async def get_persona(persona_id: str):
    persona = _svc.get(persona_id)
    if persona is None:
        raise HTTPException(status_code=404, detail="persona not found")

    return persona.model_dump()
