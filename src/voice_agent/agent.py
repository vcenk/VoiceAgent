class VoiceAgent:
    """Minimal placeholder voice agent implementation.

    This is a tiny, testable scaffold: expand with real integrations
    (Twilio, speech-to-text, CRM) according to the PRD.
    """

    def __init__(self, name: str = "voice-agent"):
        self.name = name
        self.running = False

    def start(self) -> str:
        self.running = True
        return f"{self.name} started"

    def stop(self) -> str:
        self.running = False
        return f"{self.name} stopped"

    def status(self) -> str:
        return "running" if self.running else "stopped"
