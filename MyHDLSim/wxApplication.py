import os
from multiprocessing import Process, Pipe
import wx
import wx.lib.ogl as ogl
from myhdl import Signal, Simulation, delay, instance
from MyHDLSim.SignalWrapper import EVT_SIGNAL_CHANGE, SignalWrapper
from MyHDLSim.AndGateWrapper import AndGateWrapper

def StartSim(conn):
    sim = conn.recv()
    sim.run()
    

def StartApp(app):
    app.MainLoop()
    
class MyHDLManager:
    """ This class will manage the Signals and Gates and Simulator """
    def __init__(self, canvas, frame, app):
        self._canvas = canvas
        self._frame = frame
        self._app = app
        # get passed to MyHDL simulator (gates, event listening generators, etc.)
        self._instances = list()
        # quick look up of gates/signals by ID
        self._gates = []
        self._signals = []
        self._signalMap = {}
        
        
    def CreateSignal(self):
        """ Create a signal which we can keep track of
        
        """
        signal = SignalWrapper()
        signal.AddListener(self._frame)
        self._signals.append(signal)
        return signal
    
    def AddSwitch(self, pos, signal, key):
        """ Add a switch to an existing signal
        
        """
        signal.SetX(pos[0])
        signal.SetY(pos[1])
        self._instances.append(signal.GetGenerator())
        self._signalMap[ord(key)] = signal
        self._canvas.AddMyHDLSignal(signal.GetShape())
    
    def AddAndGate(self, pos, out, a, b, c = None, d = None):
        """ Create an AND gate
        
        """
        gate = AndGateWrapper(self._canvas, pos[0], pos[1], out, a, b, c, d)
        inst = gate.GetInstance()
        self._instances.append(inst)
        self._gates.append(gate)
        
    def Start(self):
        """ Initialize and start the simulator """
        
        print "START"
        
        # we need a trick to run the simulator and the main loop...
        
        def Hack():
            @instance
            def inst():
                while(not self._frame.exit):
                    yield(delay(1))
                    self._app.MainLoop()
            return inst
        MyHack = Hack()
        self._instances.append(MyHack)
        #parent_conn, child_conn = Pipe()
        self._simulator = Simulation(*self._instances)
        #p = Process(target=StartSim, args=(child_conn,))
        #p.start()
        #parent_conn.send(self._simulator)
        self._simulator.run()
        #self._app.MainLoop()
        #p.join()
    
    def GetKeyMap(self):
        """ Get key map for figuring out what to do with events
        
        """
        return self._signalMap

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

        #evthandler = MyEvtHandler(self.log, self.frame)
        #evthandler.SetShape(shape)
        #evthandler.SetPreviousHandler(shape.GetEventHandler())
        #shape.SetEventHandler(evthandler)

        self.gates.append(shape)
        return shape
    
    def AddMyHDLSignal(self, shape):
        shape.SetCanvas(self)
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
    def __init__(self, parent, app, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,600))
        #self.panel = wx.Panel(self, size=(1,1))
        #self.panel.SetFocus()
        #self.panel.Show(False)
        #self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
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
        
        # not sure about these parameters...
        self.canvas = MyHDLCanvas(self, self)
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.buttonToolbar, 0, wx.EXPAND)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        
        # manager handles interaction with MyHDL
        self.app = app
        self.manager = MyHDLManager(self.canvas, self, app)

        #events from signals
        self.Bind(EVT_SIGNAL_CHANGE, self.OnSignalChange)
        self.canvas.Bind(wx.EVT_CHAR, self.OnKey)
        self.canvas.SetFocus()
        
        self.exit = False
        
        self.Show(True)
    
    def OnKey(self, e):
        print "HEYYYY"
        key = e.GetKeyCode()
        print key
        map = self.manager.GetKeyMap()
        if (key in map):
            print "IN"
            map[key].Toggle()
            self.app.ExitMainLoop()
        
    def OnSignalChange(self, e):
        print "CHANGE"
        self.canvas.Refresh(False)
    
    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "Trying to hook MyHDL up to wxPython", "About Demo", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
    
    def OnExit(self, e):
        self.Close(True)
        self.exit = True
        
        
def Init():
    app = wx.App(False)
    ogl.OGLInitialize()
    frame = MainWindow(None, app, 'Demo')
    return frame.manager
    
