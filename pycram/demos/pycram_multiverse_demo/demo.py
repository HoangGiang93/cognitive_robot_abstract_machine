import threading

import rclpy
from rclpy.executors import SingleThreadedExecutor

from pycram.datastructures.dataclasses import Context
from pycram.datastructures.enums import Arms, ApproachDirection, VerticalAlignment
from pycram.datastructures.grasp import GraspDescription
from pycram.motion_executor import real_robot
from pycram.plans.factories import sequential
from pycram.robot_plans.actions.core.pick_up import PickUpAction
from pycram.robot_plans.actions.core.robot_body import ParkArmsAction
from semantic_digital_twin.adapters.mjcf import MJCFParser
from semantic_digital_twin.adapters.ros.visualization.viz_marker import (
    VizMarkerPublisher,
)
from semantic_digital_twin.adapters.ros.world_fetcher import fetch_world_from_service
from semantic_digital_twin.adapters.ros.world_synchronizer import (
    ModelSynchronizer,
    StateSynchronizer,
)
from semantic_digital_twin.robots.abstract_robot import AbstractRobot
from semantic_digital_twin.spatial_types import HomogeneousTransformationMatrix

import pycram.alternative_motion_mappings.tiago_motion_mapping  # type: ignore
from semantic_digital_twin.world_description.connections import FixedConnection

rclpy.init()
node = rclpy.create_node("demo")

executor = SingleThreadedExecutor()
executor.add_node(node)

thread = threading.Thread(target=executor.spin, daemon=True, name="rclpy-executor")
thread.start()

world = fetch_world_from_service(node=node)
ModelSynchronizer(node=node, _world=world, synchronous=False)
StateSynchronizer(node=node, _world=world, synchronous=False)
VizMarkerPublisher(_world=world, node=node)


if not world.is_entity_in_world_by_name("milk_box"):
    apartment_world = MJCFParser(
        file_path="/media/giangnguyen/Storage/cram_demo/Multiverse/Demos/1_TiagoDualInApartment/assets/mjcf/apartment_with_bowl_and_milk_box.xml"
    ).parse()

    print(len(world.bodies))

    world.merge_world(apartment_world)

    print(len(world.bodies))

context = Context(
    world=world,
    robot=world.get_semantic_annotations_by_type(AbstractRobot)[0],
    ros_node=node,
    evaluate_conditions=False,
)

plan = sequential(
    children=[
        ParkArmsAction(arm=Arms.BOTH),
        PickUpAction(
            object_designator=world.get_body_by_name("milk_box"),
            arm=Arms.LEFT,
            grasp_description=GraspDescription(
                approach_direction=ApproachDirection.FRONT,
                vertical_alignment=VerticalAlignment.NoAlignment,
                manipulator=context.robot.left_arm.manipulator,
            ),
        ),
    ],
    context=context,
)

with real_robot:
    plan.perform()
