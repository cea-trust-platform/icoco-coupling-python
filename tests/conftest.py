"""conftest for pytest"""

from typing import Dict, Tuple
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


class SaveRestoreProblem(MinimalProblem):
    """Minimal implementation of ICoCo + Save/Restore capabilities"""

    def __init__(self) -> None:
        super().__init__()
        self._state: Dict[Tuple[int, str]] = {
            (0, "file"): (0.0, True),  # Emulate save in file at initial time
            (1, "file"): (100.0, False)  # Emulate save in file at final time
        }

    def save(self, label: int, method: str) -> None:
        self._state[(label, method)] = (self._time, self._stat)

    def restore(self, label: int, method: str) -> None:
        if (label, method) not in self._state:
            raise icoco.WrongArgument(prob=self.__class__.__name__,
                                      method="restore",
                                      arg="(label, method)",
                                      condition=f"({label}, {method}) is not a known save state")
        self._time = self._state[(label, method)][0]
        self._stat = self._state[(label, method)][1]

    def forget(self, label: int, method: str) -> None:
        if (label, method) in self._state:
            self._state.pop((label, method))


@pytest.fixture
def minimal_problem():
    """Generate the minimal implementation for the icoco.Problem"""

    return MinimalProblem()


@pytest.fixture
def save_restore_problem():
    """Generate the minimal implementation + save/restore for the icoco.Problem"""

    return SaveRestoreProblem()
