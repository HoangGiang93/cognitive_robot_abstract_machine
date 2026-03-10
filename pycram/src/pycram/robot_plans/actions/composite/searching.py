from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import timedelta

from semantic_digital_twin.world_description.world_entity import SemanticAnnotation
from typing_extensions import Union, Optional, Type, Any, Iterable


from pycram.datastructures.enums import DetectionTechnique

from pycram.datastructures.pose import PoseStamped

from pycram.failures import PerceptionObjectNotFound

from pycram.robot_plans.actions.base import ActionDescription


@dataclass
class SearchAction(ActionDescription):
    """
    Searches for a target object around the given location.
    """

    target_location: PoseStamped
    """
    Location around which to look for a target object.
    """

    object_sem_annotation: Type[SemanticAnnotation]
    """
    Type of the object which is searched for.
    """

    def execute(self) -> None:
        SequentialPlan(
            self.context,
            NavigateActionDescription(
                CostmapLocation(
                    target=self.target_location, visible_for=self.robot_view
                )
            ),
        ).perform()

        target_base = PoseStamped.from_spatial_type(
            self.world.transform(
                self.target_location.to_spatial_type(), self.world.root
            )
        )

        target_base_left = deepcopy(target_base)
        target_base_left.pose.position.y -= 0.5

        target_base_right = deepcopy(target_base)
        target_base_right.pose.position.y += 0.5

        plan = TryInOrderPlan(
            self.context,
            SequentialPlan(
                self.context,
                LookAtActionDescription(target_base_left),
                DetectActionDescription(
                    DetectionTechnique.TYPES,
                    object_sem_annotation=self.object_sem_annotation,
                ),
            ),
            SequentialPlan(
                self.context,
                LookAtActionDescription(target_base_right),
                DetectActionDescription(
                    DetectionTechnique.TYPES,
                    object_sem_annotation=self.object_sem_annotation,
                ),
            ),
            SequentialPlan(
                self.context,
                LookAtActionDescription(target_base),
                DetectActionDescription(
                    DetectionTechnique.TYPES,
                    object_sem_annotation=self.object_sem_annotation,
                ),
            ),
        )

        obj = plan.perform()
        if obj is not None:
            return obj
        raise PerceptionObjectNotFound(
            self.object_sem_annotation, DetectionTechnique.TYPES, self.target_location
        )

    def validate(
        self, result: Optional[Any] = None, max_wait_time: Optional[timedelta] = None
    ):
        pass
