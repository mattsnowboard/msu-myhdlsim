import wx, wx.lib.newevent
import wx.lib.ogl as ogl
from myhdl import Signal, always

# The events that wx side will listen for (must register self for this)
SignalChangeEvent, EVT_SIGNAL_CHANGE = wx.lib.newevent.NewEvent() 

class SignalWrapper:
    """ This class wraps a MyHDL.Signal object
    
    Handles wx event listening, toggling, and getting an object to draw
    """
    
    def __init__(self, signal = Signal(None), x = 0, y = 0, listener = None):
        self._signal = signal
        self._listeners = list()
        if listener != None:
            self.AddListener(listener)
        self._shape = ogl.TextShape(100,100)
        self._shape.AddText(str(self._signal.val))
        self._shape.SetX(x)
        self._shape.SetY(y)
    
    def AddListener(self, listener):
        """ Add Listener to Signal
        
        Must be done BEFORE getting instance and creating Simulator
        """
        
        self._listeners.append(listener)
    
    def RemoveListener(self, listener):
        """ Remove Listener from Signal
        
        Must be done BEFORE getting instance and creating Simulator
        """
        
        self._listeners.remove(listener)
    
    def GetSignal(self):
        """ Get the underlying object
        """
        return self._signal
    
    def Toggle(self):
        """ Toggle the signal value
        
        If it was unitialized, just assert it
        """
        
        print "toggle"
        if (self._signal == None):
            self._signal.next = True
        else:
            self._signal.next = not self._signal
    
    def GetGenerator(self):
        """ This is the function that returns a MyHDL generator.
        
        This should be passed to a MyHDL Simulator so that listeners get
        update when the Signal changes
        """
        
        # this should get run whenever signal changes
        @always(self._signal.posedge, self._signal.negedge)
        def logic():
            print "in logic!"
            self._shape.ClearText()
            self._shape.AddText(str(self._signal.val))
            evt = SignalChangeEvent(val = self._signal.val)
            
            for listener in self._listeners:
                wx.PostEvent(listener, evt)
        
        return logic
    
    def SetX(self, x):
        self._shape.SetX(x)
        
    def SetY(self, y):
        self._shape.SetY(y)
    
    def GetShape(self):
        return self._shape
    