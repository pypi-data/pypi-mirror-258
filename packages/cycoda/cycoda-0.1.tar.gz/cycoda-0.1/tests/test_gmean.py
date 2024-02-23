import numpy as np
import sys
from scipy.stats import gmean as scipy_gmean
from cycoda.gmean import gmean as cycoda_gmean

def composition_1d():
    return np.array([1, 2, 3])

def composition_2d():
    return np.array([[1, 2, 3], [4, 5, 6]])

def test_gmean_1d():
    matrix = composition_1d()
    expected = scipy_gmean(matrix)
    actual = cycoda_gmean(matrix)
    assert expected == actual, f"gmean in cycoda failed: expected {expected}, but got {actual}"

def test_gmean_2d():
    matrix = composition_2d()
    expected = scipy_gmean(matrix, axis=1)
    actual = cycoda_gmean(matrix, axis=1)
    assert (expected==actual).all(), f"gmean in cycoda failed: expected {expected}, but got {actual}"

