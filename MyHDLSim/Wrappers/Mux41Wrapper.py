import wx.lib.ogl as ogl
from myhdl import Signal, always
from MyHDLSim.combinational import Mux41
from MyHDLSim.Wrappers.GenericGateWrapper import GenericGateWrapper

class Mux41Shape(ogl.PolygonShape):
    def __init__(self):
        ogl.PolygonShape.__init__(self)

        points = [ (-25, 40),
                   (25, 40),
                   (30, 35),
                   (30, -35),
                   (25, -40),
                   (-25, -40)
                   (-30, -35)
                   (-30, 35) ]

        self.Create(points)
        self.CalculatePolygonCentre
        self.AddText("MUX 4-1")
        self.SetRegionName("MUX 21")

class Mux41Wrapper:
    """ This class wraps a MyHDLSim.combinational.MUX41 function for drawing """
    
    def __init__(self, drawManager, x, y, out, c0, c1, d0, d1, d2, d3):
        GenericGateWrapper.__init__(self, drawManager, x, y, [d0, d1, d2, d3], Mux41Shape(), [out], [c0, c1])
        self._inst = Mux41(out.GetSignal(),
			   c0.GetSignal(),
			   c1.GetSignal(),
			   d0.GetSignal(),
			   d1.GetSignal(),
			   d2.GetSignal(),
			   d3.GetSignal())
        GenericGateWrapper._connectWires(self, drawManager)
        self.SetRegionName("MUX 41")
