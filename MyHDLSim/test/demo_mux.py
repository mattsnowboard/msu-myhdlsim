import MyHDLSim.Manager

manager = MyHDLSim.Manager.Init()

a, b, s, F = [manager.CreateSignal() for i in range(4)]

manager.AddSwitch((50, 100), a, 'a')
manager.AddSwitch((50, 200), b, 'b')
manager.AddSwitch((50, 300), s, 's')

manager.AddMux21((200, 200), F, s, a, b)

manager.AddProbe((500, 200), F, 'out')

manager.Start()
