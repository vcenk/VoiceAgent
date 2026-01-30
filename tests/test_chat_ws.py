from fastapi.testclient import TestClient
from app.main import app
import json


client = TestClient(app)


def test_chat_websocket_greeting_and_reply():
    with client.websocket_connect("/api/v1/chat/ws/conv1?persona_id=listing_concierge_default") as ws:
        # Receive greeting
        greeting = ws.receive_json()
        assert greeting["type"] == "message"
        assert greeting["role"] == "assistant"

        # Send user message that should trigger scheduling action
        ws.send_text(json.dumps({"type": "message", "content": "Can I schedule a showing?"}))
        resp = ws.receive_json()
        assert resp["type"] == "message"
        assert "assistant" == resp["role"]
        # actions should include schedule_showing
        assert "schedule_showing" in resp.get("actions", [])
