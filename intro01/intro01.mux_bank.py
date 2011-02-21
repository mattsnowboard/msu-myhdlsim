from myhdl import Signal, Simulation, delay, always_comb, instances, intbv, ConcatSignal, instance
from random import randrange
from MyHDLSim.combinational import Mux21
    
def MultibitMux21(out, select, a, b):

    """ 2 to 1 multibit MUX.
    
    out -- output
    select -- control input
    a, b -- data inputs
    
    Determine the number of bits using just the intbv "a"

    """

    mux_inst = [None for i in range(len(a))]
    out_temp = [Signal(0) for i in range(len(a))]
    a_list = [a(i) for i in range(len(a))]
    b_list = [b(i) for i in range(len(b))]
    
    for i in range(len(a)):
        mux_inst[i] = Mux21(out_temp[i], select, a_list[i], b_list[i])
    
    @always_comb
    def connect_out_bits():
        for i in range(len(a)):
            out.next[i] = out_temp[i]

    return mux_inst, connect_out_bits

def testBench(width):

    out, A, B = [Signal(intbv(0)[width:]) for i in range(3)]
    select = Signal(0)

    mux = MultibitMux21(out, select, A, B)

    @instance
    def stimulus():
        print "s a b out"
        for i in range(8):
            A.next, B.next = randrange(16), randrange(16)
            for s in range(2):
                select.next = s
                yield delay(10)
                print "%s %s %s %s" % (select, A, B, out)

    return mux, stimulus

sim = Simulation(testBench(4))
sim.run()
