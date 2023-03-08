"""This test implement the minimal API."""
# Test files are expected to start with 'test_' prefix

# You can import pytest and use its features.
# import pytest


import pytest
from typing import Tuple

import icoco

def test_static_methods():
    """Tests static methods of the package"""

    # Assert to check if test is ok
    assert icoco.ICOCO_VERSION == '2.0'
    assert icoco.ICOCO_MAJOR_VERSION == 2
    assert icoco.ICOCO_MINOR_VERSION == 0

    assert icoco.Problem.GetICoCoMajorVersion() == 2

# Test functions are expected to start with 'test_' prefix
def test_minimal_api():
    # Test description:
    """Tests minimal implementation of ICoCo from the module."""

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

    minimal = Minimal()

    minimal.initialize()

    assert minimal.problem_name == "Minimal"

    assert minimal.presentTime() == 0.0

    dt, _ = minimal.computeTimeStep()

    minimal.initTimeStep(dt=dt)

    minimal.solveTimeStep()

    minimal.validateTimeStep()

    assert minimal.presentTime() == dt


    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.setDataFile("")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.setMPIComm(None)
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.isStationary()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.abortTimeStep()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.resetTime(time=0.0)
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.iterateTimeStep()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.save(label=0, method="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.restore(label=0, method="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.forget(label=0, method="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.getInputFieldsNames()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.getOutputFieldsNames()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.getFieldType(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.getMeshUnit()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.getFieldUnit(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.getInputMEDDoubleFieldTemplate(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.setInputMEDDoubleField(name="", afield=None)
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.getOutputMEDDoubleField(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.updateOutputMEDDoubleField(name="", afield=None)
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.getInputMEDIntFieldTemplate(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.setInputMEDIntField(name="", afield=None)
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.getOutputMEDIntField(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.updateOutputMEDIntField(name="", afield=None)
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.getInputMEDStringFieldTemplate(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.setInputMEDStringField(name="", afield=None)
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.getOutputMEDStringField(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.updateOutputMEDStringField(name="", afield=None)
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.getMEDCouplingMajorVersion()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.isMEDCoupling64Bits()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.getInputValuesNames()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.getOutputValuesNames()
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.getValueType(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.getValueUnit(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.setInputDoubleValue(name="", val=0.0)
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.getOutputDoubleValue(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.setInputIntValue(name="", val=0)
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.getOutputIntValue(name="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.setInputStringValue(name="", val="")
    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        minimal.getOutputStringValue(name="")


    minimal.terminate()
