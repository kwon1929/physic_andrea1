"""
Physical AI 자동 데모
전체 시스템 자동 시연
"""

import os
from dotenv import load_dotenv
from src.brain.robot_brain import RobotBrain
from src.perception.speech_recognizer import VoiceCommandListener
from src.simulation.simple_robot_sim import SimpleRobotSimulator
from src.motion.action_executor import ActionExecutor

load_dotenv()


def main():
    """자동 데모"""
    print("=" * 60)
    print("🎬 Physical AI - 전체 시스템 자동 데모")
    print("=" * 60)

    # API 키 확인
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("✗ OPENAI_API_KEY가 설정되지 않았습니다.")
        return 1

    # 시스템 초기화
    print("\n시스템 초기화 중...")
    brain = RobotBrain(api_key=api_key, model="gpt-4o-mini")
    listener = VoiceCommandListener(api_key=api_key)
    simulator = SimpleRobotSimulator()
    executor = ActionExecutor(simulator)
    print("✅ 초기화 완료\n")

    # 데모 시나리오
    scenarios = [
        ("test_audio/command1.wav", "빨간 블록 집기"),
        ("test_audio/command2.wav", "초기 위치로 복귀"),
    ]

    for i, (audio_file, description) in enumerate(scenarios, 1):
        print("=" * 60)
        print(f"시나리오 {i}/{len(scenarios)}: {description}")
        print("=" * 60)

        if not os.path.exists(audio_file):
            print(f"✗ 파일 없음: {audio_file}")
            continue

        # 1. 음성 인식
        print("\n[1단계] 음성 인식")
        user_speech = listener.listen_from_file(audio_file)

        # 2. AI 두뇌
        print("\n[2단계] AI 사고 및 계획")
        print("🧠 로봇이 생각 중...")
        response = brain.think(user_speech)
        print(f"\n💬 로봇: {response.speech}")

        # 3. 동작 실행
        if response.commands:
            print("\n[3단계] 동작 실행")
            executor.execute_commands(response.commands)

        # 4. 상태 확인
        print(simulator.get_state_summary())
        print()

    # 최종 요약
    print("=" * 60)
    print("✅ 데모 완료!")
    print("=" * 60)

    print("\n시스템 구성:")
    print("  🎤 음성 인식: OpenAI Whisper API")
    print("  🧠 AI 두뇌: GPT-4o-mini")
    print("  🤖 시뮬레이터: 간단한 6DOF 로봇팔")
    print("  ⚙️  동작 실행: pick, place, move, home 등")

    print("\n시스템 특징:")
    print("  ✓ 음성으로 자연스럽게 명령")
    print("  ✓ AI가 상황을 이해하고 판단")
    print("  ✓ 대화 맥락 기억")
    print("  ✓ 불명확한 명령은 질문")
    print("  ✓ 안전성 검증")

    print("\n다음 단계:")
    print("  - 실제 마이크 입력 지원")
    print("  - 비전 시스템 추가 (카메라)")
    print("  - 하드웨어 로봇팔 연결")
    print("  - 더 복잡한 동작 지원")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
