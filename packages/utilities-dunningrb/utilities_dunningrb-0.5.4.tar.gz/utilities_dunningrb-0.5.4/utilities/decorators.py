"""This module defines decorators.
"""
import logging
import time
from datetime import datetime
from utilities import dictutils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def timing(verbose=False):
    """For a decorated method, write two log statements recording (a) when the method was called
    and optionally its input arguments (if verbose==True), and (b) when the method finished and
    the total duration in seconds.

    Usage:

        @timing()
        def decorated_method():
            [do things...]

        @timing(verbose=True)
        def decorated_method(a, b, c=None):
            [do things...]

    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            name = f"Function {func.__name__}"
            started_at = f"started at {datetime.now()}"

            if verbose:
                started_at += f"\n\t{name} input arguments:\n\t\t\t{dictutils.get_string(locals())}"
            logger.info(f"{name} {started_at}.")

            clock_start = time.time()
            result = func(*args, **kwargs)
            clock_end = time.time()

            finished_at = f"ended at {datetime.now()}"
            with_duration = f"with duration {(clock_end - clock_start):.3f} seconds"
            logger.info(f"{name} {finished_at} {with_duration}.")

            return result

        return wrapper

    return decorator
