import os
import wx
import wx.lib.ogl as ogl
from MyHDLSim.Module import EVT_MODULE_MOVE, ModuleMoveEvent

class MyEvtHandler(ogl.ShapeEvtHandler):
    """
        This is used to handle events on the OGL shapes
        Needed to make resizing work
    """
    def __init__(self, canvas, manager):
        ogl.ShapeEvtHandler.__init__(self)
        self._canvas = canvas
        self._manager = manager

    def OnLeftClick(self, x, y, keys=0, attachment=0):
        shape = self.GetShape()
        canvas = shape.GetCanvas()
        dc = wx.ClientDC(canvas)
        canvas.PrepareDC(dc)

        if shape.Selected():
            shape.Select(False, dc)
            #canvas.Redraw(dc)
            canvas.Refresh(False)
        else:
            redraw = False
            shapeList = canvas.GetDiagram().GetShapeList()
            toUnselect = []

            for s in shapeList:
                if s.Selected():
                    # If we unselect it now then some of the objects in
                    # shapeList will become invalid (the control points are
                    # shapes too!) and bad things will happen...
                    toUnselect.append(s)

            shape.Select(True, dc)

            if toUnselect:
                for s in toUnselect:
                    s.Select(False, dc)

                ##canvas.Redraw(dc)
                canvas.Refresh(False)
    
    def OnSizingEndDragLeft(self, pt, x, y, keys, attch):
        ogl.ShapeEvtHandler.OnSizingEndDragLeft(self, pt, x, y, keys, attch)
        # refresh to clear artifacts when shrinking
        self.GetShape().GetCanvas().Refresh(False)
    
    def OnEndDragLeft(self, x, y, keys=0, attachment=0):
        shape = self.GetShape()
        ogl.ShapeEvtHandler.OnEndDragLeft(self, x, y, keys, attachment)
        # module background moves all contents
        if shape in self._canvas.modules:
            evt = ModuleMoveEvent(Shape = shape)
            wx.PostEvent(self._manager.GetFrame(), evt)
            # refresh to clear artifacts when moving a module
            self.GetShape().GetCanvas().Refresh(False)
        if not shape.Selected():
            self.OnLeftClick(x, y, keys, attachment)

class MyHDLCanvas(ogl.ShapeCanvas):
    def __init__(self, parent, frame):
        ogl.ShapeCanvas.__init__(self, parent)
        
        self.frame = frame
        self.manager = None
        self.SetBackgroundColour("LIGHT BLUE")
        self.SetSize((800, 600))
        self.diagram = ogl.Diagram()
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)
        self.gates = []
        self.modules = []
        self.signals = []
        
    def SetManager(self, manager):
        """ This is needed for some event handling
        """
        self.manager = manager
    
    def AddMyHDLGate(self, shape, pen = wx.BLACK_PEN, brush = wx.LIGHT_GREY_BRUSH):
        shape.SetCanvas(self)
        if pen:    shape.SetPen(pen)
        if brush:  shape.SetBrush(brush)
        self.diagram.AddShape(shape)
        shape.Show(True)
        self.RegisterEvents(shape)
        
        self.gates.append(shape)
        return shape
        
    def AddMyHDLModule(self, shape, pen = wx.BLACK_PEN, brush = wx.WHITE_BRUSH):
        shape.SetCanvas(self)
        if pen:    shape.SetPen(pen)
        if brush:  shape.SetBrush(brush)
        self.diagram.InsertShape(shape)
        shape.Show(True)
        self.RegisterEvents(shape)
        
        self.modules.append(shape)
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
        self.RegisterEvents(shape)
        
        self.signals.append(shape)
    
    def RegisterEvents(self, shape):
        evthandler = MyEvtHandler(self, self.manager)
        evthandler.SetShape(shape)
        evthandler.SetPreviousHandler(shape.GetEventHandler())
        shape.SetEventHandler(evthandler)
    
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
        
