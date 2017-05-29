# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bunch of log formatters to be used."""

import logging


class TextFormatter(logging.Formatter):
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


class JsonFormatter(logging.Formatter):
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


class Formatters(object):
    """Define a common class for Formatters."""

    TextFormatter = TextFormatter()
    JsonFormatter = JsonFormatter()
