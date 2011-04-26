import os
import wx
import wx.lib.ogl as ogl
import time
import threading

wxEVT_THREAD_TIMER = wx.NewEventType()
EVT_THREAD_TIMER = wx.PyEventBinder(wxEVT_THREAD_TIMER, 1)

class MyEvtHandler(ogl.ShapeEvtHandler):
    """
        This is used to handle events on the OGL shapes
        Needed to make resizing work
    """
    def __init__(self, canvas, manager):
        """

        canvas: we need this for a lot of calls
        manager: used to pass events
        """
        ogl.ShapeEvtHandler.__init__(self)
        self._canvas = canvas
        self._manager = manager

    def OnLeftClick(self, x, y, keys=0, attachment=0):
        """ Used for item selection """
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
        """ Used for resize to clear artifacts """
        ogl.ShapeEvtHandler.OnSizingEndDragLeft(self, pt, x, y, keys, attch)
        # refresh to clear artifacts when shrinking
        self.GetShape().GetCanvas().Refresh(False)
    
    def OnEndDragLeft(self, x, y, keys=0, attachment=0):
        """ Used to make a module move its contents

        @todo: Remove this?
        """
        shape = self.GetShape()
        ogl.ShapeEvtHandler.OnEndDragLeft(self, x, y, keys, attachment)
        # drag should also select
        if not shape.Selected():
            self.OnLeftClick(x, y, keys, attachment)

class MyHDLCanvas(ogl.ShapeCanvas):
    """ Custom canvas class to hold our shapes """
    def __init__(self, parent, frame):
        """ Creates the canvas and empty lists """
        ogl.ShapeCanvas.__init__(self, parent)
        
        self._frame = frame
        self._manager = None
        self.SetBackgroundColour("LIGHT BLUE")
        self.SetSize((800, 600))
        self._diagram = ogl.Diagram()
        self.SetDiagram(self._diagram)
        self._diagram.SetCanvas(self)
        self._gates = []
        self._modules = []
        self._signals = []
        self._connections = []
        
    def SetManager(self, manager):
        """ This is needed for some event handling, but can't set on init
        """
        self._manager = manager
    
    def AddMyHDLGate(self, shape, pen = wx.BLACK_PEN, brush = wx.LIGHT_GREY_BRUSH):
        """ Add a gate to the diagram and register its events

        return: the shape just in case?
        """
        shape.SetCanvas(self)
        if pen:    shape.SetPen(pen)
        if brush:  shape.SetBrush(brush)
        self._diagram.AddShape(shape)
        shape.Show(True)
        self._RegisterEvents(shape)
        
        self._gates.append(shape)
        return shape
        
    def AddMyHDLModule(self, shape, pen = wx.BLACK_PEN, brush = wx.WHITE_BRUSH):
        """ Add a module to the diagram and register its events

        return: the shape just in case?
        """
        shape.SetCanvas(self)
        if pen:    shape.SetPen(pen)
        if brush:  shape.SetBrush(brush)
        self._diagram.AddShape(shape)
        shape.Show(True)
        self._RegisterEvents(shape)
        
        self._modules.append(shape)
        return shape
        
    def AddMyHDLSignal(self, shape, x, y, reg = True):
        """ Add a signal to the diagram and register its events

        Moves it to a location x,y
        """
        if isinstance(shape, ogl.CompositeShape):
            dc = wx.ClientDC(self)
            self.PrepareDC(dc)
            shape.Move(dc, x, y)
        shape.SetCanvas(self)
        shape.SetX(x)
        shape.SetY(y)
        self._diagram.AddShape(shape)
        shape.Show(True)
        if reg:
            self._RegisterEvents(shape)
        
        self._signals.append(shape)
    
    def _RegisterEvents(self, shape):
        """ Each shape must have event handler """
        evthandler = MyEvtHandler(self, self._manager)
        evthandler.SetShape(shape)
        evthandler.SetPreviousHandler(shape.GetEventHandler())
        shape.SetEventHandler(evthandler)

    def GetModules(self):
        """ Access the module list """
        return self._modules
    
    def ConnectWires(self, shapeA, shapeB):
        """ Connect wires once everything is ready
        Actual connecting is deferred

        This just adds to a list of things to connect at the end
        because shapes have not yet been added
        """
        self._connections.append((shapeA, shapeB))

    def ConnectAllWires(self):
        """ Connect the pending wires now that shares are added
        """
        for (shapeA, shapeB) in self._connections:
            line = ogl.LineShape()
            line.SetCanvas(self)
            line.SetPen(wx.BLACK_PEN)
            line.SetBrush(wx.BLACK_BRUSH)
            line.MakeLineControlPoints(2)
            shapeA.AddLine(line, shapeB)
            self._diagram.AddShape(line)
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
        self._buttonToolbar = wx.BoxSizer(wx.HORIZONTAL)
        self._buttons = []
        # Pause Button
        self._buttons.append(wx.Button(self, -1, "Pause Simulation"))
        self._buttonToolbar.Add(self._buttons[0], 1, wx.EXPAND)
        self._buttons[0].Bind(wx.EVT_BUTTON, self._OnPauseClick)
        self._buttons[0].SetToolTip(wx.ToolTip("Click to Pause"))
        # Play button
        self._buttons.append(wx.Button(self, -1, "Play Simulation"))
        self._buttonToolbar.Add(self._buttons[1], 1, wx.EXPAND)
        self._buttons[1].Disable()
        self._buttons[1].Bind(wx.EVT_BUTTON, self._OnPlayClick)
        self._buttons[1].SetToolTip(wx.ToolTip("Click to Play"))

        for i in range(2, 6):
            self._buttons.append(wx.Button(self, -1, "Button &"+str(i)))
            self._buttonToolbar.Add(self._buttons[i], 1, wx.EXPAND)
        
        self._canvas = MyHDLCanvas(self, self)
        
        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self._sizer.Add(self._buttonToolbar, 0, wx.EXPAND)
        self._sizer.Add(self._canvas, 1, wx.EXPAND)
        
        self.SetSizer(self._sizer)
        self.SetAutoLayout(1)
        self._sizer.Fit(self)
        
        self.Show(True)
        
        self._exit = False

    def GetCanvas(self):
        """ Access to the canvas to draw on
        """
        return self._canvas
    
    def OnAbout(self, e):
        dlg = wx.MessageDialog(self, "Trying to hook MyHDL up to wxPython", "About Demo", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
    
    def OnExit(self, e):
        self.Close(True)
        self._exit = True

    def IsExit(self):
        return self._exit

    def _OnPauseClick(self, e):
        self._buttons[1].Enable()
        self._canvas._manager._pause = True
        self._buttons[0].Disable()
        self._canvas.SetFocus()

    def _OnPlayClick(self, e):
        self._buttons[1].Disable()
        self._buttons[0].Enable()
        self._canvas._manager._pause = False
        self._canvas.SetFocus()

"""
Credit to below two classes goes to http://stackoverflow.com/questions/1277968/wxpython-wx-calllater-being-very-late
Classes have been altered to fit programs naming scheme
"""
class ThreadTimer(object):
   def __init__(self, parent):
        self._parent = parent
        self._thread = Thread()
        self._thread._parent = self
        self._alive = False

   def start(self, interval):
       self._interval = interval
       self._alive = True
       self._thread.start()

   def stop(self):
       self._alive = False

class Thread(threading.Thread):
    def run(self):
       while self._parent._alive:
           time.sleep(self._parent._interval / 1000.0)
           if self._parent._alive:
               event = wx.PyEvent()
               event.SetEventType(wxEVT_THREAD_TIMER)
               wx.PostEvent(self._parent._parent, event)
