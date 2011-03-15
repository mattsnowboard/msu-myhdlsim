import wx.lib.ogl as ogl
from myhdl import Signal, always
from MyHDLSim.combinational import Not
from MyHDLSim.Wrappers.GenericGateWrapper import GenericGateWrapper

class NotGateWrapper(GenericGateWrapper):
    """ This class wraps a MyHDLSim.combinational.NOT function for drawing """
    
    def __init__(self, drawManager, x, y, out, a):
        GenericGateWrapper.__init__(self, x, y)
        self._inst = Not(out.GetSignal(),
			 a.GetSignal())
        GenericGateWrapper._addSignal(self, a)
        GenericGateWrapper._addSignal(self, out)
        # override default here!
        #self._shape = ogl.RectangleShape(100, 100)
        #self._shape.SetX(x)
        #self._shape.SetY(y)
        self._shape.AddText("NOT")
        drawManager.AddMyHDLGate(self._shape)
        GenericGateWrapper._connectWires(self, drawManager)
