import logging

import pytest

from toolkit.generic_api import pytest_api


def test_pass(request, android_device, setup):
    logging.debug("running %s", request.node.name)
    logging.info("android_device=%s", android_device)


class TestMe:
    @pytest.mark.xfail(reason="failing test")
    def test_xfail(self):
        raise AssertionError()

    @pytest.mark.xfail(reason="failing test")
    @pytest.mark.tags("smoke")
    def test_error_in_test_call(self, setup):
        pytest_api.raise_error()


@pytest.mark.xfail(reason="failing test")
def test_error_chain_in_test_call(setup):
    pytest_api.raise_error_chain()


@pytest.mark.xfail(reason="failing test")
def test_fixture_failure(fixture_error):
    pass


@pytest.mark.skip(reason="skipped")
def test_skip_test():
    assert 0
