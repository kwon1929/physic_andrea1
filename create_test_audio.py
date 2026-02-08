"""
테스트용 음성 파일 생성
macOS의 'say' 명령을 사용하여 한국어 음성 생성
"""

import subprocess
import os


def create_test_audio():
    """테스트용 음성 파일 생성"""

    test_commands = [
        ("빨간 블록을 집어줘", "test_audio/command1"),
        ("초기 위치로 돌아가", "test_audio/command2"),
        ("그리퍼를 열어줘", "test_audio/command3"),
    ]

    print("=" * 60)
    print("테스트용 음성 파일 생성 중...")
    print("=" * 60)

    os.makedirs("test_audio", exist_ok=True)

    for text, output_base in test_commands:
        aiff_file = f"{output_base}.aiff"
        wav_file = f"{output_base}.wav"

        print(f"\n생성 중: {text}")
        print(f"  1. AIFF 생성: {aiff_file}")

        try:
            # macOS의 say 명령으로 음성 생성 (AIFF)
            subprocess.run(
                ["say", "-v", "Yuna", "-o", aiff_file, text],
                check=True,
                capture_output=True
            )
            print(f"  ✓ AIFF 생성 완료")

            # AIFF를 WAV로 변환
            print(f"  2. WAV 변환: {wav_file}")
            subprocess.run(
                ["afconvert", "-f", "WAVE", "-d", "LEI16@16000", aiff_file, wav_file],
                check=True,
                capture_output=True
            )
            print(f"  ✓ WAV 변환 완료")

        except subprocess.CalledProcessError as e:
            print(f"✗ 생성 실패: {e}")
            print("macOS의 say 또는 afconvert 명령을 사용할 수 없습니다.")
            return False
        except FileNotFoundError:
            print("✗ 명령을 찾을 수 없습니다.")
            return False

    print("\n" + "=" * 60)
    print("✓ 모든 테스트 음성 파일 생성 완료!")
    print("=" * 60)
    print("\n생성된 WAV 파일:")
    for _, output_base in test_commands:
        print(f"  - {output_base}.wav")

    return True


if __name__ == "__main__":
    create_test_audio()
