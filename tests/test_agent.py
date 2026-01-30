from voice_agent.agent import VoiceAgent


def test_start_stop_status():
    a = VoiceAgent("test-agent")
    assert a.status() == "stopped"
    assert a.start() == "test-agent started"
    assert a.status() == "running"
    assert a.stop() == "test-agent stopped"
    assert a.status() == "stopped"
