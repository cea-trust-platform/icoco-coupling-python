# Introduction

This package contains a Python implementation of ICoco.

## Package version semantics

The package version has major and minor versions corresponding to ICoCo implementation.

The patch version number are correction/improvements of this package with respect to the norm.

## Installation

Simply run:

```sh
python3 -m pip install "icoco~=2.0.0"
```

to get the last version of the package implementing version 2.0 of ICoCo.

## Quick start: implement your own ICoCo class

Your ICoCo class may derive from the {class}`abc.ABC` class {class}`icoco.problem.Problem`:

```python

from icoco import Problem

class MyICoCoProblem(Problem):

    def __init__(self):
        pass

    ...
```

Once all the {func}`abc.abstractmethod` have been implmemented, you have a functional minimal API.

## Package content

- {mod}`icoco.problem` module: this package contains Python implementation of ICoCo,
- {mod}`icoco.exception` module: this module contains Python implementation of ICoCo exceptions,
- {mod}`icoco.version` module: this module contains version informations,
- {mod}`icoco.utils` module: this module contains tools for ICoCo introspection.
