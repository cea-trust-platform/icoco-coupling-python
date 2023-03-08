"""This test implement the minimal API."""
# Test files are expected to start with 'test_' prefix

# You can import pytest and use its features.
# import pytest

import pytest

import icoco

def test_exception():
    """Tests exception sub package"""

    with pytest.raises(expected_exception=icoco.WrongContext):
        raise icoco.exception.WrongContext(prob="WrongContextPb",
                                           method="test_exception",
                                           precondition="")

    with pytest.raises(expected_exception=icoco.WrongArgument):
        raise icoco.exception.WrongArgument(prob="WrongArgumentPb",
                                            method="test_exception",
                                            arg="arg_name",
                                            condition="0>1")

    with pytest.raises(expected_exception=icoco.NotImplementedMethod):
        raise icoco.exception.NotImplementedMethod(prob="NotImplementedMethodPb",
                                           method="test_exception")
