# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple example to use with Gelf logging module."""


import logging

from graypy import GELFUDPHandler

from pylogging import HandlerType, setup_logger

logger = logging.getLogger(__name__)

# If want to add extra fields.
# logger = logging.LoggerAdapter(logger, {"app_name": "test-service"})
if __name__ == '__main__':
    gelf_handler = GELFUDPHandler(host="elk.recogizer.net",
                                  port=12201,
                                  level_names=True,
                                  debugging_fields=False)

    setup_logger(log_directory='./logs',
                 file_handler_type=HandlerType.TIME_ROTATING_FILE_HANDLER,
                 allow_console_logging=True,
                 allow_file_logging=True,
                 backup_count=100,
                 max_file_size_bytes=100000,
                 when_to_rotate='D',
                 change_log_level=None,
                 gelf_handler=gelf_handler,
                 log_tags={"app_name": "Test-App"},)

    logger.error("Error logs")
    logger.debug("Debug logs")
    logger.info("Info logs")
