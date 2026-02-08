"""
설정 관리 모듈
환경 변수와 시스템 설정을 관리합니다.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """애플리케이션 설정"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # AI API Keys
    anthropic_api_key: str = Field(default="", description="Anthropic API 키")
    openai_api_key: str = Field(default="", description="OpenAI API 키")

    # Robot Configuration
    robot_type: str = Field(default="simulation", description="로봇 타입")
    robot_model: str = Field(default="6dof_arm", description="로봇 모델")

    # System Settings
    log_level: str = Field(default="INFO", description="로그 레벨")
    enable_tts: bool = Field(default=False, description="TTS 활성화")
    enable_vision: bool = Field(default=False, description="비전 활성화")

    # Safety Settings
    max_velocity: float = Field(default=1.0, description="최대 속도 (m/s)")
    workspace_limit_x: float = Field(default=0.5, description="작업 영역 X축 제한")
    workspace_limit_y: float = Field(default=0.5, description="작업 영역 Y축 제한")
    workspace_limit_z: float = Field(default=0.5, description="작업 영역 Z축 제한")


# 전역 설정 인스턴스
settings = Settings()
