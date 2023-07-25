"""This test implement the minimal API for client-server process."""
# Test files are expected to start with 'test_' prefix

# You can import pytest and use its features.
# import pytest

import os
from typing import Tuple

import pytest

import icoco

class RemoteProblem(icoco.Problem):
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

    def getOutputIntValue(self, name: str) -> int:
        return os.getpid()


# Test functions are expected to start with 'test_' prefix
def test_minimal_api():
    # Test description:
    """Tests minimal implementation of ICoCo from the module."""

    icoco.ServerManager.register('RemoteProblem', RemoteProblem)
    with pytest.raises(expected_exception=ValueError):
        icoco.ServerManager.register('RemoteProblem', RemoteProblem)

    minimal = icoco.ProblemClient('RemoteProblem')  # pylint: disable=abstract-class-instantiated

    minimal.initialize()

    assert minimal.problem_name == "RemoteProblem"

    assert minimal.presentTime() == 0.0

    dt, _ = minimal.computeTimeStep()

    minimal.initTimeStep(dt=dt)

    minimal.solveTimeStep()

    minimal.validateTimeStep()

    assert minimal.presentTime() == dt

    assert minimal.getOutputIntValue('pid') != os.getpid()

    minimal.terminate()
