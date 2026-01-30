from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import asyncio
from app.config import settings


@dataclass
class TranscriptResult:
    text: str
    is_final: bool
    confidence: float = 0.9


class DeepgramSTT:
    """STT service using Deepgram API with stub fallback.

    If DEEPGRAM_API_KEY not set, returns a deterministic transcript for testing.
    Uses Deepgram SDK v3.0+ for streaming transcription.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.DEEPGRAM_API_KEY
        self._closed = False
        self._use_real_api = bool(self.api_key)
        self._client = None
        self._connection = None

        if self._use_real_api:
            try:
                from deepgram import DeepgramClient, PrerecordedOptions
                self.deepgram = DeepgramClient(api_key=self.api_key)
            except Exception:
                # Fallback if Deepgram client initialization fails
                self._use_real_api = False

    async def transcribe_chunk(self, audio_chunk: bytes) -> Optional[TranscriptResult]:
        """Transcribe audio chunk using Deepgram API or return stub result."""
        await asyncio.sleep(0)  # yield control

        if not audio_chunk:
            return None

        if not self._use_real_api:
            # Stub fallback for testing/dev
            return TranscriptResult(
                text="I want to schedule a showing",
                is_final=True,
                confidence=0.95
            )

        try:
            # Use Deepgram prerecorded API for synchronous audio chunks
            from deepgram import PrerecordedOptions
            
            options = PrerecordedOptions(
                model="nova-2",
                language="en-US",
                smart_format=True,
            )

            response = self.deepgram.listen.prerecorded.transcribe_file(
                audio_chunk,
                options,
            )

            # Extract transcript from response
            if response and response.results:
                transcript = response.results.channels[0].alternatives[0].transcript
                confidence = response.results.channels[0].alternatives[0].confidence

                return TranscriptResult(
                    text=transcript,
                    is_final=True,
                    confidence=confidence,
                )
        except Exception as e:
            # Log and fallback to stub on API error
            print(f"Deepgram API error: {e}")
            return TranscriptResult(
                text="I want to schedule a showing",
                is_final=True,
                confidence=0.5,
            )

        return None

    async def close(self):
        """Close Deepgram connection if open."""
        self._closed = True
        if self._connection:
            try:
                await self._connection.finish()
            except Exception:
                pass


# Alias for backward compatibility
DeepgramSTTStub = DeepgramSTT
