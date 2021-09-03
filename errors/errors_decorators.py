#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTTP Errors

List of HTTP errors which can be fixed in most cases by trying again
Provides a `@retry` decorator which applies exponential backoff to a function
"""

import math
import time
import random
import logging
import functools

from googleapiclient.errors import HttpError

###############################################################################

logger = logging.getLogger(__name__)

###############################################################################
# https://developers.google.com/drive/api/v3/handle-errors

RETRY_ERRORS = {
    # 400: ["Bad request", "Invalid sharing request"],
    # 401: ["Invalid credentials"],
    403: ["Usage limit exceeded", "Daily limit exceeded",
          "Number of items in folder", "User rate limit exceeded",
          "Rate limit exceeded", "Sharing rate limit exceeded",
          "The user has not granted the app access to the file",
          "The user does not have sufficient permissions for the file",
          "App cannot be used within the authenticated user's domain"],
    404: ["File not found"],
    429: ["Too many requests"],
    500: ["Backend error"],
    502: ["Bad Gateway"],
    503: ["Service Unavailable"],
    504: ["Gateway Timeout"]
}


###############################################################################


def retry(attempts: int = 4, delay: int = 1, backoff: int = 2, hook=None):
    """
    Decorator to Retry with Exponential Backoff (on Exception)

    A function that raises an exception on failure, when decorated with this
    decorator, will retry till it returns True or number of attempts runs out.

    @params:
        delay: initial delay in seconds
        backoff: backoff multiplication factor
        hook: function with the signature
              hook(tries_remaining, exception, delay)
              (default: None)

    The decorator will call the function up to 'attempts' times if it raises
    an exception.

    By default it catches instances of the Exception class and subclasses.
    This will recover after all but the most fatal errors. You may specify a
    custom tuple of exception classes with the 'exceptions' argument; the
    function will only be retried if it raises one of the specified
    exceptions.

    Additionally you may specify a hook function which will be called prior
    to retrying with the number of remaining tries and the exception instance;
    This is primarily intended to give the opportunity to log the failure.
    Hook is not called after failure if no retries remain.
    """
    if backoff <= 1:
        raise ValueError("Backoff must be greater than 1")
    attempts_int: int = math.floor(int(attempts))
    if attempts_int < 0:
        raise ValueError("Attempts must be 0 or greater")
    if delay <= 0:
        raise ValueError("Delay must be greater than 0")

    async def decorator(func):
        # ------------------------------------------------------------------- #
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            _delay = delay
            for tries_remaining in range(attempts_int, -1, -1):
                try:
                    return func(*args, **kwargs)
                except HttpError as error:
                    if not error.resp.status in RETRY_ERRORS:
                        logger.error(f"{error.resp.status}: {error.resp.reason}")
                        raise
                    if tries_remaining < 0:
                        logger.error("Failed number of attempts exceeded.")
                        break
                    if hook is not None:
                        hook(tries_remaining, error, _delay)
                    logger.warning(f"{error.resp.status}: {error.resp.reason}")
                    logger.info(f"Retrying in {_delay} seconds ..")
                    time.sleep(_delay + random.random())
                    _delay *= backoff
                else:
                    break
        # ------------------------------------------------------------------- #
        return wrapper

    return decorator

###############################################################################
