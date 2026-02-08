"""
마이크 + TTS 테스트
녹음하고 음성 인식 후 TTS로 응답
"""

import os
from dotenv import load_dotenv
from src.perception.microphone import MicrophoneRecorder
from src.perception.speech_recognizer import SpeechRecognizer
from src.perception.text_to_speech import MacOSTTS

load_dotenv()


def test_microphone():
    """마이크 녹음 테스트"""
    print("=" * 60)
    print("🎤 마이크 테스트")
    print("=" * 60)

    mic = MicrophoneRecorder()

    # 장치 목록
    print("\n사용 가능한 장치:")
    mic.list_devices()

    # 녹음 테스트
    print("\n3초 녹음 테스트를 시작합니다...")
    input("준비되면 Enter를 누르세요...")

    audio_file = mic.record(duration=3.0)
    print(f"\n✓ 녹음 완료: {audio_file}")

    return audio_file


def test_speech_recognition(audio_file):
    """음성 인식 테스트"""
    print("\n" + "=" * 60)
    print("🎤 음성 인식 테스트")
    print("=" * 60)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("✗ OPENAI_API_KEY가 필요합니다")
        return None

    recognizer = SpeechRecognizer(api_key=api_key)

    print("\n음성 인식 중...")
    text = recognizer.transcribe_file(audio_file)

    print(f"✓ 인식 결과: {text}")
    return text


def test_tts(text):
    """TTS 테스트"""
    print("\n" + "=" * 60)
    print("🔊 TTS 테스트")
    print("=" * 60)

    tts = MacOSTTS()

    print(f"\n재생할 텍스트: {text}")
    tts.speak(text)

    print("✓ TTS 완료")


def main():
    """통합 테스트"""
    print("=" * 60)
    print("🎙️  음성 입출력 통합 테스트")
    print("=" * 60)

    # 1. 마이크 녹음
    audio_file = test_microphone()

    # 2. 음성 인식
    text = test_speech_recognition(audio_file)

    if text:
        # 3. TTS로 따라 말하기
        response = f"방금 이렇게 말씀하셨습니다. {text}"
        test_tts(response)

    print("\n" + "=" * 60)
    print("✅ 테스트 완료!")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
