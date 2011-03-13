import wx.lib.ogl as ogl
from myhdl import Signal, always
from MyHDLSim.combinational import Not

class NotGateWrapper:
    """ This class wraps a MyHDLSim.combinational.NOT function for drawing """
    
    def __init__(self, drawManager, x, y, out, a):
        self._out = out
        self._a = a
        self._inst = Not(self._out.GetSignal(),
			 self._a.GetSignal())
        self._shape = ogl.RectangleShape(100, 100)
        self._shape.SetX(x)
        self._shape.SetY(y)
        self._shape.AddText("NOT")
        drawManager.AddMyHDLGate(self._shape)
        self._connectWires(drawManager)
    
    def _connectWires(self, drawManager):
        """ Connect wires from ports to signals
        
        drawManager -- class that knows how to draw the shapes and draw lines between them
        """
        pass
        drawManager.ConnectWires(self._shape, self._out.GetShape())
        drawManager.ConnectWires(self._shape, self._a.GetShape())
         
    def GetInstance(self):
        """ Get instance for simulator """
        return self._inst
