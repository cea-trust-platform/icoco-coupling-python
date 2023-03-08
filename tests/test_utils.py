"""This test implement the minimal API."""
# Test files are expected to start with 'test_' prefix

# You can import pytest and use its features.
# import pytest

import icoco


def test_utils():
    """Tests utils sub package"""

    # Assert to check if test is ok
    assert icoco.ICOCO_VERSION == '2.0'
    assert icoco.ICOCO_MAJOR_VERSION == 2
    assert icoco.ICOCO_MINOR_VERSION == 0

    assert icoco.Problem.GetICoCoMajorVersion() == 2

    assert icoco.ValueType.Double.value == 0
    assert icoco.ValueType.Int.value == 1
    assert icoco.ValueType.String.value == 2

    assert icoco.ValueType.Double.name == "Double"
    assert icoco.ValueType.Int.name == "Int"
    assert icoco.ValueType.String.name == "String"
