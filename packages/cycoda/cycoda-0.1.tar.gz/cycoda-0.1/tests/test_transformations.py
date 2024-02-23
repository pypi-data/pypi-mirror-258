import numpy as np
import sys
from scipy.stats import gmean
from cycoda.transformations import alr, clr, rclr

def composition_1d():
    return np.array([1, 2, 3])

def composition_2d():
    return np.array([[1, 2, 3], [4, 5, 6]])

def test_alr_1d(): 
    matrix = composition_1d()
    expected = np.log(np.array([[1/3, 2/3]]))
    actual = alr(matrix)
    assert np.all(expected == actual), f"ALR transformation failed: expected {expected}, but got {actual}"

def test_alr_2d():
    matrix = composition_2d()
    expected = np.log(np.array([[1/3, 2/3], [4/6, 5/6]]))
    actual = alr(matrix)
    assert np.all(expected == actual), f"ALR transformation failed: expected {expected}, but got {actual}"

def test_clr_1d():
    matrix = composition_1d()
    expected = np.array([-0.59725316, 0.09589402,  0.50135913])
    actual = clr(matrix)
    assert np.all(expected.round(3) == actual.round(3)), f"CLR transformation failed: expected {expected}, but got {actual}"

def test_clr_2d():
    matrix = composition_2d()
    expected = np.array([[-0.59725316, 0.09589402,  0.50135913], [-0.209536,    0.013607,    0.195929  ]])
    actual = clr(matrix)
    assert np.all(expected.round(3) == actual.round(3)), f"CLR transformation failed: expected {expected.reshape(-1)}, but got {actual.reshape(-1)}"
