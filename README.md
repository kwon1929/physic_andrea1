# Physical AI - 아트레이디스 (Atreides)

"아트레이디스"라고 부르면 깨어나는 지능형 로봇팔 시스템

## 프로젝트 개요

**"아트레이디스"**라고 부르면 깨어나는 지능형 로봇팔 시스템입니다.

- 🎤 **웨이크워드**: "아트레이디스" 또는 "Atreides"
- 🧠 **AI 두뇌**: 상황을 이해하고 스스로 판단
- 🔊 **음성 대화**: 듣고, 생각하고, 말하고, 행동
- 🤖 **로봇 정체성**: 듄(Dune)의 아트레이디스 가문 정신 계승
- 💻 **소프트웨어 우선**: 하드웨어 없이도 완전한 시뮬레이션

## 시스템 아키텍처

```
사용자 음성 입력
    ↓
[Perception] 음성 인식 (STT)
    ↓
[Brain] AI 에이전트 (LLM 기반 두뇌)
    ↓         ↓
[Motion]  [Perception] 비전 시스템
동작 계획      (상황 인식)
    ↓
[Simulation/Real] 로봇팔
```

## 프로젝트 구조

```
physic_andrea1/
├── src/
│   ├── brain/          # AI 에이전트 (LLM 기반 두뇌)
│   ├── perception/     # 음성 인식, TTS, 비전
│   ├── motion/         # 동작 계획 및 제어
│   ├── simulation/     # PyBullet 시뮬레이션
│   └── utils/          # 공통 유틸리티
├── config/             # 설정 파일
├── tests/              # 테스트 코드
├── .env                # 환경 변수 (생성 필요)
└── requirements.txt    # Python 의존성
```

## 시작하기

### 1. 가상환경 활성화

```bash
source venv/bin/activate
```

### 2. 환경 변수 설정

```bash
cp .env.example .env
# .env 파일을 열어서 API 키 입력
```

필요한 API 키:
- `ANTHROPIC_API_KEY`: Claude API 키 (https://console.anthropic.com)
- `OPENAI_API_KEY`: OpenAI API 키 (Whisper 사용 시)

### 3. 패키지 설치 확인

```bash
pip list | grep -E "(anthropic|openai|pydantic)"
```

## 개발 로드맵

- [x] Phase 1: 개발 환경 설정
- [x] Phase 2: AI Brain 모듈 구현 (GPT-4o)
- [x] Phase 3: 음성 인식 모듈 구현 (Whisper)
- [x] Phase 4: 시뮬레이션 환경 구축 (간단한 시뮬레이터)
- [x] Phase 5: 동작 실행 시스템 구현
- [x] Phase 6: 전체 시스템 통합 완료
- [ ] Phase 7: 하드웨어 선정 및 구매
- [ ] Phase 8: 실제 로봇 통합

## 기술 스택

**언어 & 프레임워크**
- Python 3.13+
- Pydantic (데이터 검증)

**AI/ML**
- Claude API (로봇 두뇌)
- OpenAI Whisper (음성 인식)
- OpenAI TTS (음성 출력, 선택사항)

**시뮬레이션** (추후 설치)
- PyBullet

**개발 도구**
- pytest (테스트)
- black (코드 포맷팅)

## 예상 사용 시나리오

```
사용자: "저기 빨간 블록 집어줘"
로봇: "네, 빨간 블록이 보이네요. 지금 집을게요."
[동작 실행]
로봇: "블록을 집었어요. 어디에 놓을까요?"
사용자: "파란 블록 옆에 놓아줘"
로봇: "알겠습니다. 파란 블록 옆에 놓을게요."
[동작 실행]
로봇: "완료했습니다!"
```

## 실행 방법

### 🌟 웨이크워드 로봇 - 자비스/아트레이디스 (NEW!)

**"자비스" 또는 "아트레이디스"라고 부르면 깨어납니다!**

```bash
source venv/bin/activate
python atreides.py
# 1. 이름 선택: 자비스 (추천, 인식 쉬움)
# 2. TTS 선택: macOS 내장 (무료)
# 3. "자비스" 또는 "아트레이디스"라고 말하세요!
```

**동작 방식:**
1. 항상 대기 중 (연속 듣기)
2. "아트레이디스" 감지 → 활성화!
3. "네, 듣고 있습니다" 응답
4. 명령 듣기 (5초)
5. 명령 처리 → 동작 실행
6. 다시 대기 모드

### 🎤 대화형 로봇

**마이크로 직접 말하면 로봇이 듣고 대답하고 움직입니다!**

```bash
source venv/bin/activate
python interactive_robot.py
# TTS 선택: 1 (OpenAI) 또는 2 (macOS 내장)
# 모드 선택: 1 (연속 대화) 또는 2 (데모 3회)
```

### 음성 입출력 테스트

```bash
python test_voice_io.py
# 마이크 녹음 → 음성 인식 → TTS 응답
```

### 전체 시스템 데모 (파일 기반)

```bash
python demo.py  # 자동 데모
python demo_screenshot.py  # 시각화 이미지 저장
python main.py  # 대화형 모드 (파일 입력)
```

### 개별 모듈 테스트

```bash
python test_brain_auto.py  # AI Brain 테스트
python test_speech.py  # 음성 인식 테스트
```

## 현재 구현된 기능

✅ **실시간 마이크 입력** - sounddevice로 직접 말하기
✅ **음성 인식** - OpenAI Whisper API로 한국어 음성 → 텍스트
✅ **AI 두뇌** - GPT-4o가 자연어 이해하고 동작 계획
✅ **음성 출력 (TTS)** - OpenAI TTS 또는 macOS 내장으로 로봇이 말하기
✅ **대화 맥락** - 이전 대화 기억하고 연속 대화
✅ **시뮬레이터** - 6DOF 로봇팔 가상 환경
✅ **동작 실행** - pick, place, move, home 등 기본 동작
✅ **시각화** - 2D 그래픽으로 로봇 상태 표시
✅ **안전성 검증** - 불가능한 동작 거부

## 다음 단계

1. 비전 시스템 (웹캠으로 실제 물체 인식)
2. 하드웨어 로봇팔 구매 및 통합 (myCobot, xArm 등)
3. 더 복잡한 동작 (조립, 정리, 순서 작업 등)
4. 멀티모달 (카메라 + 음성 동시 활용)

## 라이선스

MIT

---

**시작일**: 2026-02-06
# physic_andrea1
