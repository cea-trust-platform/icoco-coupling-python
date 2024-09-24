# Introduction

## Installation

Simply run:

```sh
python3 -m pip install icoco
```

## Quick start

### Implement your own ICoCo class

Your ICoCo class must derive from {class}`icoco.problem.Problem`:

```python

from icoco import Problem

class MyICoCoProblem(Problem):

    def __init__(self):
        super().__init__()

    ...
```

Once all {class}`abstractmethods` must be implmemented, you have a functional API.

The {class}`icoco.problem.Problem` implement scope checks by default (initialization and inside/outside
time step). These checks can be disabled at any time:

```python

from icoco import Problem

class MyICoCoProblem(Problem):

    def __init__(self):
        super().__init__(ensure_scope=False)

    ...

    def other_icoco_method(self):
        ensure_scope = self._ensure_scope
        self._ensure_scope = False
        ...
        self._ensure_scope = self._ensure_scope

    ...
```

A second usefull feature is implemented within the {class}`icoco.problem.Problem` class: the possibility
to execute the ICoCo method from a specific working directory:

```python

from pathlib import Path
from icoco import Problem

class MyICoCoProblem(Problem):

    def __init__(self):
        super().__init__(working_directory=Path("/home/user/working_dir"))

    ...
```

### Use it in a *safe* way (**EXPERIMENTAL**)

The {class}`icoco.problem_wrapper.ProblemWrapper` wrapper implements checks for calls inside/outside time step
context and other coherency verifications.

```python

from icoco import Problem, ProblemWrapper

class MyICoCoProblem(Problem):

    def __init__(self):
        pass

    ...

my_problem = ProblemWrapper(MyICoCoProblem())

my_problem.solveTimeStep() # FAILS! since neither initialize nor initTimeStep have been called.

```

### Use server for ICoCo problem (**EXPERIMENTAL**)

The {class}`icoco.problem_server.ProblemClient` implements server initialization and execution.

```python

import os

from icoco import Problem, ProblemClient, ServerManager

class MyICoCoProblem(Problem):

    def __init__(self, arg1: int, arg2: int):
        pass

    def initialize(self):

        print(os.getpid())

    ...

ServerManager.register('MyICoCoProblem', MyICoCoProblem)

my_problem = ProblemClient('MyICoCoProblem', {'arg1': 1, 'arg2': 2})

my_problem.initialize()

print(os.getpid())

```
