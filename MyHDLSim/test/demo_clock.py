import MyHDLSim.Manager

manager = MyHDLSim.Manager.Init()

a, b, c, d, andOut, nandOut, orOut, norOut, xorOut, nxorOut = [manager.CreateSignal() for i in range(10)]

manager.AddSwitch((20, 100), a, 'a')
manager.AddClock((20, 200),b, 'b')

manager.AddProbe((300, 50), b, 'b')


manager.Start()
