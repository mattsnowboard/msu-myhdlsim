from unittest import TestCase
from myhdl import Signal, Simulation, delay, intbv, always
from MyHDLSim.sequential import ClkDriver, tff
from random import randrange

class TestTFF(TestCase):

    def testReset(self):
        """ Test TFF reset """
        
        q, t, clk = [Signal(0) for i in range(3)]
        clock_gen = ClkDriver(clk)
        
        # introduce some random flipping of T which has no effect
        @always(delay(7))
        def toggle():
            t.next = not t
        
        @always(clk.posedge)
        def test():
            self.assertEqual(q.next, 0)
        
        flip_flop = tff(q, t, clk, Signal(0))
        sim = Simulation(clock_gen, flip_flop, toggle, test)
        sim.run(100, quiet=1)
        
    def testSet(self):
        """ Test TFF set """
        
        q, t, clk = [Signal(0) for i in range(3)]
        clock_gen = ClkDriver(clk)
        
        # introduce some random flipping of T which has no effect
        @always(delay(7))
        def toggle():
            t.next = not t
        
        @always(clk.posedge)
        def test():
            self.assertEqual(q.next, 1)
        
        flip_flop = tff(q, t, clk, Signal(1), Signal(0))
        sim = Simulation(clock_gen, flip_flop, toggle, test)
        sim.run(100, quiet=1)
        
    def testToggleOnEdge(self):
        """ Test TFF toggles on clock rising edge """
        
        q, clk = [Signal(0) for i in range(2)]
        old_q, old_clk = [Signal(0) for i in range(2)]
        clock_gen = ClkDriver(clk)
        
        def testChange():
            for i in range(200):
                # check when no change in clock or falling edge
                if clk == old_clk or clk == 0:
                    self.assertEqual(bool(q), bool(old_q))
                # check for rising edge
                else:
                    self.assertEqual(bool(q), bool(not old_q))
                old_q.next = q
                old_clk.next = clk
                yield delay(2)
        
        flip_flop = tff(q, Signal(1), clk)
        check = testChange()
        sim = Simulation(clock_gen, flip_flop, check)
        sim.run(100, quiet=1)
 
    def testNoToggle(self):
        """ Test TFF does not toggle unless T is set """
        
        q, clk, t = [Signal(0) for i in range(3)]
        old_q, old_clk = [Signal(0) for i in range(2)]
        clock_gen = ClkDriver(clk)
        
        def testChange():
            for i in range(100):
                #print i, "t:", t, "clk:", old_clk, "->", clk, "q:", old_q, "->", q
                # check when clock has not changed, or is falling edge, or T is deasserted
                if clk == old_clk or clk == 0 or t == 0:
                    self.assertEqual(bool(q), bool(old_q))
                # check when t is asserted and rising edge
                else:
                    self.assertEqual(bool(q), bool(not old_q))
                old_q.next = q
                old_clk.next = clk
                yield delay(2)
                if i > 50:
                    t.next = 1
        
        flip_flop = tff(q, t, clk)
        check = testChange()
        sim = Simulation(clock_gen, flip_flop, check)
        sim.run(200, quiet=1)