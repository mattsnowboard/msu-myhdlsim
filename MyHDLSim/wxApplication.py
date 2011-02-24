import os
import wx
import wx.lib.ogl as ogl
from myhdl import Signal, Simulation, delay
import MyHDLSim.SignalWrapper as SignalWrapper

class MyHDLManager:
    """ This class will manage the Signals and Gates and Simulator """
    def __init___(self, canvas, frame):
        self._canvas = canvas
        self._frame = frame
        # get passed to MyHDL simulator (gates, event listening generators, etc.)
        self._instances = list()
        # quick look up of gates/signals by ID
        self._gates = []
        self._signals = []
        
        
    def CreateSignal():
        pass

class MyHDLCanvas(ogl.ShapeCanvas):
    def __init__(self, parent, frame):
        ogl.ShapeCanvas.__init__(self, parent)
        
        self.frame = frame
        self.SetBackgroundColour("LIGHT BLUE")
        self.diagram = ogl.Diagram()
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)
        self.gates = []
        self.signals = []
        
    def AddMyHDLGate(self, shape, text = False, pen = wx.BLACK_PEN, brush = wx.LIGHT_GREY_BRUSH):
        shape.SetCanvas(self)
        if pen:    shape.SetPen(pen)
        if brush:  shape.SetBrush(brush)
        if text:
            for line in text.split('\n'):
                shape.AddText(line)
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
        
class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,600))
        #self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar()
        
        # menu
        filemenu = wx.Menu()
        
        menuTest = filemenu.Append(wx.ID_ABOUT, "&Test", "Not sure...")
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
        
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)
        
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnKeyDown, menuTest)
        
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
                
        #events from signals
        #self.Bind(EVT_SIGNAL_CHANGE, self.OnSignalChange)
        #self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        
        self.Show(True)
        
    def OnKeyDown(self, e):
        
        # key = event.KeyCode()
        # shiftDown = event.ShiftDown()
        # if key in (ord('A'), ord('a')):
            # if shiftDown:
                # self.gate.SetA(1)
            # else:
                # self.gate.SetA(0)
        # elif key in (ord('B'), ord('b')):
            # if shiftDown:
                # self.gate.SetB(1)
            # else:
                # self.gate.SetB(0)
        # self.sim.Run(1)
        
    def OnSignalChange(self, e):
        pass
    
    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "Trying to hook MyHDL up to wxPython", "About Demo", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
    
    def OnExit(self, e):
        self.Close(True)
        


app = wx.App(False)
ogl.OGLInitialize()

frame = MainWindow(None, 'Demo')
app.MainLoop()