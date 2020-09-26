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

    def __send_message(self, msg: 'Message'):

        """ Send **Midi** message.
        """

        if not msg.is_meta:
            self.outport.send(msg)

        self.history.append(msg)

        return msg

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
            [ midifile.tracks.append(track) for track in data ]
            midifile.save(filename=filepathstr)

    def step(self, start=0, stop=0, step=1):
        messages = islice(self.__message_generator(), start, stop, step)
        for msg in messages:
            time.sleep(msg.time)
            self.__send_message(msg)

    def play(self):
        for msg in self.midifile.play():
            time.sleep(msg.time)
            self.__send_message(msg)

    def loop(self):
        while True:
            try:
                t0 = time.time()
                self.play()
                print(f"looped in {time.time()-t0}s (expected {self.midifile.length})")
            except KeyboardInterrupt:
                self.outport.reset()
                break



#     def dump_history(self, filename):
#         if filename:
#             track = MidiTrack()
#             [ track.append(msg) for msg in self.history ]
#         self.history = []

