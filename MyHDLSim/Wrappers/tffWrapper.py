import wx.lib.ogl as ogl
from myhdl import Signal, always
from MyHDLSim.sequential import tff
from MyHDLSim.Wrappers.GenericGateWrapper import GenericGateWrapper

class tffShape(ogl.PolygonShape):
    """ This shape is used exclusively to contruct the TFF Gate main shape.
        The shape is initially based within an 80x80 square, centered """
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
        self.AddText("S")
        self.AddText("t-flip flop")
        self.AddText("R")
        self.SetRegionName("TFF")

class TffWrapper:
    """ This class wraps a MyHDLSim.combinational.TFF function for drawing """
    
    def __init__(self, drawManager, x, y, q, t, clk, rst = None, s = None):
        GenericGateWrapper.__init__(self, drawManager, x, y, [t, clk], tffShape(), [q], [s], [rst] )
        self._CreateInstance(tff, q, t, clk, rst, s)

        GenericGateWrapper._connectWires(self, drawManager)

