import wx
import wx.lib.ogl as ogl

class GenericGateShape(ogl.CompositeShape):
    def __init__(self, canvas, numins, outshape, gateshape):
        ogl.CompositeShape.__init__(self)
        
        self.SetCanvas(canvas)
        
        # Sets main gate object from gate wrapper
        self._gate = gateshape
        self.AddChild(self._gate)

        # Determine spacing
        if (numins != 1):
            YspaceIns = (80 - 10*numins) / (numins-1)

        # Initalize & set up 'In' objects
        self._inShapes = [ogl.RectangleShape(10,10) for i in range(numins)]
        for ob in self._inShapes:
            self.AddChild(ob)
            canvas.ConnectWires(self._gate, ob)
            #ob.SetDraggable(False)

        constraintIns = ogl.Constraint(ogl.CONSTRAINT_LEFT_OF, self._gate, self._inShapes)
        constraintIns.SetSpacing(10, 0)
        self.AddConstraint(constraintIns)
        if (numins > 1): 
            for q in range(numins):
                self._inShapes[q-1].SetY((10 + YspaceIns)*(q) - 35)


        # Connect and setup 'Out' object
        self.AddChild(outshape)
        canvas.ConnectWires(self._gate, outshape)
        outshape.SetDraggable(False)
        constraintOut = ogl.Constraint(ogl.CONSTRAINT_RIGHT_OF, self._gate, [outshape])
        constraintOut.SetSpacing(10,0)
        self.AddConstraint(constraintOut)


        self.Recompute()
        
        self._gate.SetDraggable(False)

        # If we don't do this the shape will take all left-clicks for itself
        self._gate.SetSensitivityFilter(0)


class GenericGateWrapper:
    """ This class wraps a gate for drawing
    
    It can be any type of gate and this handles common code like connecting wires
    """
    
    def __init__(self, drawManager, x, y, ins, gateshape, out):
        """
        x, y : position of the gate
        """
        PurgeList(ins)
        self._inSignals = ins
	
        # default shape that other classes SHOULD override
        self._shape = GenericGateShape(drawManager, len(ins), out.GetShape(), gateshape)
        dc = wx.ClientDC(drawManager)
        drawManager.PrepareDC(dc)
        self._shape.Move(dc, x, y)
    
    """def _addSignal(self, signal):
        """""" Add signal
        
        Derived classes must add all signals so that they can be connected
        signal : a signal on the gate which we will visually connect in the UI
        """"""
        self._signals.append(signal)"""
    
    def _connectWires(self, drawManager):
        """ Connect wires from ports to signals
        
        drawManager -- class that knows how to draw the shapes and draw lines between them
        """
        for i in range(len(self._inSignals)):
            drawManager.ConnectWires(self._shape._inShapes[i-1], self._inSignals[i-1].GetShape())
        """for s in self._signals:
            if (s != None):
                drawManager.ConnectWires(self._shape._gate, s.GetShape())"""
        
    def GetInstance(self):
        """ Get instance for simulator """
        return self._inst

def PurgeList(a):
    count = a.count(None)
    for i in range(count):
        a.remove(None)

