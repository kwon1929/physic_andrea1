"""
아트레이디스 - Physical AI 로봇
웨이크워드로 깨우는 대화형 로봇
"""

import os
from dotenv import load_dotenv
from src.brain.robot_brain import RobotBrain
from src.perception.speech_recognizer import SpeechRecognizer
from src.perception.microphone import MicrophoneRecorder
from src.perception.text_to_speech import create_tts, MacOSTTS
from src.perception.wake_word import SmartWakeWordDetector
from src.simulation.simple_robot_sim import SimpleRobotSimulator
from src.motion.action_executor import ActionExecutor
import time

load_dotenv()


class Atreides:
    """
    아트레이디스 - 웨이크워드 기반 대화형 로봇

    "아트레이디스"라고 부르면 깨어나서 명령을 듣습니다.
    """

    def __init__(self, api_key: str, use_openai_tts: bool = False, name: str = "자비스"):
        """
        Args:
            api_key: OpenAI API 키
            use_openai_tts: OpenAI TTS 사용 여부
            name: 로봇 이름
        """
        self.name = name
        self.wake_words = [
            "jarvis", "자비스", "제비스",
            "atreides", "아트레이디스", "아트레이데스", "아트레",
            "ironman", "아이언맨",
        ]

        print("=" * 60)
        print(f"🤖 {self.name} System Initialization")
        print("=" * 60)

        # AI Brain - with robot identity
        self.brain = RobotBrain(api_key=api_key, model="gpt-4o-mini")
        self._customize_brain()
        print(f"✓ AI Brain ({self.name})")

        # Speech Recognition
        self.recognizer = SpeechRecognizer(api_key=api_key)
        print("✓ Speech Recognition")

        # Microphone
        self.microphone = MicrophoneRecorder()
        print("✓ Microphone")

        # Wake Word Detector
        self.wake_detector = SmartWakeWordDetector(
            self.recognizer,
            wake_words=self.wake_words
        )
        print(f"✓ Wake Word Detection ({', '.join(self.wake_words)})")

        # TTS
        self.tts = create_tts(api_key=api_key, use_openai=use_openai_tts) if use_openai_tts else MacOSTTS()
        tts_type = "OpenAI" if use_openai_tts else "macOS"
        print(f"✓ Voice Output ({tts_type})")

        # Simulator
        self.simulator = SimpleRobotSimulator()
        print("✓ Simulator")

        # Action Executor
        self.executor = ActionExecutor(self.simulator)
        print("✓ Action Executor")

        print(f"\n✅ {self.name} Ready!")

    def _customize_brain(self):
        """Add robot identity to AI brain"""
        identity = f"""
Your name is {self.name}.

# Identity
- You are a friendly and efficient AI assistant like Jarvis from Iron Man
- Your top priority is to help the user
- You are careful, wise, and prioritize user safety
- You respond efficiently and concisely

# Responses
- When first called: "Yes, {self.name} here" or "Yes" (keep it simple)
- After completing tasks: "Done" or "Completed"
- When you don't understand: "Could you repeat that, please?"

Always speak naturally and concisely in English.
"""
        # Add to system prompt
        self.brain.system_prompt = self.brain.system_prompt + "\n\n" + identity

    def greet(self):
        """Greeting"""
        greeting = f"Hello. I'm {self.name}. Feel free to call me anytime."
        print(f"\n🔊 {greeting}")
        self.tts.speak(greeting)

    def listen_for_command(self, duration=5.0):
        """
        Listen for command

        Args:
            duration: Recording duration (seconds)

        Returns:
            str: Recognized command or None
        """
        try:
            print(f"\n🎤 Listening for {duration} seconds...")
            audio_file = self.microphone.record(duration=duration)

            print("🎤 Recognizing speech...")
            command = self.recognizer.transcribe_file(audio_file)

            print(f"👤 User: {command}")
            return command

        except Exception as e:
            print(f"✗ Speech recognition failed: {e}")
            return None

    def process_command(self, command: str):
        """
        Process and execute command

        Args:
            command: User command
        """
        # Think with AI brain
        print(f"\n🧠 {self.name} is thinking...")
        response = self.brain.think(command)

        # Respond with voice
        self.tts.speak(response.speech)

        # Ask for clarification
        if response.needs_clarification:
            print(f"❓ {response.clarification_question}")
            return

        # Execute actions
        if response.commands:
            print(f"\n⚙️  Executing {len(response.commands)} action(s)")
            self.executor.execute_commands(response.commands)

            # Completion notification
            completion = "Done."
            print(f"\n🔊 {completion}")
            self.tts.speak(completion)

    def run(self):
        """
        Main loop - Wait for wake word → Process command
        """
        # Greet
        self.greet()

        print("\n" + "=" * 60)
        print("Standby Mode")
        print("=" * 60)
        print(f"\nSay '{self.wake_words[0]}' to wake me up")
        print("(Press Ctrl+C to exit)\n")

        try:
            while True:
                # Detect wake word
                detected, text = self.wake_detector.listen_smart(
                    max_silence=1.5,
                    min_volume=400
                )

                if detected:
                    # Wake up!
                    print(f"\n✅ {self.name} activated!")

                    # Acknowledgment
                    ack = "Yes, I'm listening."
                    print(f"🔊 {ack}")
                    self.tts.speak(ack)

                    # Listen for command
                    command = self.listen_for_command(duration=5.0)

                    if command:
                        # Process command
                        self.process_command(command)
                    else:
                        sorry = "Sorry, could you repeat that?"
                        print(f"\n🔊 {sorry}")
                        self.tts.speak(sorry)

                    # Return to standby
                    print(f"\n→ Returning to standby mode")
                    time.sleep(1)

        except KeyboardInterrupt:
            print(f"\n\nShutting down {self.name} system.")
            goodbye = "Goodbye."
            print(f"🔊 {goodbye}")
            self.tts.speak(goodbye)


def main():
    """Main function"""
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("✗ OPENAI_API_KEY not set.")
        return 1

    # Choose robot name
    print("\nRobot Name:")
    print("  1. Jarvis - Recommended, easy to recognize")
    print("  2. Atreides")
    print("  3. Custom")

    name_choice = input("\nChoice (1, 2, 3, default=1): ").strip() or "1"

    if name_choice == "1":
        robot_name = "Jarvis"
    elif name_choice == "2":
        robot_name = "Atreides"
    elif name_choice == "3":
        robot_name = input("Enter robot name: ").strip() or "Jarvis"
    else:
        robot_name = "Jarvis"

    # TTS selection
    print("\nTTS Options:")
    print("  1. OpenAI TTS (High quality)")
    print("  2. macOS Built-in (Free) - Recommended")

    choice = input("\nChoice (1 or 2, default=2): ").strip() or "2"
    use_openai_tts = (choice == "1")

    # Start robot
    robot = Atreides(api_key=api_key, use_openai_tts=use_openai_tts, name=robot_name)
    robot.run()

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
