import time
import logging

from pathlib import Path
from itertools import islice

from mido import MidiFile, MidiTrack, open_output # pylint: disable=no-name-in-module


logger = logging.getLogger(__name__)


class Session:
    def __init__(self, name):

        """ Session wrapper.
        """

        self.history  = []
        self.filepath = None
        self.midifile = None
        self.outport  = self.__connect_midi_in(name)
        logger.debug(f"Connected midi outport: {self.outport}")

        logger.info(f"Connected to session as {name}.")

    def __connect_midi_in(self, name: str) -> 'BaseMidiOut':

        """ Return BaseOutput class.
        """

        return open_output(name=name, autoreset=True, virtual=True)

    def __send_message(self, msg: 'Message'):

        """ Send **Midi** message.
        """

        logger.debug(f"Sending message: {msg}")

        if not msg.is_meta:
            self.outport.send(msg)

        self.history.append(msg)

        return msg

    def __play_messages(self, messages):
        time.sleep(2)   # Sleep to provide the receiver time to accept messages
        for msg in messages:
            try:
                time.sleep(msg.time)
                self.__send_message(msg)
            except KeyboardInterrupt:
                logger.debug('Caught interrupt.')
                break

    def __message_generator(self):

        """ Step into MidiFile.
        """

        if not self.midifile:
            raise Exception('MidiFile is undefined.')

        for msg in self.midifile:
            yield msg

    """ Intended to be public API. """

    def load(self, filepathstr: str):

        """ Initialize a MidiFile object.

            Takes a filepath string as an argument. Pass `verbose=True` for debug output.
        """

        self.filepath = Path(filepathstr)
        self.midifile = MidiFile(filename=str(self.filepath))
        logger.info(f"Loaded {self.filepath}: {self.midifile}")

    def write(self, filepathstr: str, data: list):

        """ Write data to MidiFile object and save to disk.

            Takes a filepath string and some data list as arguments. Pass `verbose=True` for debug output.
        """

        with MidiFile(debug=verbose) as midifile:
            track = MidiTrack()
            array_bytes = [ msg.bin() for msg in data ]
            [ track.append(byte) for byte in array_bytes ]
            midifile.tracks.append(track)
            midifile.save(filename=filepathstr)
        logger.info(f"Wrote {midifile} to {filepathstr}")

    def step(self, start: int, stop: int, step: int):

        """ Step through data in MidiFile, sending each message to be played.

            Takes start, stop, and step data. Pass `verbose=True` for debug output.
        """

        logger.debug(f"Stepping from {start} to {stop} by {step}")
        messages  = islice(self.__message_generator(), start, stop, step)
        self.__play_messages(messages)

    def play(self):

        """ Step through all data in MidiFile, sending each message to be played.

            Pass `verbose=True` for debug output.
        """

        self.step(0, None, step=1)

    def loop(self):

        """ Repeatedly step through all data in MidiFile, sending each message to be played.
            The loop can be terminated with Ctl-C.

            Pass `verbose=True` for debug output.
        """

        while True:
            try:
                t0 = time.time()
                self.play()
                logger.debug(f"Looped in {time.time()-t0} seconds (expected {self.midifile.length})")
            except KeyboardInterrupt:
                logger.debug('Caught loop interrupt.')
                self.outport.reset()
                break
