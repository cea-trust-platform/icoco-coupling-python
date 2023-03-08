"""This test implement the minimal API."""
# Test files are expected to start with 'test_' prefix

# You can import pytest and use its features.
# import pytest

from typing import Tuple

import pytest

import icoco


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


class Minimal(icoco.Problem):
    """Minimal implementation of ICoCo"""

    def __init__(self) -> None:
        super().__init__()
        self._time: float = 0.0
        self._dt: float = 0.0
        self._stat: bool = False

    def initialize(self) -> bool:
        self._time: float = 0.0
        self._dt: float = 0.0
        self._stat: bool = False
        return True

    def terminate(self) -> None:
        pass

    def presentTime(self) -> float:
        return self._time

    def computeTimeStep(self) -> Tuple[float, bool]:
        return (0.1, False)

    def initTimeStep(self, dt: float) -> bool:
        self._dt = dt
        return True

    def solveTimeStep(self) -> bool:
        print(f"Solver from t={self._time} to t+dt={self._time + self._dt}")
        return True

    def validateTimeStep(self) -> None:
        self._time += self._dt

    def setStationaryMode(self, stationaryMode: bool) -> None:
        self._stat = stationaryMode

    def getStationaryMode(self) -> bool:
        return self._stat


# Test functions are expected to start with 'test_' prefix
def test_minimal_api():
    # Test description:
    """Tests minimal implementation of ICoCo from the module."""

    minimal = Minimal()

    minimal.initialize()

    assert minimal.problem_name == "Minimal"

    assert minimal.presentTime() == 0.0

    dt, _ = minimal.computeTimeStep()

    minimal.initTimeStep(dt=dt)

    minimal.solveTimeStep()

    minimal.validateTimeStep()

    assert minimal.presentTime() == dt

    _test_raises_not_implemented(minimal)

    minimal.terminate()
