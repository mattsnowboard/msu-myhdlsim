from unittest import TestCase
from myhdl import Signal, Simulation, delay, intbv, always
from MyHDLSim.sequential import ClkDriver, dff
from random import randrange

class TestDFF(TestCase):

    def testReset(self):
        """ Test DFF reset """
        
        q, d, clk = [Signal(0) for i in range(3)]
        clock_gen = ClkDriver(clk)
        
        # introduce some random flipping of D which has no effect
        @always(delay(7))
        def toggle():
            d.next = not d
        
        @always(clk.posedge)
        def test():
            self.assertEqual(q.next, 0)
        
        flip_flop = dff(q, d, clk, Signal(0))
        sim = Simulation(clock_gen, flip_flop, toggle, test)
        sim.run(100, quiet=1)
        
    def testSet(self):
        """ Test DFF set """
        
        q, d, clk = [Signal(0) for i in range(3)]
        clock_gen = ClkDriver(clk)
        
        # introduce some random flipping of D which has no effect
        @always(delay(7))
        def toggle():
            d.next = not d
        
        @always(clk.posedge)
        def test():
            self.assertEqual(q.next, 1)
        
        flip_flop = dff(q, d, clk, Signal(1), Signal(0))
        sim = Simulation(clock_gen, flip_flop, toggle, test)
        sim.run(100, quiet=1)
        
    def testLatchOnEdge(self):
        """ Test DFF latches on clock rising edge """
        
        q, d, clk = [Signal(0) for i in range(3)]
        old_q, old_clk = [Signal(0) for i in range(2)]
        clock_gen = ClkDriver(clk)
        
        # change d longer than period so it will hold and change mid clock cycle
        @always(delay(36))
        def toggle():
            d.next = not d

        
        def testChange():
            for i in range(200):
                # check when no change in clock or falling edge
                if clk == old_clk or clk == 0:
                    self.assertEqual(bool(q), bool(old_q))
                # check for rising edge
                else:
                    self.assertEqual(bool(q), bool(d))
                old_q.next = q
                old_clk.next = clk
                yield delay(2)
        
        flip_flop = dff(q, d, clk)
        check = testChange()
        sim = Simulation(clock_gen, flip_flop, check, toggle)
        sim.run(200, quiet=1)