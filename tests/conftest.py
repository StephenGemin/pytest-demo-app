import logging
import random

import pytest

from toolkit.android.adb import AndroidDevice

pytest_plugins = ["pytest_hooks"]


@pytest.fixture
def android_device():
    return AndroidDevice(random.randint(0, 100))


@pytest.fixture
def setup(session_setup, module_setup, setup2):
    logging.debug("Running some test setup")
    yield
    logging.debug("Running some test teardown")


@pytest.fixture
def setup2():
    logging.debug("Running some more test setup")


@pytest.fixture(scope="module")
def module_setup():
    logging.debug("Running some module scoped setup")
    yield
    logging.debug("Running some module scoped cleanup ")


@pytest.fixture(scope="session")
def session_setup():
    logging.debug("Running some session scoped setup")
    yield
    logging.debug("Running some session scoped cleanup ")


@pytest.fixture
def fixture_error():
    raise RuntimeError("some fixture error")
