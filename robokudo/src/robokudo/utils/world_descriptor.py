"""World descriptor utilities for Robokudo."""

from __future__ import annotations

from typing_extensions import TYPE_CHECKING

from . import module_loader

if TYPE_CHECKING:
    from ..annotators.core import BaseAnnotator
    from ..world_descriptor import BaseWorldDescriptor


def load_world_descriptor(annotator: BaseAnnotator) -> BaseWorldDescriptor:
    """Load world descriptor from annotator parameters."""
    loader = module_loader.ModuleLoader()
    return loader.load_world_descriptor(
        annotator.descriptor.parameters.world_descriptor_ros_package,
        annotator.descriptor.parameters.world_descriptor_name,
    )
