"""This test implement the minimal API."""
# Test files are expected to start with 'test_' prefix

# You can import pytest and use its features.
# import pytest

import pytest

import icoco


def test_exception():
    """Tests exception sub package"""

    with pytest.raises(expected_exception=icoco.WrongContext) as error:
        raise icoco.exception.WrongContext(prob="WrongContextPb",
                                           method="test_exception",
                                           precondition="after toto")
    assert ("WrongContext in Problem instance with name: 'WrongContextPb'"
            " in method 'test_exception' : after toto") in str(error.value)

    with pytest.raises(expected_exception=icoco.WrongArgument) as error:
        raise icoco.exception.WrongArgument(prob="WrongArgumentPb",
                                            method="test_exception",
                                            arg="arg_name",
                                            condition="0>1")
    assert ("WrongArgument in Problem instance with name: 'WrongArgumentPb'"
            " in method 'test_exception', argument 'arg_name' : 0>1") in str(error.value)

    with pytest.raises(expected_exception=icoco.NotImplementedMethod) as error:
        raise icoco.exception.NotImplementedMethod(prob="NotImplementedMethodPb",
                                                   method="test_exception")
    assert ("NotImplemented in Problem instance with name: 'NotImplementedMethodPb'"
            " in method 'test_exception'") in str(error.value)
