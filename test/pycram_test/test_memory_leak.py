import gc
from copy import deepcopy

import objgraph

from pycram.datastructures.dataclasses import Context
from pycram.datastructures.pose import PoseStamped
from pycram.language import SequentialPlan
from pycram.motion_executor import simulated_robot
from pycram.robot_plans import NavigateActionDescription
from semantic_digital_twin.robots.pr2 import PR2


def test_ref_chain_after_copy(immutable_model_world):
    world, view, c = immutable_model_world
    copy_world = deepcopy(world)
    copy_world.name = "copy_world"
    chain = objgraph.find_ref_chain(world, lambda x: x is copy_world)
    assert chain == [world]


def test_ref_chain_after_copy_with_execute(immutable_model_world):
    world, view, c = immutable_model_world
    copy_world = deepcopy(world)
    copy_world.name = "copy_world"

    copy_context = Context(copy_world, PR2.from_world(copy_world))

    plan = SequentialPlan(
        copy_context,
        NavigateActionDescription(
            PoseStamped.from_list([1, -1, 0], frame=copy_world.root)
        ),
    )

    with simulated_robot:
        plan.perform()

    gc.collect()
    chain = objgraph.find_ref_chain(world, lambda x: x is copy_world)
    assert chain == [world]
