import wx.lib.ogl as ogl
from myhdl import Signal, always
from MyHDLSim.combinational import Mux21

class Mux21Wrapper:
    """ This class wraps a MyHDLSim.combinational.MUX21 function for drawing """
    
    def __init__(self, drawManager, x, y, out, select, a, b):
        self._out = out
	self._select = select
        self._a = a
        self._b = b
        self._init = Mux21(self._out.GetSignal(),
			   self._select.GetSignal(),
			   self._a.GetSignal(),
			   self._b.GetSignal())
        self._shape = ogl.EllipseShape(50, 100)
        self._shape.SetX(x)
        self._shape.SetY(y)
        self._shape.AddText("MUX 21")
        drawManager.AddMyHDLGate(self._shape)
        self._connectWires(drawManager)
    
    def _connectWires(self, drawManager):
        """ Connect wires from ports to signals
        
        drawManager -- class that knows how to draw the shapes and draw lines between them
        """
        pass
        drawManager.ConnectWires(self._shape, self._out.GetShape())
	drawManager.ConnectWires(self._shape, self._select.GetShape())
        drawManager.ConnectWires(self._shape, self._a.GetShape())
        drawManager.ConnectWires(self._shape, self._b.GetShape())
      
        
    def GetInstance(self):
        """ Get instance for simulator """
        return self._inst
