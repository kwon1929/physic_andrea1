"""
음성 인식 모듈 테스트
"""

import os
from dotenv import load_dotenv

load_dotenv()


def test_speech_recognition():
    """음성 인식 테스트"""

    print("=" * 60)
    print("음성 인식 모듈 테스트")
    print("=" * 60)

    # API 키 확인
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("✗ OPENAI_API_KEY가 설정되지 않았습니다.")
        return 1

    print("✓ OpenAI API 키 확인 완료")

    # 모듈 임포트
    from src.perception.speech_recognizer import VoiceCommandListener

    print("✓ 음성 인식 모듈 임포트 성공")

    # VoiceCommandListener 초기화
    listener = VoiceCommandListener(api_key=api_key)
    print("✓ VoiceCommandListener 초기화 완료")

    # 테스트 오디오 파일
    test_files = [
        "test_audio/command1.wav",
        "test_audio/command2.wav",
        "test_audio/command3.wav",
    ]

    expected_texts = [
        "빨간 블록을 집어줘",
        "초기 위치로 돌아가",
        "그리퍼를 열어줘",
    ]

    print("\n" + "=" * 60)
    print("음성 파일 인식 테스트")
    print("=" * 60)

    for i, (audio_file, expected) in enumerate(zip(test_files, expected_texts), 1):
        if not os.path.exists(audio_file):
            print(f"\n✗ 파일 없음: {audio_file}")
            print("  먼저 'python create_test_audio.py'를 실행하세요.")
            continue

        print(f"\n[테스트 {i}]")
        print(f"파일: {audio_file}")
        print(f"예상: {expected}")
        print("-" * 60)

        try:
            recognized_text = listener.listen_from_file(audio_file)

            # 결과 비교
            if recognized_text.strip() == expected.strip():
                print("✓ 정확하게 인식됨!")
            else:
                print(f"⚠ 인식되었으나 예상과 다름")
                print(f"  예상: {expected}")
                print(f"  결과: {recognized_text}")

        except Exception as e:
            print(f"✗ 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return 1

    print("\n" + "=" * 60)
    print("✓ 음성 인식 테스트 완료!")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(test_speech_recognition())
