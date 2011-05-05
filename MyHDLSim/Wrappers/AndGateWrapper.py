import wx.lib.ogl as ogl
from myhdl import Signal, always, always_comb, instances
from MyHDLSim.combinational import And
from MyHDLSim.Wrappers.GenericGateWrapper import GenericGateWrapper

class AndGateShape(ogl.PolygonShape):
    """ This shape is used exclusively to contruct the AND Gate main shape.
        The shape is initially based within an 80x80 square, centered """
    def __init__(self):
        ogl.PolygonShape.__init__(self)

        points = [ (-40, 40),
                   (20, 40),
                   (40, 15),
                   (40, -15),
                   (20, -40),
                   (-40, -40) ]

        self.Create(points)
        self.CalculatePolygonCentre
        self.AddText("And")
        self.SetRegionName("And")

class AndGateWrapper(GenericGateWrapper):
    """ This class wraps a MyHDLSim.combinational.AND function for drawing """
    
    def __init__(self, drawManager, x, y, out, a, b, c = None, d = None):
        GenericGateWrapper.__init__(self, drawManager, x, y, [a,b,c,d], AndGateShape(), out)
        self._CreateInstance(And, out, a, b, c, d)
        GenericGateWrapper._connectWires(self, drawManager)
