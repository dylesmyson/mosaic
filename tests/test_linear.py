import unittest
from math import prod

from lib import to_matrix, operations

""" Starting with the most common use cases first. """

class TestToMatrix(unittest.TestCase):
    def test_raise_element_length_error(self):
        dim = (2,2)
        vector = range(prod(dim)+1)
        with self.assertRaises(RuntimeError):
            to_matrix(dim, vector)

    def test_empty_matrix(self):
        dim, empty_vector = (0,0), []
        self.assertEqual(to_matrix(dim, empty_vector), [])

    def test_singular_matrix(self):
        dim, singular_vector = (1,1), [0]
        self.assertEqual(to_matrix(dim, singular_vector), [[0]])

    def test_2_by_2_matrix(self):
        dim, vector = (2,2), [ 0, 1, 2, 3 ]
        self.assertEqual(to_matrix(dim, vector), [ [0,1], [2, 3] ])

    def test_2_by_3_matrix(self):
        dim, vector = (2,3), [ 0, 1, 2, 3, 4, 5 ]
        self.assertEqual(to_matrix(dim, vector), [ [0,1], [2,3], [4,5] ])

    def test_3_by_2_matrix(self):
        dim, vector = (3,2), [ 0, 1, 2, 3, 4, 5 ]
        self.assertEqual(to_matrix(dim, vector), [ [0,1,2], [3,4,5] ])

class TestOperations(unittest.TestCase):

    def setUp(self):
        self.ops = operations()

    def __n_by_m_matrix(self, n, m):
        return to_matrix((n,m), list(range(n*m)))

    def __test_n_by_m_operation(self, n, m, symbol, resultant):
        n_by_m = self.__n_by_m_matrix(n,m)
        self.assertEqual(resultant, self.ops[symbol](n_by_m))

    def test_rotate_2_by_2_matrix(self):
        resultant = [ [1,3], [0,2] ]
        # Apply a rotation to the 2x2 matrix.
        self.__test_n_by_m_operation(2,2,'@',resultant)

    def test_rotate_3_by_3_matrix(self):
        resultant = [ [2,5,8], [1,4,7], [0,3,6] ]
        self.__test_n_by_m_operation(3,3,'@',resultant)

    def test_permute_2_by_2_matrix(self):
        resultant = [ [1,0], [2,3] ]
        # Apply a permutation to the 2x2 matrix.
        self.__test_n_by_m_operation(2,2,'~',resultant)

    def test_permute_3_by_3_matrix(self):
        resultant = [ [1,2,0], [3,4,5], [6,7,8] ]
        self.__test_n_by_m_operation(3,3,'~', resultant)


if __name__ == '__main__':
    unittest.main()