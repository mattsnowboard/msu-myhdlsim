import MyHDLSim.wxApplication

manager = MyHDLSim.wxApplication.Init()

## Circuit from intro01.circuit.c

a, b, c, d, F = [manager.CreateSignal() for i in range(5)]
# intermediate signals
notb, notc, notd = [manager.CreateSignal() for i in range(3)]
and1, and2 = [manager.CreateSignal() for i in range(2)]



manager.AddSwitch((20, 100), a, 'a')
manager.AddSwitch((20, 200), b, 'b')
manager.AddSwitch((20, 300), c, 'c')
manager.AddSwitch((20, 400), d, 'd')

manager.AddProbe((700, 300), F, 'f')

manager.AddProbe((300, 200), notb, 'notb')
manager.AddProbe((300, 300), notc, 'notc')
manager.AddProbe((300, 400), notd, 'notd')
manager.AddProbe((500, 200), and1, 'and1')
manager.AddProbe((500, 400), and2, 'and2')

manager.AddNotGate((200, 200), notb, b)
manager.AddNotGate((200, 200), notc, c)
manager.AddNotGate((200, 200), notd, d)

manager.AddAndGate((400, 200), and1, a, notb)
manager.AddAndGate((400, 400), and2, b, notc, notd)

manager.AddOrGate((600, 300), F, and1, and2)

manager.Start()