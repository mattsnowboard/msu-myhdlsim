import wx.lib.ogl as ogl
from myhdl import Signal, always
from MyHDLSim.combinational import Not
from MyHDLSim.Wrappers.GenericGateWrapper import GenericGateWrapper

class NotGateShape(ogl.PolygonShape):
    """ This shape is used exclusively to contruct the NOT Gate main shape.
        The shape is initially based within an 80x80 square, centered """
    def __init__(self):
        ogl.PolygonShape.__init__(self)

        points = [ (-40, 40),
                   (35, 0),
                   (35, 10),
                   (40, 10),
                   (40, -10),
                   (35, -10),
                   (35, 0),
                   (-40, -40) ]

        self.Create(points)
        self.CalculatePolygonCentre
        self.AddText("Not")
        self.SetRegionName("Not")

class NotGateWrapper(GenericGateWrapper):
    """ This class wraps a MyHDLSim.combinational.NOT function for drawing """
    
    def __init__(self, drawManager, x, y, out, a):
        GenericGateWrapper.__init__(self, drawManager, x, y, [a], NotGateShape(), out)
        self._CreateInstance(Not, out, a)
        
        GenericGateWrapper._connectWires(self, drawManager)
