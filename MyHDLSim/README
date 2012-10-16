This project uses MyHDL: http://www.myhdl.org/doku.php/overview v0.7
and wxPython: http://wxpython.org/

Start by reading about MyHDL and how it uses generators for its simulation.

The files combinational.py and sequential.py define logic gates using MyHDL
We have completed the And, Nand, Or, Nor, Xor, Nxor, Not, 2-to-1 MUX, 4-to-1 MUX and decoder combinational circuits
and a clock as well as TFF, DFF, Counter, and a parallel load register for sequential circuits.

Each of these has tests defined in the test folder.

The UI is written in wxPython. Here is a description of each source file it uses

Manager.py: Creates the window and some other wx things as well as a top-level module
which you can add elements to. The manager can create signals and modules, as well as
provide access to the top level module to add elements (AND gate, OR gate, etc.).
It lets you add a switch, which is a signal that can be toggled with a mapped key
You can create a probe, to watch the value of a signal
And you can make a clock with a given period.

The manager handles the main event loop, which gives control to wx for keyboard events.
There is an event handler for key presses so that control is passed to the MyHDL
simulator and a timer event which can pass control to the simulator for clock signals.
We handle this by stopping the wx event loop with "self._app.ExitMainLoop()" and
restarting it with "self._app.MainLoop()"
This is defined in the Start method

The manager can also handle what level of modules we render. For instance, you can 
see the contents of a module, or you can hide them and just show a box to simplify the view.
This is done with the page up and page down keys in OnKey(). We build a list of which
modules are at each level in _buildHierarchy().

wxApplication.py: This defines the main window for wx and builds the menu and button
toolbar. We handle button presses on "Play" and "Pause" to control the timer which
interrupts the wx event loop. It creates a canvas, which we define in this file
called MyHDLCanvas. The canvas handles adding OGL shapes to the view. We used OGL
so that items can be connects by wires really easily. The MyEvtHandler class
is used to make selecting and resizing work.
See the OGL demo in wx for more examples

Module.py: Modules can contain the signals and logic gates from MyHDL. Every MyHDL
element is added to a module. The manager provides a top level module, and every
user-defined module is added to that one (or is nested within another). Modules are defined
with ports which lets you connect them to other logic gates/signals/modules.

You can add modules to other modules. The method AddModule() handles moving the module
based on its parent's position.

The method Render() will create an ogl composite shape and add all contents of the module
to the shape.  This makes moving modules and resizing much easier.

The method ShowDetails() handles how the module is rendered.  You can either display
its contents or just a box with a label.  This is what Manager calls when you press
page up/page down.

The ModuleShape handles showing and hiding the internal details of a module. We did
this by using a Transparent pen/brush.  Attempting to call "hide()" on a shape
did not work.

Wrappers: Each MyHDL logic gate we defined has a Wrapper to draw it in wx. These
are in the Wrappers folder.

GenericGateWrapper.py: This is the base class for the logic gate wrappers. We have
a GenericGateShape class which defines a main shape (like the AND gate, or a simple box)
and creates box shapes to connect signals to. This class handles spacing out the boxes.
We allow left, top, and bottom input, as well as a single output. The output uses a probe
from SignalWrapper so that we can render the output of a gate (black/white for on/off).

The _createInstance method in GenericGateWrapper handles creating the MyHDL instances
needed by the simulator with 1 output and 1-6 inputs.  This handles multiple bits in
a signal by creating multiple logic gates internally (MyHDL) but showing a single
Wrapper in the UI. This may need some refactoring.

The _connectWires method will connect external signals to the boxes that were created
in the GenericGateShape.

Specific Wrappers: (And, Mux21, Mux41, Nand, Nor, Not, Nxor, Or, Xor)
Each uses a polygon shape which is based on an 80x80 square.  These ones use the 
GenericGateWrapper as a base class which handles most of the work

SignalWrapper.py: This wraps a MyHDL Signal object so that we can interact with the keyboard
and draw it. The signals can either be initialized to None, True, or False, or they
can have a width > 1 and be a vector of bits.

SignalWrapper objects can be set as Switch, Probe, or InputProbe, which affects the
way they are drawn.  The default shape is a 10x10 box, but switches and probes
have a larger box with a label. The SetClockDriver uses the same shape as a switch
but adds a MyHDL clock. The Toggle method will flip the bit or increment the value
if it is a bit vector. This lets the user change signals at run time. The Update method
will change the color and text of a signal to show what its value is.

demo_*.py: These files show examples of what user code would look like and how it gets
rendered in MyHDLSim. This is a good place to look at the code and test things out.

TODO:

- There is no way to add counters or decoders to Modules (via Manager or Module)
      - Also, these Wrappers are untested and don't derive from GenericGateWrapper
        could use some fixing
- No wrapper for Register (MyHDL code written in sequential.py)
- There is no demo for the flip flop Wrappers (not sure if they even work in wx)
- Some code may not be currently used, such as the "initial" flag in Module.Move
- Allow multiple Outputs on GenericGate to support things like decoder/counter
- Make the inputs to GenericGateShape probes so you can see the signals as they change
- GenericGateWrapper code for allowing multiple bits per signal, there is no error checking
  and the code is kind of long
- Error checking
- Signal "slicing": allow access to a single bit or range of bits in a bit vector
      - See http://www.myhdl.org/doc/current/manual/reference.html#shadow-signals
      - Also concatenation of bits may be useful.
- Label of ports in Modules and things like MUX, and flip flops
- Look at some wierd rendering bugs - resizing Modules some times does weird things
- Add something so user code can define a Signal to be printed every simulation step (as in Sim)
- Figure out how to support automated testing of MyHDLSim code (like in Sim) for grading