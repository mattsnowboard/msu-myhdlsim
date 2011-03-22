from MyHDLSim.Wrappers.SignalWrapper import SignalWrapper
from MyHDLSim.Wrappers.NotGateWrapper import NotGateWrapper
from MyHDLSim.Wrappers.AndGateWrapper import AndGateWrapper
from MyHDLSim.Wrappers.OrGateWrapper import OrGateWrapper

class Module:
    """ This class will contain wrapped Signals and Gates """
    def __init__(self, manager, canvas):
        self._manager = manager
        # @todo Figure out where "canvas" fits in here
        self._canvas = canvas
        
        self._instances = list()
        # quick look up of gates/signals by ID
        self._gates = []
    
    def AddPort(self, pos, signal, in_out, label):
        """ Add a port to interface with the module
        
        """
        pass
        
    def AddAndGate(self, pos, out, a, b, c = None, d = None):
        """ Create an AND gate
        
        """
        gate = AndGateWrapper(self._canvas, pos[0], pos[1], out, a, b, c, d)
        self._addInstance(gate)

    def AddOrGate(self, pos, out, a, b, c = None, d = None):
        """ Create an OR gate
        
        """
        gate = OrGateWrapper(self._canvas, pos[0], pos[1], out, a, b, c, d)
        self._addInstance(gate)
        
    def AddNotGate(self, pos, out, a):
        """ Create a NOT gate
        
        """
        gate = NotGateWrapper(self._canvas, pos[0], pos[1], out, a)
        self._addInstance(gate)
    
    def AddModule(self, module):
        # this needs to be implemented so Modules can contain other Modules
        pass
    
    def GetInstances(self):
        # here we need to recurse through sub modules when they exist
        return self._instances
        
        
    def _addInstance(self, gate):
        inst = gate.GetInstance()
        self._instances.append(inst)
        self._gates.append(gate)
    