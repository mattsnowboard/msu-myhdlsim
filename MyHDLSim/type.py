from myhdl import Signal, always, always_comb, instances, instance, delay
from MyHDLSim.combinational import Not, Mux21

def ClkDriver(clk, period=20):

    """ Clock Driver helper
    
    Credit to http://www.myhdl.org/doc/current/manual/intro.html
    This will generate a clock of any period (default 20)
    clk -- clock signal (output)
    period -- how long the clock period is
    
    """

    lowTime = int(period/2)
    highTime = period - lowTime

    @instance
    def driveClk():
        while True:
            yield delay(lowTime)
            clk.next = 1
            yield delay(highTime)
            clk.next = 0

    return driveClk


def tff(q, t, clk, rst = Signal(1), set = Signal(1)):
    
    """ T Flip Flop with asyncronous set/reset
    
    q -- output
    t -- input
    clk -- clock
    rst -- active low reset
    
    """
 
    @always(clk.posedge, rst.negedge, set.negedge)
    def logic():
        if rst == 0:
            q.next = 0
        elif set == 0:
            q.next = 1
        else:
            if t == 1:
                q.next = not q
            else:
                q.next = q
 
    return instances()

def dff(q, d, clk, rst = Signal(1), set = Signal(1)):
    
    """ D Flip Flop with asyncronous set/reset
    
    q -- output
    d -- input
    clk -- clock
    rst -- active low reset
    set -- active low set
    
    """
 
    @always(clk.posedge, rst.negedge, set.negedge)
    def logic():
        if rst == 0:
            q.next = 0
        elif set == 0:
            q.next = 1
        else:
            q.next = d
 
    return instances()
    
def Counter(out, clk, rst = 1):
    
    """ n-bit Counter
    
    out -- output signal with specified bit length
    clk -- clock
    rst -- active-low reset
    
    """
    
    n = len(out)
    tff_inst = [None for i in range(n)]
    not_inst = [None for i in range(n)]
    int_clk = [Signal(int(not out(i))) for i in range(n)]
    out_temp = [Signal(int(out(i))) for i in range(n)]
    
    tff_inst[0] = tff(out_temp[0], Signal(1), clk, rst)
    not_inst[0] = Not(int_clk[0], out_temp[0])
    for i in range(1, n):
        tff_inst[i] = tff(out_temp[i], Signal(1), int_clk[i - 1], rst)
        not_inst[i] = Not(int_clk[i], out_temp[i])
    
    @always_comb
    def connect_out_bits():
        for i in range(n):
            out.next[i] = out_temp[i]
    
    return instances()

def Register(out, data, clk, en):

    """ Parallel load register
    
    out -- output bit vector
    data -- input bit vector
    clk -- clock signal
    en -- enable signal to send data to outputs
    
    """
    
    n = len(data)
    dff_inst = [None for i in range(n)]
    mux_inst = [None for i in range(n)]
    out_temp = [Signal(int(out(i))) for i in range(n)]
    out_list = [out(i) for i in range(n)]
    data_list = [data(i) for i in range(n)]
    input = [Signal(0) for i in range(n)]
    
    for i in range(n):
        mux_inst[i] = Mux21(input[i], en, out_list[i], data_list[i])
        dff_inst[i] = dff(out_temp[i], input[i], clk)
        
    @always_comb
    def connect_out_bits():
        for i in range(n):
            out.next[i] = out_temp[i]
        
    return instances()
    