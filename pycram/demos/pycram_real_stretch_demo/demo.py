import threading

import rclpy
from rclpy.executors import SingleThreadedExecutor

from pycram.datastructures.dataclasses import Context
from pycram.datastructures.enums import Arms
from pycram.motion_executor import real_robot
from pycram.plans.factories import execute_single, sequential
from pycram.robot_plans.actions.core.robot_body import MoveTorsoAction, SetGripperAction
from semantic_digital_twin.adapters.ros.world_fetcher import fetch_world_from_service
from semantic_digital_twin.adapters.ros.world_synchronizer import ModelSynchronizer, StateSynchronizer
from semantic_digital_twin.datastructures.definitions import TorsoState, GripperState
from semantic_digital_twin.robots.stretch import Stretch

rclpy.init()
node = rclpy.create_node("stretch_demo_node")

executor = SingleThreadedExecutor()
executor.add_node(node)

thread = threading.Thread(target=executor.spin, daemon=True, name="rclpy-executor")
thread.start()

world = fetch_world_from_service(node)

print(len(world.bodies))

ModelSynchronizer(_world=world, node=node)
StateSynchronizer(_world=world, node=node)

robot_annotation = world.get_semantic_annotations_by_type(Stretch)[0]
context = Context(world, robot_annotation, node)

plan = sequential([MoveTorsoAction(TorsoState.MID), SetGripperAction(Arms.LEFT, GripperState.OPEN)], context).plan

with real_robot:
    plan.perform()


rclpy.shutdown()
