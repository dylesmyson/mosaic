import time

from pathlib import Path
from itertools import islice

from mido import MidiFile, MidiTrack, open_output # pylint: disable=no-name-in-module



class Session:
    def __init__(self, name):

        """ Session wrapper.
        """

        self.history  = []
        self.filepath = None
        self.midifile = None
        self.outport  = self.__connect_midi_in(name)

    def __connect_midi_in(self, name: str) -> 'BaseMidiOut':

        """ Return BaseOutput class.
        """

        return open_output(name=name, autoreset=True, virtual=True)

    def __send_message(self, msg: 'Message', verbose: bool):

        """ Send **Midi** message.
        """

        if not msg.is_meta:
            self.outport.send(msg)

        self.history.append(msg)

        if verbose: print(msg)
        return msg

    def __play_messages(self, messages, verbose):
        time.sleep(2)   # Sleep to provide the receiver time to accept messages
        for msg in messages:
            try:
                time.sleep(msg.time)
                self.__send_message(msg, verbose)
            except KeyboardInterrupt:
                print('Caught interrupt. ')
                break

        print('Exiting. ')


    def __message_generator(self):

        """ Step into MidiFile.
        """

        if not self.midifile:
            raise Exception('MidiFile is undefined. ')

        for msg in self.midifile:
            yield msg

    """ Intended to be public API. """

    def load(self, filepathstr: str, verbose: bool = False):

        """ Initialize a MidiFile object.

            Takes a filepath string as an argument. Pass `verbose=True` for debug output.
        """

        self.filepath = Path(filepathstr)
        self.midifile = MidiFile(filename=str(self.filepath), debug=verbose)

    def write(self, filepathstr: str, data: list, verbose: bool = False):

        """ Write data to MidiFile object and save to disk.

            Takes a filepath string and some data list as arguments. Pass `verbose=True` for debug output.
        """

        with MidiFile(debug=verbose) as midifile:
            track = MidiTrack()
            array_bytes = [ msg.bin() for msg in data ]
            [ track.append(byte) for byte in array_bytes ]
            midifile.tracks.append(track)
            midifile.save(filename=filepathstr)

    def step(self, start: int, stop: int, step: int, verbose: bool = False):

        """ Step through data in MidiFile, sending each message to be played.

            Takes start, stop, and step data. Pass `verbose=True` for debug output.
        """

        messages  = islice(self.__message_generator(), start, stop, step)
        self.__play_messages(messages, verbose)

    def play(self, verbose: bool = False):

        """ Step through all data in MidiFile, sending each message to be played.

            Pass `verbose=True` for debug output.
        """

        self.step(0, None, step=1, verbose=verbose)

    def loop(self, verbose: bool = False):

        """ Repeatedly step through all data in MidiFile, sending each message to be played.
            The loop can be terminated with Ctl-C.

            Pass `verbose=True` for debug output.
        """

        while True:
            try:
                t0 = time.time()
                self.play(verbose=verbose)
                print(f"looped in {time.time()-t0}s (expected {self.midifile.length})")
            except KeyboardInterrupt:
                print('Caught loop interrupt. ')
                self.outport.reset()
                break
