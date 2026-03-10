from typing_extensions import List

from pycram.datastructures.dataclasses import Context
from pycram.language import SequentialNode
from pycram.plans.plan import Plan
from pycram.plans.plan_node import PlanNode


def sequential(context: Context, nodes: List[PlanNode]) -> SequentialNode:
    result = SequentialNode()
    plan = Plan(context=context)
    plan.add_node(result)
    for node in nodes:
        plan.add_edge(result, node)
    return result
