from unittest import TestCase
from myhdl import Signal, Simulation, always, intbv, delay
from MyHDLSim.sequential import Counter, ClkDriver

class TestCounter(TestCase):

    def testCounting(self):
        """ Test a Counter from 1 to 5 bits """
        
        clk = Signal(0)
        clock_gen = ClkDriver(clk, period=4)
        
        for i in range(1, 6):
            #print "Testing", i, "bits"
            out = Signal(intbv(0)[i:])
            prev_out = Signal(intbv(2**i - 1)[i:])
            counter = Counter(out, clk, Signal(1))
            
            # make sure it increments and wraps at modulo 2^n
            @always(clk.posedge)
            def test():
                #print out, prev_out
                self.assertEqual(int(out), int((prev_out + 1) % 2**(len(prev_out))))
                prev_out.next = out
            
            sim = Simulation(counter, clock_gen, test)
            sim.run(12 * 2**i, quiet=1)
            
    def testReset(self):
        """ Test the reset function of a 4-bit counter """
        
        clk = Signal(0)
        rst = Signal(1)
        clock_gen = ClkDriver(clk, period=4)
        
        out = Signal(intbv(0)[4:])
        counter = Counter(out, clk, rst)
        
        def test():
            for i in range(200):
                # count up to 9 then reset
                if int(out) == 9:
                    rst.next = 0
                    yield delay(1)
                    self.assertEqual(int(out), 0)
                # turn off reset next time
                else:
                    rst.next = 1
                yield delay(1)
        
        check = test()
        sim = Simulation(counter, clock_gen, check)
        sim.run(400, quiet=1)