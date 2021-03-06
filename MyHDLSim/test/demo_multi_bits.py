import MyHDLSim.Manager

manager = MyHDLSim.Manager.Init()

## Circuit from intro01.circuit.c

a, b, c, d, F = [manager.CreateSignal(0, width=4) for i in range(5)]

# intermediate signals
notb, notc, notd = [manager.CreateSignal(0, width=4) for i in range(3)]
and1, and2 = [manager.CreateSignal(0, width=4) for i in range(2)]

manager.AddSwitch((50, 50), a, 'a')
manager.AddSwitch((50, 200), b, 'b')
manager.AddSwitch((50, 300), c, 'c')
manager.AddSwitch((50, 400), d, 'd')

manager.AddNotGate((200, 200), notb, b)
manager.AddNotGate((200, 320), notc, c)
manager.AddNotGate((200, 440), notd, d)

manager.AddAndGate((420, 200), and1, a, notb)
manager.AddAndGate((420, 400), and2, b, notc, notd)

manager.AddOrGate((640, 300), F, and1, and2)

manager.AddProbe((750, 300), F, 'f')

manager.Start()
