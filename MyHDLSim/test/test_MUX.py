from unittest import TestCase
from myhdl import Signal, Simulation, delay
from MyHDLSim.combinational import Mux21, Mux41

class TestMUX(TestCase):

    def test2to1(self):
        """ Test a 2 to 1 MUX """
        def test(out, c, a, b):
            yield delay(10)
            for i in range(2):
                a.next = i
                for j in range(2):
                    b.next = j
                    
                    c.next = 0
                    yield delay(10)
                    #print a, b, c, out
                    self.assertEqual(a, out)
                    
                    c.next = 1
                    yield delay(10)
                    #print a, b, c, out
                    self.assertEqual(b, out)

        c, a, b, out = [Signal(None) for i in range(4)]
        gate = Mux21(out, c, a, b)
        check = test(out, c, a, b)
        sim = Simulation(gate, check)
        sim.run(quiet=1)
        
    def test2to1Undefined(self):
        """ Test a 2 to 1 MUX """
        def test(out, c, a, b):
            yield delay(10)
            for i in range(2):
                a.next = i
                c.next = 0
                yield delay(10)
                #print a, b, c, out
                self.assertEqual(a, out)
                
                c.next = 1
                yield delay(10)
                #print a, b, c, out
                self.assertEqual(b, out)

        c, a, b, out = [Signal(None) for i in range(4)]
        gate = Mux21(out, c, a, b)
        check = test(out, c, a, b)
        sim = Simulation(gate, check)
        sim.run(quiet=1)
        
    def test4to1(self):
        """ Test a 4 to 1 MUX """
        def test(out, c0, c1, d0, d1, d2, d3):
            yield delay(10)
            for i in range(2):
                d0.next = i
                for j in range(2):
                    d1.next = j
                    for k in range(2):
                        d2.next = k
                        for l in range(2):
                            d3.next = l
                    
                            c0.next = 0
                            c1.next = 0
                            yield delay(10)
                            print "here?", c0, c1, d0, d1, d2, d3, out
                            self.assertEqual(d0, out)
                            
                            c1.next = 1
                            yield delay(10)
                            #print c0, c1, d0, d1, d2, d3, out
                            self.assertEqual(d1, out)
                            
                            c0.next = 1
                            c1.next = 0
                            yield delay(10)
                            #print c0, c1, d0, d1, d2, d3, out
                            self.assertEqual(d2, out)
                            
                            c0.next = 1
                            c1.next = 1
                            yield delay(10)
                            #print c0, c1, d0, d1, d2, d3, out
                            self.assertEqual(d3, out)

        c0, c1, d0, d1, d2, d3, d4, out = [Signal(None) for i in range(8)]
        gate = Mux41(out, c0, c1, d0, d1, d2, d3)
        check = test(out, c0, c1, d0, d1, d2, d3)
        sim = Simulation(gate, check)
        sim.run(quiet=1)
        
    def test4to1Undefined(self):
        """ Test a 4 to 1 MUX with an undefined input """
        def test(out, c0, c1, d0, d1, d2, d3):
            yield delay(10)
            for i in range(2):
                d0.next = bool(i)
                for j in range(2):
                    d1.next = bool(j)
                    for l in range(2):
                        d3.next = bool(l)
                
                        c0.next = False
                        c1.next = False
                        yield delay(10)
                        print c0, c1, d0, d1, d2, d3, out
                        self.assertEqual(d0, out)
                        
                        c1.next = True
                        yield delay(10)
                        print c0, c1, d0, d1, d2, d3, out
                        self.assertEqual(d1, out)
                        
                        c0.next = True
                        c1.next = False
                        yield delay(10)
                        print c0, c1, d0, d1, d2, d3, out
                        self.assertEqual(d2, out)
                        
                        c0.next = True
                        c1.next = True
                        yield delay(10)
                        print c0, c1, d0, d1, d2, d3, out
                        self.assertEqual(d3, out)

        c0, c1, d0, d1, d2, d3, d4, out = [Signal(None) for i in range(8)]
        gate = Mux41(out, c0, c1, d0, d1, d2, d3)
        check = test(out, c0, c1, d0, d1, d2, d3)
        sim = Simulation(gate, check)
        sim.run(quiet=1)
    
