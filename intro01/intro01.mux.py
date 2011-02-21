from myhdl import Signal, Simulation, delay, always_comb, instances
from random import randrange
from MyHDLSim.combinational import Mux41

out, c1, c0, d0, d1, d2 = [Signal(0) for i in range(6)]
one = Signal(1)

mux = Mux41(out, c0, c1, d0, d1, d2, one)

def test():
    print "c0 c1 d0 d1 d2 d3 out"
    for data_0 in range(2):
        for data_1 in range(2):
            for data_2 in range(2):
                for control_2 in range(2):
                    for control_1 in range(2):
                        c1.next, c0.next, d2.next, d1.next, d0.next = control_1, control_2, data_2, data_1, data_0
                        yield delay(10)
                        print "%s  %s  %s  %s  %s  %s  %s" % (c0, c1, d0, d1, d2, one, out)

test_1 = test()

sim = Simulation(mux, test_1)
sim.run()
