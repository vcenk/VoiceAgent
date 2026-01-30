from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
import json
import base64
from voice_agent.services.stt_stub import DeepgramSTT
from voice_agent.services.tts_stub import OpenAITTS
from voice_agent.services.persona_service import PersonaService
from voice_agent.services.async_ai_engine import AsyncAIEngine
from app.config import settings

router = APIRouter()


@router.post("/incoming")
async def handle_incoming_call(request: Request):
    """Minimal incoming voice webhook returning TwiML XML greeting."""
    form = await request.form()
    from_number = form.get("From", "")

    body = f"<Response><Say voice=\"alice\">Please wait while I connect you, caller {from_number}.</Say></Response>"
    return Response(content=body, media_type="application/xml")


@router.websocket("/stream")
async def voice_stream(websocket: WebSocket):
    """WebSocket endpoint that accepts Twilio Media Stream-like JSON events.

    - On `start` event: initialize STT, TTS, and AI engine and send a welcome TTS audio
    - On `media` event: transcribe chunk, process via AIEngine, synthesize audio, and send media back
    """
    await websocket.accept()

    stt = DeepgramSTT(api_key=settings.DEEPGRAM_API_KEY)
    tts = OpenAITTS(api_key=settings.OPENAI_API_KEY)
    persona_service = PersonaService()
    ai_engine = None

    try:
        async for raw in websocket.iter_text():
            try:
                message = json.loads(raw)
            except Exception:
                await websocket.send_json({"event": "error", "detail": "invalid_json"})
                continue

            event = message.get("event")

            if event == "start":
                # Determine persona if provided
                custom = message.get("start", {}).get("customParameters", {})
                persona_id = custom.get("persona_id", "listing_concierge_default")
                persona = persona_service.get(persona_id)
                if persona is None:
                    await websocket.send_json({"event": "error", "detail": "persona_not_found"})
                    continue

                ai_engine = AsyncAIEngine(persona, channel="voice")
                greeting = await ai_engine.get_greeting()
                audio = await tts.synthesize(greeting)
                payload = base64.b64encode(audio).decode()
                await websocket.send_json({"event": "media", "media": {"payload": payload}})

            elif event == "media":
                # media payload is base64 encoded audio
                payload_b64 = message.get("media", {}).get("payload")
                if not payload_b64:
                    continue
                audio_bytes = base64.b64decode(payload_b64)

                # Transcribe
                transcript = await stt.transcribe_chunk(audio_bytes)
                if transcript and transcript.is_final and ai_engine:
                    response = await ai_engine.process(transcript.text)
                    audio = await tts.synthesize(response.text)
                    payload = base64.b64encode(audio).decode()
                    await websocket.send_json({"event": "media", "media": {"payload": payload}})

            elif event == "stop":
                break

    except WebSocketDisconnect:
        pass
    finally:
        await stt.close()
