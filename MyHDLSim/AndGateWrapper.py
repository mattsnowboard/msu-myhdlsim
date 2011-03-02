import wx.lib.ogl as ogl
from myhdl import Signal, always
from MyHDLSim.combinational import And

class AndGateWrapper:
    """ This class wraps a MyHDLSim.combinational.AND function for drawing """
    
    def __init__(self, drawManager, x, y, out, a, b, c = None, d = None):
        self._out = out
        self._a = a
        self._b = b
        self._c = c
        self._d = d
        if (c != None and d != None):
            self._inst = And(self._out.GetSignal(),
                             self._a.GetSignal(),
                             self._b.GetSignal(),
                             self._c.GetSignal(),
                             self._d.GetSignal())
        elif (c != None):
            self._inst = And(self._out.GetSignal(),
                             self._a.GetSignal(),
                             self._b.GetSignal(),
                             self._c.GetSignal())
        else:
            self._inst = And(self._out.GetSignal(),
                             self._a.GetSignal(),
                             self._b.GetSignal())
        self._shape = ogl.RectangleShape(100, 100)
        self._shape.SetX(x)
        self._shape.SetY(y)
        self._shape.AddText("AND")
        drawManager.AddMyHDLGate(self._shape)
        self._connectWires(drawManager)
    
    def _connectWires(self, drawManager):
        """ Connect wires from ports to signals
        
        drawManager -- class that knows how to draw the shapes and draw lines between them
        """
        pass
        drawManager.ConnectWires(self._shape, self._out.GetShape())
        drawManager.ConnectWires(self._shape, self._a.GetShape())
        drawManager.ConnectWires(self._shape, self._b.GetShape())
        if (self._c != None):
            drawManager.ConnectWires(self._shape, self._c.GetShape())
        if (self._d != None):
            drawManager.ConnectWires(self._shape, self._d.GetShape())
        
        
    def GetInstance(self):
        """ Get instance for simulator """
        return self._inst