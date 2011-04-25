import wx
import wx.lib.ogl as ogl

class GenericGateShape(ogl.CompositeShape):
    def __init__(self, canvas, inLeftShapes, outShapes, mainShape, doConnect = True , topShapes = [], bottomShapes = []):
        ogl.CompositeShape.__init__(self)
        self.SetCanvas(canvas)
        
        # Sets main gate object from gate wrapper
        self._main = mainShape
        self.AddChild(self._main)

        # Determine spacing
        numLeftIn = len(inLeftShapes)
        numOut = len(outShapes)
        numTop = len(topShapes)
        numBottom = len(bottomShapes)
        shapeHeight = self._main.GetBoundingBoxMin()[1]
        if isinstance(self._main, ogl.CompositeShape):
            shapeHeight = self._main.GetHeight()
            shapeWidth = self._main.GetWidth()
        # Left spacing
        leftInHeight = 0
        if (numLeftIn > 0):
            leftInHeight = inLeftShapes[0].GetHeight()
        if (numLeftIn > 1):
            YspaceLeftIns = (shapeHeight - leftInHeight * numLeftIn) / (numLeftIn)
        # Right spacing
        outHeight = 0
        if (numOut > 0):
            outHeight = outShapes[0].GetHeight()
        if (numOut > 1):
            YspaceOuts = (shapeHeight - outHeight * numOut) / (numOut)

        # Top spacing
        topWidth = 0
        if (numTop > 0):
            topWidth = topShapes[0].GetWidth()
        if (numTop > 1):
            XspaceTops = (shapeWidth - topWidth * numTop) / (numTop)
        # Bottom spacing
        bottomWidth = 0
        if (numBottom > 0):
            bottomWidth = bottomShapes[0].GetWidth()
        if (numBottom > 1):
            XspaceBottoms = (shapeWidth - bottomWidth * numBottom) / (numBottom)

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

        # Connect and setup 'Out' objects
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

        # Connect and setup 'Top' objects
        self._topShapes = topShapes
        for ob in self._topShapes:
            self.AddChild(ob)
            if doConnect:
                canvas.ConnectWires(self._main, ob)
            ob.SetDraggable(False)

        constraintOuts = ogl.Constraint(ogl.CONSTRAINT_ABOVE, self._main, self._topShapes)
        constraintOuts.SetSpacing(0, 10)
        self.AddConstraint(constraintOuts)
        if (numOut > 1):
            for q in range(numOut):
                self._topShapes[q].SetX(XspaceTops / 2 + (XspaceTops + topWidth) * q - (shapeWidth / 2 - topWidth / 2))

        # Connect and setup 'Bottom' objects
        self._bottomShapes = bottomShapes
        for ob in self._bottomShapes:
            self.AddChild(ob)
            if doConnect:
                canvas.ConnectWires(self._main, ob)
            ob.SetDraggable(False)

        constraintOuts = ogl.Constraint(ogl.CONSTRAINT_BELOW, self._main, self._bottomShapes)
        constraintOuts.SetSpacing(0, 10)
        self.AddConstraint(constraintOuts)
        if (numOut > 1):
            for q in range(numOut):
                self._bottomShapes[q].SetX(XspaceBottoms / 2 + (XspaceBottoms + bottomWidth) * q - (shapeWidth / 2 - bottomWidth / 2))


        self.Recompute()
        
        self._main.SetDraggable(False)

        # If we don't do this the shape will take all left-clicks for itself
        self._main.SetSensitivityFilter(0)

    def SetBrushForChildren(self, brush):
        self._main.SetBrush(brush)
        for child in self.GetChildren():
            child.SetBrush(brush)

    def SetPenForChildren(self, pen):
        self._main.SetPen(pen)
        for child in self.GetChildren():
            child.SetPen(pen)


    def ChangeMain(self, main):
        """ Set a new Main shape to toggle the look of the shape
        """
        if main != None:
            self.RemoveChild(self._main)
            self._main = main
            self.AddChild(self._main)
            self.Recompute()
            self._main.SetDraggable(False)
            self._main.SetSensitivityFilter(0)


class GenericGateWrapper:
    """ This class wraps a gate for drawing
    
    It can be any type of gate and this handles common code like connecting wires
    """
    
    def __init__(self, drawManager, x, y, leftIns, gateshape, out, tops = [], bottoms = []):
        """
        x, y : position of the gate
        """
        PurgeList(leftIns)
        PurgeList(tops)
        PurgeList(bottoms)
        self._leftInSignals = leftIns
        self._tops = tops
        self._bottoms = bottoms

        leftInShapes = [ogl.RectangleShape(10, 10) for i in leftIns]
        topShapes = [ogl.RectangleShape(10, 10) for i in tops]
        bottomShapes = [ogl.RectangleShape(10, 10) for i in bottoms]
        outShapes = [out.GetShape()]
	
        # default shape that other classes SHOULD override
        self._shape = GenericGateShape(drawManager, leftInShapes, outShapes, gateshape, topShapes, bottomShapes)
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
        for i in range(len(self._tops)):
            drawManager.ConnectWires(self._shape._topShapes[i], self._tops[i].GetShape())
        for i in range(len(self._bottoms)):
            drawManager.ConnectWires(self._shape._bottomShapes[i], self._bottoms[i].GetShape())
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

