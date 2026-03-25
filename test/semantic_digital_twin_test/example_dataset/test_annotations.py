from dataclasses import field, dataclass
from typing import List, Optional

from semantic_digital_twin.world_description.world_entity import (
    Body,
    SemanticAnnotation,
)
from semantic_digital_twin.world_description.world_modification import synchronized_attribute_modification


@dataclass(eq=False)
class TestAnnotation(SemanticAnnotation):
    value: str = "default"
    entity: Optional[Body] = None
    entities: List[Body] = field(default_factory=list, hash=False)

    @synchronized_attribute_modification
    def update_value(self, new_value: str):
        self.value = new_value

    @synchronized_attribute_modification
    def update_entity(self, new_entity: Body):
        self.entity = new_entity

    @synchronized_attribute_modification
    def add_to_list(self, new_entity: Body):
        self.entities.append(new_entity)

    @synchronized_attribute_modification
    def remove_from_list(self, old_entity: Body):
        self.entities.remove(old_entity)
