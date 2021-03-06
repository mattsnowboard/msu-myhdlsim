import wx, wx.lib.newevent
import wx.lib.ogl as ogl
from myhdl import Signal, always, intbv
from MyHDLSim.sequential import ClkDriver

# OGL object to draw a signal
class SignalOGLShape(ogl.CompositeShape):
    """ This shape is used exclusively to contruct the SIGNAL main shape.
        The shape is initially based within an 80x80 square, centered """
    def __init__(self, canvas, label):
        ogl.CompositeShape.__init__(self)
        
        self.SetCanvas(canvas)
        
        # Adds the 3 layed boxes to the Signal shape
        outterBox = ogl.RectangleShape(80, 80)
        self._innerBox = ogl.RectangleShape(60, 60)
        labelBox = ogl.RectangleShape(20,30)
        
        # Sets inital color brushes for boxes
        brush = wx.Brush("WHITE", wx.SOLID)
        outterBox.SetBrush(brush)
        self._innerBox.SetBrush(brush)
        labelBox.SetBrush(wx.Brush("MEDIUM TURQUOISE", wx.SOLID))
        
        labelBox.AddText(label)
        
        self.AddChild(outterBox)
        self.AddChild(self._innerBox)
        self.AddChild(labelBox)
        
        constraint = ogl.Constraint(ogl.CONSTRAINT_MIDALIGNED_TOP, outterBox, [labelBox])
        constraint2 = ogl.Constraint(ogl.CONSTRAINT_CENTRED_BOTH, outterBox, [self._innerBox])
        self.AddConstraint(constraint)
        self.AddConstraint(constraint2)
        self.Recompute()
        
        # If we don't do this, the shapes will be able to move on their
        # own, instead of moving the composite
        outterBox.SetDraggable(False)
        self._innerBox.SetDraggable(False)
        labelBox.SetDraggable(False)

        # If we don't do this the shape will take all left-clicks for itself
        outterBox.SetSensitivityFilter(0)
        
    # Manual override for normal function: Allows us to easily change the inner box color
    def SetBrush(self, brush):
        self._innerBox.SetBrush(brush)


class SignalWrapper:
    """ This class wraps a MyHDL.Signal object
    
    Handles wx event listening, toggling, and getting an object to draw
    """
    
    def __init__(self, canvas, signal = None, width = 1, label = ''):
        """

        @todo assert that width >= 1
        """
        self._label = label
        if (width == 1):
            self._signal = Signal(signal)
        else:
            self._signal = Signal(intbv(signal)[width:])
        self._shape = ogl.RectangleShape(10,10)
        self._shape.AddText(str(self._signal.val))
        
    def SetSwitch(self, canvas, label):
        """ Setting a label, need to recreate shape
        
        """
        self._label = label
        self._shape = SignalOGLShape(canvas, label)
        self._shape.AddText(str(self._signal.val))

    def SetProbe(self, canvas, a, label):
        """ Sets signal as a probe, need to recreate shape
        
        """
        self._label = label
        self._signal = a._signal
        self._shape = SignalOGLShape(canvas, label)
        self._shape.AddText(str(self._signal.val))
        canvas.ConnectWires(self._shape, a.GetShape())

    def SetInputProbe(self, canvas, a, label):
        """ Sets signal as a probe, need to recreate shape
        
        @todo May be an output probe as well, name could change
        """
        self._label = label
        self._signal = a._signal
        canvas.ConnectWires(self._shape, a.GetShape())

    def SetClockDriver(self, canvas, label, period = 20):
        """ Setting as a clock, need to recreate shape

        """
        self._label = label
        self._shape = SignalOGLShape(canvas, label)
        self._shape.AddText("Clock")
        self._inst = ClkDriver(self._signal, period)
    
    def GetSignal(self):
        """ Get the underlying object
        """
        return self._signal
    
    def Toggle(self):
        """ Toggle the signal value
        
        If it was unitialized, just assert it
        """

        if (len(self._signal) > 1):
            if (self._signal + 1 == self._signal.max):
                self._signal.next = 0
            else:
                self._signal.next = self._signal + 1
        elif (self._signal == None):
            self._signal.next = True
        else:
            self._signal.next = not self._signal
        
    def Update(self):
        """ This visually refreshes a Signal
        
        Caller must know when Signal has changed
        """
        self._shape.ClearText()
        if self._shape.GetBrush() != wx.TRANSPARENT_BRUSH:
            # For now we are printing TEXT "True", "False", or "None"
            # Also setting inner box color (White: False; Black: True; Grey: None)
            if (self._signal.val == None):
                self._shape.AddText(str(self._signal.val))
                self._shape.SetBrush(wx.Brush("GREY", wx.SOLID))
                self._shape.SetTextColour("BLACK")
            elif (len(self._signal) > 1):
                self._shape.AddText(bin(self._signal.val))
                self._shape.SetBrush(wx.Brush("WHITE", wx.SOLID))
                self._shape.SetTextColour("BLACK")
            elif (bool(self._signal.val) == False):
                self._shape.AddText(str(bool(self._signal.val)))
                self._shape.SetBrush(wx.Brush("WHITE", wx.SOLID))
                self._shape.SetTextColour("BLACK")
            else:
                self._shape.AddText(str(bool(self._signal.val)))
                self._shape.SetBrush(wx.Brush("BLACK", wx.SOLID))
                self._shape.SetTextColour("WHITE")
    
    def SetX(self, x):
        self._x = x
        
    def SetY(self, y):
        self._y = y
    
    def GetShape(self):
        return self._shape

    def GetInstance(self):
        """ Get instance for simulator """
        return self._inst
    
