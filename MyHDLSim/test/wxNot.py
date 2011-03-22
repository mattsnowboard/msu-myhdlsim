import MyHDLSim.Manager

manager = MyHDLSim.Manager.Init()

#b, notb = [manager.CreateSignal(False) for i in range(2)]
b = manager.CreateSignal(None)
notb = manager.CreateSignal(None)


manager.AddSwitch((20, 200), b, 'b')
manager.AddProbe((400, 300), notb, 'notb')

manager.AddNotGate((200, 300), notb, b)


manager.Start()