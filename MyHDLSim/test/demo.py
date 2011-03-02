import MyHDLSim.wxApplication

manager = MyHDLSim.wxApplication.Init()

a, b, F = [manager.CreateSignal() for i in range(3)]

manager.AddSwitch((20, 100), a, 'a')
manager.AddSwitch((20, 200), b, 'b')
manager.AddSwitch((600, 150), F, 'f')

manager.AddAndGate((320, 200), F, a, b)

manager.Start()