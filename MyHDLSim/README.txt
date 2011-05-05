This project uses MyHDL: http://www.myhdl.org/doku.php/overview
and wxPython: http://wxpython.org/

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