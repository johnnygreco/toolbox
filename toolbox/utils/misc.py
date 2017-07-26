import os
import numpy as np

__all__ = ['project_dir', 'isiterable', 'vectorize_if_needed']

project_dir = os.path.dirname(os.path.dirname(__file__))


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
