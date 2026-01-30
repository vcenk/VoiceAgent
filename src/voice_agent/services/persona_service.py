from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Optional

from voice_agent.persona import Persona, load_persona_from_dict


class PersonaService:
    """Simple Persona service that loads personas from disk and caches them.

    Personas are expected under `data/personas/*.json`.
    This is intentionally minimal — replace with DB-backed repository later.
    """

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path.cwd() / "data" / "personas"
        self._cache: Dict[str, Persona] = {}

    def list_persona_files(self):
        return sorted(self.data_dir.glob("*.json"))

    def load_all(self) -> Dict[str, Persona]:
        if not self.data_dir.exists():
            return {}

        for p in self.list_persona_files():
            try:
                with open(p, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                persona = load_persona_from_dict(data)
                self._cache[persona.id] = persona
            except Exception:
                # skip invalid files
                continue

        return self._cache

    def get(self, persona_id: str) -> Optional[Persona]:
        # Return from cache if available
        if persona_id in self._cache:
            return self._cache[persona_id]

        # Otherwise attempt to load from disk
        path = self.data_dir / f"{persona_id}.json"
        if not path.exists():
            return None

        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)

        persona = load_persona_from_dict(data)
        self._cache[persona.id] = persona
        return persona
