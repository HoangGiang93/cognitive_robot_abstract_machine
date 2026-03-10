from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from typing_extensions import (
    List,
    Optional,
    Any,
)

from pycram.datastructures.pose import PoseStamped
from pycram.plans.plan import Plan, PlanEntity
from semantic_digital_twin.robots.abstract_robot import AbstractRobot
from semantic_digital_twin.world import World
from semantic_digital_twin.world_description.world_entity import Body
from semantic_digital_twin.world_description.world_modification import (
    WorldModelModificationBlock,
)


@dataclass
class Context(PlanEntity):
    """
    A dataclass for storing the context of a plan
    """

    world: World
    """
    The world in which the plan is executed
    """

    robot: AbstractRobot
    """
    The semantic robot annotation which should execute the plan
    """

    ros_node: Optional[Any] = field(default=None)
    """
    A ROS node that should be used for communication in this plan
    """

    @classmethod
    def from_world(cls, world: World, plan: Plan = None):
        """
        Create a context from a world by getting the first robot in the world. There is no super plan in this case.

        :param world: The world for which to create the context
        :param plan: The plan that manages this context
        :return: A context with the first robot in the world and no super plan
        """
        result =  cls(
            world=world,
            robot=world.get_semantic_annotations_by_type(AbstractRobot)[0],
        )
        if plan:
            plan.add_plan_entity(result)
        return result



@dataclass
class ExecutionData:
    """
    A dataclass for storing the information of an execution that is used for creating a robot description for that
    execution. An execution is a Robot with a virtual mobile base that can be used to move the robot in the environment.
    """

    execution_start_pose: PoseStamped
    """
    Start of the robot at the start of execution of an action designator
    """

    execution_start_world_state: np.ndarray
    """
    The world state at the start of execution of an action designator
    """

    execution_end_pose: Optional[PoseStamped] = None
    """
    The pose of the robot at the end of executing an action designator
    """

    execution_end_world_state: Optional[np.ndarray] = None
    """
    The world state at the end of executing an action designator
    """

    added_world_modifications: List[WorldModelModificationBlock] = field(
        default_factory=list
    )
    """
    A list of World modification blocks that were added during the execution of the action designator
    """

    manipulated_body_pose_start: Optional[PoseStamped] = None
    """
    Start pose of the manipulated Body if there was one
    """

    manipulated_body_pose_end: Optional[PoseStamped] = None
    """
    End pose of the manipulated Body if there was one
    """

    manipulated_body: Optional[Body] = None
    """
    Reference to the manipulated body 
    """

    manipulated_body_name: Optional[str] = None
    """
    Name of the manipulated body
    """



