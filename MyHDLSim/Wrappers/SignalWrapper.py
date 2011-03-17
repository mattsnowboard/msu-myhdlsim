import wx, wx.lib.newevent
import wx.lib.ogl as ogl
from myhdl import Signal, always

# The events that wx side will listen for (must register self for this)
SignalChangeEvent, EVT_SIGNAL_CHANGE = wx.lib.newevent.NewEvent() 

# OGL object to draw a signal
# this code is pretty much from the OGL demo, hope it looks ok for now
class SignalOGLShape(ogl.CompositeShape):
    def __init__(self, canvas, label):
        ogl.CompositeShape.__init__(self)
        
        self.SetCanvas(canvas)
        
        container = ogl.RectangleShape(80, 50)
        label_shape = ogl.RectangleShape(40, 30)
        
        container.SetBrush(wx.Brush("MEDIUM TURQUOISE", wx.SOLID))
        label_shape.SetBrush(wx.Brush("MEDIUM TURQUOISE", wx.SOLID))
        
        label_shape.AddText(label)
        
        self.AddChild(container)
        self.AddChild(label_shape)
        
        constraint = ogl.Constraint(ogl.CONSTRAINT_MIDALIGNED_TOP, container, [label_shape])
        self.AddConstraint(constraint)
        self.Recompute()
        
        # If we don't do this, the shapes will be able to move on their
        # own, instead of moving the composite
        container.SetDraggable(False)
        label_shape.SetDraggable(False)

        # If we don't do this the shape will take all left-clicks for itself
        container.SetSensitivityFilter(0)

class SignalWrapper:
    """ This class wraps a MyHDL.Signal object
    
    Handles wx event listening, toggling, and getting an object to draw
    """
    
    def __init__(self, canvas, signal = None, x = 0, y = 0, label = '', listener = None):
        self._label = label
        self._signal = Signal(signal)
        self._listeners = list()
        if listener != None:
            self.AddListener(listener)
        self._shape = SignalOGLShape(canvas, label)
        self._shape.AddText(str(self._signal.val))
        #self._shape.SetX(x)
        #self._shape.SetY(y)
    
    def AddListener(self, listener):
        """ Add Listener to Signal
        
        Must be done BEFORE getting instance and creating Simulator
        """
        
        self._listeners.append(listener)
    
    def RemoveListener(self, listener):
        """ Remove Listener from Signal
        
        Must be done BEFORE getting instance and creating Simulator
        """
        
        self._listeners.remove(listener)
    
    def SetLabel(self, canvas, label):
        """ Setting a label, need to recreate shape
        
        """
        self._label = label
        self._shape = SignalOGLShape(canvas, label)
        self._shape.AddText(str(self._signal.val))
    
    def GetSignal(self):
        """ Get the underlying object
        """
        return self._signal
    
    def Toggle(self):
        """ Toggle the signal value
        
        If it was unitialized, just assert it
        """
        
        if (self._signal == None):
            self._signal.next = True
        else:
            self._signal.next = not self._signal
        
    def Update(self):
        """ This visually refreshes a Signal
        
        Caller must know when Signal has changed
        """
        self._shape.ClearText()
        # For now we are printing TEXT "True", "False", or "None"
        # Change me if you want something else
        if (self._signal.val == None):
            self._shape.AddText(str(self._signal.val))
        else:
            self._shape.AddText(str(bool(self._signal.val)))
        #evt = SignalChangeEvent(val = self._signal.val)
    
    def SetX(self, x):
        self._x = x
        
    def SetY(self, y):
        self._y = y
    
    def GetShape(self):
        return self._shape
    