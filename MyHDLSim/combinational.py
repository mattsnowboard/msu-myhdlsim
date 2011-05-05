from myhdl import Signal, always_comb, instances, now

"""
The following are built on top of MyHDL to offer basic combinational circuits
"""

def And(f, a, b, c = Signal(1), d = Signal(1)):

    """ AND gate.
    
    f -- output
    a, b, c, d -- data inputs

    """

    @always_comb
    def logic():
        print now()
        if (a == None or b == None or c == None or d == None):
            f.next = None
        else:
            f.next = a and b and c and d

    return logic

def Nand(f, a, b, c = Signal(1), d = Signal(1)):

    """ NAND gate.
    
    f -- output
    a, b, c, d -- data inputs

    """

    @always_comb
    def logic():
        if (a == None or b == None or c == None or d == None):
            f.next = None
        else:
            f.next = not( a and b and c and d )

    return logic

def Or(f, a, b, c = Signal(0), d = Signal(0)):

    """ OR gate.
    
    f -- output
    a, b, c, d -- data inputs

    """

    @always_comb
    def logic():
        if (a == None or b == None or c == None or d == None):
            f.next = None
        else:
            f.next = a or b or c or d

    return logic

def Nor(f, a, b, c = Signal(0), d = Signal(0)):

    """ NOR gate.
    
    f -- output
    a, b, c, d -- data inputs

    """

    @always_comb
    def logic():
        if (a == None or b == None or c == None or d == None):
            f.next = None
        else:
            f.next = not( a or b or c or d )

    return logic

def Not(f, a):

    """ NOT gate.
    
    f -- output
    a -- data input

    """

    @always_comb
    def logic():
        if (a == None):
            f.next = None
        else:
            f.next = not a

    return logic

def Xor(f, a, b, c = Signal(0), d = Signal(0)):

    """ XOR gate.

    f -- output
    a, b, c, d -- data inputs

    """

    @always_comb
    def logic():
        if (a == None or b == None or c == None or d == None):
            f.next = None
        else:
            f.next = (a ^ b ^ c ^ d)

    return logic

def Nxor(f, a, b, c = Signal(0), d = Signal(0)):

    """ NXOR gate.
    
    f -- output
    a, b, c, d -- data inputs

    """

    @always_comb
    def logic():
        if (a == None or b == None or c == None or d == None):
            f.next = None
        else:
            f.next = not(a ^ b ^ c ^ d)

    return logic

def Mux21(out, select, a, b):

    """ 2 to 1 MUX.
    
    out -- output
    select -- control input
    a, b -- data inputs

    """

    @always_comb
    def logic():
        if select == None:
            out.next = None
        elif select == 0:
            out.next = a
        else:
            out.next = b

    return logic
    
def Mux41(out, c0, c1, d0, d1, d2, d3):
    
    """ 4 to 1 MUX implemented as 3 2-to-1 MUX's
    
    out -- output
    c0, c1 -- control inputs
    d0, d1, d2, d3 -- data inputs
    
    """
    
    # I would like the intermediates to be initialized to None, but it won't work
    lsb_out1, lsb_out2 = [Signal(None) for i in range(2)]
    lsb_mux1 = Mux21(lsb_out1, c1, d0, d1)
    lsb_mux2 = Mux21(lsb_out2, c1, d2, d3)
    msb_mux = Mux21(out, c0, lsb_out1, lsb_out2)
    
    return instances()

def Decoder(out, data, en):
    
    """ m-to-n Decoder
    
    The out must hold enough bits for the size of data
    so len(out) = n, then len(max{data}) = m, n = 2^m
    out -- output from decoder (intbv)
    data -- input to decorder (intbv)
    en -- enable
    
    """
    
    @always_comb
    def logic():
        out.next = 0
        if en == 1:
            out.next[data] = 1
    
    return logic
