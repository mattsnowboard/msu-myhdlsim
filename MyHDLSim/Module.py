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
from MyHDLSim.Wrappers.GenericGateWrapper import GenericGateShape
from myhdl import always_comb

# The events that wx side will listen for, used to move contents of a Module
ModuleMoveEvent, EVT_MODULE_MOVE = wx.lib.newevent.NewEvent() 

class ModuleShape(ogl.CompositeShape):
    def __init__(self, canvas, moduleShape, inputPorts, outputPorts):
        """ Creates a ModuleShape which is a rectangle with port squares

        @todo: reuse GenericGateWrapper shape code somehow
        canvas: where to draw shapes
        moduleShape: main shape (usually rectangle)
        inputPorts: shapes to draw as input ports (left side)
        outputPorts: shapes to draw as output ports (right side)
        """
        ogl.CompositeShape.__init__(self)

        print "DO NOT USE ME*****************************************"

        self.SetCanvas(canvas)

        self._main = moduleShape
        #self._main.SetBrush(wx.Brush(wx.Colour(0,0,0,0),wx.TRANSPARENT))
        self.AddChild(self._main)

        # Determine spacing
        numIn = len(inputPorts)
        numOut = len(outputPorts)
        if (numIn != 1):
            YspaceIns = (self._main.GetHeight() - 10 * numIn) / (numIn - 1)
        if (numOut != 1):
            YspaceOuts = (self._main.GetHeight() - 10 * numOut) / (numOut - 1)

        # Initalize & set up 'In' objects
        self._inShapes = inputPorts
        for ob in self._inShapes:
            self.AddChild(ob)
            #canvas.ConnectWires(self._main, ob)
            ob.SetDraggable(False)

        constraintIns = ogl.Constraint(ogl.CONSTRAINT_LEFT_OF, self._main, self._inShapes)
        constraintIns.SetSpacing(0, 10)
        self.AddConstraint(constraintIns)

        if (numIn > 1): 
            for q in range(numIn):
                self._inShapes[q].SetY(YspaceIns * q - (self._main.GetHeight() / 2 - 10))

        # Initalize & set up 'Out' objects
        self._outShapes = outputPorts
        for ob in self._outShapes:
            self.AddChild(ob)
            canvas.ConnectWires(self._main, ob)
            ob.SetDraggable(False)

        constraintOuts = ogl.Constraint(ogl.CONSTRAINT_RIGHT_OF, self._main, self._outShapes)
        constraintOuts.SetSpacing(10, 0)
        self.AddConstraint(constraintOuts)
        if (numOut > 1): 
            for q in range(numOut):
                self._outShapes[q-1].SetY(-YspaceOuts * q)


        self.Recompute()
        
        self._main.SetDraggable(False)

        # If we don't do this the shape will take all left-clicks for itself
        self._main.SetSensitivityFilter(0)

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
        
        self._shape = None
        
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
    
    def AddPort(self, pos, signal, is_input, label):
        """ Add a port to interface with the module
        
        pos: (x, y) tuple to place the port within the module
        signal: signal to feed to the port
        is_input: boolean set to True for input, False for output
        label: displayed on module

        return: The signal so we can connect to it!
        """
        if (is_input):
            port = SignalWrapper(self._canvas, signal.GetSignal().val, pos[0], pos[1])
            port.AddListener(self._manager._frame)
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
            port = SignalWrapper(self._canvas, signal.GetSignal().val, pos[0], pos[1])
            port.AddListener(self._manager._frame)
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
        pos: where to position the module within containing module
        name: this can be displayed

        @todo: Use the name!
        """
        # move the module and find its bounds
        module.Move(pos[0], pos[1], True)
        module._setBounds()
        # create bounding box
        boxShape = ogl.RectangleShape(module.GetWidth(), module.GetHeight())
        inPorts = [p.GetShape() for p in module._inPorts]
        outPorts = [p.GetShape() for p in module._outPorts]
        module._shape = GenericGateShape(self._canvas, inPorts, outPorts, boxShape, False)
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
        #self._canvas.AddMyHDLModule(module._shape)
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
