from __future__ import annotations
import asyncio
from typing import Optional
from app.config import settings


class OpenAITTS:
    """TTS service using OpenAI API with stub fallback.

    If OPENAI_API_KEY not set, returns deterministic bytes for testing.
    Uses OpenAI API v1.0+ for speech synthesis.
    """

    def __init__(self, voice: str = "alloy", api_key: Optional[str] = None):
        self.voice = voice
        self.api_key = api_key or settings.OPENAI_API_KEY
        self._use_real_api = bool(self.api_key)
        self._client = None

        if self._use_real_api:
            try:
                from openai import AsyncOpenAI
                self._client = AsyncOpenAI(api_key=self.api_key)
            except Exception:
                # Fallback if OpenAI client initialization fails
                self._use_real_api = False

    async def synthesize(self, text: str) -> bytes:
        """Synthesize text to speech using OpenAI API or return stub bytes."""
        await asyncio.sleep(0)

        if not self._use_real_api:
            # Stub fallback for testing/dev
            return f"AUDIO:{text}".encode("utf-8")

        try:
            if self._client is None:
                from openai import AsyncOpenAI
                self._client = AsyncOpenAI(api_key=self.api_key)

            # Call OpenAI TTS API
            response = await self._client.audio.speech.create(
                model="tts-1",
                voice=self.voice,
                input=text,
                response_format="pcm",
            )

            # response.content is the audio bytes
            return response.content

        except Exception as e:
            # Log and fallback to stub on API error
            print(f"OpenAI TTS error: {e}")
            return f"AUDIO:{text}".encode("utf-8")

    async def synthesize_streaming(self, text: str):
        """Yield small audio chunks for streaming."""
        data = await self.synthesize(text)
        for i in range(0, len(data), 8):
            yield data[i : i + 8]


# Alias for backward compatibility
OpenAITTSStub = OpenAITTS
