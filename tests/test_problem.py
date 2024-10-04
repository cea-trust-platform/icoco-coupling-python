"""This test implement the minimal API."""
# Test files are expected to start with 'test_' prefix

# You can import pytest and use its features.
# import pytest

import pytest

import icoco


def test_version():
    """Tests version infos"""

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


def test_static_methods():
    """Tests static methods of the package"""

    assert icoco.Problem.GetICoCoMajorVersion() == 2


def _test_raises_not_implemented(implem: icoco.Problem):  # pylint: disable=too-many-statements
    """Tests that not implemented do raise icoco.NotImplementedMethod"""
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.setDataFile("")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.setMPIComm(None)
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.isStationary()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.abortTimeStep()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.resetTime(time=0.0)
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.iterateTimeStep()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.save(label=0, method="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.restore(label=0, method="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.forget(label=0, method="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.getInputFieldsNames()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.getOutputFieldsNames()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.getFieldType(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.getMeshUnit()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.getFieldUnit(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.getInputMEDDoubleFieldTemplate(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.setInputMEDDoubleField(name="", afield=None)
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.getOutputMEDDoubleField(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.updateOutputMEDDoubleField(name="", afield=None)
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.getInputMEDIntFieldTemplate(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.setInputMEDIntField(name="", afield=None)
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.getOutputMEDIntField(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.updateOutputMEDIntField(name="", afield=None)
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.getInputMEDStringFieldTemplate(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.setInputMEDStringField(name="", afield=None)
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.getOutputMEDStringField(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.updateOutputMEDStringField(name="", afield=None)
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.getMEDCouplingMajorVersion()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.isMEDCoupling64Bits()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.getInputValuesNames()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.getOutputValuesNames()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.getValueType(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.getValueUnit(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.setInputDoubleValue(name="", val=0.0)
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.getOutputDoubleValue(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.setInputIntValue(name="", val=0)
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.getOutputIntValue(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.setInputStringValue(name="", val="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        implem.getOutputStringValue(name="")


# Test functions are expected to start with 'test_' prefix
def test_minimal_api(minimal_problem):
    # Test description:
    """Tests minimal implementation of ICoCo from the module."""

    minimal = minimal_problem

    minimal.initialize()

    assert minimal.presentTime() == 0.0

    dt, _ = minimal.computeTimeStep()

    minimal.initTimeStep(dt=dt)

    minimal.solveTimeStep()

    minimal.validateTimeStep()

    assert minimal.presentTime() == dt

    _test_raises_not_implemented(minimal)

    minimal.terminate()
