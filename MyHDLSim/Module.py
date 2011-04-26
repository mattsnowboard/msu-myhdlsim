import wx
import wx.lib.ogl as ogl
from MyHDLSim.Wrappers.SignalWrapper import SignalWrapper
from MyHDLSim.Wrappers.NotGateWrapper import NotGateWrapper
from MyHDLSim.Wrappers.AndGateWrapper import AndGateWrapper
from MyHDLSim.Wrappers.NandGateWrapper import NandGateWrapper
from MyHDLSim.Wrappers.OrGateWrapper import OrGateWrapper
from MyHDLSim.Wrappers.NorGateWrapper import NorGateWrapper
from MyHDLSim.Wrappers.XorGateWrapper import XorGateWrapper
from MyHDLSim.Wrappers.NxorGateWrapper import NxorGateWrapper
from MyHDLSim.Wrappers.Mux21Wrapper import Mux21Wrapper
from MyHDLSim.Wrappers.Mux41Wrapper import Mux41Wrapper
from MyHDLSim.Wrappers.tffWrapper import TffWrapper
from MyHDLSim.Wrappers.dffWrapper import DffWrapper
from MyHDLSim.Wrappers.GenericGateWrapper import GenericGateShape
from myhdl import always_comb

class ModuleShape(GenericGateShape):
    def __init__(self, canvas, inLeftShapes, outShapes, mainShape, topShapes = [], bottomShapes = [], doConnect = True):
        """ Creates a ModuleShape which is a rectangle within the GenericGate

        canvas: where to draw shapes
        width, height: main shape rectangle size
        """
        GenericGateShape.__init__(self, canvas, inLeftShapes, outShapes, mainShape, topShapes, bottomShapes, doConnect)

        self._hidden = []

    def HideModule(self):
        """ Need to remove children from canvas
        """
        for child in self.GetChildren():
            if isinstance(child, GenericGateShape):
                child.SetBrushForChildren(wx.TRANSPARENT_BRUSH)
                child.SetPenForChildren(wx.TRANSPARENT_PEN)
                self._hidden.append(child)
                child._main.ClearText()
                for wire in child.GetLines():
                    wire.SetPen(wx.TRANSPARENT_PEN)
                    wire.SetBrush(wx.TRANSPARENT_BRUSH)
                for child2 in child.GetChildren():
                    for wire in child2.GetLines():
                        wire.SetPen(wx.TRANSPARENT_PEN)
                        wire.SetBrush(wx.TRANSPARENT_BRUSH)

    def ShowModule(self):
        """ Need to add children back to canvas
        """
        for child in self._hidden:
            if isinstance(child, GenericGateShape):
                child.SetBrushForChildren(wx.WHITE_BRUSH)
                child.SetPenForChildren(wx.BLACK_PEN)
                child._main.AddText(child._main.GetRegionName())
                for wire in child.GetLines():
                    wire.SetPen(wx.BLACK_PEN)
                    wire.SetBrush(wx.BLACK_BRUSH)
                for child2 in child.GetChildren():
                    for wire in child2.GetLines():
                        wire.SetPen(wx.BLACK_PEN)
                        wire.SetBrush(wx.BLACK_BRUSH)
        self._hidden = []

class Module:
    """ This class will contain wrapped Signals and Gates """
    def __init__(self, manager, canvas):
        """ Create a Module
        
        manager: Manager class to interface with
        canvas: Used for rendering
        """
        self._manager = manager
        # @todo Figure out where "canvas" fits in here
        self._canvas = canvas

        self._showInternal = True
        self._shape = None
        self._completeShape = None
        self._hiddenShape = None
        
        # positioning
        self._x = self._y = 0
        self._width = self._height = 0

        self._rendered = False
        
        self._instances = list()
        # quick look up of gates/signals by ID
        self._gates = []
        self._modules = []
        # map the ports to the signals they are connected to
        self._portmap = {}
        # map the shapes to the signals they represent for event handling
        self._portShapeMap = {}
        # images for ports
        self._inPorts = []
        self._outPorts = []
        # keeps the inner signals which are used by modules
        self._outPortsInner = []
    
    def AddPort(self, signal, is_input, label):
        """ Add a port to interface with the module
        
        pos: (x, y) tuple to place the port within the module
        signal: signal to feed to the port
        is_input: boolean set to True for input, False for output
        label: displayed on module

        return: The signal so we can connect to it!
        """
        if (is_input):
            port = SignalWrapper(self._canvas, signal.GetSignal().val)
            self._inPorts.append(port)
            #lets map the signal to the port
            self._portmap[signal] = port
            self._portShapeMap[port.GetShape()] = signal
            portSignal = port.GetSignal()
            # wire connection to keep this signal connected to input
            def wire(output, input):
                @always_comb
                def logic():
                    output.next = input
                return logic
            connection = wire(portSignal, signal.GetSignal())
            self._instances.append(connection)
            #returned so we can use the underlying signal
            return port
        else: #output
            port = SignalWrapper(self._canvas, signal.GetSignal().val)
            self._outPorts.append(signal)
            self._outPortsInner.append(port)
            self._portmap[signal] = port
            self._portShapeMap[signal.GetShape()] = port
            # wire connection to keep this signal connected to input
            def wire(output, input):
                @always_comb
                def logic():
                    output.next = input
                return logic
            connection = wire(signal.GetSignal(), port.GetSignal())
            self._instances.append(connection)
            #returned so we can use the underlying signal
            return port
        return None
    
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

        pos: position to place gate at relative to containing module
        out: output
        a,b,c,d: inputs
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
        """ Create a NAND gate

        pos: position to place gate at relative to containing module
        out: output
        a,b,c,d: inputs
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

        pos: position to place gate at relative to containing module
        out: output
        a,b,c,d: inputs
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
        
        pos: position to place gate at relative to containing module
        out: output
        a,b,c,d: inputs
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

        pos: position to place gate at relative to containing module
        out: output
        a: input
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
        
        pos: position to place gate at relative to containing module
        out: output
        a,b,c,d: inputs
        """
        gate = NxorGateWrapper(self._canvas,
                             pos[0], pos[1],
                             self.SignalToPort(out),
                             self.SignalToPort(a),
                             self.SignalToPort(b),
                             self.SignalToPort(c),
                             self.SignalToPort(d))
        self._addInstance(gate)

    def AddMux21(self, pos, out, select, a, b):
        """ Create a 2-1 Mux

        pos: position to palce gate at relative to containing module
        out: output
        select: selection
        a,b: inputs
        """
        gate = Mux21Wrapper(self._canvas,
                            pos[0], pos[1],
                            self.SignalToPort(out),
                            self.SignalToPort(select),
                            self.SignalToPort(a),
                            self.SignalToPort(b))
        self._addInstance(gate)

    def AddMux41(self, pos, out, c0, c1, d0, d1, d2, d3):
        """ Create a 4-1 Mux

        pos: position to palce gate at relative to containing module
        out: output
        c0,c1: selection
        d0,d1,d2,d3: inputs
        """
        gate = Mux41Wrapper(self._canvas,
                            pos[0], pos[1],
                            self.SignalToPort(out),
                            self.SignalToPort(c0),
                            self.SignalToPort(c1),
                            self.SignalToPort(d0),
                            self.SignalToPort(d1),
                            self.SignalToPort(d2),
                            self.SignalToPort(d3))
        self._addInstance(gate)

    def AddTff(self, pos, q, t, clk, rst = None, s = None):
        """ Create a T Flip-Flop

        pos: position to place gate at relative to containing module
        q: output
        t, clk: inputs
        rst,s: Reset/Set
        """
        gate = TffWrapper(self._canvas,
                          pos[0], pos[1],
                          self.SignalToPort(q),
                          self.SignalToPort(t),
                          self.SignalToPort(clk),
                          self.SignalToPort(rst),
                          self.SignalToPort(s))
        self._addInstance(gate)

    def AddDff(self, pos, q, d, clk, rst = None, s = None):
        """ Create a D Flip-Flop

        pos: position to place gate at relative to containing module
        q: output
        d, clk: inputs
        rst,s: Reset/Set
        """
        gate = DffWrapper(self._canvas,
                          pos[0], pos[1],
                          self.SignalToPort(q),
                          self.SignalToPort(d),
                          self.SignalToPort(clk),
                          self.SignalToPort(rst),
                          self.SignalToPort(s))
        self._addInstance(gate)
    
    def AddModule(self, module, pos, name):
        """ Add a module
        
        module: already defined
        pos: where to position the module within containing module
        name: this can be displayed
        """
        # move the module and find its bounds
        module.Move(pos[0], pos[1], True)
        module._setBounds()
        inPorts = [p.GetShape() for p in module._inPorts]
        outPorts = [p.GetShape() for p in module._outPorts]
        # create bounding box
        boxShape = ogl.RectangleShape(module.GetWidth(), module.GetHeight())
        module._shape = ModuleShape(self._canvas, inPorts, outPorts, boxShape, [], [], False)
        # connect outer wires
        for port in module._shape._leftInShapes:
            signal = module._portShapeMap[port]
            self._canvas.ConnectWires(signal.GetShape(), port)
        for port in module._shape._outShapes:
            signal = module._portShapeMap[port]
            self._canvas.ConnectWires(signal.GetShape(), port)
        dc = wx.ClientDC(self._canvas)
        self._canvas.PrepareDC(dc)
        # when moving bouding box, it is relative to center
        module._shape.Move(dc,
                           module.GetX() + module.GetWidth() / 2,
                           module.GetY() + module.GetHeight() / 2,
                           False)
        module._shape._main.SetRegionName(name)
        self._modules.append(module)
    
    def Move(self, x, y, initial = False):
        """ Move the module and its contents
        This should be called when adding a Module
        
        initial: initially, all shapes need to be moved from original location
                 in order to be relative to the container
                 subsequent moves will just offset that
        """
        delta_x = x - self._x
        delta_y = y - self._y
        if not initial:
            self._x = self._x + delta_x
            self._y = self._y + delta_y
        else:
            self._x = x
            self._y = y

        if self._shape != None:
            dc = wx.ClientDC(self._canvas)
            self._canvas.PrepareDC(dc)
            self._shape.Move(dc,
                             self._x + self.GetWidth() / 2,
                             self._y + self.GetHeight() / 2,
                             False)
        # if rendered, then all subobjects are contained in the shape
        if not self._rendered:
            for module in self._modules:
                module.Move(delta_x + module.GetX(), delta_y + module.GetY(), False)
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
                    # just offset because we are in an outer module
                    shape.Move(dc,
                               shape.GetX() + delta_x,
                               shape.GetY() + delta_y,
                               False)

    def Render(self):
        """ This will add the Module and its contents to the canvas

        This also causes all contents to become child shapes
        which makes resize/move work
        """
        #if (self._shape != None):
        #    self._canvas.AddMyHDLModule(self._shape)
        if not self._rendered:
            for module in self._modules:
                self._canvas.AddMyHDLModule(module._shape)
            for gate in self._gates:
                self._canvas.AddMyHDLGate(gate.GetShape())
                if (self._shape != None):
                    self._shape.AddChild(gate.GetShape())
            for module in self._modules:
                module.Render()
                if (self._shape != None):
                    self._shape.AddChild(module.GetShape())
            self._rendered = True

    def GetModules(self):
        """ Get the children modules
        """
        return self._modules
    
    def GetInstances(self):
        """ Get MyHDL instances for the simulator (recursively get contents)
        """
        # here we need to recurse through sub modules when they exist
        instances = self._instances
        for module in self._modules:
            instances.extend(module.GetInstances())
        return instances
        
    def _addInstance(self, gate):
        """ Add an instance to the list

        gate: some type of gate
        """
        inst = gate.GetInstance()
        self._instances.append(inst)
        self._gates.append(gate)
    
    def _setBounds(self):
        """ This will draw a bounding box around a module, based on contents
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
        for module in self._modules:
            shape = module.GetShape()
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

    def ShowDetails(self, show = True):
        """ Toggles whether we show the inner workings or the simple shape
        """
        if show != self._showInternal:
            self._showInternal = show
            if self._showInternal:
                self._shape.ShowModule()
                self._shape._main.ClearText()
            else:
                self._shape.HideModule()
                self._shape._main.AddText(self._shape._main.GetRegionName())
        
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

    def Update(self):
        """ Update all ports and submodules (signal rendering)

        If we don't do this, intermediate shapes don't get updated
        """
        for module in self._modules:
            module.Update()
        for port in self._inPorts:
            port.Update()
        for port in self._outPortsInner:
            port.Update()
