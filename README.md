# **Midi** Mosaics in Python

A mosaic is a sort of cellular arrangement of (not necessarily) distinct
pieces. The goal of this library is to facilitate the arrangement of musical
notation (or other well-defined behavior) into various mathematical
objects.

To accomplish this, **Mosaic** implements two features. The first is a wrapper
around a **Midi** file player implementation. A library like **RTMidi** for
example is used. This wrapper maintains the state of a "session", offering many
playback and performance, as well as scripting opportunities.

The second is a set of **Midi** file-generation algorithms. These algorithms
can take a given initial state and parameters and output a valid **Midi** file,
which is also capable of being orchestrated by the wrapper.


## Getting Started

After cloning the repository, run

        $ pip3 install -r requirements

to install the package dependencies. Next, install the package

        $ pip3 install -e .

### Midi

Setting up **Midi** can involve careful trouble-shooting, and this implementation
has only been tested with __my__ setup, but in general, you'll want to connect
your devices which are capable of __receiving__ **Midi** messages to whatever
hardware will use this library.

For example, I like to connect to a DAW, since it will usually provide a lot
of sound choices, as well as many secondary musical tools-- not to mention,
**Midi** debug tooling.


## Available Scripts

### Connect

Allows you to quickly connect to and interact with a **Midi** receiver-- very
useful for debugging a connection.

#### Usage

        $ python3 -i bin/connect [CONNECTION NAME]

to begin the __interactive__ connection.

If `CONNECTION NAME` isn't given, it defaults to `mosaic`.

At any time you may use the built-in `help` function from **Python** to see the
documentation for an object.

When `connect` is run, it creates a `SessionController` object named `session`.
Call `help` on this object for API documentation:

        >>> help(session)

### Player

Another useful tool is the **Midi** file player. It allows you to play most
`.*.mid` files through your receiver. Very fun to play around with and
experiment with!

#### Usage

        $ python3 [-i] bin/player [MIDI FILE]

By appending the `-i`, you will tell the script to "leave the session open".
Together with the API functionality of the underlying session, it's possible
to dump the Midi data which is great for debugging/editing songs.

#### API

The Player API exposes control of a **Midi** file reader and several methods
for manipulating the data found within, including play back, step through,
looping, and reversing the file's contents.

### Generate

The second piece of the puzzle is the generator. It's a machine which takes as
input a configuration file (or configuration data, in general) and produces a
**Midi** file.

#### Usage

        $ python3 bin/generate [CONFIG]

The name of the saved file (and other metadata) should all be defined in a
configuration file, or passed to the generator directly.

#### Algorithms

There are currently two broad classes of algorithms available. The first
is a simple Markov process, and the second uses Algebraic groups in a similar
fashion to Rubik's cubes-- but in two dimensions. In each case, the result is a
stack of **Midi** messages. Any algorithm which takes as an input a dictionary
of configuration options and parameters, and returns a FIFO queue of
**MidiMessages** is valid.

