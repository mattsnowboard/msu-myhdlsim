import wx.lib.ogl as ogl
from myhdl import Signal, always
from MyHDLSim.combinational import Nor
from MyHDLSim.Wrappers.GenericGateWrapper import GenericGateWrapper

class NorGateShape(ogl.PolygonShape):
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
        if (c != None and d != None):
            self._inst = Nor(out.GetSignal(),
                            a.GetSignal(),
                            b.GetSignal(),
                            c.GetSignal(),
                            d.GetSignal())
        elif (c != None):
            self._inst = Nor(out.GetSignal(),
                            a.GetSignal(),
                            b.GetSignal(),
                            c.GetSignal())
        else:
            self._inst = Nor(out.GetSignal(),
                            a.GetSignal(),
                            b.GetSignal())
        #GenericGateWrapper._addSignal(self, a)
        #GenericGateWrapper._addSignal(self, b)
        #GenericGateWrapper._addSignal(self, c)
        #GenericGateWrapper._addSignal(self, d)
        #GenericGateWrapper._addSignal(self, out)
        # override default here!
        #self._shape = ogl.RectangleShape(100, 100)
        #self._shape.SetX(x)
        #self._shape.SetY(y)
        drawManager.AddMyHDLGate(self._shape)
        GenericGateWrapper._connectWires(self, drawManager)
