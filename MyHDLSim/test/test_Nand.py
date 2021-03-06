from unittest import TestCase
from myhdl import Signal, Simulation, delay
from MyHDLSim.combinational import Nand

class TestNandGate(TestCase):

    def testTwoBits(self):
        """ Check that given two bits, we return the proper output """
        def test(out, a, b):
            yield delay(10)
            for i in range(2):
                a.next = i
                for j in range(2):
                    b.next = j
                    yield delay(10)
                    #print a, b, out
                    self.assertEqual(not(a and b), out)

        a, b, out = [Signal(None) for i in range(3)]
        gate = Nand(out, a, b)
        check = test(out, a, b)
        sim = Simulation(gate, check)
        sim.run(quiet=1)
    
    def testThreeBits(self):
        """ Check that given three bits, we return the proper output """
        def test(out, a, b, c):
            yield delay(10)
            for i in range(2):
                a.next = i
                for j in range(2):
                    b.next = j
                    for k in range(2):
                        c.next = k
                        yield delay(10)
                        #print a, b, c, out
                        self.assertEqual(not(a and b and c), out)

        a, b, c, out = [Signal(None) for i in range(4)]
        gate = Nand(out, a, b, c)
        check = test(out, a, b, c)
        sim = Simulation(gate, check)
        sim.run(quiet=1)
        
    def testFourBits(self):
        """ Check that given four bits, we return the proper output """
        def test(out, a, b, c, d):
            yield delay(10)
            for i in range(2):
                a.next = i
                for j in range(2):
                    b.next = j
                    for k in range(2):
                        c.next = k
                        for l in range(2):
                            d.next = l
                            yield delay(10)
                            #print a, b, c, d, out
                            self.assertEqual(not(a and b and c and d), out)

        a, b, c, d, out = [Signal(None) for i in range(5)]
        gate = Nand(out, a, b, c, d)
        check = test(out, a, b, c, d)
        sim = Simulation(gate, check)
        sim.run(quiet=1)
        
    def testUndefinedOneOfTwo(self):
        """ Make sure NAND gate properly outputs None when given None """
        def test(out, a, b):
            yield delay(10)
            for i in range(2):
                a.next = i
                yield delay(10)
                #print a, b, out
                self.assertEqual(Signal(None), out)

        a, b, out = [Signal(None) for i in range(3)]
        gate = Nand(out, a, b)
        check = test(out, a, b)
        sim = Simulation(gate, check)
        sim.run(quiet=1)
        
    def testUndefinedOneOfFour(self):
        """ Make sure NAND gate properly outputs None when given None for 4 bits """
        def test(out, a, b, c, d):
            yield delay(10)
            for i in range(2):
                a.next = i
                for j in range(2):
                    b.next = j
                    for k in range(2):
                        d.next = k
                        yield delay(10)
                        #print a, b, c, d, out
                        self.assertEqual(Signal(None), out)

        a, b, c, d, out = [Signal(None) for i in range(5)]
        gate = Nand(out, a, b, c, d)
        check = test(out, a, b, c, d)
        sim = Simulation(gate, check)
        sim.run(quiet=1)
