# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple example to use with this module."""


import logging

from pylogging import HandlerType, setup_logger

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    setup_logger(log_directory='./logs', file_handler_type=HandlerType.ROTATING_FILE_HANDLER,
                 allow_console_logging=True, file_log_level=logging.INFO)

    logger.error("Error logs")
    logger.debug("Debug logs")
    logger.info("Info logs")
