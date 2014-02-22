import threading
from functools import wraps

"""
Created on 21.02.2014

@author: Carbon
"""
def synchronized(fn):
    """
    A method with this decorator will be synchronized as
    a java function declaring synchronized. 
    """
    lock = threading.Lock()
    @wraps(fn)
    def wrapper(*args, **wargs):
        with lock:
            fn(*args, **wargs)
    return wrapper

def semaphore(maxNbr=1, bounded=False):
    """
    A method with this decorator can only be accessed maxNbr times
    parallel 
    """
    semaphore = None
    if bounded:
        semaphore = threading.BoundedSemaphore(maxNbr)
    else:
        semaphore = threading.Semaphore(maxNbr)
        
    def semaphoreWrapper(fn):
        @wraps(fn)
        def wrapper(*args, **wargs):
            with semaphore:
                fn(*args, **wargs)
        return wrapper
    return semaphoreWrapper