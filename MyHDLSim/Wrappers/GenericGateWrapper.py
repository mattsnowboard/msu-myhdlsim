import wx
import wx.lib.ogl as ogl

class GenericGateShape(ogl.CompositeShape):
    def __init__(self, canvas, label, outputShape):
        ogl.CompositeShape.__init__(self)
        
        self.SetCanvas(canvas)
        
	# Change me once we stop using rectangles for all gates
        self._gate = ogl.RectangleShape(100, 100)
	#output._shape = ogl.RectangleShape(10,10)
	#outputShape = output._shape
               
        self._gate.AddText(label)
        
        self.AddChild(self._gate)
        self.AddChild(outputShape)
        
	# Locks the output to the right of the gate, then adds the wires
        constraint = ogl.Constraint(ogl.CONSTRAINT_MIDALIGNED_RIGHT, self._gate, [outputShape])
	constraint.SetSpacing(10,0)
        self.AddConstraint(constraint)
        self.Recompute()
	canvas.ConnectWires(self._gate, outputShape)
        
        # If we don't do this, the shapes will be able to move on their
        # own, instead of moving the composite
        self._gate.SetDraggable(False)
	outputShape.SetDraggable(False)

        # If we don't do this the shape will take all left-clicks for itself
        self._gate.SetSensitivityFilter(0)

class GenericGateWrapper:
    """ This class wraps a gate for drawing
    
    It can be any type of gate and this handles common code like connecting wires
    """
    
    def __init__(self, drawManager, x, y, out, label):
        """
        x, y : position of the gate
        """
        self._signals = list()
        # default shape that other classes SHOULD override
        self._shape = GenericGateShape(drawManager, label, out.GetShape())
     	dc = wx.ClientDC(drawManager)
    	drawManager.PrepareDC(dc)
    	self._shape.Move(dc, x, y)
    
    def _addSignal(self, signal):
        """ Add signal
        
        Derived classes must add all signals so that they can be connected
        signal : a signal on the gate which we will visually connect in the UI
        """
        self._signals.append(signal)
    
    def _connectWires(self, drawManager):
        """ Connect wires from ports to signals
        
        drawManager -- class that knows how to draw the shapes and draw lines between them
        """
        for s in self._signals:
            if (s != None):
                drawManager.ConnectWires(self._shape._gate, s.GetShape())
        
    def GetInstance(self):
        """ Get instance for simulator """
        return self._inst
