import os
from multiprocessing import Process, Pipe
import wx
import wx.lib.ogl as ogl
from myhdl import Signal, Simulation, delay, instance
from MyHDLSim.Wrappers.SignalWrapper import EVT_SIGNAL_CHANGE, SignalWrapper
from MyHDLSim.Wrappers.NotGateWrapper import NotGateWrapper
from MyHDLSim.Wrappers.AndGateWrapper import AndGateWrapper
from MyHDLSim.Wrappers.OrGateWrapper import OrGateWrapper

class MyHDLManager:
    """ This class will manage the Signals and Gates and Simulator """
    def __init__(self, app):
        self._frame = MainWindow(None, 'Demo')
        self._canvas = self._frame.canvas
        self._app = app
        
        # get passed to MyHDL simulator (gates, event listening generators, etc.)
        self._instances = list()
        # quick look up of gates/signals by ID
        self._gates = []
        self._signals = []
        self._signalMap = {}
        
        #self._frame.Bind(EVT_SIGNAL_CHANGE, self.OnSignalChange)
        self._canvas.Bind(wx.EVT_CHAR, self.OnKey)
        self._canvas.SetFocus()
        
    def CreateSignal(self, initial = None):
        """ Create a signal which we can keep track of
        
        """
        signal = SignalWrapper(self._canvas, initial)
        signal.AddListener(self._frame)
        self._signals.append(signal)
        return signal
    
    def AddSwitch(self, pos, signal, key):
        """ Add a switch to an existing signal
        
        """
        signal.SetLabel(self._canvas, key)
        signal.SetX(pos[0])
        signal.SetY(pos[1])
        self._signalMap[ord(key)] = signal
        self._canvas.AddMyHDLSignal(signal.GetShape(), pos[0], pos[1])
        
    def AddProbe(self, pos, signal, label):
        """ Add a signal visually with a label but no key events
        
        """
        signal.SetLabel(self._canvas, label)
        signal.SetX(pos[0])
        signal.SetY(pos[1])
        self._canvas.AddMyHDLSignal(signal.GetShape(), pos[0], pos[1])
        
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
        
    def _addInstance(self, gate):
        inst = gate.GetInstance()
        self._instances.append(inst)
        self._gates.append(gate)
        
    def Start(self):
        """ Initialize and start the simulator """
        
        # we need a trick to run the simulator and the main loop...
        
        def EventLoop():
            @instance
            def inst():
                while(self._frame and not self._frame.exit):
                    yield delay(1)
                    self._refresh()
                    self._app.MainLoop()
                    print "exited main loop"
            return inst
        event_loop_runner = EventLoop()
        self._instances.append(event_loop_runner)

        self._simulator = Simulation(*self._instances)

        self._simulator.run()

    def OnKey(self, e):
        key = e.GetKeyCode()
        map = self._signalMap
        if (key in map):
            map[key].Toggle()
            self._app.ExitMainLoop()
        
    def _refresh(self):
        for s in self._signals:
            s.Update()
        self._canvas.Refresh(False)

class MyHDLCanvas(ogl.ShapeCanvas):
    def __init__(self, parent, frame):
        ogl.ShapeCanvas.__init__(self, parent)
        
        self.frame = frame
        self.SetBackgroundColour("LIGHT BLUE")
        self.SetSize((800, 600))
        self.diagram = ogl.Diagram()
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)
        self.gates = []
        self.signals = []
        
    def AddMyHDLGate(self, shape, pen = wx.BLACK_PEN, brush = wx.LIGHT_GREY_BRUSH):
        shape.SetCanvas(self)
        if pen:    shape.SetPen(pen)
        if brush:  shape.SetBrush(brush)
        self.diagram.AddShape(shape)
        shape.Show(True)

        self.gates.append(shape)
        return shape
    
    def AddMyHDLSignal(self, shape, x, y):
        if isinstance(shape, ogl.CompositeShape):
            dc = wx.ClientDC(self)
            self.PrepareDC(dc)
            shape.Move(dc, x, y)
        shape.SetCanvas(self)
        shape.SetX(x)
        shape.SetY(y)
        self.diagram.AddShape(shape)
        shape.Show(True)
        self.signals.append(shape)
    
    def ConnectWires(self, shapeA, shapeB):
        line = ogl.LineShape()
        line.SetCanvas(self)
        line.SetPen(wx.BLACK_PEN)
        line.SetBrush(wx.BLACK_BRUSH)
        line.MakeLineControlPoints(2)
        shapeA.AddLine(line, shapeB)
        self.diagram.AddShape(line)
        line.Show(True)
        
class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,600))
        
        self.CreateStatusBar()
        
        # menu
        filemenu = wx.Menu()
        
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
        
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)
        
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        
        #sizers
        self.buttonToolbar = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = []
        for i in range(0, 6):
            self.buttons.append(wx.Button(self, -1, "Button &"+str(i)))
            self.buttonToolbar.Add(self.buttons[i], 1, wx.EXPAND)
        
        self.canvas = MyHDLCanvas(self, self)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.buttonToolbar, 0, wx.EXPAND)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        
        self.Show(True)
        
        self.exit = False
    
    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "Trying to hook MyHDL up to wxPython", "About Demo", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
    
    def OnExit(self, e):
        self.Close(True)
        self.exit = True
        
        
def Init():
    app = wx.App(False)
    manager = MyHDLManager(app)
    ogl.OGLInitialize()
    return manager
    
