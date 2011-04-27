import wx
import wx.lib.ogl as ogl
from myhdl import Signal, always_comb, instances

class GenericGateShape(ogl.CompositeShape):
    def __init__(self, canvas, inLeftShapes, outShapes, mainShape, topShapes = [], bottomShapes = [], doConnect = True):
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
        self._shape = GenericGateShape(drawManager, leftInShapes, outShapes, gateshape, topShapes, bottomShapes, True)
        dc = wx.ClientDC(drawManager)
        drawManager.PrepareDC(dc)

        self._shape.Move(dc, x, y)

        # store these values in case we have to recalculate
        self._x = x
        self._y = y

    def _CreateInstance(self, Type, out, a = None, b = None, c = None, d = None, e = None, f = None):
        """
        Create a MyHDL instance that takes 2-7 parameters
        """
        outSig = out.GetSignal()
        aSig = a.GetSignal()
        minArgs = 2
        bSig = None
        if (b != None):
            minArgs += 1
            bSig = b.GetSignal()
        cSig = None
        if (c != None):
            minArgs += 1
            cSig = c.GetSignal()
        dSig = None
        if (d != None):
            minArgs += 1
            dSig = d.GetSignal()
        eSig = None
        if (e != None):
            minArgs += 1
            eSig = e.GetSignal()
        fSig = None
        if (f != None):
            minArgs += 1
            fSig = f.GetSignal()
        if ( len(outSig) > 1 ):
            def Gates(Type, minArgs, outSig, aSig, bSig, cSig, dSig, eSig, fSig):
                self._inst = []
                gateInst = [None for i in range(len(outSig))]
                outTemp = [Signal(int(outSig(i))) for i in range(len(outSig))]
                outList = [outSig(i) for i in range(len(outSig))]
                aList = [aSig(i) for i in range(len(aSig))]
                bList = [None for i in range(len(outSig))]
                if (bSig != None):
                    bList = [bSig(i) for i in range(len(bSig))]
                cList = [None for i in range(len(outSig))]
                if (cSig != None):
                    cList = [cSig(i) for i in range(len(cSig))]
                dList = [None for i in range(len(outSig))]
                if (dSig != None):
                    dList = [dSig(i) for i in range(len(dSig))]
                eList = [None for i in range(len(outSig))]
                if (eSig != None):
                    eList = [eSig(i) for i in range(len(eSig))]
                fList = [None for i in range(len(outSig))]
                if (fSig != None):
                    fList = [fSig(i) for i in range(len(fSig))]
                for i in range(len(outSig)):
                    gateInst[i] = self._createSingleInstance(Type, minArgs, outTemp[i], aList[i], bList[i], cList[i], dList[i], eList[i], fList[i])

                @always_comb
                def connect_out_bits():
                    for i in range(len(outTemp)):
                        outSig.next[i] = outTemp[i]
                        
                return instances()
            self._inst = Gates(Type, minArgs, outSig, aSig, bSig, cSig, dSig, eSig, fSig)

        else:
            self._inst = self._createSingleInstance(Type, minArgs, outSig, aSig, bSig, cSig, dSig, eSig, fSig)

    def _createSingleInstance(self, Type, minArgs, out, a, b, c, d, e, f):
        """
        Create instance at the MyHDL layer
        """
        if (minArgs == 7 or b != None and c != None and d != None and e != None and f != None):
            inst = Type(out, a, b, c, d, e, f)
        elif (minArgs == 6 or b != None and c != None and d != None and e != None):
            inst = Type(out, a, b, c, d, e)
        elif (minArgs == 5 or b != None and c != None and d != None):
            inst = Type(out, a, b, c, d)
        elif (minArgs == 4 or b != None and c != None):
            inst = Type(out, a, b, c)
        elif (minArgs == 3 or b != None):
            inst = Type(out, a, b)
        else:
            inst = Type(out, a)
        return inst
    
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

