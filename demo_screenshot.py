"""
Physical AI 스크린샷 데모
시각화를 이미지로 저장
"""

import os
from dotenv import load_dotenv
from src.brain.robot_brain import RobotBrain
from src.perception.speech_recognizer import VoiceCommandListener
from src.simulation.simple_robot_sim import SimpleRobotSimulator
from src.motion.action_executor import ActionExecutor
from src.simulation.visualizer import RobotVisualizer

load_dotenv()


def main():
    """스크린샷 데모"""
    print("=" * 60)
    print("📸 Physical AI - 스크린샷 데모")
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

    # 시각화 초기화 (non-interactive)
    visualizer = RobotVisualizer(interactive=False)

    print("✅ 초기화 완료\n")

    # 출력 디렉토리
    os.makedirs("output", exist_ok=True)

    # 초기 상태 저장
    print("1. 초기 상태 스크린샷...")
    visualizer.draw_state(simulator, title="초기 상태")
    visualizer.save("output/01_initial.png")

    # 시나리오 1: 빨간 블록 집기
    print("\n" + "=" * 60)
    print("시나리오 1: 빨간 블록 집기")
    print("=" * 60)

    audio_file = "test_audio/command1.wav"
    if os.path.exists(audio_file):
        # 음성 인식
        print("\n🎤 음성 인식...")
        user_speech = listener.listen_from_file(audio_file)

        # AI 두뇌
        print("🧠 AI 사고...")
        response = brain.think(user_speech)
        print(f"💬 로봇: {response.speech}")

        # 동작 실행
        if response.commands:
            print(f"\n⚙️  동작 실행: {len(response.commands)}개")

            for j, command in enumerate(response.commands, 1):
                print(f"  {j}. {command.action_type}", end="")
                if command.target_object:
                    print(f" - {command.target_object}", end="")
                print()

                executor.execute_command(command)

                # 스크린샷 저장
                visualizer.draw_state(simulator, title=f"동작 {j} 완료")
                visualizer.save(f"output/02_action_{j}.png")

        print(f"\n2. 블록 집은 후 스크린샷 저장 완료")

    # 시나리오 2: 초기 위치로 복귀
    print("\n" + "=" * 60)
    print("시나리오 2: 초기 위치로 복귀")
    print("=" * 60)

    audio_file = "test_audio/command2.wav"
    if os.path.exists(audio_file):
        # 음성 인식
        print("\n🎤 음성 인식...")
        user_speech = listener.listen_from_file(audio_file)

        # AI 두뇌
        print("🧠 AI 사고...")
        response = brain.think(user_speech)
        print(f"💬 로봇: {response.speech}")

        # 동작 실행
        if response.commands:
            print(f"\n⚙️  동작 실행: {len(response.commands)}개")
            executor.execute_commands(response.commands)

            # 스크린샷 저장
            visualizer.draw_state(simulator, title="초기 위치 복귀")
            visualizer.save("output/03_home.png")

        print(f"\n3. 초기 위치 복귀 후 스크린샷 저장 완료")

    # 완료
    print("\n" + "=" * 60)
    print("✅ 스크린샷 데모 완료!")
    print("=" * 60)

    print("\n생성된 이미지:")
    for filename in sorted(os.listdir("output")):
        if filename.endswith(".png"):
            print(f"  - output/{filename}")

    print("\n이미지를 열어서 로봇의 동작을 확인하세요!")

    visualizer.close()

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
