# Installation and Usage

## Connect

After cloning the repository and cofiguring your DAW or synth (or anything that
responds to midi), run

        $ python3 -i bin/connect

to begin the interactive connection.

* call `help` on any method or class for its docstring. *

in particular, `help(ctrl)` is a good starting point:

```
connect as pycon
<lib.midi.MidiController object at 0x103d2ce10>
Help on MidiController in module lib.midi object:

class MidiController(builtins.object)
 |  MidiController(connector)
 |
 |  Methods defined here:
 |
 |  __init__(self, connector)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |
 |  all_off(self)
 |      stop all notes.
 |
 |  dump_history(self, filename=None)
 |      clears and potentially saves the note history.
 |
 |  history(self)
 |      ouputs the history of note events.
 |
 |  play(self, pitch=60, rhythm=3.0, veloc=64)
 |      play a note corresponding to pitch, rhythm, and velocity.
 |
 |  replay(self, filename)
 |      play back the pitch, rhythm, and velocity data from a file.
 |
 |  test_connection(self)
 |      play one note forever to test midi connection. ctrl-c to quit.
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

## Puzzle

        $ python3 -i bin/puzzle mosaic/yml/puzzle/3x3.yml 3 0

```
Initial state:
C_4 C_3 E_4
G_4 A_3 A_4
B_4 D_4 F_4

Executing: ~
from previous: 0.6666666666666666
C_3 E_4 C_4
G_4 A_3 A_4
B_4 D_4 F_4

Executing: @
from previous: 0.1111111111111111
C_4 A_4 F_4
E_4 A_3 D_4
C_3 G_4 B_4

Executing: @
from previous: 0.1111111111111111
F_4 D_4 B_4
A_4 A_3 G_4
C_4 E_4 C_3

overall: 0.1111111111111111
```
