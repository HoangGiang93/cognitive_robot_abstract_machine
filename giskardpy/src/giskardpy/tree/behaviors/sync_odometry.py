import numpy as np
from nav_msgs.msg import Odometry
from py_trees.common import Status

from giskardpy.utils.decorators import record_time
from giskardpy.middleware.ros2 import rospy
from giskardpy.tree.behaviors.plugin import GiskardBehavior
from giskardpy.tree.blackboard_utils import (
    catch_and_raise_to_blackboard,
)
from semantic_digital_twin.spatial_types import HomogeneousTransformationMatrix
from semantic_digital_twin.world_description.connections import OmniDrive


class SyncOdometry(GiskardBehavior):

    def __init__(
        self,
        odometry_topic: str,
        joint: OmniDrive,
        name_suffix: str = "",
    ):
        self.odometry_topic = odometry_topic
        if not self.odometry_topic.startswith("/"):
            self.odometry_topic = "/" + self.odometry_topic
        super().__init__(str(self) + name_suffix)
        self.joint = joint
        self.odometry_sub = rospy.node.create_subscription(
            Odometry, self.odometry_topic, self.cb, 1
        )
        rospy.node.get_logger().info(f"Subscribed to {self.odometry_topic}")

    def __str__(self):
        return f"{super().__str__()} ({self.odometry_topic})"

    def cb(self, data: Odometry):
        self.odom = data

    @catch_and_raise_to_blackboard
    @record_time
    def update(self):
        self.joint.set_origin_from_xyz_yaw(
            position_x=self.odom.pose.pose.position.x,
            position_y=self.odom.pose.pose.position.y,
            yaw=2
            * np.atan2(
                self.odom.pose.pose.orientation.z, self.odom.pose.pose.orientation.w
            ),
        )
        return Status.SUCCESS
