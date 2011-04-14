import MyHDLSim.Manager

""" This tests adding modules which contain other modules """

def Simple(manager, signalA, signalOut):
    module = manager.CreateModule()
    
    portA = module.AddPort((0,0), signalA, True, "A input")
    portO = module.AddPort((400,50), signalOut, False, "OUTPUT")

    module.AddNotGate((0,0), portO, portA)
    
    return module

manager = MyHDLSim.Manager.Init()

a, b, Out = [manager.CreateSignal() for i in range(3)]

manager.AddSwitch((50, 100), a, 'a')

mod = Simple(manager, a, b)

manager.AddModule(mod, (150, 300), "Name to display")
#### NOTE: if you try to add the SAME module twice, it will crash!

manager.AddNotGate((400, 100), Out, b)

manager.AddProbe((750, 300), Out, 'out')

manager.Start()
