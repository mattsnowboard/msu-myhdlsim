import wx.lib.ogl as ogl
from myhdl import Signal, always
from MyHDLSim.combinational import Nand
from MyHDLSim.Wrappers.GenericGateWrapper import GenericGateWrapper

class NandGateShape(ogl.PolygonShape):
    def __init__(self):
        ogl.PolygonShape.__init__(self)

        points = [ (-40, 40),
                   (20, 40),
                   (35, 15),
                   (35, 0),
                   (35, 10),
                   (40, 10),
                   (40, -10),
                   (35, -10),
                   (35, 0),
                   (35, -15),
                   (20, -40),
                   (-40, -40) ]

        self.Create(points)
        self.CalculatePolygonCentre
        self.AddText("Nand")
        self.SetRegionName("Nand")

class NandGateWrapper(GenericGateWrapper):
    """ This class wraps a MyHDLSim.combinational.NAND function for drawing """
    
    def __init__(self, drawManager, x, y, out, a, b, c = None, d = None):
        GenericGateWrapper.__init__(self, drawManager, x, y, [a,b,c,d], NandGateShape(), out)
        self._CreateInstance(Nand, out, a, b, c, d)

        GenericGateWrapper._connectWires(self, drawManager)
