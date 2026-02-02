import os

import krrood
import krrood.entity_query_language
from krrood.utils import get_package_root
import pytest


def test_get_package_root():
    root = get_package_root(krrood)

    absolute_root = os.path.abspath(root)

    assert absolute_root.endswith(
        os.path.join("cognitive_robot_abstract_machine", "krrood")
    )

    with pytest.raises(FileNotFoundError):
        get_package_root(pytest)

    assert (
        os.path.abspath(get_package_root(krrood.entity_query_language)) == absolute_root
    )
