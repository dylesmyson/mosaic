""" Defines several useful types. 

Begins by assuming dimensions are inherently whole number combinations."""

from typing import List, Tuple, Dict, Callable



# In general, a Matrix can have any dimensions which are a partition of the
# number of elements of the Matrx. A Matrix with 36 elements, for example, can
# have dimensions (6, 6), (9, 4), (12, 3), and (18, 2)-- plus, their inverses.
Dimensions = Tuple[int, int]

# For simplicity and ease-of-caclulation, a Matrix's elements are simply a
# range of numbers up to the size of the Matrix. E.g.,
#   [ [0, 1, 2],
#     [3, 4, 5],
#     [6, 7, 8] ]
# Howvever, in the context of the Matrix as a puzzle, the Matrix should encode
# for our puzzle elements, such as musical notes, alpha-numeric characters, or
# any other Hashable types. In Python, each numerical index of the Matrix maps
# to a string value which can be overlayed at will later
# (see `pretty` function).
Values     = Dict[int, str]

Vector     = List[int]
Matrix     = List[Vector]
Operations = Dict[str, Callable]

Puzzle     = Tuple[Matrix, Operations, Values]