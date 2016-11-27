# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Docstring for logging module."""

import logging
import logging.handlers
import os

from future.utils import raise_with_traceback as rwt
from future.utils import iteritems

from pylogging.handler_types import HandlerType
from pylogging.log_levels import LogLevel


class LogFormatter(logging.Formatter):
    """Format the meta data in the log message to fix string length."""

    datefmt = '%Y-%m-%d %H:%M:%S'

    def format(self, record):
        """Default formatter."""
        error_location = "%s.%s" % (record.name, record.funcName)
        line_number = "%s" % (record.lineno)
        location_line = error_location[:32] + ":" + line_number
        s = "%.19s [%-8s] [%-36s] %s" % (self.formatTime(record, self.datefmt),
                                         record.levelname,  location_line, record.getMessage())
        return s


def __set_log_levels(level_dict):
    """Set the log levels for any log-handler for e.g. level_dict = {'requests':'error'}."""
    if not isinstance(level_dict, dict):
        rwt(TypeError('Expecting dict object with format:  \{\'requests\':\'warning\'\} \n' +
                      'Available levels are: {0}'.format(LogLevel.levels.keys)))
    else:
        for key, val in iteritems(level_dict):
            logging.getLogger(key).setLevel(LogLevel.get_level(val))


def __setup_file_logging(g_logger=None,
                         log_directory='.',
                         file_handler_type=HandlerType.TIME_ROTATING_FILE_HANDLER,
                         backup_count=100,
                         max_file_size_bytes=10000,
                         when_to_rotate='D'):
    """Attach logs to be written to disk if its required."""
    generated_files = os.path.join(os.path.abspath(os.path.expanduser(log_directory)))
    if not os.path.exists(generated_files):
        os.makedirs(generated_files)
    all_logs_fname = '{0}/all.log'.format(generated_files)
    error_logs_fname = '{0}/error.log'.format(generated_files)

    # create error file handler and set level to error
    if file_handler_type == HandlerType.ROTATING_FILE_HANDLER:
        handler = logging.handlers.RotatingFileHandler(error_logs_fname,
                                                       maxBytes=max_file_size_bytes,
                                                       backupCount=backup_count)
    else:
        handler = logging.handlers.TimedRotatingFileHandler(error_logs_fname,
                                                            when=when_to_rotate,
                                                            backupCount=backup_count)

    handler.setLevel(logging.ERROR)
    handler.setFormatter(LogFormatter())
    g_logger.addHandler(handler)

    # create debug file handler and set level to debug
    if file_handler_type == HandlerType.ROTATING_FILE_HANDLER:
        handler = logging.handlers.RotatingFileHandler(all_logs_fname,
                                                       maxBytes=max_file_size_bytes,
                                                       backupCount=backup_count)
    else:
        handler = logging.handlers.TimedRotatingFileHandler(all_logs_fname,
                                                            when=when_to_rotate,
                                                            backupCount=backup_count)

    handler.setLevel(logging.DEBUG)
    handler.setFormatter(LogFormatter())
    g_logger.addHandler(handler)

    print('Logging into directory {}\n'.format(generated_files))


def setup_logger(log_directory='.',
                 file_handler_type=HandlerType.TIME_ROTATING_FILE_HANDLER,
                 allow_console_logging=True,
                 allow_file_logging=True,
                 backup_count=100,
                 max_file_size_bytes=100000,
                 when_to_rotate='D',
                 change_log_level=None):
    """Set up the global logging settings.

    Args:
        log_directory:str          directory to write log files to. Applicable only when `allow_file_logging` = True
        file_handler_type:         object of logging handler from HandlerType class. Applicable only when `allow_file_logging` = True
        allow_console_logging:bool Turn off/on the console logging.
        allow_file_logging:bool    Turn off/on if logs need to go in files as well.
        backup_count:int           Number of files to backup before rotating the logs.
        max_file_size_bytes:int    Size of file in bytes before rotating the file. Applicable only to ROTATING_FILE_HANDLER.
        when_to_rotate:str         Duration after which a file can be rotated. Applicable only to TIME_ROTATING_FILE_HANDLER
                                   Accepts following values:
                                    'S'	Seconds
                                    'M'	Minutes
                                    'H'	Hours
                                    'D'	Days
                                    'W0'-'W6'	Weekday (0=Monday)
                                    'midnight'	Roll over at midnight
        change_log_level:dict      A dictionary of handlers with corresponding log-level ( for eg. {'requests':'warning'} )
    """
    if file_handler_type not in [HandlerType.ROTATING_FILE_HANDLER,
                                 HandlerType.TIME_ROTATING_FILE_HANDLER]:
        rwt(ValueError('Please pass an object of HandlerType class'))

    if change_log_level:
        __set_log_levels(change_log_level)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to info
    if allow_console_logging:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(LogFormatter())
        logger.addHandler(handler)

    if allow_file_logging:
        __setup_file_logging(g_logger=logger,
                             log_directory=log_directory,
                             file_handler_type=file_handler_type,
                             backup_count=backup_count,
                             max_file_size_bytes=max_file_size_bytes,
                             when_to_rotate=when_to_rotate)
