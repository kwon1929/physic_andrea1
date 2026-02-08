"""
웨이크워드 감지 테스트
"자비스" 또는 "아트레이디스" 인식 테스트
"""

import os
from dotenv import load_dotenv
from src.perception.speech_recognizer import SpeechRecognizer
from src.perception.wake_word import SmartWakeWordDetector

load_dotenv()


def main():
    """웨이크워드 테스트"""
    print("=" * 60)
    print("🎤 웨이크워드 감지 테스트")
    print("=" * 60)

    # API 키 확인
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("✗ OPENAI_API_KEY가 필요합니다")
        return 1

    # 초기화
    recognizer = SpeechRecognizer(api_key=api_key)
    detector = SmartWakeWordDetector(recognizer)

    print("\n지원하는 웨이크워드:")
    for word in detector.wake_words:
        print(f"  - {word}")

    print("\n" + "=" * 60)
    print("연속 감지 모드")
    print("=" * 60)
    print("\n아무거나 말해보세요:")
    print("  '자비스' 또는 '아트레이디스'")
    print("  (Ctrl+C로 종료)\n")

    try:
        count = 0
        while count < 10:  # 10번 시도
            detected, text = detector.listen_smart(
                max_silence=1.5,
                min_volume=400
            )

            if detected:
                print(f"\n🎉 웨이크워드 감지됨! (시도 {count + 1})")
                print(f"   인식된 텍스트: '{text}'")
                count += 1

                if count < 10:
                    print("\n다시 말해보세요...")
            else:
                if text:
                    print(f"\n   '{text}' - 웨이크워드 아님")

    except KeyboardInterrupt:
        print("\n\n종료합니다.")

    print("\n" + "=" * 60)
    print(f"✅ 테스트 완료! ({count}번 성공)")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
