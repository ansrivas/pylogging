# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Docstring for logging module."""

import os
import logging
import logging.handlers

from pylogging.log_levels import LogLevel
from pylogging.formatters import Formatters
from pylogging.handler_types import HandlerType

from future.utils import iteritems
from future.utils import raise_with_traceback as rwt


def __set_log_levels(level_dict):
    """Set the log levels for any log-handler for e.g. level_dict = {'requests':'error'}."""
    if not isinstance(level_dict, dict):
        rwt(TypeError("Expecting dict object with format for e.g. {'requests':'warning'} \n"
                      "Available levels are: {0}".format(LogLevel.levels.keys)))

    for key, val in iteritems(level_dict):
        logging.getLogger(key).setLevel(LogLevel.get_level(val))


def __setup_file_logging(g_logger=None,
                         log_directory='.',
                         file_handler_type=HandlerType.TIME_ROTATING_FILE_HANDLER,
                         backup_count=100,
                         max_file_size_bytes=10000,
                         when_to_rotate='D',
                         log_formatter=Formatters.TextFormatter,
                         file_log_level=logging.DEBUG):
    """Attach logs to be written to disk if its required."""
    generated_files = os.path.join(os.path.abspath(os.path.expanduser(log_directory)))
    if not os.path.exists(generated_files):
        os.makedirs(generated_files)

    all_logs_fname = '{0}/all.log'.format(generated_files)
    info_logs_fname = '{0}/info.log'.format(generated_files)
    error_logs_fname = '{0}/error.log'.format(generated_files)

    def __add_handlers_to_global_logger(file_handler_type, fname, log_level):
        """Add different file handlers to global logger.

        By default three types of files are generated in logs.
        - all.log will contain all the log levels i.e. including DEBUG
        - info.log will contain all the log level above and including INFO
        - error.log will contain all the log level which are above and including ERROR
        """
        # create error file handler and set level to error
        if file_handler_type == HandlerType.ROTATING_FILE_HANDLER:
            handler = logging.handlers.RotatingFileHandler(fname,
                                                           maxBytes=max_file_size_bytes,
                                                           backupCount=backup_count)
        else:
            handler = logging.handlers.TimedRotatingFileHandler(fname,
                                                                when=when_to_rotate,
                                                                backupCount=backup_count)

        handler.setLevel(log_level)
        handler.setFormatter(log_formatter)
        g_logger.addHandler(handler)

    if file_log_level == logging.DEBUG:
        __add_handlers_to_global_logger(file_handler_type, error_logs_fname, logging.ERROR)
        __add_handlers_to_global_logger(file_handler_type, all_logs_fname, logging.DEBUG)
        __add_handlers_to_global_logger(file_handler_type, info_logs_fname, logging.INFO)
    elif file_log_level == logging.INFO:
        __add_handlers_to_global_logger(file_handler_type, error_logs_fname, logging.ERROR)
        __add_handlers_to_global_logger(file_handler_type, info_logs_fname, logging.INFO)
    elif file_log_level == logging.WARNING:
        __add_handlers_to_global_logger(file_handler_type, error_logs_fname, logging.WARNING)
    else:
        __add_handlers_to_global_logger(file_handler_type, error_logs_fname, logging.ERROR)

    print('Logging into directory {}\n'.format(generated_files))


def setup_logger(log_directory='.',
                 file_handler_type=HandlerType.TIME_ROTATING_FILE_HANDLER,
                 allow_console_logging=True,
                 allow_file_logging=True,
                 backup_count=100,
                 max_file_size_bytes=100000,
                 when_to_rotate='D',
                 change_log_level=None,
                 log_formatter=Formatters.TextFormatter,
                 gelf_handler=None,
                 file_log_level=logging.DEBUG,
                 **kwargs):
    """Set up the global logging settings.

    Args:
        log_directory (str)            :directory to write log files to. Applicable only when
            `allow_file_logging` = True
        file_handler_type              :object of logging handler from HandlerType class. Applicable only when
            `allow_file_logging` = True
        allow_console_logging (bool)   :Turn off/on the console logging.
        allow_file_logging (bool)      :Turn off/on if logs need to go in files as well.
        backup_count (int)             :Number of files to backup before rotating the logs.
        max_file_size_bytes (int)      :Size of file in bytes before rotating the file. Applicable only to
            ROTATING_FILE_HANDLER.
        when_to_rotate (str)           :Duration after which a file can be rotated. Applicable only to
            TIME_ROTATING_FILE_HANDLER
                                        Accepts following values:
                                        'S'	Seconds
                                        'M'	Minutes
                                        'H'	Hours
                                        'D'	Days
                                        'W0'-'W6'	Weekday (0=Monday)
                                        'midnight'	Roll over at midnight
        change_log_level (dict)        :A dictionary of handlers with corresponding log-level
            ( for eg. {'requests':'warning'} )
        console_log_level (logging)    :Change the LogLevel of console log handler, default is logging.INFO
            (e.g. logging.DEBUG, logging.INFO)
        file_log_level (logging)       :Change the LogLevel of file log handler, default is logging.DEBUG
            (e.g. logging.DEBUG, logging.INFO)
        gelf_handler                   :An external handler for graylog data publishing.
    """
    file_handlers = [HandlerType.ROTATING_FILE_HANDLER, HandlerType.TIME_ROTATING_FILE_HANDLER]
    if file_handler_type not in file_handlers:
        rwt(ValueError('Please pass an object of HandlerType class'))

    if change_log_level:
        __set_log_levels(change_log_level)

    logger = logging.getLogger()
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    if gelf_handler:
        logger.addHandler(gelf_handler)

    # create console handler and set level to info
    if allow_console_logging:
        handler = logging.StreamHandler()
        log_level = kwargs.get("console_log_level", logging.INFO)
        handler.setLevel(log_level)
        handler.setFormatter(log_formatter)
        logger.addHandler(handler)

    if allow_file_logging:
        __setup_file_logging(g_logger=logger,
                             log_directory=log_directory,
                             file_handler_type=file_handler_type,
                             backup_count=backup_count,
                             max_file_size_bytes=max_file_size_bytes,
                             when_to_rotate=when_to_rotate,
                             file_log_level=file_log_level)
