import wx.lib.ogl as ogl
from myhdl import Signal, always
from MyHDLSim.combinational import Decoder
from MyHDLSim.Wrappers.GenericGateWrapper import GenericGateWrapper

class DecoderShape(ogl.PolygonShape):
    def __init__(self, m, n):
        ogl.PolygonShape.__init__(self)

        points = [ (-40, 40),
                   (40, 40),
                   (40, -40),
                   (-40, -40) ]

        self.Create(points)
        self.CalculatePolygonCentre
        self.AddText("Decoder")
        self.SetRegionName("Decoder")

class DecoderWrapper:
    """ This class wraps a MyHDLSim.combinational.Decoder function for drawing """
    
    def __init__(self, drawManager, x, y, out, data, en):
        GenericGateWrapper.__init__(self, drawManager, x, y, [en, data], DecoderShape(), [out])
        self._inst = Decoder( out.GetSignal(), data.GetSignal(), en.GetSignal() )
        GenericGateWrapper._connectWires(self, drawManager)

