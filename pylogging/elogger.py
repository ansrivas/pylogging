# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Small wrapper which sends an asynchronous post request to a given http port."""

import json
import logging
from functools import partial

from requests import ConnectionError
from requests_futures.sessions import FuturesSession

logger = logging.getLogger(__name__)


class ElasticLoggger(object):
    """Post your log messages to ELK cluster with logstash-http-input.

    Ideally in a package this should be setup in a module like utils, which is shared
    across the application. Just create the object of this class and keep reusing it.
    """

    def __init__(self, tag, elastic_url, headers=None, auth=None):
        """Initialize the ElasticLoggger class.

        Args:
            tag           :Unique identifiable tag for the application which is using current logger
            elastic_url   :Url of elastic-http-input to push logs to (for eg. 'http://localhost:3332' )
            headers       :Since this is post request headers are required, defaults to {'content-type': 'application/json'}
            auth          :A tuple containing username and password: for eg.  ('myuser', 'mypassword')
        """
        self.elastic_url = elastic_url
        self.auth = auth
        self.headers = headers
        if not self.headers:
            self.headers = {'content-type': 'application/json'}

        self.debug_method = partial(self.__log, level='debug')
        self.error_method = partial(self.__log, level='error')
        self.info_method = partial(self.__log, level='info')
        self.exception_method = partial(self.__log, level='exception')
        self.session = FuturesSession(max_workers=10)
        self.tag = tag

    def set_application_name(self, tag):
        """Rename the application `explicitly` for which logs are being generated."""
        self.tag = tag

    def __log(self, msg, level):
        payload = {'tag': str(self.tag), 'log_level': level, 'message': msg}
        try:
            self.session.post(url=self.elastic_url,
                              data=json.dumps(payload),
                              headers=self.headers,
                              auth=self.auth)
        except ConnectionError as ce:
            logging.error(ce.message)
            logging.exception('Unable to connect to Elastic Search. Check the `elastic_url` and `auth`')
            logging.error(msg)

    def info(self,  msg):
        """Info function to send data with loglevel info."""
        self.info_method(msg)

    def debug(self,  msg):
        """Debug function to send data with loglevel debug."""
        self.debug_method(msg)

    def error(self,  msg):
        """Error function to send data with loglevel error."""
        self.error_method(msg)

    def exception(self,  msg):
        """Exception function to send data with loglevel error."""
        self.exception_method(msg)
