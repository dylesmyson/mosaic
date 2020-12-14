from math import prod
from functools import reduce
from typing import Callable, Any

from lib.definitions import Dimensions, Vector, Matrix, Operations, Values



def __element_lengths_equal(vector: Vector, dimensions: Dimensions) -> bool:
    return prod(dimensions) == len(vector)

def __dimensions(matrix: Matrix) -> Dimensions:
    return len(matrix[0]), len(matrix)

def __matmul(left: Matrix, right: Matrix) -> Matrix:
    return [[sum(i*j for i,j in zip(acol,bcol)) for bcol in zip(*right)] for acol in left]

def __transpose(matrix: Matrix) -> Matrix:
    return list(map(list, zip(*matrix)))

def __to_vector(matrix: Matrix) -> Vector:

    """ Converts matrix into a row vector.

    For example, this will convert a 2x2 Matrix into a 4x1 Vector.

    >>> to_vector([[1,2], [3,4]])
    [1, 2, 3, 4]
    """

    return [value for vector in matrix for value in vector]

def __create_rotation_matrix(dimensions: Dimensions) -> Matrix:
    rotation_matrix = to_matrix(dimensions, prod(dimensions)*[0])
    for i, vector in enumerate(rotation_matrix, 1):
        vector[len(vector)-i] = 1
    return rotation_matrix

def __create_permutation_matrix(dimensions: Dimensions) -> Matrix:

    """ Generate a "special" permutation matrix.

    The matrix is a rotation matrix where the last row becomes the first
    row, pushing all the others further down. This creates a permutation
    through a single row that resembles permutation of a rubik's cube slice.

    >>> create_permutation_matrix((3,3))
    [[0,0,1],[1,0,0],[0,1,0]]
    """

    permutation_matrix = []
    rotation = __create_rotation_matrix(dimensions)

    for vector in rotation[1:]:
        permutation_matrix.append(vector)

    permutation_matrix.reverse()
    permutation_matrix.insert(0, rotation[0])

    return permutation_matrix

def __apply_rotation(matrix: Matrix) -> Matrix:
    rotation = __create_rotation_matrix(__dimensions(matrix))
    return __transpose(__matmul(matrix, rotation))

def __apply_row_permutation(matrix: Matrix, row: int = 0) -> Matrix:
    resultant    = matrix.copy()
    permutation  = __create_permutation_matrix(__dimensions(matrix))
    inverted     = __matmul(matrix, permutation)
    resultant[row] = inverted[row]
    return resultant


# API - Higher Order Functions/Secondary Objects
def to_matrix(dimensions: Dimensions, vector: Vector) -> Matrix:

    """ Converts a vector and a tuple of dimensions into matrix.

    For example, this can convert a (row) vector of size 4 into any matrix
    with dimensions that are a partition of 4, which is 2x2 or 4x1 (or 1x4).
    By convention, the incoming vector is a row vector, or in another words,
    dimensions x >= y.
    >>> to_matrix([1,2,3,4], (2,2))
    [[1, 2], [3, 4]]

    This can be used to convert a row vector into a column vector by simply
    reversing the dimensions. For example,
    >>> to_matrix([1,2,3,4], (1,4))
    [[1], [2], [3], [4]]
    """

    if not __element_lengths_equal(vector, dimensions):
        raise RuntimeError("Element lengths not equal!")

    dim_prod = prod(dimensions)
    if not dim_prod > 0:
        return []

    x_span: int = dimensions[0]

    resultant: Matrix = []
    for index in range(0, dim_prod, x_span):
        resultant.append(vector[index:index+x_span])

    return resultant

def pretty(matrix: Matrix, values: Values) -> str:
    accumulator: list = []
    for vector in matrix:
        for value in vector:
            accumulator.append(f"{values[value]} ")
        accumulator.append("\n")
    return "".join(accumulator)

def compose(*functions: Callable) -> Any:

    """ Reduce such that functions f and g, each with one input x,
        reduce like f(g(x)).

        >>> def f(x): return x+1
        >>> def g(x): return 2*x
        >>> compose(f,g)(1)
        3
        >>> compose(g,f)(1)
        4

        This can be chained arbitrarily many times. For example
        >>> compose(g,g,g,g)(1)
        16

        This can be written much more succinctly but cryptically like
        >>> compose(*4*[g])(1)
        16

        In general, any list of functions can be applied
        >>> operations = [f, g, g, f]
        >>> compose(*operations)(1)
        9
    """

    return reduce(lambda f,g: lambda x: f(g(x)), functions, lambda x: x)

def operations() -> Operations:
    return { '@': __apply_rotation, '~': __apply_row_permutation }
