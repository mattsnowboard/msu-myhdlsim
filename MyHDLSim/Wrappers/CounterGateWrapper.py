import wx.lib.ogl as ogl
from myhdl import Signal, always
from MyHDLSim.sequential import Counter
from MyHDLSim.Wrappers.GenericGateWrapper import GenericGateWrapper

class CounterShape(ogl.PolygonShape):
    """ This shape is used exclusively to contruct the COUNTER Gate main shape.
        The shape is initially based within an 80x80 square, centered """
    def __init__(self, m, n):
        ogl.PolygonShape.__init__(self)

        points = [ (-40, 40),
                   (40, 40),
                   (40, -40),
                   (-40, -40) ]

        self.Create(points)
        self.CalculatePolygonCentre
        self.AddText("Counter")
        self.SetRegionName("Counter")

class CounterWrapper:
    """ This class wraps a MyHDLSim.combinational.Counter function for drawing """
    
    def __init__(self, drawManager, x, y, out, clk, rst = None):
        GenericGateWrapper.__init__(self, drawManager, x, y, [clk], DecoderShape(), [out], [rst])
        if (rst != None):        
            self._inst = Counter( out.GetSignal(), clk.GetSignal(), rst.GetSignal() )
        else:
            self._inst = Counter( out.GetSignal(), clk.GetSignal() )
        GenericGateWrapper._connectWires(self, drawManager)

