import os
import wx
import wx.lib.ogl as ogl

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
        
