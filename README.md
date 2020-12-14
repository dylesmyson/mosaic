# **Midi** Mosaics in Python

A mosaic is a sort of cellular arrangement of (not necessarily) distinct
pieces. The goal of this library is to facilitate the arrangement of musical
notation (or other well-defined behavior) into various mathematical
objects.

To accomplish this, **Mosaic** implements two features. The first is a wrapper
around a midifile player. A library like **RTMidi** for example is used. This
wrapper maintains the state of a "session", offering many playback,
live-performance, and scripting opportunities.

The second is a set of midifile generation algorithms. These algorithms can take
a given configuration and output a valid midifile, which is also capable of being
orchestrated by the session wrapper.


## Getting Started

After cloning the repository, run

        $ pip3 install -r requirements

to install the package dependencies. Next, install the package

        $ pip3 install -e .

### Midi

Setting up your midi devices can involve careful trouble-shooting, and this
implementation has only been tested with **my** setup, but in general,
you'll want to connect your devices which are capable of __receiving__ midi
messages to whatever hardware will use this library.

For example, I like to connect to a DAW, since it will usually provide a lot
of sound library choices, as well as many secondary musical tools-- not to
mention, midi debug tooling.


## Available Scripts

### Connect

Allows you to quickly connect to and interact with a midi receiver-- very
useful for debugging a connection.

#### Usage

        $ python3 -i bin/connect [CONNECTION NAME]

to begin the __interactive__ connection.

If `CONNECTION NAME` isn't given, it defaults to `mosaic`.

At any time you may use the built-in `help` function from within the **Python**
interpreter to see the documentation for an object.

When `connect` is run, it creates a `SessionController` object named `session`.
Call `help` on this object for API documentation:

        >>> help(session)

```
Help on Session in module lib.session object:

class Session(builtins.object)
 |  Session(name='mosaic')
 |  
 |  Methods defined here:
 |  
 |  __init__(self, name='mosaic')
 |      Session wrapper.
 |  
 |  load(self, filepathstr: str, verbose: bool = False)
 |      Initialize a MidiFile object.
 |      
 |      Takes a filepath string as an argument. Pass `verbose=True` for debug output.
 |  
 |  loop(self, verbose: bool = False)
 |      Repeatedly step through all data in MidiFile, sending each message to be played.
 |      The loop can be terminated with Ctl-C.
 |      
 |      Pass `verbose=True` for debug output.
 |  
 |  play(self, verbose: bool = False)
 |      Step through all data in MidiFile, sending each message to be played.
 |      
 |      Pass `verbose=True` for debug output.
 |  
 |  step(self, start: int, stop: int, step: int, verbose: bool = False)
 |      Step through data in MidiFile, sending each message to be played.
 |      
 |      Takes start, stop, and step data. Pass `verbose=True` for debug output.
 |  
 |  write(self, filepathstr: str, data: list, verbose: bool = False)
 |      Write data to MidiFile object and save to disk.
 |      
 |      Takes a filepath string and some data list as arguments. Pass `verbose=True` for debug output.
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
 ```

### Player

The first piece of core functionality is the midifile player. It allows you to
play most `*.mid`/`*.midi` files through your receiver. Very fun to play
around with and experiment with!

#### Usage

        $ python3 [-i] bin/player [MIDI FILE]

By appending the `-i`, you will tell the script to "leave the session open".
Together with the API functionality of the underlying session, it's possible
to dump the Midi data which is great for debugging/editing songs.

#### API

The Player API exposes control of a midifile reader and several methods
for manipulating the data found within, including playback, step-through,
looping, and reversing the file's contents.

### Generate

The second piece of core functionality is the generator. It's a machine which takes as
input a configuration file and produces a playable midifile.

#### Usage

        $ python3 bin/generate [CONFIG]

The name of the saved file (and other data) should all be defined in a
configuration file.

#### Algorithms

There are currently two broad classes of algorithms available. The first
is a simple Markov process, and the second uses Algebraic groups in a similar
fashion to Rubik's cubes-- but in two dimensions. In each case, the result is a
stack of midi messages. Any algorithm which takes as an input a dictionary
of configuration options and parameters, and returns a midifile is valid.

