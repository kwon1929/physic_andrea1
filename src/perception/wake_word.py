"""
웨이크워드 감지 모듈
"아트레이디스" / "Atreides" 감지
"""

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import tempfile
import time


class WakeWordDetector:
    """
    웨이크워드 감지기
    연속으로 듣다가 특정 단어 감지
    """

    def __init__(self, recognizer, wake_words=None):
        """
        Args:
            recognizer: SpeechRecognizer 인스턴스
            wake_words: 감지할 단어 리스트
        """
        self.recognizer = recognizer
        self.wake_words = wake_words or [
            # 기본 이름들
            "자비스",
            "jarvis",
            "제비스",
            # 아트레이디스 변형들
            "아트레이디스",
            "atreides",
            "아트레이데스",
            "아트레",
            "아이언맨",
        ]
        self.sample_rate = 16000
        self.is_listening = False

    def listen_for_wake_word(self, chunk_duration=3.0, timeout=60.0):
        """
        웨이크워드를 계속 듣기

        Args:
            chunk_duration: 한 번에 녹음할 시간 (초)
            timeout: 최대 대기 시간 (초)

        Returns:
            bool: 웨이크워드 감지 여부
        """
        print("\n👂 웨이크워드 대기 중...")
        print(f"   '{self.wake_words[0]}'라고 말하세요")
        print("   (Ctrl+C로 종료)\n")

        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                # 짧은 오디오 녹음
                audio_data = sd.rec(
                    int(chunk_duration * self.sample_rate),
                    samplerate=self.sample_rate,
                    channels=1,
                    dtype='int16'
                )
                sd.wait()

                # 볼륨 체크 (너무 조용하면 스킵)
                volume = np.abs(audio_data).mean()
                if volume < 300:  # 조용함
                    print(".", end="", flush=True)
                    continue

                print("\n🎤 소리 감지, 인식 중...", end="", flush=True)

                # 임시 파일로 저장
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                write(temp_file.name, self.sample_rate, audio_data)

                # 음성 인식
                try:
                    text = self.recognizer.transcribe_file(temp_file.name, language="en")
                    text_lower = text.lower().strip()

                    print(f" → '{text}'")

                    # 웨이크워드 확인 (유연한 매칭)
                    if self._check_wake_word(text_lower):
                        return True

                    print("   (웨이크워드 아님, 계속 대기...)")

                except Exception as e:
                    print(f" → 인식 실패: {e}")

            except KeyboardInterrupt:
                print("\n\n중단됨")
                return False

        print("\n⏱️  타임아웃")
        return False

    def _check_wake_word(self, text):
        """
        웨이크워드 유연한 매칭

        Args:
            text: 인식된 텍스트 (소문자)

        Returns:
            bool: 웨이크워드 포함 여부
        """
        # 정확한 매칭
        for wake_word in self.wake_words:
            if wake_word.lower() in text:
                print(f"\n✅ 웨이크워드 감지: '{wake_word}' (정확)")
                return True

        # 부분 매칭 (유사도)
        for wake_word in self.wake_words:
            wake_lower = wake_word.lower()

            # 길이가 3자 이상인 경우만 부분 매칭
            if len(wake_lower) >= 3:
                # 웨이크워드의 앞 3자가 포함되어 있으면 인정
                if wake_lower[:3] in text:
                    print(f"\n✅ 웨이크워드 감지: '{wake_word}' (부분 매칭)")
                    return True

                # 띄어쓰기 무시 매칭
                text_no_space = text.replace(" ", "")
                if wake_lower in text_no_space:
                    print(f"\n✅ 웨이크워드 감지: '{wake_word}' (띄어쓰기 무시)")
                    return True

        return False

    def continuous_listen(self, on_wake_word_detected):
        """
        연속으로 웨이크워드 감지하고 콜백 실행

        Args:
            on_wake_word_detected: 웨이크워드 감지 시 실행할 함수
        """
        print("=" * 60)
        print("🤖 아트레이디스 - 대기 모드")
        print("=" * 60)
        print(f"\n웨이크워드: {', '.join(self.wake_words)}")
        print("언제든지 불러주세요!\n")

        try:
            while True:
                # 웨이크워드 대기
                if self.listen_for_wake_word(chunk_duration=3.0):
                    # 웨이크워드 감지됨!
                    print("\n🔊 네, 무엇을 도와드릴까요?")

                    # 콜백 실행
                    try:
                        on_wake_word_detected()
                    except Exception as e:
                        print(f"\n✗ 오류: {e}")

                    print("\n다시 대기 모드로 돌아갑니다...")
                    time.sleep(1)

        except KeyboardInterrupt:
            print("\n\n종료합니다.")


class SmartWakeWordDetector:
    """
    향상된 웨이크워드 감지
    침묵 감지 + 볼륨 기반 활성화
    """

    def __init__(self, recognizer, wake_words=None):
        """
        Args:
            recognizer: SpeechRecognizer 인스턴스
            wake_words: 감지할 단어 리스트
        """
        self.recognizer = recognizer
        self.wake_words = wake_words or [
            "자비스", "jarvis", "제비스",
            "아트레이디스", "atreides", "아트레이데스", "아트레",
            "아이언맨",
        ]
        self.sample_rate = 16000
        self.recording_buffer = []

    def listen_smart(self, max_silence=2.0, min_volume=400):
        """
        스마트 녹음: 소리가 시작되면 녹음, 침묵이 지속되면 분석

        Args:
            max_silence: 침묵 지속 시간 (초)
            min_volume: 최소 볼륨 임계값

        Returns:
            tuple: (detected, text) - 웨이크워드 감지 여부와 인식된 텍스트
        """
        print("\n👂 대기 중... (말씀하세요)", end="", flush=True)

        self.recording_buffer = []
        silence_chunks = 0
        max_silence_chunks = int(max_silence * 10)  # 0.1초 단위
        is_recording = False

        def callback(indata, frames, time_info, status):
            nonlocal silence_chunks, is_recording

            volume = np.abs(indata).mean()

            if volume > min_volume:
                # 소리 감지
                if not is_recording:
                    print("\n🎤 녹음 중...", end="", flush=True)
                    is_recording = True
                self.recording_buffer.append(indata.copy())
                silence_chunks = 0
            else:
                # 침묵
                if is_recording:
                    self.recording_buffer.append(indata.copy())
                    silence_chunks += 1

        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                callback=callback,
                dtype='int16',
                blocksize=1600  # 0.1초
            ):
                while True:
                    time.sleep(0.1)

                    # 침묵이 지속되고 녹음된 데이터가 있으면 분석
                    if is_recording and silence_chunks > max_silence_chunks:
                        break

        except KeyboardInterrupt:
            return False, ""

        if not self.recording_buffer:
            return False, ""

        print(" 처리 중...", end="", flush=True)

        # 오디오 데이터 결합
        audio_data = np.concatenate(self.recording_buffer, axis=0)

        # 임시 파일로 저장
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        write(temp_file.name, self.sample_rate, audio_data)

        # 음성 인식
        try:
            text = self.recognizer.transcribe_file(temp_file.name, language="en")
            text_lower = text.lower().strip()

            print(f" → '{text}'")

            # 웨이크워드 확인 (유연한 매칭)
            if self._check_wake_word_flexible(text_lower):
                return True, text

            return False, text

        except Exception as e:
            print(f" → 인식 실패: {e}")
            return False, ""

    def _check_wake_word_flexible(self, text):
        """
        웨이크워드 유연한 매칭

        Args:
            text: 인식된 텍스트 (소문자)

        Returns:
            bool: 웨이크워드 포함 여부
        """
        # 정확한 매칭
        for wake_word in self.wake_words:
            if wake_word.lower() in text:
                print(f" ✅ '{wake_word}'")
                return True

        # 부분 매칭
        for wake_word in self.wake_words:
            wake_lower = wake_word.lower()

            if len(wake_lower) >= 3:
                # 앞 3자 포함
                if wake_lower[:3] in text:
                    print(f" ✅ '{wake_word}' (부분)")
                    return True

                # 띄어쓰기 무시
                text_no_space = text.replace(" ", "")
                if wake_lower in text_no_space:
                    print(f" ✅ '{wake_word}' (띄어쓰기 무시)")
                    return True

        # 특수 케이스: "비스" 또는 "트레" 같은 부분만 인식
        if any(ending in text for ending in ["비스", "vis", "트레", "tre", "맨", "man", "자비", "jarv"]):
            print(f" ✅ '웨이크워드' (일부 매칭)")
            return True

        return False
