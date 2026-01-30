from fastapi import APIRouter

from .personas import router as personas_router
from .voice import router as voice_router
from .chat import router as chat_router

api_router = APIRouter()

api_router.include_router(personas_router, prefix="/personas", tags=["personas"])
api_router.include_router(voice_router, prefix="/voice", tags=["voice"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
