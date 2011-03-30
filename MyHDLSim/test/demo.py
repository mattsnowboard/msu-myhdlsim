import MyHDLSim.Manager

def MyModule(manager, signalA, signalB, signalOut):
    module = manager.CreateModule()
    
    notA = manager.CreateSignal()
    
    # lets give input/output ports some names for rendering
    # give locations relative to the module box
    module.AddPort((0,0), signalA, True, "A input")
    module.AddPort((0,50), signalB, True, "B input")
    module.AddPort((400,50), signalOut, False, "OUTPUT")
    
    #hmm, locations don't matter too much usually...
    # just add gates to the module
    module.AddNotGate((100,100), notA, signalA)
    module.AddAndGate((200,150), signalOut, notA, signalB)
    
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
manager.AddModule(myModule, (320, 200), "Name to display")
manager.AddModule(myModule2, (320, 500), "Name2")

manager.AddOrGate((640, 300), Out, F, G)

manager.AddProbe((750, 300), Out, 'out')

manager.Start()
