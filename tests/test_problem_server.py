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
        if name != "pid":
            raise icoco.exception.WrongArgument(
                prob=self._problem_name,
                method="getOutputIntValue",
                arg=name,
                condition="Name not in ['pid']")
        return os.getpid()

class RemoteProblem2(RemoteProblem):
    """Minimal implementation of ICoCo"""


# Test functions are expected to start with 'test_' prefix
def test_client():
    # Test description:
    """Tests server/client implementation of ICoCo from the module."""

    typeid = icoco.ServerManager.register(RemoteProblem)
    with pytest.raises(expected_exception=ValueError) as error:
        icoco.ServerManager.register(RemoteProblem)
    assert "typeid RemoteProblem is already registerd." in str(error.value)

    client = icoco.ProblemClient(typeid)  # pylint: disable=abstract-class-instantiated

    client.initialize()

    assert client.problem_name == "RemoteProblem"

    assert client.presentTime() == 0.0

    dt, _ = client.computeTimeStep()

    client.initTimeStep(dt=dt)

    client.solveTimeStep()

    client.validateTimeStep()

    assert client.presentTime() == dt

    assert client.getOutputIntValue('pid') != os.getpid()

    with pytest.raises(icoco.problem_server.RemoteException) as error:
        client.getOutputIntValue(name='pod')
    print(error.value)
    assert ("RemoteException raised from:\n"
            "WrongArgument in Problem instance with name: 'RemoteProblem'"
            " in method 'getOutputIntValue', argument 'pod' : Name not in ['pid']"
            in str(error.value))

    client.terminate()

    del client
