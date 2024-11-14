"""
ICoCo file common to several codes
Version 2 -- 02/2021

WARNING: this file is part of the official ICoCo API and should not be modified.
The official version can be found at the following URL:

https://github.com/cea-trust-platform/icoco-coupling
"""


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


try:
    import mpi4py
    mpi4py.rc.initialize = False
    mpi4py.rc.finalize = False
    from mpi4py.MPI import Intracomm as MPIComm  # type: ignore  # pylint: disable=unused-import
    mpi4py.rc.initialize = True
    mpi4py.rc.finalize = True
except ModuleNotFoundError:  # pragma: no cover
    class MPIComm:  # pylint: disable=too-few-public-methods
        """Basic class for type hinting when mi4py is not available"""


class ICoCoMethods:  # pylint: disable=too-few-public-methods
    """Namespace to list all ICoCo methods."""

    PROBLEM = ["setDataFile", "setMPIComm", "initialize", "terminate"]
    """ICoco methods of section Problem"""

    TIME_STEP = ["presentTime", "computeTimeStep", "initTimeStep", "solveTimeStep",
                 "validateTimeStep", "setStationaryMode", "getStationaryMode", "isStationary",
                 "abortTimeStep", "resetTime", "iterateTimeStep"]
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

    ALL = ["GetICoCoMajorVersion"] + PROBLEM + TIME_STEP + RESTORE + IO_FIELD + IO_VALUE
    """All ICoCo methods"""


class ICoCoMethodContext:  # pylint: disable=too-few-public-methods
    """Namespace to list all context restrictions for ICoCo methods."""

    ONLY_BEFORE_INITIALIZE = ["setDataFile", "setMPIComm", "initialize"]
    """Methods which must be called only BEFORE ``initialize``."""

    ONLY_AFTER_INITIALIZE = [name for name in ICoCoMethods.ALL
                             if name not in ["setDataFile", "setMPIComm", "initialize",
                                             "getMEDCouplingMajorVersion", "isMEDCoupling64Bits",
                                             "GetICoCoMajorVersion"]]
    """Methods which must be called only AFTER ``initialize``."""

    ONLY_INSIDE_TIME_STEP_DEFINED = ["solveTimeStep", "iterateTimeStep",
                                     "validateTimeStep", "abortTimeStep"]
    """Methods which must be called only inside TIME_STEP_DEFINED context."""

    ONLY_OUTSIDE_TIME_STEP_DEFINED = [  # "getStationaryMode", FIXME norme says it should be here
        "terminate", "computeTimeStep", "initTimeStep", "setStationaryMode",
        "isStationary", "resetTime", "save", "restore"]
    """Methods which must be called only outside TIME_STEP_DEFINED context."""
