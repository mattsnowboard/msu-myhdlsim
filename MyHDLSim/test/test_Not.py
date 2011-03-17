from unittest import TestCase
from myhdl import Signal, Simulation, delay
from MyHDLSim.combinational import Not

class TestNotGate(TestCase):

    def testOneBit(self):
        """ Check that given a bit, we return the inverse """
        def test(out, a):
            yield delay(10)
            for i in range(2):
                a.next = i
                yield delay(10)
                #print a, b, out
                self.assertEqual(not a, out)

        a, out = [Signal(None) for i in range(2)]
        gate = Not(out, a)
        check = test(out, a)
        sim = Simulation(gate, check)
        sim.run(quiet=1)
        
    def testUndefinedBit(self):
        """ Make sure NOT gate properly outputs None when given None """
        def test(out, a):
            yield delay(10)
            self.assertEqual(Signal(None), out)

        a, out = [Signal(None) for i in range(2)]
        gate = Not(out, a)
        check = test(out, a)
        sim = Simulation(gate, check)
        sim.run(quiet=1)
        
    def testToggleUndefinedBit(self):
        """ Make sure NOT gate properly output changes when input changes from None """
       
        
        def test(out, a):
            yield delay(10)
            self.assertEqual(Signal(None), a)
            self.assertEqual(Signal(None), out)
            a.next = True
            yield delay(10)
            self.assertEqual(Signal(False), out)
            
        a, out = [Signal(None) for i in range(2)]
        gate = Not(out, a)
        check = test(out, a)
        sim = Simulation(gate, check)
        sim.run(quiet=1)