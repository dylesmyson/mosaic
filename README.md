# **MIDI** Mosaics in Python

A mosaic is a sort of cellular arrangement of (not necessarily) distinct
pieces. The goal of this library is to facilitate the arrangement of musical
notation (or other well-defined behavior) into various mathematical
objects.

To accomplish this, **Mosaic** implements two features. The first is a wrapper
around a **MIDI** file player implementation. A library like **RTMidi** for
example is used. This wrapper maintains the state of a "session", offering many
playback and performance, as well as scripting opportunities.

The second is a set of **Midi** file-generation algorithms. These algorithms
can take a given initial state and parameters and output a valid **MIDI** file,
which is also capable of being orchestrated by the wrapper.


## Getting Started

After cloning the repository, run

        $ pip3 install -r requirements

to install the package dependencies. Next, install the package

        $ pip3 install -e .

### Midi

Setting up **MIDI** can involve careful trouble-shooting, and this implementation
has only been tested with __my__ setup, but in general, you'll want to connect
your devices which are capable of __receiving__ **MIDI** messages to whatever
hardware will use this library.

For example, I like to connect to a DAW, since it will usually provide a lot
of sound choices, as well as many secondary musical tools-- not to mention,
**MIDI** debug tooling.


## Available Scripts

### Connect

Allows you to quickly connect to and interact with a **MIDI** receiver-- very
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

Another useful tool is the **MIDI** file player. It allows you to play most
`.*.mid` files through your receiver. Very fun to play around with and
experiment with!

#### Usage

        $ python3 [-i] bin/player [MIDI FILE]

By appending the `-i`, you will tell the script to "leave the session open".
Together with the API functionality of the underlying session, it's possible
to dump the MIDI data which is great for debugging/editing songs.
