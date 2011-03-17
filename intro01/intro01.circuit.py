import MyHDLSim.wxApplication

manager = MyHDLSim.wxApplication.Init()

## Circuit from intro01.circuit.c

a, b, c, d, F = [manager.CreateSignal() for i in range(5)]
# intermediate signals
notb, notc, notd = [manager.CreateSignal() for i in range(3)]
and1, and2 = [manager.CreateSignal() for i in range(2)]



manager.AddSwitch((50, 50), a, 'a')
manager.AddSwitch((50, 200), b, 'b')
manager.AddSwitch((50, 300), c, 'c')
manager.AddSwitch((50, 400), d, 'd')

manager.AddProbe((750, 300), F, 'f')

manager.AddProbe((310, 200), notb, 'notb')
manager.AddProbe((310, 320), notc, 'notc')
manager.AddProbe((310, 440), notd, 'notd')
manager.AddProbe((530, 200), and1, 'and1')
manager.AddProbe((530, 400), and2, 'and2')

manager.AddNotGate((200, 200), notb, b)
manager.AddNotGate((200, 320), notc, c)
manager.AddNotGate((200, 440), notd, d)

manager.AddAndGate((420, 200), and1, a, notb)
manager.AddAndGate((420, 400), and2, b, notc, notd)

manager.AddOrGate((640, 300), F, and1, and2)

manager.Start()
