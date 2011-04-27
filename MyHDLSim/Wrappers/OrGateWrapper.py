import wx.lib.ogl as ogl
from myhdl import Signal, always
from MyHDLSim.combinational import Or
from MyHDLSim.Wrappers.GenericGateWrapper import GenericGateWrapper

class OrGateShape(ogl.PolygonShape):
    def __init__(self):
        ogl.PolygonShape.__init__(self)

        points = [ (-40, 40),
                   (20, 40),
                   (40, 0),
                   (20, -40),
                   (-40, -40),
                   (-30,-20),
                   (-30,20) ]

        self.Create(points)
        self.CalculatePolygonCentre
        self.AddText("Or")
        self.SetRegionName("Or")

class OrGateWrapper(GenericGateWrapper):
    """ This class wraps a MyHDLSim.combinational.OR function for drawing """
    
    def __init__(self, drawManager, x, y, out, a, b, c = None, d = None):
        GenericGateWrapper.__init__(self, drawManager, x, y, [a,b,c,d], OrGateShape(), out)
        self._CreateInstance(Or, out, a, b, c, d)

        GenericGateWrapper._connectWires(self, drawManager)
