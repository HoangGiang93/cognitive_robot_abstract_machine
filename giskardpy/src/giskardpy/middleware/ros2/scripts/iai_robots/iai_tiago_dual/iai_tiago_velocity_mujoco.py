from giskardpy.middleware.ros2.ros2_interface import get_robot_description
from giskardpy.middleware.ros2.scripts.iai_robots.iai_tiago_dual.configs import WorldWithTiagoConfig, \
    TiagoVelocityInterface
from giskardpy.middleware.ros2.utils.utils import load_xacro
from giskardpy.qp.qp_controller_config import QPControllerConfig
from giskardpy.middleware.ros2.behavior_tree_config import ClosedLoopBTConfig
from giskardpy.middleware.ros2.giskard import Giskard
from giskardpy.middleware.ros2 import rospy


def main():
    rospy.init_node("giskard")
    urdf = get_robot_description()
    giskard = Giskard(
        world_config=WorldWithTiagoConfig(urdf=urdf),
        robot_interface_config=TiagoVelocityInterface(),
        qp_controller_config=QPControllerConfig(
            target_frequency=30, prediction_horizon=15
        ),
        behavior_tree_config=ClosedLoopBTConfig(debug_mode=False),
    )
    giskard.live()
    ...


if __name__ == "__main__":
    main()
