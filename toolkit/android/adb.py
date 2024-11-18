import logging

logger = logging.getLogger(__name__)


class AndroidDevice:
    def __init__(self, serial):
        self.serial = serial

    def shell(self, cmd):
        logger.debug("Running ")

    def __str__(self):
        return f"{self.__class__.__name__}(serial={self.serial}"

    def __repr__(self):
        return str(self)
