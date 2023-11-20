"""This test implement the minimal API."""
# Test files are expected to start with 'test_' prefix

# You can import pytest and use its features.
# import pytest

from pathlib import Path
import pytest

import icoco


def test_context():
    """Tests ProblemWrapper.Context class"""

    context = icoco.ProblemWrapper.Context()

    assert context.time == 0.0
    assert context.dt == 0.0
    assert not context.time_step_defined
    assert not context.stationnary

    context.reset_time(time=10.0)
    assert context.time == 10.0
    context.set_stationnary(stationnary=True)
    assert context.stationnary

    context.save(label=0, method="")

    context.initialize_step(dt=20.0)
    assert context.time_step_defined
    assert context.dt == 20.0
    context.validate_step()
    assert not context.time_step_defined
    assert context.dt == 0.0
    assert context.time == 30.0

    context.initialize_step(dt=40.0)
    assert context.time_step_defined
    assert context.dt == 40.0
    context.abort_step()
    assert not context.time_step_defined
    assert context.dt == 0.0
    assert context.time == 30.0

    context.restore(label=0, method="")
    context.forget(label=0, method="")


def test_static_methods():
    """Tests static methods of the package"""

    assert icoco.ProblemWrapper.GetICoCoMajorVersion() == 2


def _raise_outside_time_step(implem: icoco.ProblemWrapper):
    """Test raise WrongContext outside time step"""
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.solveTimeStep()
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.validateTimeStep()
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.abortTimeStep()
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.iterateTimeStep()


def _raise_inside_time_step(implem: icoco.ProblemWrapper):
    """Test raise WrongContext inside time step"""
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.computeTimeStep()
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.initTimeStep(dt=0.0)
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.setStationaryMode(stationaryMode=True)
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.isStationary()
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.resetTime(time=0.0)
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.save(label=0, method="")
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.restore(label=0, method="")
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.terminate()


def _raises_after_initialize(implem: icoco.ProblemWrapper):  # pylint: disable=too-many-statements
    """Test raise WrongContext after initialize"""

    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.initialize()
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.setDataFile(__file__)
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.setMPIComm(None)


def _raises_before_initialize(implem: icoco.ProblemWrapper):  # pylint: disable=too-many-statements
    """Test raise WrongContext before initialize"""
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.computeTimeStep()
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.initTimeStep(dt=0.0)
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.solveTimeStep()
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.validateTimeStep()
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.setStationaryMode(stationaryMode=True)
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.getStationaryMode()
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.presentTime()
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.isStationary()
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.abortTimeStep()
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.resetTime(time=0.0)
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.iterateTimeStep()
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.save(label=0, method="")
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.restore(label=0, method="")
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.forget(label=0, method="")
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.getInputFieldsNames()
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.getOutputFieldsNames()
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.getFieldType(name="")
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.getMeshUnit()
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.getFieldUnit(name="")
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.getInputMEDDoubleFieldTemplate(name="")
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.setInputMEDDoubleField(name="", afield=None)
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.getOutputMEDDoubleField(name="")
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.updateOutputMEDDoubleField(name="", afield=None)
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.getInputMEDIntFieldTemplate(name="")
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.setInputMEDIntField(name="", afield=None)
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.getOutputMEDIntField(name="")
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.updateOutputMEDIntField(name="", afield=None)
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.getInputMEDStringFieldTemplate(name="")
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.setInputMEDStringField(name="", afield=None)
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.getOutputMEDStringField(name="")
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.updateOutputMEDStringField(name="", afield=None)
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.getInputValuesNames()
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.getOutputValuesNames()
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.getValueType(name="")
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.getValueUnit(name="")
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.setInputDoubleValue(name="", val=0.0)
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.getOutputDoubleValue(name="")
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.setInputIntValue(name="", val=0)
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.getOutputIntValue(name="")
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.setInputStringValue(name="", val="")
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.getOutputStringValue(name="")
    with pytest.raises(expected_exception=icoco.WrongContext):
        implem.terminate()


# Test functions are expected to start with 'test_' prefix
def test_minimal_api(save_restore_problem):
    # Test description:
    """Tests minimal implementation of ICoCo from the module."""

    with pytest.raises(expected_exception=icoco.WrongArgument):
        minimal = icoco.ProblemWrapper(
            save_restore_problem, Path(__file__).resolve().parent / "not_existing_dir")


    minimal = icoco.ProblemWrapper(save_restore_problem, Path(__file__).resolve().parent)

    assert minimal.GetICoCoMajorVersion() == 2

    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.getMEDCouplingMajorVersion()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.isMEDCoupling64Bits()

    with pytest.raises(expected_exception=icoco.WrongArgument):
        minimal.setDataFile("")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.setDataFile(__file__)
    with pytest.raises(expected_exception=icoco.WrongContext):
        minimal.setDataFile(__file__)

    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.setMPIComm(icoco.utils.MPIComm())
    with pytest.raises(expected_exception=icoco.WrongContext):
        minimal.setMPIComm(None)

    _raises_before_initialize(implem=minimal)

    minimal.initialize()

    _raises_after_initialize(implem=minimal)

    _raise_outside_time_step(implem=minimal)

    assert minimal.presentTime() == 0.0

    dt, _ = minimal.computeTimeStep()

    assert not minimal.getStationaryMode()

    minimal.setStationaryMode(stationaryMode=True)

    with pytest.raises(expected_exception=icoco.WrongArgument):
        minimal.initTimeStep(dt=-1.0)
    minimal.initTimeStep(dt=dt)
    _raise_inside_time_step(implem=minimal)

    assert minimal.getStationaryMode()

    minimal.solveTimeStep()

    minimal.validateTimeStep()

    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.isStationary()

    assert minimal.presentTime() == dt

    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.resetTime(10.0)

    assert minimal.presentTime() == 10.0

    minimal.initTimeStep(dt=dt)
    minimal.solveTimeStep()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.iterateTimeStep()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.abortTimeStep()

    _test_save_restore_forget(implem=minimal)
    _test_raises_not_implemented_without_context(implem=minimal)

    minimal.terminate()


def _test_save_restore_forget(implem: icoco.Problem):

    implem.save(label=2, method="memory")
    time2 = implem.presentTime()
    stat2 = implem.getStationaryMode()
    implem.restore(label=1, method="file")
    assert implem.presentTime() == 100.0
    assert not implem.getStationaryMode()
    implem.restore(label=0, method="file")
    assert implem.presentTime() == 0.0
    assert implem.getStationaryMode()
    implem.restore(label=2, method="memory")
    assert implem.presentTime() == time2
    assert implem.getStationaryMode() == stat2
    implem.forget(label=2, method="memory")

    with pytest.raises(expected_exception=icoco.WrongArgument):
        implem.restore(label=1, method="non existing")


def _test_raises_not_implemented_without_context(implem: icoco.Problem):  # pylint: disable=too-many-statements
    """Tests that not implemented do raise icoco.NotImplementedMethod"""
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
