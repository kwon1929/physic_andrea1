"""
Speech Recognition Module
음성 인식 모듈 - OpenAI Whisper API 사용
"""

import io
import wave
from typing import Optional
from openai import OpenAI


class SpeechRecognizer:
    """
    음성 인식 클래스
    마이크 입력 또는 오디오 파일을 받아 텍스트로 변환
    """

    def __init__(self, api_key: str, model: str = "whisper-1"):
        """
        Args:
            api_key: OpenAI API 키
            model: Whisper 모델 (기본: whisper-1)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def transcribe_file(self, audio_file_path: str, language: str = "en") -> str:
        """
        오디오 파일을 텍스트로 변환

        Args:
            audio_file_path: 오디오 파일 경로 (.wav, .mp3, .m4a 등)
            language: 언어 코드 (ko: 한국어, en: 영어)

        Returns:
            str: 변환된 텍스트
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    language=language,
                    response_format="text"
                )
            return transcript.strip()
        except Exception as e:
            raise Exception(f"음성 인식 실패: {str(e)}")

    def transcribe_bytes(self, audio_data: bytes, format: str = "wav", language: str = "en") -> str:
        """
        바이트 데이터를 텍스트로 변환

        Args:
            audio_data: 오디오 바이트 데이터
            format: 오디오 포맷 (wav, mp3 등)
            language: 언어 코드

        Returns:
            str: 변환된 텍스트
        """
        try:
            # 바이트 데이터를 파일처럼 다루기
            audio_file = io.BytesIO(audio_data)
            audio_file.name = f"audio.{format}"

            transcript = self.client.audio.transcriptions.create(
                model=self.model,
                file=audio_file,
                language=language,
                response_format="text"
            )
            return transcript.strip()
        except Exception as e:
            raise Exception(f"음성 인식 실패: {str(e)}")


class AudioRecorder:
    """
    마이크로 음성 녹음
    macOS에서 기본적으로 사용 가능한 방식
    """

    def __init__(self, sample_rate: int = 16000, channels: int = 1):
        """
        Args:
            sample_rate: 샘플링 레이트 (Hz)
            channels: 채널 수 (1: 모노, 2: 스테레오)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.frames = []

    def record_from_file(self, duration: float = 5.0) -> bytes:
        """
        임시: 파일 기반 녹음 (실제 마이크 녹음은 추후 구현)

        Args:
            duration: 녹음 시간 (초)

        Returns:
            bytes: WAV 포맷 오디오 데이터
        """
        # 실제 구현은 pyaudio 또는 sounddevice 사용
        # 지금은 테스트용 더미 구현
        raise NotImplementedError(
            "실시간 마이크 녹음은 pyaudio 또는 sounddevice 설치 후 사용 가능합니다.\n"
            "현재는 오디오 파일을 사용하세요."
        )

    def save_to_wav(self, audio_data: bytes, filename: str):
        """
        오디오 데이터를 WAV 파일로 저장

        Args:
            audio_data: 오디오 바이트 데이터
            filename: 저장할 파일명
        """
        with wave.open(filename, "wb") as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_data)


class VoiceCommandListener:
    """
    음성 명령 리스너
    음성 입력을 받아 텍스트로 변환하고 Brain에 전달
    """

    def __init__(self, api_key: str):
        """
        Args:
            api_key: OpenAI API 키
        """
        self.recognizer = SpeechRecognizer(api_key=api_key)
        self.recorder = AudioRecorder()

    def listen_from_file(self, audio_file_path: str) -> str:
        """
        오디오 파일에서 명령 추출

        Args:
            audio_file_path: 오디오 파일 경로

        Returns:
            str: 인식된 텍스트
        """
        print(f"🎤 오디오 파일 분석 중: {audio_file_path}")
        text = self.recognizer.transcribe_file(audio_file_path)
        print(f"📝 인식 결과: {text}")
        return text

    def listen_from_microphone(self, duration: float = 5.0) -> str:
        """
        마이크에서 음성 녹음 및 인식

        Args:
            duration: 녹음 시간 (초)

        Returns:
            str: 인식된 텍스트
        """
        print(f"🎤 {duration}초 동안 녹음 중...")
        audio_data = self.recorder.record_from_file(duration)
        text = self.recognizer.transcribe_bytes(audio_data)
        print(f"📝 인식 결과: {text}")
        return text
