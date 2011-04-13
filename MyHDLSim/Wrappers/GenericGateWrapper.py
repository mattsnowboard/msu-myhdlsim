import wx
import wx.lib.ogl as ogl

class GenericGateShape(ogl.CompositeShape):
    def __init__(self, canvas, inLeftShapes, outShapes, mainShape, doConnect = True):
        ogl.CompositeShape.__init__(self)
        
        self.SetCanvas(canvas)
        
        # Sets main gate object from gate wrapper
        self._main = mainShape
        self.AddChild(self._main)

        # Determine spacing
        numLeftIn = len(inLeftShapes)
        numOut = len(outShapes)
        shapeHeight = self._main.GetBoundingBoxMin()[1]
        if isinstance(self._main, ogl.CompositeShape):
            shapeHeight = self._main.GetHeight()        
        leftInHeight = 0
        if (numLeftIn > 0):
            leftInHeight = inLeftShapes[0].GetHeight()
        if (numLeftIn > 1):
            YspaceLeftIns = (shapeHeight - leftInHeight * numLeftIn) / (numLeftIn)
        outHeight = 0
        if (numOut > 0):
            outHeight = outShapes[0].GetHeight()
        if (numOut > 1):
            YspaceOuts = (shapeHeight - outHeight * numOut) / (numOut)

        # Initalize & set up 'In' objects
        self._leftInShapes = inLeftShapes
        for ob in self._leftInShapes:
            self.AddChild(ob)
            if doConnect:
                canvas.ConnectWires(self._main, ob)
            ob.SetDraggable(False)

        constraintLeftIns = ogl.Constraint(ogl.CONSTRAINT_LEFT_OF, self._main, self._leftInShapes)
        constraintLeftIns.SetSpacing(10, 0)
        self.AddConstraint(constraintLeftIns)
        if (numLeftIn > 1): 
            for q in range(numLeftIn):
                self._leftInShapes[q].SetY(YspaceLeftIns / 2 + (YspaceLeftIns + leftInHeight) * q - (shapeHeight / 2 - leftInHeight / 2))

        # Connect and setup 'Out' object
        self._outShapes = outShapes
        for ob in self._outShapes:
            self.AddChild(ob)
            if doConnect:
                canvas.ConnectWires(self._main, ob)
            ob.SetDraggable(False)

        constraintOuts = ogl.Constraint(ogl.CONSTRAINT_RIGHT_OF, self._main, self._outShapes)
        constraintOuts.SetSpacing(10, 0)
        self.AddConstraint(constraintOuts)
        if (numOut > 1): 
            for q in range(numOut):
                self._outShapes[q].SetY(YspaceOuts / 2 + (YspaceOuts + outHeight) * q - (shapeHeight / 2 - outHeight / 2))

        self.Recompute()
        
        self._main.SetDraggable(False)

        # If we don't do this the shape will take all left-clicks for itself
        self._main.SetSensitivityFilter(0)


class GenericGateWrapper:
    """ This class wraps a gate for drawing
    
    It can be any type of gate and this handles common code like connecting wires
    """
    
    def __init__(self, drawManager, x, y, leftIns, gateshape, out):
        """
        x, y : position of the gate
        """
        PurgeList(leftIns)
        self._leftInSignals = leftIns

        leftInShapes = [ogl.RectangleShape(10, 10) for i in leftIns]
        outShapes = [out.GetShape()]
	
        # default shape that other classes SHOULD override
        self._shape = GenericGateShape(drawManager, leftInShapes, outShapes, gateshape)
        dc = wx.ClientDC(drawManager)
        drawManager.PrepareDC(dc)

        self._shape.Move(dc, x, y)

        # store these values in case we have to recalculate
        self._x = x
        self._y = y
    
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
        for i in range(len(self._leftInSignals)):
            drawManager.ConnectWires(self._shape._leftInShapes[i], self._leftInSignals[i].GetShape())
        """for s in self._signals:
            if (s != None):
                drawManager.ConnectWires(self._shape._main, s.GetShape())"""
        
    def GetInstance(self):
        """ Get instance for simulator """
        return self._inst
        
    def GetShape(self):
        """ Get the OGL shape for manipulation """
        return self._shape

    def GetX(self):
        """ Desired x location """
        return self._x

    def GetY(self):
        """ Desicred y location """
        return self._y

    def SetPos(self, x, y):
        """ Set desired location """
        self._x = x
        self._y = y

def PurgeList(a):
    count = a.count(None)
    for i in range(count):
        a.remove(None)

