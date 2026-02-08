"""
음성 제어 로봇 자동 데모
"""

import os
from dotenv import load_dotenv
from src.brain.robot_brain import RobotBrain
from src.perception.speech_recognizer import VoiceCommandListener

load_dotenv()


def main():
    """자동 데모"""
    print("=" * 60)
    print("🎬 음성 제어 로봇 자동 데모")
    print("=" * 60)

    # API 키 확인
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("✗ OPENAI_API_KEY가 설정되지 않았습니다.")
        return 1

    # 초기화
    brain = RobotBrain(api_key=api_key, model="gpt-4o-mini")
    listener = VoiceCommandListener(api_key=api_key)
    print("✓ 시스템 초기화 완료\n")

    # 데모 시나리오
    demo_files = [
        "test_audio/command1.wav",
        "test_audio/command2.wav",
        "test_audio/command3.wav",
    ]

    for i, audio_file in enumerate(demo_files, 1):
        print("=" * 60)
        print(f"시나리오 {i}/3")
        print("=" * 60)

        if not os.path.exists(audio_file):
            print(f"✗ 파일 없음: {audio_file}")
            continue

        # 1. 음성 인식
        print(f"🎤 음성 파일: {audio_file}")
        user_speech = listener.listen_from_file(audio_file)

        # 2. AI 두뇌 처리
        print(f"\n🧠 로봇이 생각 중...")
        response = brain.think(user_speech)

        # 3. 응답
        print(f"\n💬 로봇: {response.speech}")

        # 4. 동작 계획
        if response.commands:
            print(f"\n📋 실행할 동작 ({len(response.commands)}개):")
            for j, cmd in enumerate(response.commands, 1):
                action_desc = f"{j}. {cmd.action_type}"
                if cmd.target_object:
                    action_desc += f" - {cmd.target_object}"
                print(f"  {action_desc}")
                print(f"     └ {cmd.reasoning}")
        else:
            print("\n📋 동작 없음")

        if response.needs_clarification:
            print(f"\n❓ {response.clarification_question}")

        print()

    # 대화 이력 테스트
    print("=" * 60)
    print("맥락 이해 테스트")
    print("=" * 60)

    brain.reset_conversation()

    # 연속된 대화
    conversation = [
        ("사용자", "파란 컵을 집어줘"),
        ("사용자", "그걸 테이블 왼쪽에 놓아줘"),
    ]

    for speaker, message in conversation:
        print(f"\n{speaker}: {message}")
        response = brain.think(message)
        print(f"로봇: {response.speech}")

    print("\n" + "=" * 60)
    print("✓ 데모 완료!")
    print("=" * 60)

    print("\n시스템 기능:")
    print("  ✓ 음성 인식 (Whisper)")
    print("  ✓ 자연어 이해 (GPT-4o)")
    print("  ✓ 대화 맥락 유지")
    print("  ✓ 동작 명령 생성")
    print("  ✓ 안전성 검증")

    print("\n다음 단계:")
    print("  - 시뮬레이션 환경 구축")
    print("  - 동작 실행 시스템")
    print("  - 실시간 마이크 입력")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
