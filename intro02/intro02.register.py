from myhdl import Signal, Simulation, delay, always_comb, always, instances, traceSignals, intbv, concat
from random import randrange
from MyHDLSim.sequential import Register

def test():

    clk = Signal(0)
    enable = Signal(1)
    data = Signal(intbv(5)[4:])
    out = Signal(intbv(0)[4:])

    register = Register(out, data, clk, enable)

    @always(delay(10))
    def clkgen():
        clk.next = not clk
        
    @always(clk.posedge)
    def printVal():
        print "Data: %s Enable: %s Register out: %s" % (data, enable, out)
    
    @always(delay(3))
    def change():
        enable.next = not enable
        data.next = intbv(randrange(16))
        
    
    return instances()

        
def simulate(timesteps):
    tb = traceSignals(test)
    sim = Simulation(tb)
    sim.run(timesteps)
 
simulate(200)
