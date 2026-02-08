"""
실시간 마이크 입력 모듈
sounddevice를 사용한 실시간 음성 녹음
"""

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import tempfile
import time


class MicrophoneRecorder:
    """
    실시간 마이크 녹음 클래스
    """

    def __init__(self, sample_rate=16000, channels=1):
        """
        Args:
            sample_rate: 샘플링 레이트 (Hz)
            channels: 채널 수 (1: 모노, 2: 스테레오)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = []

    def list_devices(self):
        """사용 가능한 오디오 장치 목록"""
        print("=" * 60)
        print("사용 가능한 오디오 장치:")
        print("=" * 60)
        print(sd.query_devices())
        print("=" * 60)

    def record(self, duration=5.0) -> str:
        """
        음성 녹음 및 WAV 파일로 저장

        Args:
            duration: 녹음 시간 (초)

        Returns:
            str: 임시 WAV 파일 경로
        """
        print(f"\n🎤 Recording for {duration} seconds...")
        print("(Speak now!)")

        # Record
        audio_data = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype='int16'
        )

        # Progress indicator
        for i in range(int(duration)):
            time.sleep(1)
            print(f"  {i+1}s...", end="\r")

        sd.wait()  # Wait for recording to complete
        print(f"\n✓ Recording complete!")

        # 임시 파일로 저장
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        write(temp_file.name, self.sample_rate, audio_data)

        return temp_file.name

    def record_until_silence(self, max_duration=10.0, silence_threshold=500, silence_duration=1.5):
        """
        소리가 멈출 때까지 녹음 (고급 기능)

        Args:
            max_duration: 최대 녹음 시간 (초)
            silence_threshold: 침묵 판단 임계값
            silence_duration: 침묵 지속 시간 (초)

        Returns:
            str: 임시 WAV 파일 경로
        """
        print(f"\n🎤 녹음 시작 (침묵 감지 모드)")
        print("(말씀하세요. 말이 끝나면 자동으로 멈춥니다)")

        recording = []
        silence_frames = 0
        silence_threshold_frames = int(silence_duration * self.sample_rate / 1024)

        def callback(indata, frames, time_info, status):
            nonlocal silence_frames
            recording.append(indata.copy())

            # 볼륨 레벨 확인
            volume = np.abs(indata).mean()

            if volume < silence_threshold:
                silence_frames += 1
            else:
                silence_frames = 0

        # 스트리밍 녹음
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=callback,
            dtype='int16',
            blocksize=1024
        ):
            start_time = time.time()
            while time.time() - start_time < max_duration:
                time.sleep(0.1)

                # 침묵이 지속되면 종료
                if silence_frames > silence_threshold_frames and len(recording) > 10:
                    print("\n✓ 침묵 감지, 녹음 종료")
                    break

        print(f"✓ 녹음 완료! ({len(recording)} 프레임)")

        # 오디오 데이터 결합
        if recording:
            audio_data = np.concatenate(recording, axis=0)

            # 임시 파일로 저장
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            write(temp_file.name, self.sample_rate, audio_data)

            return temp_file.name
        else:
            raise Exception("녹음된 데이터가 없습니다")


class VoiceActivityDetector:
    """
    음성 활동 감지 (VAD)
    간단한 볼륨 기반 감지
    """

    def __init__(self, sample_rate=16000, threshold=500):
        """
        Args:
            sample_rate: 샘플링 레이트
            threshold: 음성 감지 임계값
        """
        self.sample_rate = sample_rate
        self.threshold = threshold

    def is_speech(self, audio_data):
        """
        오디오 데이터에 음성이 포함되어 있는지 확인

        Args:
            audio_data: numpy array

        Returns:
            bool: 음성 포함 여부
        """
        volume = np.abs(audio_data).mean()
        return volume > self.threshold
