"""
대화형 Physical AI 로봇
마이크로 말하면 로봇이 듣고, 생각하고, 대답하고, 동작하는 시스템
"""

import os
from dotenv import load_dotenv
from src.brain.robot_brain import RobotBrain
from src.perception.speech_recognizer import SpeechRecognizer
from src.perception.microphone import MicrophoneRecorder
from src.perception.text_to_speech import create_tts
from src.simulation.simple_robot_sim import SimpleRobotSimulator
from src.motion.action_executor import ActionExecutor
from src.simulation.visualizer import RobotVisualizer
import time

load_dotenv()


class InteractiveRobot:
    """
    대화형 로봇 시스템
    실시간 음성 대화 + 동작 실행
    """

    def __init__(self, api_key: str, use_openai_tts: bool = True):
        """
        Args:
            api_key: OpenAI API 키
            use_openai_tts: OpenAI TTS 사용 (False면 macOS 내장 사용)
        """
        print("=" * 60)
        print("🤖 대화형 Physical AI 로봇")
        print("=" * 60)

        # 시스템 초기화
        print("\n시스템 초기화 중...")

        self.brain = RobotBrain(api_key=api_key, model="gpt-4o-mini")
        print("✓ AI 두뇌")

        self.recognizer = SpeechRecognizer(api_key=api_key)
        print("✓ 음성 인식 (Whisper)")

        self.microphone = MicrophoneRecorder()
        print("✓ 마이크")

        self.tts = create_tts(api_key=api_key, use_openai=use_openai_tts)
        tts_type = "OpenAI TTS" if use_openai_tts else "macOS 내장"
        print(f"✓ 음성 출력 ({tts_type})")

        self.simulator = SimpleRobotSimulator()
        print("✓ 시뮬레이터")

        self.executor = ActionExecutor(self.simulator)
        print("✓ 동작 실행기")

        self.visualizer = None  # 선택사항

        print("\n✅ 시스템 준비 완료!")

    def listen_and_respond(self, duration=5.0, execute_actions=True):
        """
        한 번의 대화 사이클
        듣기 → 생각 → 대답 → 동작

        Args:
            duration: 녹음 시간 (초)
            execute_actions: 동작 실행 여부

        Returns:
            bool: 성공 여부
        """
        print("\n" + "=" * 60)

        # 1. 마이크로 녹음
        try:
            audio_file = self.microphone.record(duration=duration)
        except Exception as e:
            print(f"✗ 녹음 실패: {e}")
            return False

        # 2. 음성 인식
        print("\n🎤 음성 인식 중...")
        try:
            user_speech = self.recognizer.transcribe_file(audio_file)
            print(f"👤 사용자: {user_speech}")
        except Exception as e:
            print(f"✗ 음성 인식 실패: {e}")
            return False

        # 3. AI 사고
        print("\n🧠 로봇이 생각 중...")
        response = self.brain.think(user_speech)

        # 4. 음성으로 응답
        self.tts.speak(response.speech)

        # 5. 추가 질문이 있으면 출력
        if response.needs_clarification:
            print(f"\n❓ {response.clarification_question}")
            return True

        # 6. 동작 실행
        if execute_actions and response.commands:
            print(f"\n⚙️  동작 실행: {len(response.commands)}개")
            self.executor.execute_commands(response.commands)

            # 시각화 업데이트
            if self.visualizer:
                self.visualizer.draw_state(self.simulator, title="동작 완료")

        return True

    def run(self, enable_visualization=False):
        """
        대화형 모드 실행
        계속 듣고 응답하기

        Args:
            enable_visualization: 시각화 활성화
        """
        if enable_visualization:
            self.visualizer = RobotVisualizer(interactive=True)
            self.visualizer.draw_state(self.simulator, title="초기 상태")

        print("\n" + "=" * 60)
        print("💬 대화 시작!")
        print("=" * 60)
        print("\n명령:")
        print("  - 마이크에 대고 말하세요")
        print("  - 'quit' 말하면 종료")
        print("  - 'reset' 말하면 대화 초기화")
        print("  - Ctrl+C로 강제 종료")
        print("=" * 60)

        try:
            while True:
                # 대화 사이클
                success = self.listen_and_respond(duration=5.0)

                if not success:
                    print("\n다시 시도하세요...")
                    time.sleep(1)

        except KeyboardInterrupt:
            print("\n\n종료합니다.")
        finally:
            if self.visualizer:
                self.visualizer.close()

    def demo_mode(self, num_cycles=3):
        """
        데모 모드 - 정해진 횟수만큼 대화

        Args:
            num_cycles: 대화 횟수
        """
        print("\n" + "=" * 60)
        print(f"📢 데모 모드 ({num_cycles}번 대화)")
        print("=" * 60)

        for i in range(num_cycles):
            print(f"\n[{i+1}/{num_cycles}번째 대화]")
            self.listen_and_respond(duration=5.0)

            if i < num_cycles - 1:
                print("\n다음 명령까지 3초 대기...")
                time.sleep(3)

        print("\n✅ 데모 완료!")


def main():
    """메인 함수"""
    # API 키 확인
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("✗ OPENAI_API_KEY가 설정되지 않았습니다.")
        return 1

    # TTS 옵션
    print("\nTTS 옵션:")
    print("  1. OpenAI TTS (고품질, API 비용 발생)")
    print("  2. macOS 내장 (무료, 한국어 지원)")

    choice = input("\n선택 (1 또는 2, 기본=2): ").strip() or "2"
    use_openai_tts = (choice == "1")

    # 로봇 초기화
    robot = InteractiveRobot(api_key=api_key, use_openai_tts=use_openai_tts)

    # 모드 선택
    print("\n모드 선택:")
    print("  1. 연속 대화 모드")
    print("  2. 데모 모드 (3번만)")

    mode = input("\n선택 (1 또는 2): ").strip()

    if mode == "1":
        robot.run(enable_visualization=False)
    elif mode == "2":
        robot.demo_mode(num_cycles=3)
    else:
        print("잘못된 선택입니다.")
        return 1

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
