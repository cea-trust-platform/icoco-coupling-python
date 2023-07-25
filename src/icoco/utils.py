"""
ICoCo file common to several codes
Version 2 -- 02/2021

WARNING: this file is part of the official ICoCo API and should not be modified.
The official version can be found at the following URL:

https://github.com/cea-trust-platform/icoco-coupling
"""

from enum import Enum

try:
    import medcoupling  # pylint: disable=unused-import
except ImportError:  # pragma: no cover
    import warnings
    warnings.warn(message="medcoupling module not found",
                  category=ImportWarning)

    class medcoupling:  # pylint: disable=too-few-public-methods, invalid-name
        """dummy class for type hinting"""
        class MEDCouplingFieldDouble:  # pylint: disable=too-few-public-methods
            """dummy class for MEDCouplingFieldDouble type hinting"""
        class MEDCouplingFieldInt:  # pylint: disable=too-few-public-methods
            """dummy class for MEDCouplingFieldInt type hinting"""
        class MEDCouplingField:  # pylint: disable=too-few-public-methods
            """dummy class for MEDCouplingField type hinting"""

ICOCO_VERSION = "2.0"
ICOCO_MAJOR_VERSION = 2
ICOCO_MINOR_VERSION = 0

class ICoCoMethods: # pylint: disable=too-few-public-methods
    """Namespace to list all ICoCo methods."""

    PROBLEM = ["setDataFile", "setMPIComm", "initialize", "terminate"]
    """ICoco methods of section Problem"""

    TIME_STEP = ["presentTime", "computeTimeStep", "initTimeStep", "solveTimeStep",
                 "validateTimeStep", "setStationaryMode", "getStationaryMode", "isStationary",
                 "abortTimeStep", "resetTime", "iterateTimeStep",]
    """ICoco methods of section TimeStepManagement"""

    RESTORE = ["save", "restore", "forget"]
    """ICoco methods of section Restorable"""

    IO_FIELD = ["getInputFieldsNames", "getOutputFieldsNames",
                "getFieldType", "getMeshUnit", "getFieldUnit",
                "getInputMEDDoubleFieldTemplate", "setInputMEDDoubleField",
                "getOutputMEDDoubleField", "updateOutputMEDDoubleField",
                "getInputMEDIntFieldTemplate", "setInputMEDIntField",
                "getOutputMEDIntField", "updateOutputMEDIntField",
                "getInputMEDStringFieldTemplate", "setInputMEDStringField",
                "getOutputMEDStringField", "updateOutputMEDStringField",
                "getMEDCouplingMajorVersion", "isMEDCoupling64Bits"
                ]
    """ICoco methods of section Field I/O"""

    IO_VALUE = ["getInputValuesNames", "getOutputValuesNames", "getValueType", "getValueUnit",
                "setInputDoubleValue", "getOutputDoubleValue",
                "setInputIntValue", "getOutputIntValue",
                "setInputStringValue", "getOutputStringValue"]
    """ICoco methods of section Scalar values I/O"""

    ALL = ['GetICoCoMajorVersion'] + PROBLEM + TIME_STEP + RESTORE + IO_FIELD + IO_VALUE
    """All ICoCo methods"""


class ValueType(Enum):
    """The various possible types for fields or scalar values."""

    Double = 0
    """Double scalar value or field type"""
    Int = 1
    """Int scalar value or field type"""
    String = 2
    """String scalar value or field type"""


try:
    from mpi4py.MPI import Intracomm as MPIComm  # type: ignore  # pylint: disable=unused-import
except ModuleNotFoundError:  # pragma: no cover
    class MPIComm:  # pylint: disable=too-few-public-methods
        """Basic class for type hinting when mi4py is not available"""
