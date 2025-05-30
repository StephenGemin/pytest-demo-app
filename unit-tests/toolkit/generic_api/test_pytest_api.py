import pytest

from toolkit.generic_api import pytest_api as mut  # module under test


def test_test_name(request):
    assert isinstance(mut.test_name(request), str)


def test_raise_error():
    with pytest.raises(RuntimeError):
        mut.raise_error()


def test_raise_error_chain():
    with pytest.raises(FileExistsError):
        mut.raise_error_chain()
