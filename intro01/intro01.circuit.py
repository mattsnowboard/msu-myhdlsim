from myhdl import Signal, Simulation, delay, always_comb, instances
from random import randrange
from MyHDLSim.combinational import Not, And, Or

def Circuit(a, b, c, d, f):
    
    """ Circuit component
    
    This contains several gates
    a, b, c, d -- input signals
    f -- output signal
    
    """
    
    notb, notc, notd = [Signal(0) for i in range(3)]
    and1, and2 = [Signal(0) for i in range(2)]
    not_b_inst = Not(notb, b)
    not_c_inst = Not(notc, c)
    not_d_inst = Not(notd, d)
    
    and1_inst = And(and1, a, notb)
    and2_inst = And(and2, b, notc, notd)
    
    or_inst = Or(f, and1, and2)
    
    return instances()

a, b, c, d, f = [Signal(0) for i in range(5)]

circuit = Circuit(a, b, c, d, f)

def test():
    print "a b c d f"
    for a_count in range(2):
        for b_count in range(2):
            for c_count in range(2):
                for d_count in range(2):
                    a.next, b.next, c.next, d.next = a_count, b_count, c_count, d_count
                    yield delay(10)
                    print "%s %s %s %s %s" % (a, b, c, d, f)

test_1 = test()

sim = Simulation(circuit, test_1)
sim.run()
