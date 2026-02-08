"""
마이크 장치 확인
"""

import sounddevice as sd


def main():
    print("=" * 60)
    print("🎤 마이크 장치 확인")
    print("=" * 60)

    print("\n사용 가능한 오디오 장치:")
    print(sd.query_devices())

    print("\n" + "=" * 60)
    print("✅ sounddevice가 정상적으로 작동합니다!")
    print("=" * 60)

    print("\n다음 단계:")
    print("  python test_voice_io.py")
    print("  - 마이크 녹음 → 음성 인식 → TTS 테스트")
    print("\n  python interactive_robot.py")
    print("  - 실제 대화형 로봇 실행")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
