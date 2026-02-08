"""
AI Brain 모듈 테스트 스크립트
로봇의 두뇌가 제대로 작동하는지 테스트합니다.
"""

import sys
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()


def test_brain_basic():
    """기본 동작 테스트"""
    print("=" * 60)
    print("AI Brain 기본 동작 테스트")
    print("=" * 60)

    # API 키 확인
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("✗ OPENAI_API_KEY가 .env 파일에 설정되지 않았습니다.")
        print("\n.env 파일을 만들고 다음을 추가하세요:")
        print("OPENAI_API_KEY=your_api_key_here")
        return False

    print("✓ OpenAI API 키 확인 완료")

    # RobotBrain 임포트 및 초기화
    try:
        from src.brain.robot_brain import RobotBrain

        print("✓ RobotBrain 모듈 임포트 성공")

        brain = RobotBrain(api_key=api_key, model="gpt-4o-mini")
        print("✓ RobotBrain 인스턴스 생성 성공 (모델: gpt-4o-mini)")
    except Exception as e:
        print(f"✗ RobotBrain 초기화 실패: {e}")
        return False

    return brain


def test_simple_commands(brain):
    """간단한 명령 테스트"""
    print("\n" + "=" * 60)
    print("간단한 명령 테스트")
    print("=" * 60)

    test_cases = [
        "빨간 블록을 집어줘",
        "초기 위치로 돌아가",
        "그리퍼를 열어줘",
    ]

    for i, command in enumerate(test_cases, 1):
        print(f"\n[테스트 {i}] 사용자: {command}")
        try:
            response = brain.think(command)
            print(f"로봇: {response.speech}")
            print(f"동작 개수: {len(response.commands)}")

            for j, cmd in enumerate(response.commands, 1):
                print(f"  동작 {j}: {cmd.action_type}")
                if cmd.target_object:
                    print(f"    대상: {cmd.target_object}")
                print(f"    이유: {cmd.reasoning}")

            if response.needs_clarification:
                print(f"  질문: {response.clarification_question}")

            print("✓ 응답 생성 성공")
        except Exception as e:
            print(f"✗ 오류 발생: {e}")
            return False

    return True


def test_context_awareness(brain):
    """맥락 이해 테스트 (이전 대화 기억)"""
    print("\n" + "=" * 60)
    print("맥락 이해 테스트")
    print("=" * 60)

    brain.reset_conversation()

    conversation = [
        "파란 컵을 집어줘",
        "그걸 테이블 왼쪽에 놓아줘",
        "아니, 오른쪽이 나을 것 같아",
    ]

    for i, msg in enumerate(conversation, 1):
        print(f"\n[대화 {i}] 사용자: {msg}")
        try:
            response = brain.think(msg)
            print(f"로봇: {response.speech}")
            print("✓ 맥락 유지 성공")
        except Exception as e:
            print(f"✗ 오류 발생: {e}")
            return False

    return True


def test_clarification(brain):
    """불명확한 명령 처리 테스트"""
    print("\n" + "=" * 60)
    print("불명확한 명령 처리 테스트")
    print("=" * 60)

    brain.reset_conversation()

    command = "저거 좀 옮겨줘"
    print(f"\n사용자: {command}")

    try:
        response = brain.think(command)
        print(f"로봇: {response.speech}")

        if response.needs_clarification:
            print("✓ 불명확한 명령을 감지하고 질문함")
            print(f"  질문: {response.clarification_question}")
        else:
            print("⚠ 명령이 불명확한데 질문하지 않음 (개선 필요)")

    except Exception as e:
        print(f"✗ 오류 발생: {e}")
        return False

    return True


def interactive_mode(brain):
    """대화형 모드"""
    print("\n" + "=" * 60)
    print("대화형 모드 (종료: 'quit', 초기화: 'reset')")
    print("=" * 60)

    brain.reset_conversation()

    while True:
        try:
            user_input = input("\n사용자: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit", "종료"]:
                print("대화를 종료합니다.")
                break

            if user_input.lower() == "reset":
                brain.reset_conversation()
                print("대화 이력이 초기화되었습니다.")
                continue

            if user_input.lower() == "history":
                print("\n[대화 이력]")
                print(brain.get_conversation_summary())
                continue

            response = brain.think(user_input)
            print(f"\n로봇: {response.speech}")

            if response.commands:
                print(f"\n[계획된 동작: {len(response.commands)}개]")
                for i, cmd in enumerate(response.commands, 1):
                    print(f"  {i}. {cmd.action_type}", end="")
                    if cmd.target_object:
                        print(f" ({cmd.target_object})", end="")
                    print(f" - {cmd.reasoning}")

        except KeyboardInterrupt:
            print("\n\n대화를 종료합니다.")
            break
        except Exception as e:
            print(f"\n오류 발생: {e}")


def main():
    """메인 테스트 함수"""
    # 기본 동작 테스트
    brain = test_brain_basic()
    if not brain:
        return 1

    # 자동 테스트 실행
    print("\n자동 테스트를 실행할까요? (y/n)")
    choice = input("> ").strip().lower()

    if choice == "y":
        if not test_simple_commands(brain):
            return 1

        if not test_context_awareness(brain):
            return 1

        if not test_clarification(brain):
            return 1

        print("\n" + "=" * 60)
        print("모든 자동 테스트 통과!")
        print("=" * 60)

    # 대화형 모드
    print("\n대화형 모드로 전환할까요? (y/n)")
    choice = input("> ").strip().lower()

    if choice == "y":
        interactive_mode(brain)

    return 0


if __name__ == "__main__":
    sys.exit(main())
