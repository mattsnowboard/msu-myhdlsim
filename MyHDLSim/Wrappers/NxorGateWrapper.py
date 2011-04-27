import wx.lib.ogl as ogl
from myhdl import Signal, always
from MyHDLSim.combinational import Nxor
from MyHDLSim.Wrappers.GenericGateWrapper import GenericGateWrapper

class NxorGateShape(ogl.CompositeShape):
    def __init__(self, canvas):
        ogl.CompositeShape.__init__(self)

        self.SetCanvas(canvas) 

        shape1 = ogl.PolygonShape()
        points1 = [ (-2.5, 40),
                    (2.5, 20),
                    (2.5, -20),
                    (-2.5, -40),
                    (2.5, -20),
                    (2.5, 20) ]
        shape1.Create(points1)                  
        
        shape2 = ogl.PolygonShape()
        points2 = [ (-35, 40),
                    (20, 40),
                    (35, 0),
                    (35, 10),
                    (40, 10),
                    (40, -10),
                    (35, -10),
                    (35, 0),
                    (20, -40),
                    (-35, -40),
                    (-30, -20),
                    (-30, 20) ]
        shape2.Create(points2)

        self.AddText("Nxor")
        self.SetRegionName("Nxor")

        self.AddChild(shape1)
        self.AddChild(shape2)
  
        constraint = ogl.Constraint(ogl.CONSTRAINT_RIGHT_OF, shape1, [shape2])
        constraint.SetSpacing(1,0)
        self.AddConstraint(constraint)
        self.Recompute()
  
        # If we don't do this, the shapes will be able to move on their
        # own, instead of moving the composite
        shape1.SetDraggable(False)
        shape2.SetDraggable(False)
  
        # If we don't do this the shape will take all left-clicks for itself
        shape1.SetSensitivityFilter(0)

class NxorGateWrapper(GenericGateWrapper):
    """ This class wraps a MyHDLSim.combinational.NXOR function for drawing """
    
    def __init__(self, drawManager, x, y, out, a, b, c = None, d = None):
        GenericGateWrapper.__init__(self, drawManager, x, y, [a,b,c,d], NxorGateShape(drawManager), out)
        self._CreateInstance(Nxor, out, a, b, c, d)

        GenericGateWrapper._connectWires(self, drawManager)
