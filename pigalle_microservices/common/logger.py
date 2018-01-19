import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

def get_logger(name):
    return logger.getChild(name)
