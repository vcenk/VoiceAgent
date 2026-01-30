from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from typing import Optional
from voice_agent.services.persona_service import PersonaService
from voice_agent.services.async_ai_engine import AsyncAIEngine
import json

router = APIRouter()


@router.websocket("/ws/{conversation_id}")
async def chat_websocket(websocket: WebSocket, conversation_id: str, persona_id: Optional[str] = Query(None)):
    """WebSocket endpoint for real-time chat using the local AIEngine stub.

    Query param `persona_id` chooses which persona to load (defaults to listing template).
    """
    await websocket.accept()

    persona_service = PersonaService()
    pid = persona_id or "listing_concierge_default"
    persona = persona_service.get(pid)
    if persona is None:
        await websocket.send_json({"type": "error", "detail": "persona_not_found"})
        await websocket.close()
        return

    ai = AsyncAIEngine(persona, channel="chat")

    # Send greeting
    greeting = await ai.get_greeting()
    await websocket.send_json({
        "type": "message",
        "role": "assistant",
        "content": greeting,
    })

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                msg = json.loads(raw)
            except Exception:
                await websocket.send_json({"type": "error", "detail": "invalid_json"})
                continue

            if msg.get("type") == "message":
                user_text = msg.get("content", "")
                resp = await ai.process(user_text)
                await websocket.send_json({
                    "type": "message",
                    "role": "assistant",
                    "content": resp.text,
                    "actions": resp.actions,
                })
            elif msg.get("type") == "end":
                await websocket.send_json({"type": "info", "detail": "conversation_ended"})
                await websocket.close()
                break

    except WebSocketDisconnect:
        return
