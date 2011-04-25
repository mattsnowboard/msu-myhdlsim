import wx
import wx.lib.ogl as ogl
from myhdl import Signal, Simulation, delay, instance, StopSimulation
from MyHDLSim.Wrappers.SignalWrapper import EVT_SIGNAL_CHANGE, SignalWrapper
from MyHDLSim.Module import Module, EVT_MODULE_MOVE
from MyHDLSim.wxApplication import MainWindow, ThreadTimer, EVT_THREAD_TIMER

class Manager:
    """ This class will manage the Signals and Gates and Simulator """
    def __init__(self, app):
        """ Given an application, create the window and canvas

        Creates a top level module
        Binds some events
        """
        self._frame = MainWindow(None, 'Demo')
        self._canvas = self._frame.GetCanvas()
        self._canvas.SetManager(self)
        self._app = app
        
        # top level module
        self._top = Module(self, self._canvas)
        
        # get passed to MyHDL simulator (gates, event listening generators, etc.)
        self._instances = list()
        # quick look up of gates/signals by ID
        self._modules = []
        self._gates = []
        self._signals = []
        self._signalMap = {}
        self._moduleMap = {}

        # this is to help with showing/hiding modules
        self._moduleHierarchy = []
        self._displayDepth = 0
        
        self._frame.Bind(EVT_MODULE_MOVE, self.OnModuleMove)
        self._canvas.Bind(wx.EVT_CHAR, self.OnKey)

        # Set timing events
        self._pause = False
        self._timer = ThreadTimer(self._frame)
        self._timer.start(150)
        self._frame.Bind(EVT_THREAD_TIMER, self.OnTimer)

        self._canvas.SetFocus()
        
    def CreateSignal(self, initial = None):
        """ Create a signal which we can keep track of
        
        This needs to be done before adding switches or probes
        """
        signal = SignalWrapper(self._canvas, initial)
        signal.AddListener(self._frame)
        self._signals.append(signal)
        return signal
        
    def CreateModule(self):
        """ Create a module that a user can define
        
        return: the module ready to be customized
        """
        module = Module(self, self._canvas)
        self._modules.append(module)
        return module
    
    def AddSwitch(self, pos, signal, key):
        """ Add a switch to an existing signal
        
        """
        # @todo verify we have created the signal, else it won't update
        signal.SetSwitch(self._canvas, key)
        signal.SetX(pos[0])
        signal.SetY(pos[1])
        self._signalMap[ord(key)] = signal
        self._canvas.AddMyHDLSignal(signal.GetShape(), pos[0], pos[1])
        
    def AddProbe(self, pos, a, label):
        """ Add a signal visually with a label but no key events
        
        """
        # @todo verify we have created the signal, else it won't update
        signal = self.CreateSignal()
        signal.SetProbe(self._canvas, a, label)
        signal.SetX(pos[0])
        signal.SetY(pos[1])
        self._canvas.AddMyHDLSignal(signal.GetShape(), pos[0], pos[1])
 
    def AddClock(self, pos, signal, label, period = 20):
        """ Add a switch to an existing signal
        
        """
        # @todo verify we have created the signal, else it won't update
        signal.SetClockDriver(self._canvas, label, period)
        signal.SetX(pos[0])
        signal.SetY(pos[1])
        self._canvas.AddMyHDLSignal(signal.GetShape(), pos[0], pos[1], False)
        self._top._addInstance(signal)
       
    def AddAndGate(self, pos, out, a, b, c = None, d = None):
        """ Create an AND gate
        
        This is a way to allow users to ignore the underlying module
        """
        self._top.AddAndGate(pos, out, a, b, c, d)

    def AddNandGate(self, pos, out, a, b, c = None, d = None):
        """ Create a NAND gate
        
        This is a way to allow users to ignore the underlying module
        """
        self._top.AddNandGate(pos, out, a, b, c, d)

    def AddOrGate(self, pos, out, a, b, c = None, d = None):
        """ Create an OR gate
        
        This is a way to allow users to ignore the underlying module
        """
        self._top.AddOrGate(pos, out, a, b, c, d)

    def AddNorGate(self, pos, out, a, b, c = None, d = None):
        """ Create an NOR gate
        
        This is a way to allow users to ignore the underlying module
        """
        self._top.AddNorGate(pos, out, a, b, c, d)
        
    def AddNotGate(self, pos, out, a):
        """ Create a NOT gate
        
        This is a way to allow users to ignore the underlying module
        """
        self._top.AddNotGate(pos, out, a)

    def AddXorGate(self, pos, out, a, b, c = None, d = None):
        """ Create an XOR gate
        
        This is a way to allow users to ignore the underlying module
        """
        self._top.AddXorGate(pos, out, a, b, c, d)

    def AddNxorGate(self, pos, out, a, b, c = None, d = None):
        """ Create an NXOR gate
        
        This is a way to allow users to ignore the underlying module
        """
        self._top.AddNxorGate(pos, out, a, b, c, d)

    def AddMux21(self, pos, out, select, a, b):
        """ Create a 2-1 MUX

        This is a way to allow users to ignore the underlying module
        """
        self._top.AddMux21(pos, out, select, a, b)

    def AddMux41(self, pos, out, c0, c1, d0, d1, d2, d3):
        """ Create a 4-1 MUX

        This is a way to allow users to ignore the underlying module
        """
        self._top.AddMux41(pos, out, c0, c1, d0, d1, d2, d3)

    def AddTff(self, pos, q, t, clk, rst = None, s = None):
        """ Create a T Flip-Flop

        This is a way to allow users to ignore the underlying module
        """
        self._top.AddTff(pos, q, t, clk, rst = None, s = None)

    def AddDff(self, pos, q, d, clk, rst = None, s = None):
        """ Create a D Flip-Flop

        This is a way to allow users to ignore the underlying module
        """
        self._top.AddDff(pos, q, d, clk, rst = None, s = None)
    
    def AddModule(self, module, pos, name):
        """ Add a module
        
        This is a way to allow users to ignore the underlying module
        """
        self._top.AddModule(module, pos, name)
        # map it for lookup by shape object
        self._moduleMap[module.GetShape()] = module
    
    def Start(self):
        """ Initialize and start the simulator """

        # we have deferred adding anything to the canvas until now
        self._top.Render()
        self._canvas.ConnectAllWires()

        # this will build a list of lists, from highest to lowest level
        # of modules so we can show/hide them all
        self._moduleHierarchy.append([]) # empty top node
        self._buildHierarchy(self._top, 1)
        self._displayDepth = len(self._moduleHierarchy) - 1
        
        # we need a trick to run the simulator and the main loop...
        
        def EventLoop():
            @instance
            def inst():
                while(self._frame and not self._frame.IsExit()):
                    yield delay(1)
                    self._refresh()
                    self._app.MainLoop()
                else:
                    self._timer.stop()
                    raise StopSimulation
            return inst
        event_loop_runner = EventLoop()
        
        # grab top module

        self._instances.append(self._top.GetInstances())
        
        self._instances.append(event_loop_runner)

        self._simulator = Simulation(*self._instances)

        self._simulator.run()


    def _buildHierarchy(self, module, level):
        """ Recursive calls to build the module hierarchy list
        """
        for m in module.GetModules():
            if level + 1 > len(self._moduleHierarchy):
                self._moduleHierarchy.append([])
            self._moduleHierarchy[level].append(m)
            self._buildHierarchy(m, level + 1)

    def OnTimer(self, e):
        """ Handle timing simulation
        """
        if not self._pause:
            self._app.ExitMainLoop()

    def OnKey(self, e):
        """ Switch toggling by keypress
        Also handles "zooming" level of detail to display
        """
        key = e.GetKeyCode()
        map = self._signalMap
        if (key in map):
            map[key].Toggle()
            self._app.ExitMainLoop()
        elif key in [wx.WXK_PRIOR, wx.WXK_PAGEUP]:
            tempDepth = max([self._displayDepth - 1, 0])
            if (tempDepth != self._displayDepth):
                for m in self._moduleHierarchy[self._displayDepth]:
                    m.ShowDetails(False)
            self._displayDepth = tempDepth
            self._refresh()
        elif key in [wx.WXK_NEXT, wx.WXK_PAGEDOWN]:
            tempDepth = min([self._displayDepth + 1, len(self._moduleHierarchy) - 1])
            if (tempDepth != self._displayDepth):
                for m in self._moduleHierarchy[tempDepth]:
                    m.ShowDetails(True)
            self._displayDepth = tempDepth
            self._refresh()
    
    def OnModuleMove(self, e):
        """ When a module moves (the shape) we need to move its contents
        e.Shape holds the shape that actually moved
        We look up the shape against our module dictionary
        """
##        moduleShape = e.Shape
##        if (moduleShape in self._moduleMap):
##            module = self._moduleMap[moduleShape]
##            module.Move(moduleShape.GetX() - module.GetWidth() / 2,
##                        moduleShape.GetY() - module.GetHeight() / 2)
        ## We don't need this if we use children shapes
        pass
            
    def GetFrame(self):
        """ Get the frame for event firing
        """
        return self._frame
    
    def _refresh(self):
        """ Refresh the canvas after updating signal shapes
        """
        for s in self._signals:
            s.Update()
        self._top.Update()
        self._canvas.Refresh(False)

       
       
def Init():
    app = wx.App(False)
    manager = Manager(app)
    ogl.OGLInitialize()
    return manager
    
