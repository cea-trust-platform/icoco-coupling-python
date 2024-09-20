"""This test implement the minimal API."""
# pylint: disable=protected-access
# # Test files are expected to start with 'test_' prefix

# You can import pytest and use its features.
# import pytest

import pytest
from test_problem_wrapper import _raises_before_initialize

import icoco


def test_static_methods():
    """Tests static methods of the package"""

    assert icoco.Problem.GetICoCoMajorVersion() == 2


def _test_raises_not_implemented(implem: icoco.Problem, check_minimal_api = False):  # pylint: disable=too-many-statements
    """Tests that not implemented do raise icoco.NotImplementedMethod"""

    if check_minimal_api:
        return

    if not implem._initialized:
        with pytest.raises(expected_exception=icoco.NotImplementedMethod):
            implem.setDataFile("")
        with pytest.raises(expected_exception=icoco.NotImplementedMethod):
            implem.setMPIComm(None)
        return

    if implem._time_step_defined:
        with pytest.raises(expected_exception=icoco.NotImplementedMethod):
            implem.iterateTimeStep()
        with pytest.raises(expected_exception=icoco.NotImplementedMethod):
            implem.abortTimeStep()
    else:
        with pytest.raises(expected_exception=icoco.NotImplementedMethod):
            implem.isStationary()
        with pytest.raises(expected_exception=icoco.NotImplementedMethod):
            implem.resetTime(0.0)
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
def run_test_minimal_api(minimal_problem, check_minimal_api: bool):
    # Test description:
    """Tests minimal implementation of ICoCo from the module."""

    minimal = minimal_problem

    assert "Minimal implementation" in minimal.__doc__

    _raises_before_initialize(minimal, check_minimal_api)

    _test_raises_not_implemented(minimal, check_minimal_api)

    minimal.initialize()

    assert minimal.problem_name in ["MinimalProblem", "MinimalProblemNoDoc", "MinimalNotAProblem"]

    assert minimal.presentTime() == 0.0

    dt, _ = minimal.computeTimeStep()

    minimal.initTimeStep(dt=dt)

    _test_raises_not_implemented(minimal, check_minimal_api)

    minimal.solveTimeStep()

    minimal.validateTimeStep()

    assert minimal.presentTime() == dt

    _test_raises_not_implemented(minimal, check_minimal_api)

    minimal.terminate()


def test_minimal_api(minimal_problem):
    """Tests minimal implementation of ICoCo from the module unsing icoco.Problem."""
    run_test_minimal_api(minimal_problem, check_minimal_api = False)


def test_minimal_api_nodoc(minimal_problem_nodoc):
    """Tests minimal implementation of ICoCo from the module unsing icoco.Problem
    wo class docstring."""
    run_test_minimal_api(minimal_problem_nodoc, check_minimal_api = False)


def test_minimal_api_not_a_problem(minimal_not_a_problem):
    """Tests minimal implementation of ICoCo from the module unsing check_scope."""
    run_test_minimal_api(minimal_not_a_problem, check_minimal_api = True)
