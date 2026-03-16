import os
from dataclasses import dataclass
from pathlib import Path

from robokudo.object_knowledge_base import BaseObjectKnowledgeBase, ObjectKnowledge, PredefinedObject
from semantic_digital_twin.datastructures.prefixed_name import PrefixedName
from semantic_digital_twin.spatial_types import HomogeneousTransformationMatrix
from semantic_digital_twin.world_description.connections import Connection6DoF
from semantic_digital_twin.world_description.geometry import Box, Scale, Color, FileMesh
from semantic_digital_twin.world_description.shape_collection import ShapeCollection
from semantic_digital_twin.world_description.world_entity import Body


@dataclass
class ObjectKnowledgeBase(BaseObjectKnowledgeBase):
    def __init__(self):
        super().__init__()
        root = self.world.root

        milk_path = (
                Path(__file__).resolve().parents[5]
                / "semantic_digital_twin"
                / "resources"
                / "stl"
                / "milk.stl"
        )

        milk_mesh = FileMesh(
            origin=HomogeneousTransformationMatrix(), filename=str(milk_path)
        )

        foobar1_shape = Box(scale=Scale(0.20, 0.20, 0.20), color=Color(0.1, 0.2, 0.8, 1.0))
        foobar1_body = Body(
            name=PrefixedName(name="cereal"),
            visual=ShapeCollection([foobar1_shape]),
            collision=ShapeCollection([foobar1_shape]),
        )

        milk_shape = Box(scale=Scale(0.10, 0.15, 0.40), color=Color(0.1, 0.2, 0.8, 1.0))
        milk_body = Body(
            name=PrefixedName(name="milk"),
            visual=ShapeCollection([milk_shape, milk_mesh]),
            collision=ShapeCollection([milk_shape]),
        )

        with self.world.modify_world():
            result_world_C_foobar1 = Connection6DoF.create_with_dofs(parent=root, child=foobar1_body, world=self.world)
            result_world_C_milk = Connection6DoF.create_with_dofs(parent=root, child=milk_body, world=self.world)
            self.world.add_connection(result_world_C_foobar1)
            self.world.add_connection(result_world_C_milk)
            self.world.add_semantic_annotation(PredefinedObject(body=foobar1_body))
            self.world.add_semantic_annotation(PredefinedObject(body=milk_body))

        # Set origins in a separate modification block so FK is compiled first
        with (self.world.modify_world()):
            result_world_C_foobar1.origin = HomogeneousTransformationMatrix.from_xyz_rpy(x=-1.3, y=1.0, z=1.1,
                                                                                         reference_frame=root)
            result_world_C_milk.origin = HomogeneousTransformationMatrix.from_xyz_rpy(x=-1.3, y=1.2, z=1.1,
                                                                                      reference_frame=root)
