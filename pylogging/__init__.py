# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Initialize module utils."""
__all__ = ['setup_logger', 'HandlerType', 'Formatters']
from ._create_logger import setup_logger
from .handler_types import HandlerType
from .formatters import Formatters

__version__ = '0.2.5'
