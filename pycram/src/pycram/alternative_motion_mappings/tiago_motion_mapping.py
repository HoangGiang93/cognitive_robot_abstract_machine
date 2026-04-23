from giskardpy.motion_statechart.goals.cartesian_goals import DifferentialDriveBaseGoal
from giskardpy.motion_statechart.ros2_nodes.gripper_nodes import SendFloat64
from pycram.datastructures.enums import ExecutionType
from pycram.robot_plans import MoveMotion, MoveGripperMotion
from pycram.robot_plans.motions.base import AlternativeMotion
from semantic_digital_twin.datastructures.definitions import GripperState
from semantic_digital_twin.robots.tiago import Tiago, TiagoMujoco
from std_msgs.msg import Float64


class TiagoMoveSim(MoveMotion, AlternativeMotion[Tiago]):
    """
    Uses a diff drive goal for the tiago base.
    """

    execution_type = ExecutionType.SIMULATED

    def perform(self):
        return

    @property
    def _motion_chart(self):

        return DifferentialDriveBaseGoal(
            goal_pose=self.target,
        )


class TiagoMoveGripperMotion(MoveGripperMotion, AlternativeMotion[TiagoMujoco]):
    """
    Use topics to open/close Tiago in mujoco.
    """

    execution_type = ExecutionType.REAL

    def perform(self):
        return

    @property
    def _motion_chart(self):
        value = 0 if self.motion == GripperState.OPEN else 255
        if "l" in self.gripper.name:
            return SendFloat64(topic_name="/gripper_left", msg=Float64(data=value))
        return SendFloat64(topic_name="/gripper_right", msg=Float64(data=value))
