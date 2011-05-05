import wx.lib.ogl as ogl
from myhdl import Signal, always
from MyHDLSim.combinational import Mux21
from MyHDLSim.Wrappers.GenericGateWrapper import GenericGateWrapper

class Mux21Shape(ogl.PolygonShape):
    def __init__(self):
        ogl.PolygonShape.__init__(self)

        points = [ (-25, 40),
                   (25, 40),
                   (30, 35),
                   (30, -35),
                   (25, -40),
                   (-25, -40),
                   (-30, -35),
                   (-30, 35) ]

        self.Create(points)
        self.CalculatePolygonCentre
        self.AddText("MUX 2-1")
        self.SetRegionName("MUX 2-1")

class Mux21Wrapper(GenericGateWrapper):
    """ This class wraps a MyHDLSim.combinational.MUX21 function for drawing """
    
    def __init__(self, drawManager, x, y, out, select, a, b):
        GenericGateWrapper.__init__(self, drawManager, x, y, [a,b], Mux21Shape(), out, [select])
        self._CreateInstance(Mux21, out, select, a, b)

        GenericGateWrapper._connectWires(self, drawManager)

