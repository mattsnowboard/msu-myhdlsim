import wx.lib.ogl as ogl
from myhdl import Signal, always
from MyHDLSim.combinational import Not
from MyHDLSim.Wrappers.GenericGateWrapper import GenericGateWrapper

class NotGateShape(ogl.PolygonShape):
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

class NotGateWrapper(GenericGateWrapper):
    """ This class wraps a MyHDLSim.combinational.NOT function for drawing """
    
    def __init__(self, drawManager, x, y, out, a):
        GenericGateWrapper.__init__(self, drawManager, x, y, [a], NotGateShape(), out)
        self._inst = Not(out.GetSignal(),
			 a.GetSignal())
        #GenericGateWrapper._addSignal(self, a)
        #GenericGateWrapper._addSignal(self, out)
        # override default here!
        #self._shape = ogl.RectangleShape(100, 100)
        #self._shape.SetX(x)
        #self._shape.SetY(y)
        drawManager.AddMyHDLGate(self._shape)
        GenericGateWrapper._connectWires(self, drawManager)
