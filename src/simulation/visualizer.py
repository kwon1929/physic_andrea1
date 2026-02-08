"""
로봇 시뮬레이터 시각화
matplotlib를 사용하여 로봇과 환경을 2D로 시각화
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import Optional
import time


class RobotVisualizer:
    """
    로봇 상태를 시각화하는 클래스
    2D top-down view로 로봇과 물체들을 표시
    """

    def __init__(self, interactive=True):
        """
        Args:
            interactive: 대화형 모드 (실시간 업데이트)
        """
        self.interactive = interactive

        if interactive:
            plt.ion()  # 대화형 모드

        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.setup_plot()

    def setup_plot(self):
        """플롯 초기 설정"""
        self.ax.set_xlim(-0.6, 0.6)
        self.ax.set_ylim(-0.6, 0.6)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel('X (m)', fontsize=12)
        self.ax.set_ylabel('Y (m)', fontsize=12)
        self.ax.set_title('Physical AI - 로봇 시뮬레이터 (Top View)', fontsize=14, fontweight='bold')

        # 작업 영역 표시
        workspace = patches.Circle((0, 0), 0.5, fill=False, edgecolor='gray',
                                   linestyle='--', linewidth=2, alpha=0.5)
        self.ax.add_patch(workspace)

        # 원점 표시
        self.ax.plot(0, 0, 'k+', markersize=15, markeredgewidth=2, label='원점')

    def draw_robot(self, robot_state):
        """
        로봇 상태 그리기

        Args:
            robot_state: RobotState 객체
        """
        self.ax.clear()
        self.setup_plot()

        # End effector 위치
        x, y, z = robot_state.end_effector_pos

        # 로봇팔 (간단히 선으로 표현)
        self.ax.plot([0, x], [0, y], 'b-', linewidth=3, label='로봇팔')

        # End effector
        gripper_color = 'red' if not robot_state.gripper_open else 'green'
        gripper_label = '그리퍼 (닫힘)' if not robot_state.gripper_open else '그리퍼 (열림)'

        self.ax.plot(x, y, 'o', color=gripper_color, markersize=20,
                    markeredgecolor='black', markeredgewidth=2, label=gripper_label)

        # 높이 표시 (텍스트)
        self.ax.text(x, y + 0.08, f'z={z:.2f}m', ha='center', fontsize=10,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        # 들고 있는 물체 표시
        if robot_state.holding_object:
            self.ax.text(x, y - 0.08, f'들고있음: {robot_state.holding_object}',
                        ha='center', fontsize=9, color='red', fontweight='bold')

    def draw_objects(self, objects):
        """
        환경 내 물체들 그리기

        Args:
            objects: dict of WorldObject
        """
        color_map = {
            'red': 'red',
            'blue': 'blue',
            'green': 'green',
            'yellow': 'yellow',
        }

        for name, obj in objects.items():
            x, y, z = obj.position
            color = color_map.get(obj.color, 'gray')

            # 물체 그리기 (사각형)
            size = obj.size[0]  # x 크기 사용
            rect = patches.Rectangle(
                (x - size/2, y - size/2), size, size,
                linewidth=2, edgecolor='black', facecolor=color, alpha=0.7
            )
            self.ax.add_patch(rect)

            # 물체 이름 표시
            self.ax.text(x, y, name.replace('_', '\n'), ha='center', va='center',
                        fontsize=8, fontweight='bold', color='white',
                        bbox=dict(boxstyle='round', facecolor='black', alpha=0.5))

    def draw_state(self, simulator, title=None):
        """
        시뮬레이터 전체 상태 그리기

        Args:
            simulator: SimpleRobotSimulator 객체
            title: 추가 제목
        """
        self.draw_robot(simulator.robot)
        self.draw_objects(simulator.objects)

        # 범례
        self.ax.legend(loc='upper right', fontsize=10)

        # 상태 정보 텍스트
        status_text = f"위치: ({simulator.robot.end_effector_pos[0]:.2f}, {simulator.robot.end_effector_pos[1]:.2f}, {simulator.robot.end_effector_pos[2]:.2f})"
        status_text += f"\n그리퍼: {'닫힘' if not simulator.robot.gripper_open else '열림'}"
        if simulator.robot.holding_object:
            status_text += f"\n들고 있음: {simulator.robot.holding_object}"

        self.ax.text(0.02, 0.98, status_text, transform=self.ax.transAxes,
                    fontsize=10, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

        # 제목 추가
        if title:
            self.ax.set_title(f'Physical AI - {title}', fontsize=14, fontweight='bold')

        if self.interactive:
            plt.draw()
            plt.pause(0.1)

    def save(self, filename):
        """이미지로 저장"""
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"✓ 시각화 저장: {filename}")

    def show(self):
        """창 표시 (non-interactive 모드)"""
        if not self.interactive:
            plt.show()

    def close(self):
        """창 닫기"""
        plt.close(self.fig)
