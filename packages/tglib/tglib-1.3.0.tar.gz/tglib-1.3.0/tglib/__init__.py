#!/bin/env python3

__version__ = '1.3.0'
VERSION = __version__

__all__ = (
    '__version__',
    'VERSION',
    'Client',
    'NextFunction',
    'TelegramError',
)

from .client import (
    Client,
    NextFunction,
    TelegramError
)
