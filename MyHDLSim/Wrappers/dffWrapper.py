import wx.lib.ogl as ogl
from myhdl import Signal, always
from MyHDLSim.sequential import dff
from MyHDLSim.Wrappers.GenericGateWrapper import GenericGateWrapper

class dffShape(ogl.PolygonShape):
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
        self.AddText("d-flip flop")
        self.AddText("R")
        self.SetRegionName("DFF")

class DffWrapper:
    """ This class wraps a MyHDLSim.combinational.DFF function for drawing """
    
    def __init__(self, drawManager, x, y, q, d, clk, rst = None, s = None):
        GenericGateWrapper.__init__(self, drawManager, x, y, [d, clk], dffShape(), [q], [s], [rst] )
        self._CreateInstance(dff, q, d, clk, rst, s)

        GenericGateWrapper._connectWires(self, drawManager)

