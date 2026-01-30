import argparse
from voice_agent import VoiceAgent


def main():
    parser = argparse.ArgumentParser(description="Run the minimal VoiceAgent scaffold")
    parser.add_argument("--name", default="voice-agent", help="Agent name")
    parser.add_argument("--action", choices=["start", "stop", "status"], default="start")
    args = parser.parse_args()

    agent = VoiceAgent(args.name)

    if args.action == "start":
        print(agent.start())
    elif args.action == "stop":
        print(agent.stop())
    else:
        print(agent.status())


if __name__ == "__main__":
    main()
