# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module to manage different log levels based on different strings."""

import logging

from future.utils import raise_with_traceback as rwt


class LogLevel(object):
    """Manage loglevels based on different strings."""

    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    @staticmethod
    def get_level(level):
        """Get log level from a string."""
        if level.upper() not in LogLevel.levels.keys():
            rwt(AttributeError('Log level not found: {0}'.format(level.upper())))
        return LogLevel.levels[level.upper()]
