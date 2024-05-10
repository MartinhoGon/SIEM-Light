import logging
from django.conf import settings

def get_logger():
    logger = logging.getLogger(settings.CUSTOM_LOGGER_NAME)
    return logger