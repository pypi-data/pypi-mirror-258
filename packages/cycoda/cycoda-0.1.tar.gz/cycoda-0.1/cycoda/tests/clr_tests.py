import unittest
import sys
import numpy as np
import cupy as cp

sys.path.append('../')
from cycoda.clr import gmean, clr

class gmeanTests(unittest.TestCase):
    def testOutput_1(self):
        eo = np.array([4])
        o = clr(cp.array([2, 8])).get()

        self.assertEqual(o, eo)
    
    def testOutput_2(self):
        eo = np.array([0.5])
        o = clr(cp.array([4, 1, 1/32])).get()

        self.assertEqual(o, eo)
        self.assertTr

class clrTests(unittest.TestCase):
    def testOutput(self):
        eo = np.array([-0.59725316,  0.09589402,  0.50135913])
        o = clr(cp.array([1, 2, 3]))

        self.assertEqual(o, eo)

if __name__ == '__main__':
    unittest.main()