import wx
import wx.lib.ogl as ogl
from MyHDLSim.Wrappers.SignalWrapper import SignalWrapper
from MyHDLSim.Wrappers.NotGateWrapper import NotGateWrapper
from MyHDLSim.Wrappers.AndGateWrapper import AndGateWrapper
from MyHDLSim.Wrappers.OrGateWrapper import OrGateWrapper
from myhdl import always_comb

# The events that wx side will listen for, used to move contents of a Module
ModuleMoveEvent, EVT_MODULE_MOVE = wx.lib.newevent.NewEvent() 

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
        
        self._shape = None
        
        # positioning
        self._x = self._y = 0
        self._width = self._height = 0
        
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
        """ Create an AND gate
        
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
        
    def AddNotGate(self, pos, out, a):
        """ Create a NOT gate
        
        """
        gate = NotGateWrapper(self._canvas,
                              pos[0], pos[1],
                              self.SignalToPort(out),
                              self.SignalToPort(a))
        self._addInstance(gate)
    
    def AddModule(self, module, pos, name):
        """ Add a module
        
        module: already defined
        pos: where to position the module
        """
        # move the module and find its bounds
        module.Move(pos[0], pos[1], True)
        module._setBounds()
        # create bounding box
        module._shape = ogl.RectangleShape(module.GetWidth(), module.GetHeight())
        dc = wx.ClientDC(self._canvas)
        self._canvas.PrepareDC(dc)
        # when moving bouding box, it is relative to center
        module._shape.Move(dc,
                           module.GetX() + module.GetWidth() / 2,
                           module.GetY() + module.GetHeight() / 2,
                           False)
        self._canvas.AddMyHDLModule(module._shape)
        self._modules.append(module)
    
    def Move(self, x, y, initial = False):
        """ Move the module and its contents
        This should be called when adding a Module
        
        initial: initially, all shapes need to be moved from original location
                 subsequent moves will just offset that
        """
        delta_x = x - self._x
        delta_y = y - self._y
        self._x = x
        self._y = y
        for module in self._modules:
            module.Move(x, y)
        for gate in self._gates:
            shape = gate.GetShape()
            dc = wx.ClientDC(self._canvas)
            self._canvas.PrepareDC(dc)
            if initial:
                # keep a padding of 10 on each side
                shape.Move(dc,
                           shape.GetX() + shape.GetWidth() / 2 + self._x + 10,
                           shape.GetY() + shape.GetHeight() / 2 + self._y + 10,
                           False)
            else:
                shape.Move(dc,
                           shape.GetX() + delta_x,
                           shape.GetY() + delta_y,
                           False)
    
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
    
    def _setBounds(self):
        """ This will draw a bounding box around a module
        """
        self._width = 0
        self._height = 0
        for gate in self._gates:
            shape = gate.GetShape()
            new_w = shape.GetWidth() / 2  + shape.GetX() - self._x
            new_h = shape.GetHeight() / 2 + shape.GetY() - self._y
            if new_w > self._width:
                # include 20 padding
                self._width = new_w + 20
            if new_h > self._height:
                #include 20 padding
                self._height = new_h + 20
    
    def GetShape(self):
        """ Get the shape for this Module
        """
        return self._shape
        
    def GetWidth(self):
        """ Get width for drawing bounding box
        """
        return self._width
        
    def GetHeight(self):
        """ Get height for drawing bounding box
        """
        return self._height
        
    def GetX(self):
        """ Get X position for drawing bounding box
        """
        return self._x
        
    def GetY(self):
        """ Get Y position for drawing bounding box
        """
        return self._y
        