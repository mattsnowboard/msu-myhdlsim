import MyHDLSim.Manager

manager = MyHDLSim.Manager.Init()

a, b, notb, F = [manager.CreateSignal() for i in range(4)]
x, y, out = [manager.CreateSignal() for i in range(3)]

manager.AddSwitch((20, 100), a, 'a')
manager.AddSwitch((20, 200), b, 'b')
manager.AddProbe((400, 300), notb, 'notb')
manager.AddProbe((600, 150), F, 'f')

manager.AddSwitch((20, 400), x, 'x')
manager.AddSwitch((20, 500), y, 'y')
manager.AddProbe((400, 500), out, 'out')

manager.AddAndGate((200, 400), out, x, y)

manager.AddNotGate((200, 300), notb, b)

manager.AddAndGate((520, 200), F, a, notb)

manager.Start()