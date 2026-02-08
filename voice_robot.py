"""
음성 제어 로봇 - Brain + Speech 통합
음성으로 로봇과 대화하고 명령하기
"""

import os
from dotenv import load_dotenv
from src.brain.robot_brain import RobotBrain
from src.perception.speech_recognizer import VoiceCommandListener

load_dotenv()


class VoiceControlledRobot:
    """
    음성으로 제어되는 지능형 로봇
    음성 인식 → AI 두뇌 → 동작 명령
    """

    def __init__(self, api_key: str):
        """
        Args:
            api_key: OpenAI API 키
        """
        self.brain = RobotBrain(api_key=api_key, model="gpt-4o-mini")
        self.listener = VoiceCommandListener(api_key=api_key)
        print("✓ 음성 제어 로봇 초기화 완료")

    def process_voice_command(self, audio_file_path: str):
        """
        음성 파일로부터 명령을 받아 처리

        Args:
            audio_file_path: 음성 파일 경로

        Returns:
            응답 텍스트와 동작 명령
        """
        print("\n" + "=" * 60)
        print("🎤 음성 명령 처리")
        print("=" * 60)

        # 1. 음성 인식
        try:
            user_speech = self.listener.listen_from_file(audio_file_path)
        except Exception as e:
            print(f"✗ 음성 인식 실패: {e}")
            return None

        # 2. AI 두뇌로 사고
        print(f"\n🧠 로봇이 생각 중...")
        response = self.brain.think(user_speech)

        # 3. 응답 출력
        print(f"\n💬 로봇: {response.speech}")

        # 4. 동작 계획 출력
        if response.commands:
            print(f"\n📋 계획된 동작 ({len(response.commands)}개):")
            for i, cmd in enumerate(response.commands, 1):
                print(f"  {i}. {cmd.action_type}", end="")
                if cmd.target_object:
                    print(f" - {cmd.target_object}", end="")
                print()
                print(f"     └ {cmd.reasoning}")
        else:
            print("\n📋 동작 없음 (대화만)")

        if response.needs_clarification:
            print(f"\n❓ 추가 질문: {response.clarification_question}")

        return response

    def interactive_mode(self):
        """대화형 모드 (오디오 파일 기반)"""
        print("\n" + "=" * 60)
        print("대화형 모드 시작")
        print("=" * 60)
        print("명령:")
        print("  - 오디오 파일 경로 입력")
        print("  - 'quit' 또는 'exit': 종료")
        print("  - 'reset': 대화 초기화")
        print("=" * 60)

        while True:
            try:
                user_input = input("\n오디오 파일 경로 (또는 명령): ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ["quit", "exit", "종료"]:
                    print("대화를 종료합니다.")
                    break

                if user_input.lower() == "reset":
                    self.brain.reset_conversation()
                    print("✓ 대화 이력 초기화 완료")
                    continue

                # 파일 존재 확인
                if not os.path.exists(user_input):
                    print(f"✗ 파일을 찾을 수 없습니다: {user_input}")
                    continue

                # 음성 명령 처리
                self.process_voice_command(user_input)

            except KeyboardInterrupt:
                print("\n\n대화를 종료합니다.")
                break
            except Exception as e:
                print(f"\n✗ 오류 발생: {e}")

    def demo_mode(self):
        """데모 모드 - 미리 준비된 음성 파일로 시연"""
        print("\n" + "=" * 60)
        print("🎬 데모 모드 - 음성 제어 로봇 시연")
        print("=" * 60)

        demo_files = [
            "test_audio/command1.wav",
            "test_audio/command2.wav",
            "test_audio/command3.wav",
        ]

        for audio_file in demo_files:
            if not os.path.exists(audio_file):
                print(f"\n✗ 데모 파일 없음: {audio_file}")
                print("먼저 'python create_test_audio.py'를 실행하세요.")
                return

            self.process_voice_command(audio_file)

            # 다음 명령 전 대기
            input("\n[Enter 키를 눌러 다음 명령 실행...]")

        print("\n" + "=" * 60)
        print("✓ 데모 완료!")
        print("=" * 60)


def main():
    """메인 함수"""
    print("=" * 60)
    print("음성 제어 로봇 시스템")
    print("=" * 60)

    # API 키 확인
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("✗ OPENAI_API_KEY가 설정되지 않았습니다.")
        print(".env 파일을 확인하세요.")
        return 1

    # 로봇 초기화
    robot = VoiceControlledRobot(api_key=api_key)

    # 모드 선택
    print("\n모드를 선택하세요:")
    print("  1. 데모 모드 (자동 시연)")
    print("  2. 대화형 모드 (직접 파일 선택)")

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
