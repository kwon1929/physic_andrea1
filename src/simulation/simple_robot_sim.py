"""
간단한 로봇 시뮬레이터
PyBullet 없이 로봇 동작을 시뮬레이션하고 시각화
"""

import time
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
import math


@dataclass
class JointState:
    """관절 상태"""
    position: float = 0.0  # 라디안
    velocity: float = 0.0
    name: str = ""


@dataclass
class RobotState:
    """로봇 전체 상태"""
    joint_positions: List[float] = field(default_factory=lambda: [0.0] * 6)
    gripper_open: bool = True
    end_effector_pos: Tuple[float, float, float] = (0.0, 0.0, 0.3)
    holding_object: Optional[str] = None


@dataclass
class WorldObject:
    """환경 내 물체"""
    name: str
    position: Tuple[float, float, float]
    color: str
    size: Tuple[float, float, float] = (0.05, 0.05, 0.05)


class SimpleRobotSimulator:
    """
    간단한 6DOF 로봇팔 시뮬레이터
    물리 엔진 없이 기본적인 동작만 시뮬레이션
    """

    def __init__(self):
        """초기화"""
        self.robot = RobotState()
        self.objects: Dict[str, WorldObject] = {}
        self.action_log: List[str] = []

        # 초기 물체 배치
        self._setup_world()

    def _setup_world(self):
        """초기 환경 설정"""
        self.objects = {
            "red_block": WorldObject(
                name="red_block",
                position=(0.3, 0.2, 0.05),
                color="red"
            ),
            "blue_cup": WorldObject(
                name="blue_cup",
                position=(0.2, -0.2, 0.05),
                color="blue",
                size=(0.06, 0.06, 0.1)
            ),
            "green_block": WorldObject(
                name="green_block",
                position=(-0.2, 0.1, 0.05),
                color="green"
            ),
        }
        self.log("환경 초기화 완료")

    def log(self, message: str):
        """로그 기록"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.action_log.append(log_entry)
        print(f"  🤖 {log_entry}")

    def get_object_position(self, object_name: str) -> Optional[Tuple[float, float, float]]:
        """물체 위치 가져오기"""
        obj = self.objects.get(object_name)
        if obj:
            return obj.position
        return None

    def move_to(self, target_pos: Tuple[float, float, float], target_object: Optional[str] = None):
        """
        로봇을 특정 위치로 이동

        Args:
            target_pos: 목표 위치 (x, y, z)
            target_object: 목표 물체 이름
        """
        if target_object:
            obj_pos = self.get_object_position(target_object)
            if obj_pos:
                target_pos = obj_pos
                self.log(f"{target_object} 위치({obj_pos[0]:.2f}, {obj_pos[1]:.2f}, {obj_pos[2]:.2f})로 이동 시작")
            else:
                self.log(f"⚠ {target_object}을(를) 찾을 수 없습니다")
                return False
        else:
            self.log(f"위치 ({target_pos[0]:.2f}, {target_pos[1]:.2f}, {target_pos[2]:.2f})로 이동 시작")

        # 거리 계산
        current = self.robot.end_effector_pos
        distance = math.sqrt(
            (target_pos[0] - current[0])**2 +
            (target_pos[1] - current[1])**2 +
            (target_pos[2] - current[2])**2
        )

        # 이동 시뮬레이션 (간단히 딜레이)
        move_time = distance * 2  # 거리에 비례한 시간
        time.sleep(min(move_time, 2.0))  # 최대 2초

        # 위치 업데이트
        self.robot.end_effector_pos = target_pos
        self.log(f"✓ 이동 완료")
        return True

    def pick(self, object_name: str):
        """
        물체 집기

        Args:
            object_name: 집을 물체 이름
        """
        obj = self.objects.get(object_name)
        if not obj:
            self.log(f"⚠ {object_name}을(를) 찾을 수 없습니다")
            return False

        # 물체 위치 확인
        obj_pos = obj.position
        current_pos = self.robot.end_effector_pos
        distance = math.sqrt(
            (obj_pos[0] - current_pos[0])**2 +
            (obj_pos[1] - current_pos[1])**2 +
            (obj_pos[2] - current_pos[2])**2
        )

        if distance > 0.1:
            self.log(f"⚠ {object_name}이(가) 너무 멉니다 (거리: {distance:.2f}m). 먼저 이동하세요")
            return False

        if not self.robot.gripper_open:
            self.log(f"⚠ 그리퍼가 이미 닫혀있습니다. 먼저 열어주세요")
            return False

        self.log(f"{object_name} 집기 시작")
        time.sleep(0.5)

        # 그리퍼 닫기
        self.robot.gripper_open = False
        self.robot.holding_object = object_name

        self.log(f"✓ {object_name}을(를) 집었습니다")
        return True

    def place(self, target_pos: Tuple[float, float, float]):
        """
        물체 놓기

        Args:
            target_pos: 놓을 위치
        """
        if not self.robot.holding_object:
            self.log("⚠ 들고 있는 물체가 없습니다")
            return False

        obj_name = self.robot.holding_object
        self.log(f"{obj_name}을(를) 놓기 시작")
        time.sleep(0.5)

        # 물체 위치 업데이트
        if obj_name in self.objects:
            self.objects[obj_name].position = target_pos

        # 그리퍼 열기
        self.robot.gripper_open = True
        self.robot.holding_object = None

        self.log(f"✓ {obj_name}을(를) ({target_pos[0]:.2f}, {target_pos[1]:.2f}, {target_pos[2]:.2f})에 놓았습니다")
        return True

    def open_gripper(self):
        """그리퍼 열기"""
        if self.robot.gripper_open:
            self.log("⚠ 그리퍼가 이미 열려있습니다")
            return True

        self.log("그리퍼 열기")
        time.sleep(0.3)
        self.robot.gripper_open = True
        self.log("✓ 그리퍼 열림")
        return True

    def close_gripper(self):
        """그리퍼 닫기"""
        if not self.robot.gripper_open:
            self.log("⚠ 그리퍼가 이미 닫혀있습니다")
            return True

        self.log("그리퍼 닫기")
        time.sleep(0.3)
        self.robot.gripper_open = False
        self.log("✓ 그리퍼 닫힘")
        return True

    def home(self):
        """초기 위치로 복귀"""
        self.log("초기 위치로 복귀 시작")
        time.sleep(1.0)

        self.robot.joint_positions = [0.0] * 6
        self.robot.end_effector_pos = (0.0, 0.0, 0.3)
        if self.robot.holding_object:
            self.robot.gripper_open = True
            self.robot.holding_object = None

        self.log("✓ 초기 위치 복귀 완료")
        return True

    def get_state_summary(self) -> str:
        """현재 상태 요약"""
        lines = []
        lines.append("\n" + "=" * 60)
        lines.append("로봇 상태")
        lines.append("=" * 60)
        lines.append(f"위치: ({self.robot.end_effector_pos[0]:.2f}, "
                    f"{self.robot.end_effector_pos[1]:.2f}, "
                    f"{self.robot.end_effector_pos[2]:.2f})")
        lines.append(f"그리퍼: {'열림' if self.robot.gripper_open else '닫힘'}")
        lines.append(f"들고 있는 물체: {self.robot.holding_object or '없음'}")

        lines.append("\n환경 내 물체:")
        for name, obj in self.objects.items():
            lines.append(f"  - {name} ({obj.color}): "
                        f"({obj.position[0]:.2f}, {obj.position[1]:.2f}, {obj.position[2]:.2f})")

        return "\n".join(lines)

    def get_action_log(self) -> str:
        """행동 로그 가져오기"""
        if not self.action_log:
            return "로그 없음"
        return "\n".join(self.action_log[-10:])  # 최근 10개
