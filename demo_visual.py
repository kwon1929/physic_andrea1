"""
Physical AI 시각화 데모
로봇이 동작하는 걸 눈으로 볼 수 있는 데모
"""

import os
from dotenv import load_dotenv
from src.brain.robot_brain import RobotBrain
from src.perception.speech_recognizer import VoiceCommandListener
from src.simulation.simple_robot_sim import SimpleRobotSimulator
from src.motion.action_executor import ActionExecutor
from src.simulation.visualizer import RobotVisualizer
import time

load_dotenv()


def main():
    """시각화 데모"""
    print("=" * 60)
    print("🎬 Physical AI - 시각화 데모")
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

    # 시각화 초기화
    print("시각화 창 열기...")
    visualizer = RobotVisualizer(interactive=True)

    print("✅ 초기화 완료\n")

    # 초기 상태 표시
    print("초기 상태 표시 중...")
    visualizer.draw_state(simulator, title="초기 상태")
    time.sleep(2)

    # 데모 시나리오
    scenarios = [
        {
            "file": "test_audio/command1.wav",
            "description": "빨간 블록 집기"
        },
        {
            "file": "test_audio/command2.wav",
            "description": "초기 위치로 복귀"
        },
    ]

    for i, scenario in enumerate(scenarios, 1):
        audio_file = scenario["file"]
        description = scenario["description"]

        print("\n" + "=" * 60)
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

        # 3. 동작 실행 (시각화 포함)
        if response.commands:
            print("\n[3단계] 동작 실행")
            print(f"⚙️  {len(response.commands)}개 동작 실행 시작")

            for j, command in enumerate(response.commands, 1):
                print(f"\n[동작 {j}/{len(response.commands)}]")
                print(f"⚙️  실행: {command.action_type}", end="")
                if command.target_object:
                    print(f" (대상: {command.target_object})", end="")
                print(f" - {command.reasoning}")

                # 동작 전 상태
                visualizer.draw_state(simulator, title=f"동작 {j} 실행 전")

                # 동작 실행
                executor.execute_command(command)

                # 동작 후 상태
                visualizer.draw_state(simulator, title=f"동작 {j} 완료")
                time.sleep(1)

        else:
            print("\n(대화만 하고 동작은 없습니다)")

        # 최종 상태
        print("\n" + "=" * 60)
        print("최종 상태:")
        print(simulator.get_state_summary())
        visualizer.draw_state(simulator, title=f"시나리오 {i} 완료")

        if i < len(scenarios):
            print("\n[다음 시나리오로 계속...]")
            time.sleep(3)

    # 완료
    print("\n" + "=" * 60)
    print("✅ 데모 완료!")
    print("=" * 60)
    print("\n시각화 창이 열려있습니다.")
    print("창을 닫으려면 아무 키나 누르세요...")

    input()
    visualizer.close()

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
