from unittest import TestCase
from myhdl import Signal, Simulation, always, intbv, delay, now
from MyHDLSim.sequential import Register, Counter, ClkDriver

class TestRegister(TestCase):

    def testLoad(self):
        """ Test a Register load from 1 to 7 bits, always enabled """
        
        for i in range(1, 8):
            clk = Signal(0)
            clock_gen = ClkDriver(clk, period=4)
            
            #print "Testing", i, "bits"
            out = Signal(intbv(0)[i:])
            data = Signal(intbv(2**i - 1)[i:])
            en = Signal(1)
            reg = Register(out, data, clk, en)
            
            flag = Signal(0)
            
            # make sure it gets register value updated
            @always(clk.posedge)
            def test():
                # need to delay by one
                if flag == 1:
                    self.assertEqual(int(out), int(data))
                else:
                    flag.next = 1
            
            sim = Simulation(reg, clock_gen, test)
            sim.run(20, quiet=1)
            
    def testNoLoad(self):
        """ Test a Register load from 1 to 7 bits, always disabled """
        
        for i in range(1, 8):
            clk = Signal(0)
            clock_gen = ClkDriver(clk, period=4)
            
            #print "Testing", i, "bits"
            out = Signal(intbv(2**(i - 1))[i:])
            data = Signal(intbv(2**i - 1)[i:])
            en = Signal(0)
            reg = Register(out, data, clk, en)
            
            flag = Signal(0)
            
            # make sure it gets register value does not change
            @always(clk.posedge)
            def test():
                # need to delay by one
                if flag == 1:
                    self.assertEqual(int(out), int(out))
                else:
                    flag.next = 1
            
            sim = Simulation(reg, clock_gen, test)
            sim.run(20, quiet=1)
    
    def testLoadingCounter(self):
        """ Test a Register load from 1 to 4 bits, using a counter """
        
        for i in range(1, 5):
            clk = Signal(0)
            clock_gen = ClkDriver(clk, period=4)
            
            #print "Testing", i, "bits"
            out = Signal(intbv(2**(i - 1))[i:])
            data, prev_data = [Signal(intbv(2**i - 1)[i:]) for j in range(2)]
            en, prev_en = [Signal(0) for j in range(2)]
            reg = Register(out, data, clk, en)
            count = Counter(data, clk, Signal(1))
            
            flag = Signal(0)
            
            # make sure it gets register value updated if enabled
            @always(clk.posedge)
            def test():
                #print now(), ":", "data:", prev_data, "->", data, "out:", out, flag, "en?", en
                
                # need to delay checking by one so the register gets written, use flag
                if flag == 1:
                    # register only changes if enabled
                    #compare to previous data since we are one step late (see above)
                    if int(prev_en) == 1:
                        self.assertEqual(int(out), int(prev_data))
                    else:
                        self.assertEqual(int(out), int(out))
                    flag.next = 0
                else:
                    # need to store current data and enable value for the check next time (data is delayed)
                    prev_en.next = en
                    prev_data.next = data
                    flag.next = 1
                    
                #toggle en when we reach highest count, just to mix things up
                if int(data) == (2**i - 1):
                    en.next = not en
            
            sim = Simulation(count, reg, clock_gen, test)
            # runs long enough that we cycle through the numbers a little
            sim.run(60, quiet=1)            