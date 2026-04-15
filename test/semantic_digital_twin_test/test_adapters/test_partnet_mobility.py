from semantic_digital_twin.adapters.partnet_mobility_dataset.loader import (
    PartnetMobilityDatasetLoader,
)


def test_loader():
    loader = PartnetMobilityDatasetLoader()
    world = loader.load()
    print(world)
