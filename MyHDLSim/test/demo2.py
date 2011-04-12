import MyHDLSim.Manager

manager = MyHDLSim.Manager.Init()

a, b, c, d, andOut, nandOut, orOut, norOut, xorOut, nxorOut = [manager.CreateSignal() for i in range(10)]

manager.AddSwitch((20, 100), a, 'a')
manager.AddSwitch((20, 200), b, 'b')
manager.AddSwitch((20, 300), c, 'c')
manager.AddSwitch((20, 400), d, 'd')

manager.AddAndGate((100, 50), andOut, a, b, c, d)
manager.AddNandGate((100,100), nandOut, a, b, c, d)

manager.AddOrGate((100,150), orOut, a, b, c, d)
manager.AddNorGate((100, 200), norOut, a, b, c, d)

manager.AddXorGate((100, 250), xorOut, a, b, c, d)
manager.AddNxorGate((100, 300), nxorOut, a, b, c, d)

manager.AddProbe((300, 50), andOut, 'and out')
manager.AddProbe((300, 100), nandOut, 'nand out')
manager.AddProbe((300, 150), orOut, 'or out')
manager.AddProbe((300, 200), norOut, 'nor out')
manager.AddProbe((300, 250), xorOut, 'xor out')
manager.AddProbe((300, 300), nxorOut, 'nxor out')

manager.Start()
