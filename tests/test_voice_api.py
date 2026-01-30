from fastapi.testclient import TestClient
from app.main import app
import json


client = TestClient(app)


def test_incoming_call_returns_xml():
    resp = client.post(
        "/api/v1/voice/incoming",
        data={"From": "+15551234567", "CallSid": "CA123"},
    )

    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("application/xml")
    assert "Please wait while I connect you" in resp.text


def test_voice_stream_websocket_echo():
    # Connect and send start event to get greeting audio
    with client.websocket_connect("/api/v1/voice/stream") as ws:
        start_msg = {"event": "start", "start": {"customParameters": {"persona_id": "listing_concierge_default"}}}
        ws.send_text(json.dumps(start_msg))
        data = ws.receive_json()
        # Should receive a media event with base64 payload
        assert data.get("event") == "media"
        assert "payload" in data.get("media", {})

        # Now send a media chunk (base64 of any bytes) and expect a TTS response
        import base64
        sample_audio = base64.b64encode(b"dummy-audio")
        media_msg = {"event": "media", "media": {"payload": sample_audio.decode()}}
        ws.send_text(json.dumps(media_msg))
        resp = ws.receive_json()
        assert resp.get("event") == "media"
        assert "payload" in resp.get("media", {})
