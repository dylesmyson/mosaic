#!/usr/bin/env python3



from math import prod
from enum import Enum
from time import sleep
from pathlib import Path
from yaml import safe_load
from random import choice, choices
from functools import reduce
from itertools import product
from typing import List, Tuple, Dict, Callable, Any, Optional

from mido import open_output, MidiFile




Vector     = List[int]
Matrix     = List[Vector]

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

Operations = Dict[str, Callable]
Puzzle     = Tuple[Matrix, Values]




# Methods on Vectors
def element_lengths_equal(vector: Vector, dimensions: Dimensions) -> bool:
    return prod(dimensions) == len(vector)

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

    if not element_lengths_equal(vector, dimensions):
        raise RuntimeError

    x_span: int = dimensions[0]

    resultant: Matrix = []
    for index in range(0, prod(dimensions), x_span):
        resultant.append(vector[index:index+x_span])

    return resultant


# Methods on Matrices
def dimensions(matrix: Matrix) -> Dimensions:
    return len(matrix[0]), len(matrix)

def matmul(left: Matrix, right: Matrix) -> Matrix:
    return [[sum(i*j for i,j in zip(acol,bcol)) for bcol in zip(*right)] for acol in left]

def transpose(matrix: Matrix) -> Matrix:
    return list(map(list, zip(*matrix)))

def to_vector(matrix: Matrix) -> Vector:

    """ Converts matrix into a row vector.

    For example, this will convert a 2x2 Matrix into a 4x1 Vector.

    >>> to_vector([[1,2], [3,4]])
    [1, 2, 3, 4]
    """

    return [value for vector in matrix for value in vector]

def create_rotation_matrix(dimensions: Dimensions) -> Matrix:
    rotation_matrix = to_matrix(dimensions, prod(dimensions)*[0])
    for i, vector in enumerate(rotation_matrix, 1):
        vector[len(vector)-i] = 1
    return rotation_matrix

def create_permutation_matrix(dimensions: Dimensions) -> Matrix:

    """ Generate a "special" permutation matrix.

    The matrix is a rotation matrix where the last row becomes the first
    row, pushing all the others further down. This creates a permutation
    through a single row that resembles permutation of a rubik's cube slice.

    >>> create_permutation_matrix((3,3))
    [[0,0,1],[1,0,0],[0,1,0]]
    """

    permutation_matrix = []
    rotation = create_rotation_matrix(dimensions)

    for vector in rotation[1:]:
        permutation_matrix.append(vector)

    permutation_matrix.reverse()
    permutation_matrix.insert(0, rotation[0])

    return permutation_matrix

def apply_rotation(matrix: Matrix) -> Matrix:
    rotation = create_rotation_matrix(dimensions=dimensions(matrix))
    return transpose(matmul(matrix, rotation))

def apply_row_permutation(matrix: Matrix, row: int = 0) -> Matrix:
    resultant    = matrix.copy()
    permutation  = create_permutation_matrix(dimensions(matrix))
    inverted     = matmul(matrix, permutation)
    resultant[row] = inverted[row]
    return resultant

def pretty(matrix: Matrix, values: Values) -> str:
    accumulator: list = []
    for vector in matrix:
        for value in vector:
            accumulator.append(f"{values[value]} ")
        accumulator.append("\n")
    return "".join(accumulator)


# Higher Order Functions/Secondary Objects
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
    return { '@': apply_rotation, '~': apply_row_permutation }


# Configuration Methods
def load_midi_file(filepath: str) -> MidiFile:
    return MidiFile(filename=str(Path(filepath)))

def safe_load_yaml(filepath: str) -> dict:
    with open(str(Path(filepath)), 'r') as stream:
        return safe_load(stream)


# Midi Objects and Methods
class MidiConnector:
    def __init__(self, name: str) -> 'MidiConnector':
        self.name = name
        self.__midi = open_output(self.name, virtual=True)
        print( f"Connected as {self.name}" )

    def send_msg(self, msg: Any) -> None:
        self.__midi.send(msg)

class MidiController:
    class NoteState(Enum):
        ON = 0x90
        OFF = 0x80

    def __init__(self, connector: 'MidiConnector') -> 'MidiController':
        self.__history: list = []
        self.__active_notes: list = []
        self.__connector: 'MidiConnector' = connector

    def __wait_real_time(self, seconds: float) -> None:
        sleep(seconds)

    def __send_msg(self, parity: NoteState, pitch: int, veloc: int) -> None:
        if parity is self.NoteState.ON:
            self.__active_notes.append((pitch, veloc))

        elif parity is self.NoteState.OFF:
            self.__active_notes.remove((pitch, veloc))

        self.__connector.send_message(parity, pitch, veloc)

    def __send_off(self, pitch: int, veloc: int) -> None:
        self.__send_msg(self.NoteState.OFF, pitch, veloc)

    def __send_all_off(self) -> None:
        for pitch, veloc in self.__active_notes:
            self.__send_off(pitch, veloc)

    def name(self) -> str:
        return self.__connector.name

    def all_off(self) -> None:
        """ stop all notes. """
        self.__send_all_off()

    def send(self, msg) -> None:
        self.__connector.send_msg(msg)

    def play(self, pitch: int = 60, rhythm: float = 3.0, veloc: int = 64) -> None:
        """ play a note corresponding to pitch, rhythm, and velocity. """

        self.__send_msg(self.NoteState.ON, pitch, veloc)
        self.__wait_real_time(rhythm*(60/120))
        self.__send_msg(self.NoteState.OFF, pitch, veloc)

        self.__history.append((pitch, rhythm, veloc))

    def test_connection(self) -> None:
        """ play one note forever to test midi connection. ctrl-c to quit. """
        while True:
            try:
                self.play()
            except KeyboardInterrupt:
                break

        self.all_off()

    def dump_history(self, filename: Optional[str] = None) -> None:
        """ clears and potentially saves the note history.  """

        if filename:
            with open(filename, 'w') as fn:
                for triple in self.__history:
                    fn.write( ','.join([str(a) for a in triple]) + '\n' )

        self.__history = []

    def history(self) -> None:
        """ ouputs the history of note events. """
        for pitch, rhythm, veloc in self.__history:
            print(pitch, rhythm, veloc)

    def replay(self, filename: str) -> None:
        """ play back the pitch, rhythm, and velocity data from a file. """
        with open(filename, 'r') as fn:
            for line in fn:
                pitch, rhythm, veloc = line.split(',')
                self.play(int(pitch), float(rhythm), int(veloc))

def connect(name: Optional[str] = 'mosaic') -> 'MidiController':
    return MidiController(connector = MidiConnector(name = name))


# Mathematical Methods
def proportion_of(top: list, bottom: list) -> float:
    return len(top)/len(bottom)

def statistical_mean(sample: list) -> float:
    return sum(sample)/len(sample)

def products(symbols: list, repeat: int) -> list:
    return list(product(symbols, repeat=repeat))

def similarity(initial: Matrix, final: Matrix) -> float:
    starting  = to_vector(initial)
    resultant = to_vector(final)
    matching  = [ i for i, j in zip(starting, resultant) if i == j ]
    return proportion_of(matching, starting)

def markov_chain(start: int, iterate_count:int, states: Vector, transition: Matrix) -> int:

    """ Ultra-basic implementation of a markov process.

        Yield states by first obtaining the corresponding row vector and
        sampling a discrete probability distribution with an array of possible
        states and an inital state.

        >>> xm = [[0.5,0.5],[1,0]]
        This matrix represents the probability distribution of transitioning
        to any state given some current state. For example, if the system is in
        the state which corresponds to the first value of
        `xm` (state 0) [0.5,0.5], then the probability of transitioning to
        either state is 50%. But if the system is in state 1, there is a
        100% chance of transitioning back to state 0 on the next iteration.

        >>> for state in markov_chain(0, range(2), xm, 5):
        ...     print(f"{state[0]}: {state[1]} from {state[2]}")
        0: 0 from [0.5, 0.5]
        1: 1 from [0.5, 0.5]
        2: 0 from [1, 0]
        3: 0 from [0.5, 0.5]
        4: 1 from [0.5, 0.5]
    """

    for _ in range(iterate_count):
        distr = transition[states.index(start)]
        start = choices(states, distr).pop()
        yield start


# Library API
## Puzzles
def load_puzzle_from_file(filename: str) -> Puzzle:
    data = safe_load_yaml(filename)['data']['pitch']
    values     = data['values']
    dimensions = data['dimensions']
    return to_matrix(dimensions, range(prod(dimensions))), values

def random_sequence(length: int) -> list:
    return choice(products(operations().keys(), length))

def average_similarity(initial: Matrix, length: int, trials: int) -> float:
    similarities = []
    for _ in range(trials):
        sequence = random_sequence(length)
        final = compose(*map(operations().get, sequence))(initial)
        similarities.append(similarity(initial, final))
    return statistical_mean(similarities)

## Midi
def play(filepath: str, controller: Optional['MidiController'] = None) -> 'MidiController':
    if not controller:
        controller = connect()
    midifile = load_midi_file(filepath)
    sleep(1)
    for msg in midifile.play():
        controller.send(msg)
    return controller

def messages(filepath: str) -> Any:
    midifile = MidiFile(filename=str(Path(filepath)))
    for _, track in enumerate(midifile.tracks):
        for msg in track:
            yield msg
