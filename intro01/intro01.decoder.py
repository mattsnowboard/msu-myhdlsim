from myhdl import Signal, Simulation, delay, always_comb, always, instances, traceSignals, intbv, concat
from random import randrange
from MyHDLSim.sequential import Counter
from MyHDLSim.combinational import Decoder

def test():

    clk = Signal(0)
    enable = Signal(1)
    rst = Signal(1)
    count = Signal(intbv(0)[3:])
    decode = Signal(intbv(0)[8:])

    counter = Counter(count, clk, rst)
    decoder = Decoder(decode, count, enable)

    @always(delay(10))
    def clkgen():
        clk.next = not clk
        
    @always(clk.posedge)
    def printVal():
        print "Counter: %s Enable: %s Decoder: %s" % (count, enable, decode)
    
    return counter, decoder, clkgen, printVal

        
def simulate(timesteps):
    tb = traceSignals(test)
    sim = Simulation(tb)
    sim.run(timesteps)
 
simulate(200)
