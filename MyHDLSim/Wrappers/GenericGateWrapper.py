import wx.lib.ogl as ogl

class GenericGateWrapper:
    """ This class wraps a gate for drawing
    
    It can be any type of gate and this handles common code like connecting wires
    """
    
    def __init__(self, x, y):
        """
        x, y : position of the gate
        """
        self._signals = list()
        # default shape that other classes SHOULD override
        self._shape = ogl.RectangleShape(100, 100)
        self._shape.SetX(x)
        self._shape.SetY(y)
    
    def _addSignal(self, signal):
        """ Add signal
        
        Derived classes must add all signals so that they can be connected
        signal : a signal on the gate which we will visually connect in the UI
        """
        self._signals.append(signal)
    
    def _connectWires(self, drawManager):
        """ Connect wires from ports to signals
        
        drawManager -- class that knows how to draw the shapes and draw lines between them
        """
        for s in self._signals:
            if (s != None):
                drawManager.ConnectWires(self._shape, s.GetShape())
        
    def GetInstance(self):
        """ Get instance for simulator """
        return self._inst