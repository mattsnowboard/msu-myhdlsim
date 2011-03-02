
# this is the interface I think we should provide for defining modules

import MyHDLSim.wxApplication

def MyModule(manager, signalA, signalB, signalC, signalOut):
    # creates a blank "module" object
    # modules have same interface as manager
    module = manager.CreateModule()
    
    # can create signals that live in the module object
    intermediate1, intermediate2 = [module.CreateSignal() for i in range(2)]
    
    # lets give input/output ports some names for rendering
    # give locations relative to the module box
    module.AddPort((0,0), signalA, "A input")
    module.AddPort((0, 50), signalB, "B input")
    module.AddPort((0, 100), signalC, "C input")
    module.AddPort((100,50), signalOut, "OUTPUT")
    
    #hmm, locations don't matter too much usually...
    # just add gates to the module
    module.AddAndGate((100,100), intermediate1, signalA, signalB)
    module.AddAndGate((100,200), intermediate2, signalB, signalC)
    module.AddAndGate((200,150), signalOut, intermediate1, intermediate2)
    
    # this magic method here will do all the fancy MyHDL stuff to take these wrapped
    # gates and signals to form a generator function that MyHDL likes
    # also adds the ports to be rendered properly
    module.Create()

manager = MyHDLSim.wxApplication.Init()

a, b, c, F = [manager.CreateSignal() for i in range(4)]

manager.AddSwitch((20, 100), a, 'a')
manager.AddSwitch((20, 200), b, 'b')
manager.AddSwitch((600, 150), c, 'c')

myModule = MyModule(manager, a, b, c, F)

#takes the module which a user now has built and does the appropriate wiring and grabbing the instance
manager.AddModule((320, 200), myModule, "Name to display")

manager.Start()

################################################################################
# just some other thoughts follow 

# alternatively, a module could be examined by something like...
manager.Start(myModule)
# or
myModule.Start()
# for debugging

# not sure if this is needed

# another idea is that rather than just show a box for a module
# allow users to see the inner workings
# this would render the gates within the module
module.Inspect(True)
manager.Start()