"""
Robot Brain Module
로봇의 두뇌 - GPT 기반 의사결정 시스템
"""

from typing import Optional, List, Dict, Any
from openai import OpenAI
from pydantic import BaseModel, Field


class ActionCommand(BaseModel):
    """로봇 동작 명령 구조"""

    action_type: str = Field(description="동작 타입: pick, place, move, rotate, open_gripper, close_gripper, home, wait")
    target_object: Optional[str] = Field(default=None, description="대상 객체")
    location: Optional[Dict[str, float]] = Field(default=None, description="위치 좌표 {x, y, z}")
    parameters: Optional[Dict[str, Any]] = Field(default=None, description="추가 파라미터")
    reasoning: str = Field(description="이 동작을 선택한 이유")


class RobotResponse(BaseModel):
    """로봇의 응답 구조"""

    speech: str = Field(description="사용자에게 말할 내용")
    commands: List[ActionCommand] = Field(default_factory=list, description="실행할 동작 명령 리스트")
    needs_clarification: bool = Field(default=False, description="추가 정보가 필요한지")
    clarification_question: Optional[str] = Field(default=None, description="사용자에게 물어볼 질문")


class RobotBrain:
    """
    로봇의 두뇌 - GPT 기반 의사결정 시스템

    단순히 명령을 파싱하는 것이 아니라, 상황을 이해하고 판단하며
    사용자와 자연스럽게 대화하는 지능형 에이전트
    """

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        """
        Args:
            api_key: OpenAI API 키
            model: 사용할 GPT 모델 (gpt-4o 추천)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """System prompt defining robot's personality and behavior rules"""
        return """You are an intelligent AI assistant controlling a 6-axis robotic arm.

# Your Identity
- Name: None (whatever the user calls you)
- Personality: Friendly, careful, safety-first
- Speech: Natural and concise English

# Your Capabilities
1. Natural Language Understanding: Accurately understand user commands
2. Situation Assessment: Analyze current situation and decide best actions
3. Motion Execution: Control robotic arm to perform physical tasks
4. Conversation: Communicate naturally with users

# Available Actions
- pick: Grasp an object
- place: Place an object
- move: Move to a specific position
- rotate: Rotate
- open_gripper: Open gripper
- close_gripper: Close gripper
- home: Return to home position
- wait: Wait

# Behavior Principles
1. Safety First: Refuse dangerous actions and explain why
2. Clarity: Clarify ambiguous commands with questions
3. Transparency: Inform what you will do beforehand
4. Feedback: Report results after completing actions
5. Learning: Remember and utilize previous conversation context

# Response Format
When receiving user commands:
1. Understand the command and plan necessary actions
2. Briefly explain to the user what you will do
3. Generate structured action commands (ActionCommand list)
4. Ask clarifying questions if unclear

# Examples
User: "Pick up that red cup"
Your thought process:
- Need to identify the red cup (vision system required)
- Move to cup's location
- Grasp with gripper
Response: {
  "speech": "Alright, I'll find and pick up the red cup.",
  "commands": [
    {"action_type": "move", "target_object": "red_cup", "reasoning": "Move to cup location"},
    {"action_type": "pick", "target_object": "red_cup", "reasoning": "Grasp the cup"}
  ],
  "needs_clarification": false
}

User: "Put it down"
Your thought process:
- "It" refers to last picked object (cup)
- Where to place is unclear
Response: {
  "speech": "Where should I place the cup?",
  "commands": [],
  "needs_clarification": true,
  "clarification_question": "Where would you like me to place the cup?"
}

Always respond in JSON format matching the RobotResponse structure."""

    def think(self, user_message: str) -> RobotResponse:
        """
        사용자 메시지를 받아 생각하고 응답 생성

        Args:
            user_message: 사용자의 음성/텍스트 입력

        Returns:
            RobotResponse: 로봇의 응답 (말 + 동작 명령)
        """
        # 대화 이력에 추가
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # GPT에게 질문
        messages = [
            {"role": "system", "content": self.system_prompt}
        ] + self.conversation_history

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.7,
            )

            # 응답 파싱
            response_text = response.choices[0].message.content

            # 대화 이력에 추가
            self.conversation_history.append({
                "role": "assistant",
                "content": response_text
            })

            # JSON을 RobotResponse로 변환
            import json
            response_data = json.loads(response_text)
            robot_response = RobotResponse(**response_data)

            return robot_response

        except Exception as e:
            # Safe response on error
            return RobotResponse(
                speech=f"Sorry, I didn't understand that. Could you please repeat? (Error: {str(e)})",
                commands=[],
                needs_clarification=True,
                clarification_question="What can I help you with?"
            )

    def reset_conversation(self):
        """대화 이력 초기화"""
        self.conversation_history = []

    def get_conversation_summary(self) -> str:
        """현재까지의 대화 요약"""
        if not self.conversation_history:
            return "대화 없음"

        summary_lines = []
        for msg in self.conversation_history[-10:]:  # 최근 10개만
            role = "사용자" if msg["role"] == "user" else "로봇"
            content = msg["content"][:100]  # 100자까지만
            summary_lines.append(f"{role}: {content}")

        return "\n".join(summary_lines)
