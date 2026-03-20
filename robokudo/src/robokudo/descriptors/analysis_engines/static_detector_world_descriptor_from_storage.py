import robokudo.analysis_engine
from robokudo.annotators.camera_viewpoint_visualizer import CameraViewpointVisualizer

from robokudo.annotators.collection_reader import CollectionReaderAnnotator
from robokudo.annotators.image_preprocessor import ImagePreprocessorAnnotator
from robokudo.annotators.object_hypothesis_visualizer import ObjectHypothesisVisualizer
from robokudo.annotators.plane import PlaneAnnotator
from robokudo.annotators.pointcloud_cluster_extractor import PointCloudClusterExtractor
from robokudo.annotators.pointcloud_crop import PointcloudCropAnnotator

import robokudo.descriptors.camera_configs.config_mongodb_playback

import robokudo.io.storage_reader_interface

import robokudo.behaviours.clear_errors

import robokudo.idioms
from robokudo.annotators.static_object_detector import (
    StaticObjectDetectorAnnotator,
    StaticObjectMode,
)
from robokudo.descriptors import CrDescriptorFactory


class AnalysisEngine(robokudo.analysis_engine.AnalysisEngineInterface):
    def name(self):
        return "static_detector_world_descriptor_from_storage"

    def implementation(self):
        cr_storage_config = CrDescriptorFactory.create_descriptor("mongo")

        sod = StaticObjectDetectorAnnotator.Descriptor()
        sod.parameters.mode = StaticObjectMode.WORLD_DESCRIPTOR
        sod.parameters.world_descriptor_name = "world_iai_kitchen20"
        sod.parameters.class_names = ["cereal", "milk"]
        sod.parameters.create_bounding_box_annotation = True
        sod.parameters.create_pose_annotation = True

        oh_vis = ObjectHypothesisVisualizer.Descriptor()
        oh_vis.parameters.visualize_full_cloud = True

        seq = robokudo.pipeline.Pipeline("StoragePipeline")
        seq.add_children(
            [
                robokudo.idioms.pipeline_init(),
                CollectionReaderAnnotator(descriptor=cr_storage_config),
                ImagePreprocessorAnnotator("ImagePreprocessor"),
                StaticObjectDetectorAnnotator(descriptor=sod),
                ObjectHypothesisVisualizer(descriptor=oh_vis),
            ])
        return seq
