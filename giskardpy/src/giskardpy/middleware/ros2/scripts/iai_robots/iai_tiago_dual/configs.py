from dataclasses import dataclass, field

from giskardpy.model.world_config import WorldWithOmniDriveRobot, WorldWithDiffDriveRobot
from giskardpy.middleware.ros2.giskard import RobotInterfaceConfig
from semantic_digital_twin.datastructures.prefixed_name import PrefixedName
from semantic_digital_twin.robots.abstract_robot import AbstractRobot
from semantic_digital_twin.robots.pr2 import PR2
from semantic_digital_twin.robots.tiago import TiagoMujoco
from semantic_digital_twin.world_description.connections import (
    OmniDrive, Connection6DoF, DifferentialDrive,
)


@dataclass
class WorldWithTiagoConfig(WorldWithDiffDriveRobot):
    odom_body_name: PrefixedName = PrefixedName("odom")
    urdf_view: AbstractRobot = field(kw_only=True, default=TiagoMujoco, init=False)




class TiagoVelocityInterface(RobotInterfaceConfig):

    def setup(self):
        self.sync_6dof_joint_with_tf_frame(
            joint=self.world.get_connections_by_type(Connection6DoF)[0],
            tf_parent_frame="map",
            tf_child_frame="odom",
        )

        omni_drive = self.world.get_connections_by_type(DifferentialDrive)[0]
        self.sync_odometry_topic(
            "/odom",
            omni_drive,
        )

        self.add_base_cmd_velocity(
            cmd_vel_topic="/cmd_vel", joint=omni_drive
        )

        self.sync_joint_state_topic("/joint_states")
        joints_left = [
            "head_1_joint",
            "head_2_joint",
            "torso_lift_joint",
            "arm_left_1_joint",
            "arm_left_2_joint",
            "arm_left_3_joint",
            "arm_left_4_joint",
            "arm_left_5_joint",
            "arm_left_6_joint",
            "arm_left_7_joint",
            "arm_right_1_joint",
            "arm_right_2_joint",
            "arm_right_3_joint",
            "arm_right_4_joint",
            "arm_right_5_joint",
            "arm_right_6_joint",
            "arm_right_7_joint"
        ]
        self.add_joint_velocity_group_controller(
            cmd_topic="/upper_body_velocity_controller/command", connections=joints_left
        )
