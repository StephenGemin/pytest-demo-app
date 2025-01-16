import logging
import os
import uuid
from pathlib import Path

import pytest

logger = logging.getLogger()


def pytest_addoption(parser):
    parser.addoption(
        "--log-file-root",
        action="store",
        default=".logs",
        help="Specify the directory where session logs are stored relative to rootpath",
    )
    parser.addoption(
        "--no-collect-skip",
        action="store_true",
        help="Remove skipped tests from collection",
    )


def create_log_directories(config):
    log_root = config.rootpath / config.option.log_file_root
    log_root.mkdir(parents=True, exist_ok=True)

    session_id = str(uuid.uuid4())
    config.option.session_id = session_id
    session_path = log_root / session_id
    session_path.mkdir(exist_ok=False)
    config.option.session_log_dir = session_path
    return session_path


def is_log_cli_enabled(config):
    return config.getoption("log_cli", None) or config.getini("log_cli")


def set_log_level(config, option):
    """Default to cmd input, then config then cmd log_level, then ini log_level"""
    log_level = (
        config.getini(option)  # Check pytest.ini or pyproject.toml
        or config.getoption("log_level")  # Fallback to another CLI option
        or config.getini("log_level")  # Fallback to another INI option
        or "WARNING"  # Default to WARNING
    )
    setattr(config.option, option, log_level)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # There appears to be separation of cmd line options vs ini options
    # It would be nice if these eventually combined into one config, but I couldn't find documentation supporting this desire
    # So, forgive the below niave approach
    if is_log_cli_enabled(config):
        if not config.getoption("log_format", None):
            config.option.log_format = config.getini("log_format")
        set_log_level(config, "log_cli_level")
        # have root logger share same level as console level
        # able to have minimal console output, with full log file output
        logger.setLevel(config.option.log_cli_level)
        set_log_level(config, "log_file_level")
        if not config.getoption("log_date_format"):
            config.option.log_date_format = config.getini("log_date_format")
        session_path = create_log_directories(config)
        config.option.htmlpath = session_path / "report.html"
        config.option.self_contained_html = True

    config.option.test_index1 = 0
    config.option.test_log_dir = None


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(items):
    def is_skipped(item):
        return any(m for m in item.own_markers if m.name == "skip")

    try:
        config = items[0].config
    except IndexError:
        pass
    else:
        if config.getoption("no_collect_skip"):
            items[:] = [item for item in items if not is_skipped(item)]


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    if not is_log_cli_enabled(session.config):
        return
    file_handler = logging.FileHandler(
        session.config.getoption("session_log_dir") / "session.log", mode="w"
    )
    file_handler.setLevel(session.config.option.log_file_level)
    file_handler.setFormatter(_create_log_formatter(session.config))
    logger.addHandler(file_handler)
    logger.info("Session started")


def _create_log_formatter(config):
    return logging.Formatter(
        fmt=config.option.log_format, datefmt=config.option.log_date_format
    )


def _increment_test_index(config):
    config.option.test_index1 += 1


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_protocol(item, nextitem):
    config = item.config
    _increment_test_index(config)
    if is_log_cli_enabled(config):
        test_log_dir = (
            Path(config.option.session_log_dir)
            / f"{config.option.test_index1:04d}_{item.name}"
        )
        os.makedirs(test_log_dir)
        config.test_log_dir = str(test_log_dir)
        assert os.path.exists(str(test_log_dir))

        file_handler = logging.FileHandler(test_log_dir / "debug.log", mode="w")
        file_handler.setLevel(config.option.log_file_level)
        file_handler.setFormatter(_create_log_formatter(config))
        logger.addHandler(file_handler)

    try:
        return (yield)
    finally:
        if is_log_cli_enabled(config):
            logger.debug("Remove test log handler")
            logger.removeHandler(file_handler)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logstart(nodeid, location):
    logger.debug("Start test %s", nodeid)


@pytest.hookimpl(trylast=True)
def pytest_runtest_logfinish(nodeid, location):
    logger.debug("End of test %s", nodeid)


@pytest.hookimpl(trylast=True)
def pytest_runtest_logreport(report):
    # TODO: this stacktrace syntax woulbe be better if it was more consistent with Python's standard format
    if report.failed:
        logger.debug(f"Test {report.nodeid} failed during {report.when} phase")
        if report.longrepr:
            logger.debug(f"Stacktrace:\n{report.longrepr}\n")


def pytest_html_report_title(report):
    report.title = "Pytest-Demo-App"


# def pytest_report_teststatus(report, config):
#     if report.when == "teardown":
#         logger.info("in teardown")
#     print(f"report_teststatus {report.when} {id(report)}")
#     xfail = ""
#     if report.when == "call":
#         xfail = getattr(report, "wasxfail", "")
#
#
# def pytest_runtest_makereport(item):
#     outcome = yield
#     report = outcome.get_result()
#     if report.when == "call":
#         report.user_properties.append(("xfailreason", getattr(report, "wasxfail", None)))
#     print(f"runtest_makereport {report.when} {id(report)}")
