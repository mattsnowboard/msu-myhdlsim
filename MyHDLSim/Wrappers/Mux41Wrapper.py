import wx.lib.ogl as ogl
from myhdl import Signal, always
from MyHDLSim.combinational import Mux41

class Mux41Wrapper:
    """ This class wraps a MyHDLSim.combinational.MUX41 function for drawing """
    
    def __init__(self, drawManager, x, y, out, c0, c1, d0, d1, d2, d3):
        self._out = out
	self._c0 = c0
        self._c1 = c1
        self._d0 = d0
	self._d1 = d1
	self._d2 = d2
	self._d3 = d3
        self._init = Mux41(self._out.GetSignal(),
			   self._c0.GetSignal(),
			   self._c1.GetSignal(),
			   self._d0.GetSignal(),
			   self._d1.GetSignal(),
			   self._d2.GetSignal(),
			   self._d3.GetSignal())
        self._shape = ogl.EllipseShape(50, 100)
        self._shape.SetX(x)
        self._shape.SetY(y)
        self._shape.AddText("MUX 41")
        drawManager.AddMyHDLGate(self._shape)
        self._connectWires(drawManager)
    
    def _connectWires(self, drawManager):
        """ Connect wires from ports to signals
        
        drawManager -- class that knows how to draw the shapes and draw lines between them
        """
        pass
        drawManager.ConnectWires(self._shape, self._out.GetShape())
	drawManager.ConnectWires(self._shape, self._c0.GetShape())
	drawManager.ConnectWires(self._shape, self._c1.GetShape())
	drawManager.ConenctWires(self._shape, self._d0.GetShape())
	drawManager.ConnectWires(self._shape, self._d1.GetShape())
        drawManager.ConnectWires(self._shape, self._d2.GetShape())
        drawManager.ConnectWires(self._shape, self._d3.GetShape())
      
        
    def GetInstance(self):
        """ Get instance for simulator """
        return self._inst
