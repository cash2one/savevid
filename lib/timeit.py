import logging
import time

logger = logging.getLogger(__name__)

def timeit(f):
    fname = f.__name__
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        duration = end - start
        logger.debug("%s takes %f" % (fname, duration))
        return result
    return wrapper
