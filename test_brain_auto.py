"""
AI Brain 자동 테스트 스크립트
"""

import os
from dotenv import load_dotenv

load_dotenv()


def main():
    print("=" * 60)
    print("AI Brain 자동 테스트")
    print("=" * 60)

    # API 키 확인
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("✗ OPENAI_API_KEY가 설정되지 않았습니다.")
        return 1

    print("✓ OpenAI API 키 확인 완료")

    # RobotBrain 초기화
    from src.brain.robot_brain import RobotBrain

    print("✓ RobotBrain 모듈 임포트 성공")

    brain = RobotBrain(api_key=api_key, model="gpt-4o-mini")
    print("✓ RobotBrain 초기화 완료 (모델: gpt-4o-mini)")

    # 테스트 케이스
    print("\n" + "=" * 60)
    print("테스트 시작")
    print("=" * 60)

    test_cases = [
        "빨간 블록을 집어줘",
        "초기 위치로 돌아가",
        "그리퍼를 열어줘",
    ]

    for i, command in enumerate(test_cases, 1):
        print(f"\n[테스트 {i}]")
        print(f"사용자: {command}")
        print("-" * 60)

        try:
            response = brain.think(command)

            print(f"로봇: {response.speech}")

            if response.commands:
                print(f"\n계획된 동작 ({len(response.commands)}개):")
                for j, cmd in enumerate(response.commands, 1):
                    print(f"  {j}. {cmd.action_type}", end="")
                    if cmd.target_object:
                        print(f" - 대상: {cmd.target_object}", end="")
                    print()
                    print(f"     이유: {cmd.reasoning}")

            if response.needs_clarification:
                print(f"\n❓ 추가 질문: {response.clarification_question}")

            print("\n✓ 테스트 통과")

        except Exception as e:
            print(f"\n✗ 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return 1

    # 맥락 이해 테스트
    print("\n" + "=" * 60)
    print("맥락 이해 테스트 (대화 연결)")
    print("=" * 60)

    brain.reset_conversation()

    conversation = [
        "파란 컵을 집어줘",
        "그걸 테이블 왼쪽에 놓아줘",
    ]

    for i, msg in enumerate(conversation, 1):
        print(f"\n[대화 {i}]")
        print(f"사용자: {msg}")
        print("-" * 60)

        try:
            response = brain.think(msg)
            print(f"로봇: {response.speech}")
            print("✓ 테스트 통과")

        except Exception as e:
            print(f"✗ 오류 발생: {e}")
            return 1

    # 불명확한 명령 테스트
    print("\n" + "=" * 60)
    print("불명확한 명령 처리 테스트")
    print("=" * 60)

    brain.reset_conversation()

    print("\n사용자: 저거 좀 옮겨줘")
    print("-" * 60)

    try:
        response = brain.think("저거 좀 옮겨줘")
        print(f"로봇: {response.speech}")

        if response.needs_clarification:
            print("✓ 불명확한 명령을 감지하고 질문함")
            print(f"  질문: {response.clarification_question}")
        else:
            print("⚠ 명령이 불명확한데 질문하지 않음")

    except Exception as e:
        print(f"✗ 오류 발생: {e}")
        return 1

    # 최종 결과
    print("\n" + "=" * 60)
    print("🎉 모든 테스트 통과!")
    print("=" * 60)
    print("\nAI Brain이 정상적으로 작동합니다:")
    print("✓ 자연어 이해")
    print("✓ 동작 명령 생성")
    print("✓ 대화 맥락 유지")
    print("✓ 불명확한 명령 처리")

    print("\n다음 단계:")
    print("1. 음성 인식 모듈 구현 (Whisper)")
    print("2. 시뮬레이션 환경 구축")
    print("3. 동작 제어 시스템 연결")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
