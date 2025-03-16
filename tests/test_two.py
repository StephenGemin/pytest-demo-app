import logging

import pytest

from toolkit.generic_api import pytest_api


class TestClass:
    @pytest.mark.tags("smoke")
    def test_pass(self, request, android_device):
        logging.debug("running %s", request.node.name)
        logging.info("android_device=%s", android_device)
        assert pytest_api.test_name(request)

    @pytest.mark.xfail(reason="failing test")
    def test_assert_failure1(self):
        var = "foo"
        assert var == "bar"

    @pytest.mark.xfail(reason="failing test")
    def test_assert_failure2(self):
        actual = [1, 2]
        expected = [2, 1]
        for v1, v2 in zip(actual, expected):
            assert v1 == v2
