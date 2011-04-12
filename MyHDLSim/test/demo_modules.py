import MyHDLSim.Manager

""" This tests adding modules which contain other modules """

def SubModule(manager, X, Y, Out):
    module = manager.CreateModule()

    module.AddPort((0,0), X, True, "X")
    module.AddPort((0,50), Y, True, "Y")
    module.AddPort((100,0), Out, False, "Out")

    module.AddOrGate((0,0), Out, X, Y)

    return module

def MyModule(manager, signalA, signalB, signalOut):
    module = manager.CreateModule()
    
    notA = manager.CreateSignal()
    orWire = manager.CreateSignal()
    
    # lets give input/output ports some names for rendering
    # give locations relative to the module box
    portA = module.AddPort((0,0), signalA, True, "A input")
    portB = module.AddPort((0,50), signalB, True, "B input")
    portO = module.AddPort((400,50), signalOut, False, "OUTPUT")

    module.AddNotGate((0,0), notA, signalA)

    subModule = SubModule(manager, portB, notA, orWire)
    module.AddModule(subModule, (160, 50), "Sub")
    
    module.AddAndGate((320,0), signalOut, notA, orWire)
    
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
