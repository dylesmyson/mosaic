from math import prod
from random import choice, choices

from lib.linear import to_matrix, operations
from lib.definitions import Dimensions, Values, Operations, Vector, Matrix

from mido import MidiFile, MidiTrack, Message



def algebraic(dimensions: Dimensions, operations: Operations):

    """ Algebraic. """

    op_symbols = list(operations.keys())
    state = to_matrix(dimensions, range(prod(dimensions)))

    while True:
        random_move = choice(op_symbols)
        state = operations[random_move](state)
        yield state

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
        >>> for state in markov_chain(0, 5, [0,1], xm):
        ...     print(f"step: {state[0]} - trans. to {state[1]} using dist. {state[2]}")
        step: 0 - trans. to 0 using dist. [0.5, 0.5]
        step: 1 - trans. to 1 using dist. [0.5, 0.5]
        step: 2 - trans. to 0 using dist. [1, 0]
        step: 3 - trans. to 0 using dist. [0.5, 0.5]
        step: 4 - trans. to 1 using dist. [0.5, 0.5]
    """

    for step in range(iterate_count):
        distr = transition[states.index(start)]
        start = choices(states, distr).pop()
        yield start


class Generators():

    @staticmethod
    def algebraic(conf):

        """ Return a MidiFile. """

        steps               = conf.get('steps', 10)

        author              = conf.get('author', 'unknown')
        filename            = conf.get('filename', 'unknown.mid')

        pitch_values        = conf.get('values').get('pitch')
        pitch_dimensions    = conf.get('dimensions').get('pitch')

        velocity_values     = conf.get('values').get('velocity')
        velocity_dimensions = conf.get('dimensions').get('velocity')

        rhythm_values       = conf.get('values').get('rhythm')
        rhythm_dimensions   = conf.get('dimensions').get('rhythm')

        with MidiFile() as midifile:
            track = MidiTrack()
            track.append(Message('program_change', program=12, time=0))

            pitch_state    = algebraic(pitch_dimensions, operations())
            velocity_state = algebraic(velocity_dimensions, operations())
            rhythm_state   = algebraic(rhythm_dimensions, operations())

            for _ in range(steps):
                next_pitch_state    = next(pitch_state)
                next_velocity_state = next(velocity_state)
                next_rhythm_state   = next(rhythm_state)

                for vector in next_pitch_state:
                    for component in vector:
                        pitch = pitch_values[component]

                        track.append(Message('note_on', note=pitch, velocity=64, time=200))
                        track.append(Message('note_off', note=pitch, velocity=64, time=200)) 

            midifile.tracks.append(track)
            midifile.save(filename=filename)

    @staticmethod
    def markov(conf):

        """ Return a MidiFile. """

        steps         = conf.get('steps', 10)

        author        = conf.get('author', 'unknown')
        filename      = conf.get('filename', 'unknown.mid')

        values        = conf['values']
        transitions   = conf['transitions']

        with MidiFile() as midifile:
            track = MidiTrack()
            track.append(Message('program_change', program=12, time=0))

            pitch_chain    = markov_chain(values['pitch'][0], steps, values['pitch'], transitions['pitch'])
            velocity_chain = markov_chain(values['velocity'][0], steps, values['velocity'], transitions['velocity'])
            rhythm_chain   = markov_chain(values['rhythm'][0], steps, values['rhythm'], transitions['rhythm'])

            for _ in range(steps):
                next_pitch    = next(pitch_chain)
                next_velocity = next(velocity_chain)
                next_rhythm   = next(rhythm_chain)

                track.append(Message('note_on', note=next_pitch, velocity=next_velocity, time=next_rhythm))
                track.append(Message('note_off', note=next_pitch, velocity=next_velocity, time=next_rhythm))

            midifile.tracks.append(track)
            midifile.save(filename=filename)
