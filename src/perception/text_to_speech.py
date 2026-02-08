"""
Text-to-Speech 모듈
OpenAI TTS API를 사용한 음성 합성
"""

import subprocess
import tempfile
from openai import OpenAI
import os


class TextToSpeech:
    """
    텍스트를 음성으로 변환
    """

    def __init__(self, api_key: str, voice: str = "alloy"):
        """
        Args:
            api_key: OpenAI API 키
            voice: 음성 종류 (alloy, echo, fable, onyx, nova, shimmer)
        """
        self.client = OpenAI(api_key=api_key)
        self.voice = voice

    def speak(self, text: str, play_audio: bool = True) -> str:
        """
        텍스트를 음성으로 변환하고 재생

        Args:
            text: 말할 텍스트
            play_audio: 자동 재생 여부

        Returns:
            str: 생성된 오디오 파일 경로
        """
        print(f"\n🔊 로봇: {text}")

        try:
            # OpenAI TTS API 호출
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=self.voice,
                input=text
            )

            # 임시 파일로 저장
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            response.stream_to_file(temp_file.name)

            # 재생
            if play_audio:
                self._play_audio(temp_file.name)

            return temp_file.name

        except Exception as e:
            print(f"✗ TTS 오류: {e}")
            # 폴백: macOS say 명령 사용
            print("  → macOS 내장 음성 사용")
            subprocess.run(["say", text], check=False)
            return ""

    def _play_audio(self, audio_file: str):
        """
        오디오 파일 재생 (macOS)

        Args:
            audio_file: 재생할 오디오 파일 경로
        """
        try:
            # macOS에서 afplay 사용
            subprocess.run(["afplay", audio_file], check=True)
        except FileNotFoundError:
            print("  ⚠ 오디오 재생 실패 (afplay 없음)")
        except Exception as e:
            print(f"  ⚠ 오디오 재생 오류: {e}")


class MacOSTTS:
    """
    macOS 내장 TTS 사용 (폴백용, 무료)
    """

    def __init__(self, voice: str = "Yuna"):
        """
        Args:
            voice: macOS 음성 (Yuna: 한국어, Samantha: 영어 등)
        """
        self.voice = voice

    def speak(self, text: str, play_audio: bool = True):
        """
        텍스트를 음성으로 변환 및 재생

        Args:
            text: 말할 텍스트
            play_audio: 재생 여부
        """
        print(f"\n🔊 로봇: {text}")

        try:
            if play_audio:
                # 직접 재생
                subprocess.run(["say", "-v", self.voice, text], check=True)
            else:
                # 파일로 저장
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.aiff')
                subprocess.run(
                    ["say", "-v", self.voice, "-o", temp_file.name, text],
                    check=True
                )
                return temp_file.name
        except Exception as e:
            print(f"✗ TTS 오류: {e}")
            return ""


def create_tts(api_key: str = None, use_openai: bool = True):
    """
    TTS 인스턴스 생성 (자동 선택)

    Args:
        api_key: OpenAI API 키 (선택사항)
        use_openai: OpenAI TTS 사용 여부

    Returns:
        TextToSpeech 또는 MacOSTTS 인스턴스
    """
    if use_openai and api_key:
        try:
            return TextToSpeech(api_key=api_key)
        except Exception as e:
            print(f"⚠ OpenAI TTS 초기화 실패: {e}")
            print("→ macOS 내장 TTS로 전환")

    # 폴백: macOS 내장 TTS
    return MacOSTTS()
