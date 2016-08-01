import numpy as np

__all__ = ['isiterable', 'vectorize_if_needed']

def isiterable(obj):
    """
    Returns `True` if the given object is iterable.

    Taken from astropy/utils/misc.py
    """
    try:
        iter(obj)
        return True
    except TypeError:
        return False

def vectorize_if_needed(func, *x):
    """ 
    Helper function to vectorize functions on array inputs

    Taken from astropy/cosmology/core.py
    """
    if any(map(isiterable, x)):
        return np.vectorize(func)(*x)
    else:
        return func(*x)
