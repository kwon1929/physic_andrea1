"""
설정 테스트 스크립트
개발 환경이 제대로 설정되었는지 확인합니다.
"""

import sys


def test_imports():
    """필수 패키지 import 테스트"""
    print("패키지 import 테스트 중...")

    try:
        import anthropic

        print("✓ anthropic 패키지 정상")
    except ImportError as e:
        print(f"✗ anthropic 패키지 오류: {e}")
        return False

    try:
        import openai

        print("✓ openai 패키지 정상")
    except ImportError as e:
        print(f"✗ openai 패키지 오류: {e}")
        return False

    try:
        import numpy

        print("✓ numpy 패키지 정상")
    except ImportError as e:
        print(f"✗ numpy 패키지 오류: {e}")
        return False

    try:
        from pydantic import BaseModel

        print("✓ pydantic 패키지 정상")
    except ImportError as e:
        print(f"✗ pydantic 패키지 오류: {e}")
        return False

    return True


def test_settings():
    """설정 파일 테스트"""
    print("\n설정 파일 테스트 중...")

    try:
        from config.settings import settings

        print("✓ 설정 파일 로드 정상")
        print(f"  - 로봇 타입: {settings.robot_type}")
        print(f"  - 로봇 모델: {settings.robot_model}")
        print(f"  - 로그 레벨: {settings.log_level}")

        # API 키 확인 (값은 출력하지 않음)
        if settings.anthropic_api_key:
            print("✓ ANTHROPIC_API_KEY 설정됨")
        else:
            print("⚠ ANTHROPIC_API_KEY 미설정 (.env 파일 확인 필요)")

        if settings.openai_api_key:
            print("✓ OPENAI_API_KEY 설정됨")
        else:
            print("⚠ OPENAI_API_KEY 미설정 (.env 파일 확인 필요)")

        return True
    except Exception as e:
        print(f"✗ 설정 파일 오류: {e}")
        return False


def test_project_structure():
    """프로젝트 구조 테스트"""
    print("\n프로젝트 구조 테스트 중...")
    import os

    required_dirs = [
        "src/brain",
        "src/perception",
        "src/motion",
        "src/simulation",
        "src/utils",
        "config",
        "tests",
    ]

    all_exist = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✓ {dir_path} 존재")
        else:
            print(f"✗ {dir_path} 없음")
            all_exist = False

    return all_exist


def main():
    """메인 테스트 함수"""
    print("=" * 50)
    print("Physical AI - 개발 환경 설정 테스트")
    print("=" * 50)

    results = []

    results.append(("패키지 import", test_imports()))
    results.append(("프로젝트 구조", test_project_structure()))
    results.append(("설정 파일", test_settings()))

    print("\n" + "=" * 50)
    print("테스트 결과 요약")
    print("=" * 50)

    all_passed = True
    for name, passed in results:
        status = "✓ 통과" if passed else "✗ 실패"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n모든 테스트 통과! 개발 환경이 정상적으로 설정되었습니다.")
        print("\n다음 단계:")
        print("1. .env 파일에 API 키 입력")
        print("2. AI Brain 모듈 개발 시작")
        return 0
    else:
        print("\n일부 테스트 실패. 위의 오류를 확인해주세요.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
