import wx.lib.ogl as ogl
from myhdl import Signal, always
from MyHDLSim.combinational import Mux41
from MyHDLSim.Wrappers.GenericGateWrapper import GenericGateWrapper

class Mux41Shape(ogl.PolygonShape):
    """ This shape is used exclusively to contruct the MUX 4-1 Gate main shape.
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
        self.AddText("MUX 4-1")
        self.SetRegionName("MUX 4-1")

class Mux41Wrapper:
    """ This class wraps a MyHDLSim.combinational.MUX41 function for drawing """
    
    def __init__(self, drawManager, x, y, out, c0, c1, d0, d1, d2, d3):
        GenericGateWrapper.__init__(self, drawManager, x, y, [d0, d1, d2, d3], Mux41Shape(), [out], [c0, c1])
        self._CreateInstance(Mux41, out, c0, c1, d0, d1, d2, d3)
        
        GenericGateWrapper._connectWires(self, drawManager)
        self.SetRegionName("MUX 4-1")
