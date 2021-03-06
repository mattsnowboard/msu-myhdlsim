import MyHDLSim.Manager

""" This tests adding modules which contain other modules """

def SubModule(manager, X, Y, Out):
    module = manager.CreateModule()

    portX = module.AddPort(X, True, "X")
    portY = module.AddPort(Y, True, "Y")
    portO = module.AddPort(Out, False, "Out")

    module.AddOrGate((0,0), portO, portX, portY)

    return module

def MyModule(manager, signalA, signalB, signalOut):
    module = manager.CreateModule()
    
    notA = manager.CreateSignal()
    orWire = manager.CreateSignal()
    
    # lets give input/output ports some names for rendering
    portA = module.AddPort(signalA, True, "A input")
    portB = module.AddPort(signalB, True, "B input")
    portO = module.AddPort(signalOut, False, "OUTPUT")

    module.AddNotGate((0,0), notA, signalA)

    subModule = SubModule(manager, portB, notA, orWire)
    module.AddModule(subModule, (160, 50), "Sub")
    
    module.AddAndGate((320,0), portO, notA, orWire)
    
    #module.Create()
    return module

manager = MyHDLSim.Manager.Init()

a, b, c, F, G, Out = [manager.CreateSignal() for i in range(6)]

manager.AddSwitch((50, 100), a, 'a')
manager.AddSwitch((50, 200), b, 'b')
manager.AddSwitch((50, 300), c, 'c')

myModule = MyModule(manager, a, b, F)
myModule2 = MyModule(manager, c, a, G)

#takes the module which a user now has built and does the appropriate wiring and grabbing the instance
manager.AddModule(myModule, (150, 50), "Name to display")
manager.AddModule(myModule2, (150, 300), "Name2")
#### NOTE: if you try to add the SAME module twice, it will crash!

manager.AddOrGate((750, 500), Out, F, G)

manager.AddProbe((750, 300), Out, 'out')

manager.Start()
