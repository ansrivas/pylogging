# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Publish logs to elastic search."""

from pylogging.elogger import ElasticLoggger
import logging
ellog = ElasticLoggger(tag="my_app", elastic_url="http://localhost:3332", auth=('myuser', 'mypassword'))


class Log(object):
    """Logger object."""

    def __init__(self, module_name):
        """Pass the logger NAME i.e. __name__ object here for each module:  `logger = logging.getLogger(__name__)` ."""
        self.logger = logging.getLogger(name=module_name)

    def stringify(self, *args):
        """Handle multiple arguments and return them as a string format."""
        return(",".join(str(x) for x in args))

    def debug(self, *args):
        """Debug logs."""
        msg = self.stringify(args)
        self.logger.debug(msg)
        ellog.debug(msg)

    def error(self, *args):
        """Error logs."""
        msg = self.stringify(args)
        self.logger.error(msg)
        ellog.error(msg)

    def exception(self, *args):
        """Exception logs."""
        msg = self.stringify(args)
        self.logger.exception(msg)
        ellog.exception(msg)

    def info(self, *args):
        """Info logs."""
        msg = self.stringify(args)
        self.logger.info(msg)
        ellog.info(msg)
