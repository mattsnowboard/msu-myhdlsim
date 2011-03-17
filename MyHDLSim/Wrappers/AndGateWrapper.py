import wx.lib.ogl as ogl
from myhdl import Signal, always
from MyHDLSim.combinational import And
from MyHDLSim.Wrappers.GenericGateWrapper import GenericGateWrapper

class AndGateWrapper(GenericGateWrapper):
    """ This class wraps a MyHDLSim.combinational.AND function for drawing """
    
    def __init__(self, drawManager, x, y, out, a, b, c = None, d = None):
	GenericGateWrapper.__init__(self, drawManager, x, y, out, "AND")
        if (c != None and d != None):
            self._inst = And(out.GetSignal(),
                             a.GetSignal(),
                             b.GetSignal(),
                             c.GetSignal(),
                             d.GetSignal())
        elif (c != None):
            self._inst = And(out.GetSignal(),
                             a.GetSignal(),
                             b.GetSignal(),
                             c.GetSignal())
        else:
            self._inst = And(out.GetSignal(),
                             a.GetSignal(),
                             b.GetSignal())
	GenericGateWrapper._addSignal(self, a)
        GenericGateWrapper._addSignal(self, b)
        GenericGateWrapper._addSignal(self, c)
        GenericGateWrapper._addSignal(self, d)
        GenericGateWrapper._addSignal(self, out)
	# override default here!
	#self._shape = ogl.RectangleShape(100, 100)
        #self._shape.SetX(x)
        #self._shape.SetY(y)
        drawManager.AddMyHDLGate(self._shape)
        GenericGateWrapper._connectWires(self, drawManager)
