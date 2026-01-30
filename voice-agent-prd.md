# Product Requirements Document (PRD) v3.0
# Multi-Channel Real Estate AI Agent Platform

**Version:** 3.0  
**Date:** January 30, 2025  
**Author:** Cenk  
**Status:** Draft

---

## 1. Executive Summary

### 1.1 Product Overview
A real-time multi-channel AI agent platform designed for real estate professionals. The system handles voice calls, website chat, WhatsApp, SMS, and social messaging to automate lead capture, qualification, and nurturing.

### 1.2 Tech Stack

#### Backend (Python)
| Component | Technology | Purpose |
|-----------|------------|---------|
| Framework | **FastAPI** | REST API + WebSocket server |
| AI Orchestration | **LangChain** | LLM chain management |
| Voice STT | **Deepgram Python SDK** | Speech-to-Text |
| Voice TTS | **OpenAI TTS** | Text-to-Speech |
| LLM | **OpenAI GPT-4o-mini** | Conversation AI |
| Telephony | **Twilio Python SDK** | Voice + SMS |
| Task Queue | **Celery + Redis** | Background jobs |
| WebSockets | **FastAPI WebSockets** | Real-time streaming |

#### Frontend (TypeScript)
| Component | Technology | Purpose |
|-----------|------------|---------|
| Framework | **Next.js 14** | Dashboard + API routes |
| UI Library | **shadcn/ui** | Component library |
| Styling | **Tailwind CSS** | Styling |
| State | **Zustand** | State management |
| Forms | **React Hook Form + Zod** | Form handling |
| Charts | **Recharts** | Analytics charts |

#### Database & Infrastructure
| Component | Technology | Purpose |
|-----------|------------|---------|
| Database | **Supabase (PostgreSQL)** | Primary database |
| Cache | **Redis** | Caching + pub/sub |
| File Storage | **Supabase Storage** | Media files |
| Hosting (API) | **Railway / Render** | FastAPI deployment |
| Hosting (Web) | **Vercel** | Next.js deployment |

### 1.3 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND                                        │
│                         Next.js (Vercel)                                    │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐               │
│  │   Dashboard     │ │   Chat Widget   │ │   Admin Panel   │               │
│  │   (React)       │ │   (Embeddable)  │ │   (React)       │               │
│  └────────┬────────┘ └────────┬────────┘ └────────┬────────┘               │
└───────────┼────────────────────┼────────────────────┼───────────────────────┘
            │                    │                    │
            └────────────────────┼────────────────────┘
                                 │ REST + WebSocket
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              BACKEND                                         │
│                      FastAPI (Railway/Render)                               │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         API LAYER                                    │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │   │
│  │  │  /voice  │ │  /chat   │ │ /whatsapp│ │  /sms    │ │  /admin  │  │   │
│  │  │ webhooks │ │ messages │ │ webhooks │ │ webhooks │ │  routes  │  │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      CHANNEL ADAPTERS                                │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │   │
│  │  │  Twilio  │ │ WebSocket│ │ WhatsApp │ │ Messenger│ │  Email   │  │   │
│  │  │  Voice   │ │   Chat   │ │  (Meta)  │ │  (Meta)  │ │(SendGrid)│  │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                       AI ENGINE                                      │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐                 │   │
│  │  │   LangChain  │ │   Deepgram   │ │  OpenAI TTS  │                 │   │
│  │  │  (LLM Chain) │ │    (STT)     │ │              │                 │   │
│  │  └──────────────┘ └──────────────┘ └──────────────┘                 │   │
│  │  ┌──────────────┐ ┌──────────────┐                                  │   │
│  │  │   Persona    │ │  RAG Engine  │                                  │   │
│  │  │   Manager    │ │ (Properties) │                                  │   │
│  │  └──────────────┘ └──────────────┘                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    BACKGROUND TASKS (Celery)                         │   │
│  │  • Drip campaigns  • MLS sync  • Analytics  • Reminders             │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DATA LAYER                                        │
│  ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐   │
│  │      Supabase       │ │       Redis         │ │   Supabase Storage  │   │
│  │    (PostgreSQL)     │ │   (Cache/Queue)     │ │      (Files)        │   │
│  └─────────────────────┘ └─────────────────────┘ └─────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.4 Cost Estimates

#### API Costs (Per Minute of Conversation)
| Service | Cost/min | Notes |
|---------|----------|-------|
| Deepgram (STT) | $0.0043 | Nova-2 model |
| OpenAI GPT-4o-mini | $0.002 | ~500 tokens/min |
| OpenAI TTS | $0.02 | ~150 words/min |
| Twilio Voice | $0.02 | Inbound + outbound |
| **Total** | **~$0.05** | Per minute |

#### Infrastructure Costs (Monthly)
| Service | Free Tier | Paid |
|---------|-----------|------|
| Vercel (Frontend) | ✅ Free | $20/mo |
| Railway (Backend) | $5 credit | ~$10-20/mo |
| Supabase (DB) | 500MB free | $25/mo |
| Redis (Upstash) | 10K cmds free | $10/mo |
| **Total** | **~$0-5/mo** | **~$50-75/mo** |

---

## 2. Supported Channels

### 2.1 Channel Overview

| Channel | Provider | Priority | Status |
|---------|----------|----------|--------|
| 📞 Voice Calls | Twilio | P0 | MVP |
| 💬 Website Chat | WebSocket | P0 | MVP |
| 📱 WhatsApp | Twilio/Meta | P0 | MVP |
| 📝 SMS | Twilio | P1 | v1.1 |
| 💭 Messenger | Meta | P1 | v1.1 |
| 📸 Instagram DM | Meta | P1 | v1.1 |
| 📧 Email | SendGrid | P2 | v1.2 |
| 🗺️ Google Business | Google | P2 | v1.2 |

### 2.2 Channel Feature Matrix

| Feature | Voice | Chat | WhatsApp | SMS | Messenger |
|---------|-------|------|----------|-----|-----------|
| Real-time | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| Rich Media | ❌ | ✅ | ✅ | ⚠️ MMS | ✅ |
| Buttons | ❌ | ✅ | ✅ | ❌ | ✅ |
| Carousels | ❌ | ✅ | ✅ | ❌ | ✅ |
| File Upload | ❌ | ✅ | ✅ | ✅ | ✅ |
| Proactive | ✅ | ⚠️ | ✅* | ✅* | ✅* |
| 24/7 | ✅ | ✅ | ✅ | ✅ | ✅ |

*Requires opt-in/templates

---

## 3. Real Estate Agent Personas

### 3.1 Persona Library

| Persona | Purpose | Channels | Priority |
|---------|---------|----------|----------|
| 🏠 Listing Concierge | Property inquiries | All | P0 |
| 🎯 Lead Qualifier | Screen & score leads | Voice, SMS, WhatsApp | P0 |
| 📅 Showing Scheduler | Book viewings | All | P0 |
| 🔄 Follow-Up Agent | Nurture leads | Voice, SMS, Email | P1 |
| 🏡 Open House Host | Event management | SMS, WhatsApp | P1 |
| 📋 Listing Assistant | Seller support | Voice, SMS | P2 |
| 🔑 Rental Agent | Tenant screening | All | P2 |

### 3.2 Persona Configuration

```python
# Python Pydantic Model
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

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
    tone: str = "warm"  # warm, professional, casual
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
    description: str
    
    # Voice
    voice_settings: VoiceSettings
    
    # Personality
    personality: Personality
    
    # Prompts
    system_prompt: str
    greeting: str
    
    # Capabilities
    capabilities: List[str]
    channels_enabled: List[str]
    
    # Qualification
    qualification_questions: List[QualificationQuestion]
    
    # Compliance
    fair_housing_enabled: bool = True
    recording_disclosure: bool = True
    
    # Escalation
    escalation_triggers: List[str] = [
        "speak to agent",
        "talk to human",
        "complaint"
    ]
```

### 3.3 Listing Concierge (Default Persona)

```python
LISTING_CONCIERGE = Persona(
    id="listing_concierge_default",
    name="Listing Concierge",
    type=PersonaType.LISTING_CONCIERGE,
    description="Handles inbound property inquiries across all channels",
    
    voice_settings=VoiceSettings(
        provider="openai",
        voice_id="alloy",
        speed=1.0
    ),
    
    personality=Personality(
        tone="warm",
        formality="professional",
        verbosity="concise",
        empathy_level="high"
    ),
    
    system_prompt="""You are a friendly and knowledgeable real estate assistant for {agent_name} at {brokerage_name}.

Your role is to help potential buyers learn about properties and schedule viewings.

CURRENT PROPERTY (if applicable):
{property_context}

GUIDELINES:
- Be warm, helpful, and professional
- Answer property questions accurately using the provided data
- If you don't know something, offer to have the agent follow up
- Always try to schedule a showing or capture contact information
- Mention unique selling points naturally
- Comply with Fair Housing laws - never discriminate or steer
- Keep responses concise (2-3 sentences for voice, can be longer for chat)

QUALIFICATION (ask naturally in conversation):
1. Are you currently working with a real estate agent?
2. What's your timeline for purchasing?
3. Are you pre-approved for a mortgage?
4. What's your ideal price range?

AVAILABLE ACTIONS:
- Answer property questions
- Schedule showings (check {calendar_availability})
- Send property photos/details (chat/WhatsApp only)
- Transfer to human agent
- Capture lead contact information

When you don't have information, say "I'll have {agent_name} get back to you with that detail."
""",
    
    greeting="Hi! Thanks for reaching out about {property_address}. I'm here to help answer any questions you have. What would you like to know?",
    
    capabilities=[
        "answer_property_questions",
        "schedule_showings",
        "qualify_leads",
        "send_media",
        "capture_contact",
        "transfer_to_human"
    ],
    
    channels_enabled=["voice", "chat", "whatsapp", "sms", "messenger"],
    
    qualification_questions=[
        QualificationQuestion(
            key="working_with_agent",
            question="Are you currently working with a real estate agent?",
            required=True,
            options=["Yes", "No", "Not sure"]
        ),
        QualificationQuestion(
            key="timeline",
            question="What's your timeline for purchasing?",
            required=True,
            options=["ASAP", "1-3 months", "3-6 months", "6+ months", "Just browsing"]
        ),
        QualificationQuestion(
            key="pre_approved",
            question="Have you been pre-approved for a mortgage?",
            required=False,
            options=["Yes", "No", "In process"]
        ),
        QualificationQuestion(
            key="budget",
            question="What's your price range?",
            required=True
        )
    ],
    
    fair_housing_enabled=True,
    recording_disclosure=True,
    
    escalation_triggers=[
        "speak to agent",
        "speak to human",
        "talk to someone",
        "real person",
        "complaint",
        "lawyer",
        "sue"
    ]
)
```

### 3.4 Lead Scoring Matrix

```python
from enum import Enum

class LeadScore(str, Enum):
    HOT = "hot"      # 80-100 points
    WARM = "warm"    # 50-79 points
    COLD = "cold"    # 0-49 points

SCORING_RULES = {
    # Timeline
    "timeline_asap": 30,
    "timeline_1_3_months": 25,
    "timeline_3_6_months": 15,
    "timeline_6_plus_months": 5,
    "timeline_browsing": 0,
    
    # Pre-approval
    "pre_approved_yes": 25,
    "pre_approved_in_process": 15,
    "pre_approved_no": 5,
    
    # Working with agent
    "has_agent_no": 20,
    "has_agent_not_sure": 10,
    "has_agent_yes": 0,
    
    # Budget defined
    "budget_defined": 15,
    "budget_vague": 5,
    
    # Engagement
    "scheduled_showing": 10,
    "asked_multiple_questions": 5,
    "requested_callback": 5,
}

def calculate_lead_score(qualification_data: dict) -> tuple[int, LeadScore]:
    score = 0
    
    # Timeline
    timeline = qualification_data.get("timeline", "").lower()
    if "asap" in timeline or "immediate" in timeline:
        score += SCORING_RULES["timeline_asap"]
    elif "1-3" in timeline or "1 to 3" in timeline:
        score += SCORING_RULES["timeline_1_3_months"]
    # ... etc
    
    # Determine tier
    if score >= 80:
        return score, LeadScore.HOT
    elif score >= 50:
        return score, LeadScore.WARM
    else:
        return score, LeadScore.COLD
```

---

## 4. Backend API Specification (FastAPI)

### 4.1 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry
│   ├── config.py               # Settings & env vars
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependencies (auth, db)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py       # Main router
│   │       ├── voice.py        # Twilio voice webhooks
│   │       ├── chat.py         # WebSocket chat
│   │       ├── whatsapp.py     # WhatsApp webhooks
│   │       ├── sms.py          # SMS webhooks
│   │       ├── calls.py        # Call management
│   │       ├── conversations.py # Conversation history
│   │       ├── contacts.py     # Contact/lead management
│   │       ├── properties.py   # Property listings
│   │       ├── showings.py     # Showing scheduler
│   │       ├── agents.py       # Agent/persona config
│   │       └── analytics.py    # Analytics endpoints
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py         # Auth, JWT
│   │   ├── exceptions.py       # Custom exceptions
│   │   └── middleware.py       # Request middleware
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_engine.py        # LangChain orchestration
│   │   ├── stt_service.py      # Deepgram STT
│   │   ├── tts_service.py      # OpenAI TTS
│   │   ├── llm_service.py      # GPT-4o-mini
│   │   ├── persona_service.py  # Persona management
│   │   ├── twilio_service.py   # Twilio voice/SMS
│   │   ├── whatsapp_service.py # WhatsApp messaging
│   │   ├── calendar_service.py # Google Calendar
│   │   ├── crm_service.py      # CRM integrations
│   │   └── mls_service.py      # MLS data sync
│   │
│   ├── channels/
│   │   ├── __init__.py
│   │   ├── base.py             # Base channel adapter
│   │   ├── voice_channel.py    # Voice (Twilio)
│   │   ├── chat_channel.py     # WebSocket chat
│   │   ├── whatsapp_channel.py # WhatsApp
│   │   ├── sms_channel.py      # SMS
│   │   └── messenger_channel.py # Facebook Messenger
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py             # Base model
│   │   ├── user.py             # User/Agent
│   │   ├── conversation.py     # Conversation
│   │   ├── message.py          # Message
│   │   ├── contact.py          # Contact/Lead
│   │   ├── property.py         # Property listing
│   │   ├── showing.py          # Showing appointment
│   │   └── persona.py          # AI Persona
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── message.py          # Message schemas
│   │   ├── conversation.py     # Conversation schemas
│   │   ├── contact.py          # Contact schemas
│   │   ├── property.py         # Property schemas
│   │   └── webhook.py          # Webhook payloads
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py          # Database session
│   │   └── repositories/       # Data access layer
│   │       ├── __init__.py
│   │       ├── conversation_repo.py
│   │       ├── contact_repo.py
│   │       └── property_repo.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── audio.py            # Audio processing
│       ├── phone.py            # Phone number utils
│       └── templates.py        # Message templates
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_voice.py
│   ├── test_chat.py
│   └── test_ai_engine.py
│
├── alembic/                    # DB migrations
│   ├── versions/
│   └── env.py
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

### 4.2 Main FastAPI App

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.api.v1.router import api_router
from app.db.session import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    pass

app = FastAPI(
    title="Real Estate AI Agent API",
    description="Multi-channel AI agent platform for real estate",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### 4.3 Voice Webhook (Twilio)

```python
# app/api/v1/voice.py
from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Connect

from app.services.ai_engine import AIEngine
from app.services.stt_service import DeepgramSTT
from app.services.tts_service import OpenAITTS
from app.channels.voice_channel import VoiceChannel

router = APIRouter(prefix="/voice", tags=["voice"])

@router.post("/incoming")
async def handle_incoming_call(request: Request):
    """Handle incoming Twilio voice call"""
    form_data = await request.form()
    call_sid = form_data.get("CallSid")
    from_number = form_data.get("From")
    to_number = form_data.get("To")
    
    # Create TwiML response with Media Stream
    response = VoiceResponse()
    
    # Optional: Play greeting while connecting
    response.say("Please wait while I connect you.", voice="alice")
    
    # Connect to WebSocket for media streaming
    connect = Connect()
    stream = connect.stream(
        url=f"wss://{request.headers['host']}/api/v1/voice/stream",
        track="both_tracks"
    )
    stream.parameter(name="call_sid", value=call_sid)
    stream.parameter(name="from_number", value=from_number)
    response.append(connect)
    
    return Response(content=str(response), media_type="application/xml")

@router.websocket("/stream")
async def voice_stream(websocket: WebSocket):
    """WebSocket endpoint for Twilio Media Stream"""
    await websocket.accept()
    
    call_sid = None
    ai_engine = None
    stt = DeepgramSTT()
    tts = OpenAITTS()
    
    try:
        async for message in websocket.iter_json():
            event = message.get("event")
            
            if event == "start":
                # Extract call metadata
                start_data = message.get("start", {})
                call_sid = start_data.get("callSid")
                custom_params = start_data.get("customParameters", {})
                from_number = custom_params.get("from_number")
                
                # Initialize AI engine with persona
                ai_engine = AIEngine(
                    persona_type="listing_concierge",
                    channel="voice"
                )
                
                # Send greeting
                greeting = await ai_engine.get_greeting()
                audio = await tts.synthesize(greeting)
                await send_audio_to_twilio(websocket, audio, message.get("streamSid"))
                
            elif event == "media":
                # Receive audio from caller
                payload = message.get("media", {}).get("payload")
                
                # Send to Deepgram for transcription
                transcript = await stt.transcribe_chunk(payload)
                
                if transcript and transcript.is_final:
                    # Process with AI
                    response = await ai_engine.process(transcript.text)
                    
                    # Convert to speech
                    audio = await tts.synthesize(response)
                    
                    # Send back to Twilio
                    await send_audio_to_twilio(
                        websocket, 
                        audio, 
                        message.get("streamSid")
                    )
                    
            elif event == "stop":
                # Call ended - save conversation
                if ai_engine:
                    await ai_engine.save_conversation()
                break
                
    except WebSocketDisconnect:
        pass
    finally:
        await stt.close()
        
async def send_audio_to_twilio(websocket: WebSocket, audio: bytes, stream_sid: str):
    """Send audio back to Twilio"""
    import base64
    
    # Convert to mulaw format for Twilio
    # ... audio conversion logic
    
    await websocket.send_json({
        "event": "media",
        "streamSid": stream_sid,
        "media": {
            "payload": base64.b64encode(audio).decode()
        }
    })
```

### 4.4 Chat WebSocket

```python
# app/api/v1/chat.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Dict
import json

from app.services.ai_engine import AIEngine
from app.schemas.message import ChatMessage, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])

# Active connections
connections: Dict[str, WebSocket] = {}

@router.websocket("/ws/{conversation_id}")
async def chat_websocket(
    websocket: WebSocket,
    conversation_id: str,
    token: str = None  # Auth token as query param
):
    """WebSocket endpoint for real-time chat"""
    await websocket.accept()
    connections[conversation_id] = websocket
    
    # Initialize AI engine
    ai_engine = AIEngine(
        persona_type="listing_concierge",
        channel="chat",
        conversation_id=conversation_id
    )
    
    try:
        # Send greeting
        greeting = await ai_engine.get_greeting()
        await websocket.send_json({
            "type": "message",
            "role": "assistant",
            "content": greeting,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Message loop
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "message":
                user_text = message.get("content")
                
                # Show typing indicator
                await websocket.send_json({"type": "typing", "status": True})
                
                # Process with AI
                response = await ai_engine.process(user_text)
                
                # Send response
                await websocket.send_json({
                    "type": "message",
                    "role": "assistant",
                    "content": response.text,
                    "rich_content": response.rich_content,  # buttons, cards, etc.
                    "timestamp": datetime.utcnow().isoformat()
                })
                
            elif message.get("type") == "end":
                await ai_engine.save_conversation()
                break
                
    except WebSocketDisconnect:
        await ai_engine.save_conversation()
    finally:
        connections.pop(conversation_id, None)
```

### 4.5 WhatsApp Webhook

```python
# app/api/v1/whatsapp.py
from fastapi import APIRouter, Request, HTTPException
from twilio.request_validator import RequestValidator

from app.services.ai_engine import AIEngine
from app.services.whatsapp_service import WhatsAppService
from app.config import settings

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])
whatsapp = WhatsAppService()

@router.post("/webhook")
async def whatsapp_webhook(request: Request):
    """Handle incoming WhatsApp messages via Twilio"""
    # Validate Twilio signature
    validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
    form_data = await request.form()
    
    if not validator.validate(
        str(request.url),
        dict(form_data),
        request.headers.get("X-Twilio-Signature", "")
    ):
        raise HTTPException(status_code=403, detail="Invalid signature")
    
    # Extract message data
    from_number = form_data.get("From")  # whatsapp:+1234567890
    to_number = form_data.get("To")
    body = form_data.get("Body")
    num_media = int(form_data.get("NumMedia", 0))
    
    # Get or create conversation
    conversation = await get_or_create_conversation(
        channel="whatsapp",
        contact_phone=from_number.replace("whatsapp:", "")
    )
    
    # Initialize AI engine
    ai_engine = AIEngine(
        persona_type="listing_concierge",
        channel="whatsapp",
        conversation_id=conversation.id
    )
    
    # Process message
    response = await ai_engine.process(body)
    
    # Send response via WhatsApp
    await whatsapp.send_message(
        to=from_number,
        body=response.text,
        media_url=response.media_url if response.media_url else None
    )
    
    return {"status": "ok"}
```

### 4.6 AI Engine Service

```python
# app/services/ai_engine.py
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
from typing import Optional, List
import json

from app.models.persona import Persona
from app.services.persona_service import PersonaService
from app.db.repositories.conversation_repo import ConversationRepository
from app.db.repositories.property_repo import PropertyRepository

class AIResponse:
    def __init__(
        self,
        text: str,
        rich_content: Optional[dict] = None,
        media_url: Optional[str] = None,
        actions: Optional[List[str]] = None
    ):
        self.text = text
        self.rich_content = rich_content
        self.media_url = media_url
        self.actions = actions

class AIEngine:
    def __init__(
        self,
        persona_type: str,
        channel: str,
        conversation_id: Optional[str] = None,
        property_id: Optional[str] = None
    ):
        self.persona = PersonaService.get_persona(persona_type)
        self.channel = channel
        self.conversation_id = conversation_id
        self.property_id = property_id
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=150 if channel == "voice" else 500
        )
        
        # Conversation memory (last 10 turns)
        self.memory = ConversationBufferWindowMemory(
            k=10,
            return_messages=True,
            memory_key="history"
        )
        
        # Load existing conversation if resuming
        if conversation_id:
            self._load_conversation_history()
        
        # Build prompt
        self.prompt = self._build_prompt()
        
        # Create chain
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            memory=self.memory,
            verbose=True
        )
    
    def _build_prompt(self) -> ChatPromptTemplate:
        """Build the prompt template with persona"""
        # Get property context if available
        property_context = ""
        if self.property_id:
            property_data = PropertyRepository.get(self.property_id)
            if property_data:
                property_context = self._format_property_context(property_data)
        
        system_prompt = self.persona.system_prompt.format(
            agent_name="Your Agent",  # TODO: Get from config
            brokerage_name="Acme Realty",
            property_context=property_context,
            calendar_availability="Available: Tomorrow 10am, 2pm, Saturday 11am"
        )
        
        # Add channel-specific instructions
        if self.channel == "voice":
            system_prompt += "\n\nIMPORTANT: Keep responses brief (1-2 sentences) for natural conversation."
        elif self.channel == "chat":
            system_prompt += "\n\nYou can use rich formatting and suggest quick reply buttons."
        
        return ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
    
    async def get_greeting(self) -> str:
        """Get persona greeting"""
        greeting = self.persona.greeting
        
        # Personalize if property context available
        if self.property_id:
            property_data = PropertyRepository.get(self.property_id)
            if property_data:
                greeting = greeting.format(
                    property_address=property_data.address_full
                )
        else:
            greeting = greeting.format(
                property_address="our listings"
            )
        
        return greeting
    
    async def process(self, user_input: str) -> AIResponse:
        """Process user input and generate response"""
        # Check for escalation triggers
        if self._should_escalate(user_input):
            return AIResponse(
                text="I'll connect you with a human agent right away. Please hold.",
                actions=["escalate_to_human"]
            )
        
        # Run LLM chain
        result = await self.chain.ainvoke({"input": user_input})
        response_text = result["text"]
        
        # Parse for actions (scheduling, etc.)
        actions = self._detect_actions(user_input, response_text)
        
        # Generate rich content for chat/WhatsApp
        rich_content = None
        if self.channel in ["chat", "whatsapp", "messenger"]:
            rich_content = self._generate_rich_content(response_text, actions)
        
        return AIResponse(
            text=response_text,
            rich_content=rich_content,
            actions=actions
        )
    
    def _should_escalate(self, user_input: str) -> bool:
        """Check if user wants human agent"""
        user_lower = user_input.lower()
        return any(
            trigger in user_lower 
            for trigger in self.persona.escalation_triggers
        )
    
    def _detect_actions(self, user_input: str, response: str) -> List[str]:
        """Detect actionable intents"""
        actions = []
        combined = f"{user_input} {response}".lower()
        
        if any(word in combined for word in ["schedule", "showing", "tour", "visit", "see it"]):
            actions.append("schedule_showing")
        if any(word in combined for word in ["price", "cost", "how much"]):
            actions.append("provide_pricing")
        if any(word in combined for word in ["photo", "picture", "image"]):
            actions.append("send_photos")
            
        return actions
    
    def _generate_rich_content(self, text: str, actions: List[str]) -> dict:
        """Generate buttons, cards for rich channels"""
        rich = {"buttons": [], "cards": []}
        
        if "schedule_showing" in actions:
            rich["buttons"].append({
                "type": "postback",
                "title": "📅 Schedule Showing",
                "payload": "SCHEDULE_SHOWING"
            })
        
        rich["buttons"].append({
            "type": "postback",
            "title": "📞 Speak to Agent",
            "payload": "SPEAK_TO_AGENT"
        })
        
        return rich
    
    async def save_conversation(self):
        """Save conversation to database"""
        if self.conversation_id:
            messages = self.memory.chat_memory.messages
            await ConversationRepository.save_messages(
                self.conversation_id,
                messages
            )
```

### 4.7 Deepgram STT Service

```python
# app/services/stt_service.py
from deepgram import Deepgram
from typing import Optional
import asyncio

from app.config import settings

class TranscriptResult:
    def __init__(self, text: str, is_final: bool, confidence: float):
        self.text = text
        self.is_final = is_final
        self.confidence = confidence

class DeepgramSTT:
    def __init__(self):
        self.client = Deepgram(settings.DEEPGRAM_API_KEY)
        self.connection = None
        self.transcript_queue = asyncio.Queue()
        
    async def connect(self):
        """Establish streaming connection"""
        self.connection = await self.client.transcription.live({
            "model": "nova-2",
            "language": "en-US",
            "smart_format": True,
            "interim_results": True,
            "utterance_end_ms": 1000,
            "vad_events": True,
            "encoding": "mulaw",
            "sample_rate": 8000,
            "channels": 1
        })
        
        # Set up event handlers
        self.connection.on("transcript", self._on_transcript)
        self.connection.on("error", self._on_error)
        
    def _on_transcript(self, transcript):
        """Handle incoming transcript"""
        if transcript.get("channel"):
            alternatives = transcript["channel"]["alternatives"]
            if alternatives:
                text = alternatives[0].get("transcript", "")
                is_final = transcript.get("is_final", False)
                confidence = alternatives[0].get("confidence", 0)
                
                if text.strip():
                    self.transcript_queue.put_nowait(
                        TranscriptResult(text, is_final, confidence)
                    )
    
    def _on_error(self, error):
        """Handle errors"""
        print(f"Deepgram error: {error}")
    
    async def transcribe_chunk(self, audio_chunk: bytes) -> Optional[TranscriptResult]:
        """Send audio chunk and get transcript"""
        if not self.connection:
            await self.connect()
        
        # Send audio
        self.connection.send(audio_chunk)
        
        # Check for results
        try:
            result = self.transcript_queue.get_nowait()
            return result
        except asyncio.QueueEmpty:
            return None
    
    async def close(self):
        """Close connection"""
        if self.connection:
            await self.connection.finish()
```

### 4.8 OpenAI TTS Service

```python
# app/services/tts_service.py
from openai import AsyncOpenAI
import base64

from app.config import settings

class OpenAITTS:
    def __init__(self, voice: str = "alloy"):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.voice = voice
        
    async def synthesize(self, text: str) -> bytes:
        """Convert text to speech"""
        response = await self.client.audio.speech.create(
            model="tts-1",
            voice=self.voice,
            input=text,
            response_format="pcm"  # Raw audio for streaming
        )
        
        return response.content
    
    async def synthesize_streaming(self, text: str):
        """Stream audio chunks"""
        async with self.client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice=self.voice,
            input=text,
            response_format="pcm"
        ) as response:
            async for chunk in response.iter_bytes(chunk_size=1024):
                yield chunk
```

---

## 5. Frontend Specification (Next.js)

### 5.1 Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx                 # Dashboard home
│   │   ├── (auth)/
│   │   │   ├── login/page.tsx
│   │   │   └── register/page.tsx
│   │   ├── (dashboard)/
│   │   │   ├── layout.tsx           # Dashboard layout
│   │   │   ├── calls/
│   │   │   │   ├── page.tsx         # Calls list
│   │   │   │   └── [id]/page.tsx    # Call detail
│   │   │   ├── conversations/
│   │   │   │   ├── page.tsx
│   │   │   │   └── [id]/page.tsx
│   │   │   ├── contacts/
│   │   │   │   ├── page.tsx
│   │   │   │   └── [id]/page.tsx
│   │   │   ├── properties/
│   │   │   │   ├── page.tsx
│   │   │   │   └── [id]/page.tsx
│   │   │   ├── showings/
│   │   │   │   └── page.tsx
│   │   │   ├── agents/
│   │   │   │   ├── page.tsx         # Personas list
│   │   │   │   └── [id]/page.tsx    # Persona editor
│   │   │   ├── analytics/
│   │   │   │   └── page.tsx
│   │   │   └── settings/
│   │   │       └── page.tsx
│   │   └── api/                     # Next.js API routes (proxy)
│   │       └── [...path]/route.ts
│   │
│   ├── components/
│   │   ├── ui/                      # shadcn/ui components
│   │   ├── layout/
│   │   │   ├── sidebar.tsx
│   │   │   ├── topbar.tsx
│   │   │   └── page-header.tsx
│   │   ├── dashboard/
│   │   │   ├── stats-cards.tsx
│   │   │   ├── call-volume-chart.tsx
│   │   │   ├── live-activity.tsx
│   │   │   └── recent-calls.tsx
│   │   ├── calls/
│   │   │   ├── calls-table.tsx
│   │   │   ├── call-detail.tsx
│   │   │   └── transcript-viewer.tsx
│   │   ├── conversations/
│   │   │   ├── conversation-list.tsx
│   │   │   └── message-thread.tsx
│   │   ├── contacts/
│   │   │   ├── contacts-table.tsx
│   │   │   ├── contact-detail.tsx
│   │   │   └── lead-score-badge.tsx
│   │   ├── personas/
│   │   │   ├── persona-card.tsx
│   │   │   └── persona-editor.tsx
│   │   └── shared/
│   │       ├── status-badge.tsx
│   │       ├── phone-number.tsx
│   │       └── data-table.tsx
│   │
│   ├── lib/
│   │   ├── api.ts                   # API client
│   │   ├── websocket.ts             # WebSocket client
│   │   └── utils.ts
│   │
│   ├── hooks/
│   │   ├── use-calls.ts
│   │   ├── use-conversations.ts
│   │   ├── use-websocket.ts
│   │   └── use-realtime.ts
│   │
│   ├── stores/
│   │   ├── auth-store.ts
│   │   ├── call-store.ts
│   │   └── conversation-store.ts
│   │
│   └── types/
│       ├── api.ts
│       ├── call.ts
│       ├── conversation.ts
│       └── contact.ts
│
├── public/
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── next.config.js
```

### 5.2 Key Components

See previous **UI/UX Specification Document** for detailed component designs:
- Dashboard with stats cards and charts
- Calls list with filters and pagination
- Conversation viewer with transcript
- Persona editor with live preview
- Contact/lead management
- Analytics dashboard

---

## 6. Database Schema

### 6.1 Core Tables

```sql
-- Organizations (multi-tenant)
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    plan VARCHAR(50) DEFAULT 'starter',
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Users (agents/admins)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(50) DEFAULT 'agent',
    phone VARCHAR(20),
    avatar_url TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Personas (AI agents)
CREATE TABLE personas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id),
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    description TEXT,
    system_prompt TEXT NOT NULL,
    greeting TEXT NOT NULL,
    voice_settings JSONB DEFAULT '{}',
    personality JSONB DEFAULT '{}',
    capabilities TEXT[],
    qualification_questions JSONB DEFAULT '[]',
    channels_enabled TEXT[],
    escalation_triggers TEXT[],
    is_active BOOLEAN DEFAULT true,
    is_template BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Contacts (leads/customers)
CREATE TABLE contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id),
    
    -- Identity
    phone VARCHAR(20),
    email VARCHAR(255),
    whatsapp_id VARCHAR(50),
    facebook_id VARCHAR(50),
    
    -- Profile
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    full_name VARCHAR(200),
    
    -- Lead data
    lead_score INTEGER DEFAULT 0,
    lead_status VARCHAR(20) DEFAULT 'new',
    qualification_data JSONB DEFAULT '{}',
    assigned_agent_id UUID REFERENCES users(id),
    
    -- Preferences
    preferred_channel VARCHAR(20),
    opted_in_sms BOOLEAN DEFAULT false,
    opted_in_whatsapp BOOLEAN DEFAULT false,
    
    -- Source
    source VARCHAR(50),
    source_details JSONB,
    
    -- CRM
    external_crm_id VARCHAR(100),
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Conversations
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id),
    contact_id UUID REFERENCES contacts(id),
    persona_id UUID REFERENCES personas(id),
    
    -- Channel
    channel VARCHAR(20) NOT NULL,
    channel_conversation_id VARCHAR(100),
    
    -- For voice calls
    call_sid VARCHAR(50),
    from_number VARCHAR(20),
    to_number VARCHAR(20),
    direction VARCHAR(10),
    duration_seconds INTEGER,
    recording_url TEXT,
    
    -- Status
    status VARCHAR(20) DEFAULT 'active',
    handed_off_to UUID REFERENCES users(id),
    handed_off_at TIMESTAMPTZ,
    
    -- Context
    property_id UUID REFERENCES properties(id),
    
    -- Stats
    message_count INTEGER DEFAULT 0,
    
    -- Timing
    started_at TIMESTAMPTZ DEFAULT NOW(),
    last_message_at TIMESTAMPTZ,
    ended_at TIMESTAMPTZ,
    
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Messages
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    
    -- Direction
    direction VARCHAR(10) NOT NULL,
    sender_type VARCHAR(10) NOT NULL,
    sender_id UUID,
    
    -- Content
    content_type VARCHAR(20) DEFAULT 'text',
    content_text TEXT,
    content_media_url TEXT,
    rich_content JSONB,
    
    -- AI
    intent_detected VARCHAR(50),
    sentiment VARCHAR(20),
    
    -- Status
    status VARCHAR(20) DEFAULT 'sent',
    
    -- Timing
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    delivered_at TIMESTAMPTZ,
    read_at TIMESTAMPTZ
);

-- Properties
CREATE TABLE properties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id),
    
    -- MLS
    mls_id VARCHAR(50),
    mls_source VARCHAR(50),
    
    -- Address
    address_street VARCHAR(255),
    address_city VARCHAR(100),
    address_state VARCHAR(50),
    address_zip VARCHAR(20),
    address_full TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    
    -- Details
    property_type VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',
    price INTEGER,
    bedrooms INTEGER,
    bathrooms DECIMAL(3, 1),
    sqft INTEGER,
    year_built INTEGER,
    
    -- Features
    features JSONB DEFAULT '[]',
    description TEXT,
    
    -- Media
    photos JSONB DEFAULT '[]',
    virtual_tour_url TEXT,
    
    -- Agent
    listing_agent_id UUID REFERENCES users(id),
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Showings
CREATE TABLE showings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id),
    property_id UUID REFERENCES properties(id),
    contact_id UUID REFERENCES contacts(id),
    agent_id UUID REFERENCES users(id),
    conversation_id UUID REFERENCES conversations(id),
    
    -- Scheduling
    scheduled_at TIMESTAMPTZ NOT NULL,
    duration_minutes INTEGER DEFAULT 30,
    
    -- Status
    status VARCHAR(20) DEFAULT 'scheduled',
    confirmed_at TIMESTAMPTZ,
    cancelled_at TIMESTAMPTZ,
    cancellation_reason TEXT,
    
    -- Reminders
    reminder_24h_sent BOOLEAN DEFAULT false,
    reminder_2h_sent BOOLEAN DEFAULT false,
    
    -- Feedback
    feedback JSONB,
    
    -- Notes
    notes TEXT,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Analytics (daily aggregates)
CREATE TABLE analytics_daily (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id),
    date DATE NOT NULL,
    
    -- Calls
    total_calls INTEGER DEFAULT 0,
    inbound_calls INTEGER DEFAULT 0,
    outbound_calls INTEGER DEFAULT 0,
    total_call_duration INTEGER DEFAULT 0,
    
    -- Messages
    total_messages INTEGER DEFAULT 0,
    chat_messages INTEGER DEFAULT 0,
    whatsapp_messages INTEGER DEFAULT 0,
    sms_messages INTEGER DEFAULT 0,
    
    -- Leads
    new_leads INTEGER DEFAULT 0,
    qualified_leads INTEGER DEFAULT 0,
    
    -- Showings
    showings_booked INTEGER DEFAULT 0,
    showings_completed INTEGER DEFAULT 0,
    
    -- Costs
    total_cost_cents INTEGER DEFAULT 0,
    
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(organization_id, date)
);

-- Indexes
CREATE INDEX idx_contacts_org ON contacts(organization_id);
CREATE INDEX idx_contacts_phone ON contacts(phone);
CREATE INDEX idx_contacts_lead_status ON contacts(lead_status);

CREATE INDEX idx_conversations_org ON conversations(organization_id);
CREATE INDEX idx_conversations_contact ON conversations(contact_id);
CREATE INDEX idx_conversations_channel ON conversations(channel);
CREATE INDEX idx_conversations_status ON conversations(status);

CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_timestamp ON messages(timestamp DESC);

CREATE INDEX idx_properties_org ON properties(organization_id);
CREATE INDEX idx_properties_status ON properties(status);

CREATE INDEX idx_showings_scheduled ON showings(scheduled_at);
CREATE INDEX idx_showings_status ON showings(status);
```

---

## 7. Development Phases

### Phase 1: Core Foundation (Weeks 1-4)
- [ ] FastAPI project setup
- [ ] Database schema & migrations
- [ ] Authentication (JWT)
- [ ] Twilio voice integration
- [ ] Deepgram STT streaming
- [ ] OpenAI LLM + TTS integration
- [ ] Basic conversation flow
- [ ] Next.js dashboard scaffold

### Phase 2: Chat & WhatsApp (Weeks 5-8)
- [ ] WebSocket chat backend
- [ ] Chat widget (embeddable)
- [ ] WhatsApp webhook integration
- [ ] Message templates
- [ ] Multi-channel conversation view
- [ ] Contact management

### Phase 3: Real Estate Features (Weeks 9-12)
- [ ] Persona system
- [ ] Property database
- [ ] MLS integration (optional)
- [ ] Showing scheduler
- [ ] Lead scoring
- [ ] Calendar integration

### Phase 4: Dashboard & Analytics (Weeks 13-16)
- [ ] Full dashboard UI
- [ ] Call/conversation history
- [ ] Analytics charts
- [ ] Persona editor
- [ ] Settings pages

### Phase 5: Additional Channels (Weeks 17-20)
- [ ] SMS integration
- [ ] Facebook Messenger
- [ ] Instagram DM
- [ ] Email automation

### Phase 6: Polish & Launch (Weeks 21-24)
- [ ] Performance optimization
- [ ] Error handling
- [ ] Testing
- [ ] Documentation
- [ ] Production deployment

---

## 8. Environment Variables

```bash
# .env.example

# App
APP_ENV=development
APP_DEBUG=true
API_BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/voiceagent
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your-supabase-key

# Redis
REDIS_URL=redis://localhost:6379

# Auth
JWT_SECRET=your-super-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRY_HOURS=24

# Twilio
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_PHONE_NUMBER=+1234567890

# Deepgram
DEEPGRAM_API_KEY=xxxxx

# OpenAI
OPENAI_API_KEY=sk-xxxxx

# WhatsApp (via Twilio)
WHATSAPP_PHONE_NUMBER=+1234567890

# SendGrid (Email)
SENDGRID_API_KEY=SG.xxxxx

# Google Calendar
GOOGLE_CALENDAR_CREDENTIALS={}

# CRM Integrations
FOLLOW_UP_BOSS_API_KEY=xxxxx
```

---

## 9. Deployment

### 9.1 Backend (Railway)

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 9.2 Frontend (Vercel)

```json
// vercel.json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "env": {
    "NEXT_PUBLIC_API_URL": "@api_url"
  }
}
```

---

## 10. Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Product Owner | Cenk | | |
| Tech Lead | | | |
| Developer | | | |

---

**Document Version History:**
| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-01-30 | Initial voice-only PRD |
| 2.0 | 2025-01-30 | Multi-channel + Real Estate |
| 3.0 | 2025-01-30 | Python FastAPI + Next.js stack |
