from unittest import TestCase
from myhdl import Signal, Simulation, delay, intbv
from MyHDLSim.combinational import Decoder

class TestDecoder(TestCase):

    def testAll(self):
        """ Test a 2 to 4, 3 to 8, and 4 to 16 decoder while enabled """
        def test(out, data):
            yield delay(10)
            for i in range(data.max):
                data.next = i
                yield delay(10)
                #print a, b, c, out
                #check for a single 1, and the remaining bits 0
                self.assertEqual(out[data], 1)
                for i in range(len(out)):
                    if i != data:
                        self.assertEqual(out[i], 0)
        
        for i in range(2, 4):
            data = Signal(intbv(0)[i:])
            out = Signal(intbv(0)[2**i:])
            gate = Decoder(out, data, Signal(1))
            check = test(out, data)
            sim = Simulation(gate, check)
            sim.run(quiet=1)
    
    def testDisabled(self):
        """ Test 2 to 4, 3 to 8, and 4 to 16 decoder while disabled """
        def test(out, data):
            yield delay(10)
            for i in range(data.max):
                data.next = i
                yield delay(10)
                #print a, b, c, out
                self.assertEqual(out, 0)
        
        for i in range(2, 4):
            data = Signal(intbv(0)[i:])
            out = Signal(intbv(0)[2**i:])
            gate = Decoder(out, data, Signal(0))
            check = test(out, data)
            sim = Simulation(gate, check)
            sim.run(quiet=1)
 