#!/usr/bin/env python3



import time

from pathlib import Path
from itertools import islice
from mido import Message, MidiFile, MidiTrack, open_output



class Session:

    def __init__(self, name = 'mosaic'):

        """ Session wrapper.
        """

        self.history  = []
        self.filename = None
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
        for msg in messages:
            time.sleep(msg.time)
            self.__send_message(msg, verbose)

    def __message_generator(self):

        """ Step into MidiFile.
        """

        if not self.midifile:
            raise Exception('MidiFile is undefined. ')

        for msg in self.midifile:
            yield msg



    def load(self, filepathstr: str):

        """ Initialize a MidiFile object.
        """

        self.filename = filepathstr
        self.midifile = MidiFile(filename=str(Path(self.filename)), debug=False)

    def write(self, filepathstr, data):

        """ Write data to MidiFile.
        """

        with MidiFile(debug=True) as midifile:
            track = MidiTrack()
            array_bytes = [ msg.bin() for msg in data ]
            [ track.append(byte) for byte in array_bytes ]
            midifile.tracks.append(track)
            midifile.save(filename=filepathstr)

    def step(self, start, stop, step, verbose=False):
        generator = self.__message_generator()
        messages  = islice(generator, start, stop, step)
        self.__play_messages(messages, verbose)

    def play(self, verbose=False):
        self.step(0, None, step=1, verbose=verbose)

    def loop(self, verbose=False):
        while True:
            try:
                t0 = time.time()
                self.play(verbose=verbose)
                print(f"looped in {time.time()-t0}s (expected {self.midifile.length})")
            except KeyboardInterrupt:
                self.outport.reset()
                break
