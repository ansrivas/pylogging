# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Initialize module utils."""

from send_to_elastic_search import Log
from pylogging import HandlerType, setup_logger

logger = Log(__name__)

if __name__ == '__main__':
    setup_logger(log_directory='./logs', file_handler_type=HandlerType.TIME_ROTATING_FILE_HANDLER, allow_console_logging=True,
                 backup_count=100, max_file_size_bytes=10000, when_to_rotate='D', change_log_level=None, allow_file_logging=False)

    logger.debug("hello debug", "this is my message")
    logger.error("hello error", "this doesn't look to be mine")
    logger.info("hello info", 1, 2, 3)
    logger.exception("hello exception", {"efficiency": 20})
