from dataclasses import dataclass

from giskardpy.motion_statechart.ros2_nodes.topic_monitor import (
    PublishOnStart,
)
from std_msgs.msg import Float64


@dataclass(eq=False, repr=False)
class SendFloat64(PublishOnStart[Float64]): ...
