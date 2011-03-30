import wx
import wx.lib.ogl as ogl
from myhdl import Signal, Simulation, delay, instance
from MyHDLSim.Wrappers.SignalWrapper import EVT_SIGNAL_CHANGE, SignalWrapper
from MyHDLSim.Module import Module, EVT_MODULE_MOVE
from MyHDLSim.wxApplication import MainWindow

class Manager:
    """ This class will manage the Signals and Gates and Simulator """
    def __init__(self, app):
        self._frame = MainWindow(None, 'Demo')
        self._canvas = self._frame.canvas
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
        
        self._frame.Bind(EVT_MODULE_MOVE, self.OnModuleMove)
        self._canvas.Bind(wx.EVT_CHAR, self.OnKey)
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
        
    def AddNotGate(self, pos, out, a):
        """ Create a NOT gate
        
        This is a way to allow users to ignore the underlying module
        """
        self._top.AddNotGate(pos, out, a)
    
    def AddModule(self, module, pos, name):
        self._top.AddModule(module, pos, name)
        # map it for lookup by shape object
        self._moduleMap[module.GetShape()] = module
    
    def Start(self):
        """ Initialize and start the simulator """
        
        # we need a trick to run the simulator and the main loop...
        
        def EventLoop():
            @instance
            def inst():
                while(self._frame and not self._frame.exit):
                    yield delay(1)
                    self._refresh()
                    self._app.MainLoop()
            return inst
        event_loop_runner = EventLoop()
        
        # grab top module
        self._instances.append(self._top.GetInstances())
        
        self._instances.append(event_loop_runner)

        self._simulator = Simulation(*self._instances)

        self._simulator.run()

    def OnKey(self, e):
        key = e.GetKeyCode()
        map = self._signalMap
        if (key in map):
            map[key].Toggle()
            self._app.ExitMainLoop()
    
    def OnModuleMove(self, e):
        """ When a module moves (the shape) we need to move its contents
        e.Shape holds the shape that actually moved
        We look up the shape against our module dictionary
        """
        moduleShape = e.Shape
        if (moduleShape in self._moduleMap):
            module = self._moduleMap[moduleShape]
            module.Move(moduleShape.GetX() - module.GetWidth() / 2,
                        moduleShape.GetY() - module.GetHeight() / 2)
    def GetFrame(self):
        """ Get the frame for event firing
        """
        return self._frame
    
    def _refresh(self):
        for s in self._signals:
            s.Update()
        self._canvas.Refresh(False)
       
       
def Init():
    app = wx.App(False)
    manager = Manager(app)
    ogl.OGLInitialize()
    return manager
    
