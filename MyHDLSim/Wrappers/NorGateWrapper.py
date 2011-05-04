import wx.lib.ogl as ogl
from myhdl import Signal, always
from MyHDLSim.combinational import Nor
from MyHDLSim.Wrappers.GenericGateWrapper import GenericGateWrapper

class NorGateShape(ogl.PolygonShape):
    """ This shape is used exclusively to contruct the NOR Gate main shape.
        The shape is initially based within an 80x80 square, centered """
    def __init__(self):
        ogl.PolygonShape.__init__(self)

        points = [ (-40, 40),
                   (20, 40),
                   (35, 0),
                   (35, 10),
                   (40, 10),
                   (40, -10),
                   (35, -10),
                   (35, 0),
                   (20, -40),
                   (-40, -40),
                   (-30,-20),
                   (-30,20) ]

        self.Create(points)
        self.CalculatePolygonCentre
        self.AddText("Nor")
        self.SetRegionName("Nor")

class NorGateWrapper(GenericGateWrapper):
    """ This class wraps a MyHDLSim.combinational.NOR function for drawing """
    
    def __init__(self, drawManager, x, y, out, a, b, c = None, d = None):
        GenericGateWrapper.__init__(self, drawManager, x, y, [a,b,c,d], NorGateShape(), out)
        self._CreateInstance(Nor, out, a, b, c, d)

        GenericGateWrapper._connectWires(self, drawManager)
