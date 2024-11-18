import logging

logger = logging.getLogger(__name__)


def test_name(request):
    name = request.node.name
    logger.debug("test name is %s", name)
    return name


def raise_error():
    raise RuntimeError("some error")


def raise_error_chain():
    try:
        raise_error()
    except RuntimeError as e:
        raise FileExistsError("force error chain") from e
