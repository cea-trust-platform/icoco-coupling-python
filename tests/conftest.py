"""conftest for pytest"""

from typing import Tuple
import pytest

import icoco


class MinimalProblem(icoco.Problem):
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


@pytest.fixture
def minimal_problem():
    """Generate the minimal implementation for the icoco.Problem"""

    return MinimalProblem()
