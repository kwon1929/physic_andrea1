"""
Physical AI - 메인 프로그램
음성 제어 지능형 로봇팔 시스템
"""

import os
from dotenv import load_dotenv
from src.brain.robot_brain import RobotBrain
from src.perception.speech_recognizer import VoiceCommandListener
from src.simulation.simple_robot_sim import SimpleRobotSimulator
from src.motion.action_executor import ActionExecutor

load_dotenv()


class PhysicalAIRobot:
    """
    Physical AI 로봇 시스템
    음성 인식 → AI 두뇌 → 동작 실행의 전체 파이프라인
    """

    def __init__(self, api_key: str):
        """
        Args:
            api_key: OpenAI API 키
        """
        print("=" * 60)
        print("Physical AI - 음성 제어 로봇 시스템")
        print("=" * 60)

        # 각 모듈 초기화
        print("\n초기화 중...")
        self.brain = RobotBrain(api_key=api_key, model="gpt-4o-mini")
        print("✓ AI 두뇌 초기화")

        self.listener = VoiceCommandListener(api_key=api_key)
        print("✓ 음성 인식 초기화")

        self.simulator = SimpleRobotSimulator()
        print("✓ 시뮬레이터 초기화")

        self.executor = ActionExecutor(self.simulator)
        print("✓ 동작 실행기 초기화")

        print("\n✅ 시스템 준비 완료!")

    def process_voice_command(self, audio_file_path: str):
        """
        음성 파일로부터 전체 파이프라인 실행

        Args:
            audio_file_path: 음성 파일 경로
        """
        print("\n" + "=" * 60)
        print("🎤 음성 명령 처리 시작")
        print("=" * 60)

        # 1. 음성 인식
        print("\n[1단계] 음성 인식")
        try:
            user_speech = self.listener.listen_from_file(audio_file_path)
        except Exception as e:
            print(f"✗ 음성 인식 실패: {e}")
            return

        # 2. AI 두뇌 처리
        print("\n[2단계] AI 사고 및 계획")
        print(f"🧠 로봇이 생각 중...")
        response = self.brain.think(user_speech)

        print(f"\n💬 로봇: {response.speech}")

        # 3. 동작 계획 확인
        if response.needs_clarification:
            print(f"\n❓ 추가 질문: {response.clarification_question}")
            print("(추가 정보가 필요하여 동작을 실행하지 않습니다)")
            return

        if not response.commands:
            print("\n(대화만 하고 동작은 없습니다)")
            return

        # 4. 동작 실행
        print("\n[3단계] 동작 실행")
        self.executor.execute_commands(response.commands)

        # 5. 결과 확인
        print(self.simulator.get_state_summary())

    def demo_mode(self):
        """데모 모드 - 미리 준비된 음성으로 시연"""
        print("\n" + "=" * 60)
        print("🎬 데모 모드")
        print("=" * 60)

        demo_scenarios = [
            {
                "file": "test_audio/command1.wav",
                "description": "빨간 블록 집기"
            },
            {
                "file": "test_audio/command2.wav",
                "description": "초기 위치로 복귀"
            },
            {
                "file": "test_audio/command3.wav",
                "description": "그리퍼 열기"
            },
        ]

        for i, scenario in enumerate(demo_scenarios, 1):
            audio_file = scenario["file"]
            description = scenario["description"]

            if not os.path.exists(audio_file):
                print(f"\n✗ 파일 없음: {audio_file}")
                print("먼저 'python create_test_audio.py'를 실행하세요.")
                return

            print(f"\n{'='*60}")
            print(f"시나리오 {i}/{len(demo_scenarios)}: {description}")
            print(f"{'='*60}")

            self.process_voice_command(audio_file)

            if i < len(demo_scenarios):
                input("\n[Enter 키를 눌러 다음 시나리오로...]")

        print("\n" + "=" * 60)
        print("✅ 데모 완료!")
        print("=" * 60)

    def interactive_mode(self):
        """대화형 모드"""
        print("\n" + "=" * 60)
        print("💬 대화형 모드")
        print("=" * 60)
        print("명령:")
        print("  - 오디오 파일 경로 입력하여 음성 명령 실행")
        print("  - 'state': 현재 로봇 상태 확인")
        print("  - 'reset': 대화 초기화")
        print("  - 'quit': 종료")
        print("=" * 60)

        while True:
            try:
                user_input = input("\n입력> ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ["quit", "exit", "종료"]:
                    print("시스템을 종료합니다.")
                    break

                if user_input.lower() == "reset":
                    self.brain.reset_conversation()
                    print("✓ 대화 이력 초기화 완료")
                    continue

                if user_input.lower() == "state":
                    print(self.simulator.get_state_summary())
                    continue

                # 파일 존재 확인
                if not os.path.exists(user_input):
                    print(f"✗ 파일을 찾을 수 없습니다: {user_input}")
                    continue

                # 음성 명령 처리
                self.process_voice_command(user_input)

            except KeyboardInterrupt:
                print("\n\n시스템을 종료합니다.")
                break
            except Exception as e:
                print(f"\n✗ 오류 발생: {e}")


def main():
    """메인 함수"""
    # API 키 확인
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("✗ OPENAI_API_KEY가 설정되지 않았습니다.")
        print(".env 파일을 확인하세요.")
        return 1

    # 로봇 시스템 초기화
    robot = PhysicalAIRobot(api_key=api_key)

    # 모드 선택
    print("\n모드를 선택하세요:")
    print("  1. 데모 모드 (자동 시연)")
    print("  2. 대화형 모드 (직접 제어)")

    choice = input("\n선택 (1 또는 2): ").strip()

    if choice == "1":
        robot.demo_mode()
    elif choice == "2":
        robot.interactive_mode()
    else:
        print("잘못된 선택입니다.")
        return 1

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
