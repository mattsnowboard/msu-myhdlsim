from MyHDLSim.Wrappers.SignalWrapper import SignalWrapper
from MyHDLSim.Wrappers.NotGateWrapper import NotGateWrapper
from MyHDLSim.Wrappers.AndGateWrapper import AndGateWrapper
from MyHDLSim.Wrappers.NandGateWrapper import NandGateWrapper
from MyHDLSim.Wrappers.OrGateWrapper import OrGateWrapper
from MyHDLSim.Wrappers.NorGateWrapper import NorGateWrapper
from MyHDLSim.Wrappers.XorGateWrapper import XorGateWrapper
from MyHDLSim.Wrappers.NxorGateWrapper import NxorGateWrapper
from myhdl import always_comb

class Module:
    """ This class will contain wrapped Signals and Gates """
    def __init__(self, manager, canvas):
        """ Create a Module
        
        manager: Manager class to interface with
        canvas: Used for rendering(?)
        """
        self._manager = manager
        # @todo Figure out where "canvas" fits in here
        self._canvas = canvas
        
        self._instances = list()
        # quick look up of gates/signals by ID
        self._gates = []
        self._modules = []
        # map the ports to the signals they are connected to
        self._portmap = {}
    
    def AddPort(self, pos, signal, is_input, label):
        """ Add a port to interface with the module
        
        pos: (x, y) tuple to place the port within the module
        signal: signal to feed to the port
        is_input: boolean set to True for input, False for output
        label: displayed on module
        TODO: do we need this? Probably for rendering as a box with I/O
        """
        # if (is_input):
            # port = SignalWrapper(self._canvas, signal.GetSignal().val, pos[0], pos[1])
            # port.SetProbe(self._canvas, signal, label)
            # port.AddListener(self._manager._frame)
            # port.SetX(pos[0])
            # port.SetY(pos[1])
            # self._canvas.AddMyHDLSignal(port.GetShape(), pos[0], pos[1])
            # #lets map the signal to the port
            # self._portmap[signal] = port
        # portSignal = port.GetSignal()
        # def wire(output, input):
            # @always_comb
            # def logic():
                # output.next = input
            # return logic
        # connection = wire(portSignal, signal.GetSignal())
        # self._instances.append(connection)
        pass
    
    def SignalToPort(self, signal):
        """ When a signal has been set as a port, we want to internally use the port
        
        signal: the signal to lookup
        return: the signal or the port if it exists
        """
        if (signal in self._portmap):
            return self._portmap[signal]
        else:
            return signal
    
    def AddAndGate(self, pos, out, a, b, c = None, d = None):
        """ Create an AND gate
        
        """
        gate = AndGateWrapper(self._canvas,
                              pos[0], pos[1],
                              self.SignalToPort(out),
                              self.SignalToPort(a),
                              self.SignalToPort(b),
                              self.SignalToPort(c),
                              self.SignalToPort(d))
        self._addInstance(gate)

    def AddNandGate(self, pos, out, a, b, c = None, d = None):
        """ Create an NAND gate
        
        """
        gate = NandGateWrapper(self._canvas,
                              pos[0], pos[1],
                              self.SignalToPort(out),
                              self.SignalToPort(a),
                              self.SignalToPort(b),
                              self.SignalToPort(c),
                              self.SignalToPort(d))
        self._addInstance(gate)

    def AddOrGate(self, pos, out, a, b, c = None, d = None):
        """ Create an OR gate
        
        """
        gate = OrGateWrapper(self._canvas,
                             pos[0], pos[1],
                             self.SignalToPort(out),
                             self.SignalToPort(a),
                             self.SignalToPort(b),
                             self.SignalToPort(c),
                             self.SignalToPort(d))
        self._addInstance(gate)

    def AddNorGate(self, pos, out, a, b, c = None, d = None):
        """ Create an NOR gate
        
        """
        gate = NorGateWrapper(self._canvas,
                             pos[0], pos[1],
                             self.SignalToPort(out),
                             self.SignalToPort(a),
                             self.SignalToPort(b),
                             self.SignalToPort(c),
                             self.SignalToPort(d))
        self._addInstance(gate)
        
    def AddNotGate(self, pos, out, a):
        """ Create a NOT gate
        
        """
        gate = NotGateWrapper(self._canvas,
                              pos[0], pos[1],
                              self.SignalToPort(out),
                              self.SignalToPort(a))
        self._addInstance(gate)

    def AddXorGate(self, pos, out, a, b, c = None, d = None):
        """ Create an XOR gate
        
        """
        gate = XorGateWrapper(self._canvas,
                             pos[0], pos[1],
                             self.SignalToPort(out),
                             self.SignalToPort(a),
                             self.SignalToPort(b),
                             self.SignalToPort(c),
                             self.SignalToPort(d))
        self._addInstance(gate)

    def AddNxorGate(self, pos, out, a, b, c = None, d = None):
        """ Create an NXOR gate
        
        """
        gate = NxorGateWrapper(self._canvas,
                             pos[0], pos[1],
                             self.SignalToPort(out),
                             self.SignalToPort(a),
                             self.SignalToPort(b),
                             self.SignalToPort(c),
                             self.SignalToPort(d))
        self._addInstance(gate)
    
    def AddModule(self, module, pos, name):
        """ Add a module
        
        module: already defined
        pos: where to position the module
        """
        self._modules.append(module)
    
    def GetInstances(self):
        # here we need to recurse through sub modules when they exist
        instances = self._instances
        for module in self._modules:
            instances.extend(module.GetInstances())
        return instances
        
        
    def _addInstance(self, gate):
        inst = gate.GetInstance()
        self._instances.append(inst)
        self._gates.append(gate)
    
