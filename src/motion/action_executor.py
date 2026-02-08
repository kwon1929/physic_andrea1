"""
동작 실행 모듈
Brain이 생성한 명령을 로봇 시뮬레이터로 실행
"""

from typing import List
from src.brain.robot_brain import ActionCommand
from src.simulation.simple_robot_sim import SimpleRobotSimulator


class ActionExecutor:
    """
    동작 실행기
    Brain의 명령을 받아 시뮬레이터에서 실행
    """

    def __init__(self, simulator: SimpleRobotSimulator):
        """
        Args:
            simulator: 로봇 시뮬레이터
        """
        self.sim = simulator

    def execute_command(self, command: ActionCommand) -> bool:
        """
        단일 명령 실행

        Args:
            command: 실행할 명령

        Returns:
            성공 여부
        """
        action_type = command.action_type
        target_object = command.target_object
        location = command.location
        parameters = command.parameters or {}

        print(f"\n⚙️  실행: {action_type}", end="")
        if target_object:
            print(f" (대상: {target_object})", end="")
        print(f" - {command.reasoning}")

        try:
            if action_type == "pick":
                # 집기: 먼저 물체 위치로 이동 후 집기
                if not target_object:
                    print("  ⚠ 대상 물체가 지정되지 않았습니다")
                    return False

                # 물체 위치로 이동
                obj_pos = self.sim.get_object_position(target_object)
                if obj_pos:
                    # 1. 물체 바로 위로 접근
                    approach_pos = (obj_pos[0], obj_pos[1], obj_pos[2] + 0.1)
                    self.sim.move_to(approach_pos, target_object=None)

                    # 2. 물체 위치로 하강
                    self.sim.move_to(obj_pos, target_object=None)

                # 집기
                return self.sim.pick(target_object)

            elif action_type == "place":
                # 놓기
                if location:
                    target_pos = (
                        location.get("x", 0.0),
                        location.get("y", 0.0),
                        location.get("z", 0.05)
                    )
                else:
                    # 기본 위치
                    target_pos = (0.0, 0.0, 0.05)

                return self.sim.place(target_pos)

            elif action_type == "move":
                # 이동
                if location:
                    target_pos = (
                        location.get("x", 0.0),
                        location.get("y", 0.0),
                        location.get("z", 0.0)
                    )
                    return self.sim.move_to(target_pos, target_object=None)
                elif target_object:
                    obj_pos = self.sim.get_object_position(target_object)
                    if obj_pos:
                        return self.sim.move_to(obj_pos, target_object=target_object)
                    else:
                        print(f"  ⚠ {target_object}을(를) 찾을 수 없습니다")
                        return False
                else:
                    print("  ⚠ 목표 위치가 지정되지 않았습니다")
                    return False

            elif action_type == "rotate":
                # 회전 (간단히 로그만)
                angle = parameters.get("angle", 0)
                self.sim.log(f"회전: {angle}도")
                return True

            elif action_type == "open_gripper":
                # 그리퍼 열기
                return self.sim.open_gripper()

            elif action_type == "close_gripper":
                # 그리퍼 닫기
                return self.sim.close_gripper()

            elif action_type == "home":
                # 초기 위치
                return self.sim.home()

            elif action_type == "wait":
                # 대기
                duration = parameters.get("duration", 1.0)
                self.sim.log(f"{duration}초 대기")
                import time
                time.sleep(duration)
                return True

            else:
                print(f"  ⚠ 알 수 없는 동작: {action_type}")
                return False

        except Exception as e:
            print(f"  ✗ 실행 실패: {e}")
            return False

    def execute_commands(self, commands: List[ActionCommand]) -> bool:
        """
        여러 명령을 순차적으로 실행

        Args:
            commands: 실행할 명령 리스트

        Returns:
            모든 명령 성공 여부
        """
        if not commands:
            print("\n⚙️  실행할 동작이 없습니다")
            return True

        print(f"\n⚙️  {len(commands)}개 동작 실행 시작")
        print("=" * 60)

        success_count = 0
        for i, command in enumerate(commands, 1):
            print(f"\n[동작 {i}/{len(commands)}]")

            if self.execute_command(command):
                success_count += 1
            else:
                print(f"  ✗ 동작 {i} 실패")
                # 실패해도 계속 진행 (사용자가 선택하도록 수정 가능)

        print("\n" + "=" * 60)
        print(f"실행 완료: {success_count}/{len(commands)} 성공")

        return success_count == len(commands)
