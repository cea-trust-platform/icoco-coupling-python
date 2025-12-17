"""test icoco.utils module"""
import icoco.utils


def test_utils_icoco_methods():
    """Tests ICoCoMethods"""

    assert len(icoco.utils.ICoCoMethods.PROBLEM) == 4
    assert len(icoco.utils.ICoCoMethods.TIME_STEP) == 11
    assert len(icoco.utils.ICoCoMethods.RESTORE) == 3
    assert len(icoco.utils.ICoCoMethods.IO_FIELD) == 19
    assert len(icoco.utils.ICoCoMethods.IO_VALUE) == 10
    assert len(icoco.utils.ICoCoMethods.ALL) == 48


def test_utils_icoco_method_context():
    """Tests ICoCoMethodContext"""

    assert len(icoco.utils.ICoCoMethodContext.ONLY_BEFORE_INITIALIZE) == 3
    assert len(icoco.utils.ICoCoMethodContext.ONLY_AFTER_INITIALIZE ) == (
        len(icoco.utils.ICoCoMethods.ALL) - 6)
    assert len(icoco.utils.ICoCoMethodContext.ONLY_INSIDE_TIME_STEP_DEFINED) == 4
    assert len(icoco.utils.ICoCoMethodContext.ONLY_OUTSIDE_TIME_STEP_DEFINED) == 8
