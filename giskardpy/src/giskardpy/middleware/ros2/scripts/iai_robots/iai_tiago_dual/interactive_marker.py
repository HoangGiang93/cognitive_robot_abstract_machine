import rclpy

from giskardpy.middleware.ros2 import rospy
from giskardpy.middleware.ros2.scripts.tools.interactive_marker import InteractiveMarkerNode


def main(args: None = None) -> None:
    rospy.init_node("interactive_marker")
    node = InteractiveMarkerNode(root_link="map", tip_link="arm_right_tool_link")
    # node = InteractiveMarkerNode(root_link="map", tip_link="torso_lift_link")
    node.giskard.node_handle.get_logger().info("interactive marker server running")
    rospy.spinner_thread.join()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
