
""" This is an example of how intro01.circuit.c could be coded in our python code
    It defines our public interface which we will design to """

# handle all building the UI stuff (create the frames, buttons, etc.)
app = wxSim.CreateApp()

# signals to use, our wxSim object can create signals which it is aware of
# these are not MyHDL.Signal, but some class we wrap around it
# maybe this just returns some identifier which later calls can use?
# could also have app.CheckSignal(a) to read value for debugging
a, b, c, d, F = [app.CreateSignal() for i in range(5)]

# intermediate signals
notb, notc, notd, and1, and2 = [app.CreateSignl() for i in range(5)]
 
# Components and interconnections

# switches have location, signal, and event key
app.AddSwitch((20, 100), a, 'a')
app.AddSwitch((20, 200), b, 'b')
app.AddSwitch((20, 300), c, 'c')
app.AddSwitch((20, 400), d, 'd')

# gates have location, output, input, [input], [input], [input]
app.AddNotGate((120, 200), notb, b)
app.AddNotGate((120, 300), notc, c)
app.AddNotGate((120, 400), notd, d)

app.AddAndGate((320, 200), and1, a, notb)
app.AddAndGate((320, 300), and2, b, notc, notd)

app.AddOrGate((320, 400), F, and1, and2)

# define what output we want: location, signal
app.ProbeOutput((320, 500), F)

# start the UI loop, this includes creating the simulator
# simulator could be controlled by button (start, stop, step, etc.)
app.Start()