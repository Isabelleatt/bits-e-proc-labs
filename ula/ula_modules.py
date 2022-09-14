#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

from myhdl import *


@block
def halfAdder(a, b, soma, carry):
    @always_comb
    def comb():
        soma.next = a ^ b
        carry.next = a & b

    return instances()


@block
def fullAdder(a, b, c, soma, carry):
    s = [Signal(bool(0)) for i in range(3)]

    half_1 = halfAdder(a, b, s[0], s[1]) 
    half_2 = halfAdder(c, s[0], soma, s[2]) 

    @always_comb
    def comb():
        carry.next = s[1] | s[2]

    return instances()


@block
def adder2bits(x, y, soma, carry):
    carry_2 = Signal((bool(0)))
    half = halfAdder(x[0], y[0], soma[0], carry_2)
    full = fullAdder(x[1], y[1], carry_2, soma[1], carry)        
    return instances()


@block
def adder(x, y, soma, carry):
    n = len(x)
    faList = [None for i in range(n)]
    c = [Signal(bool(0)) for i in range(n+1)]

    faList[0] = fullAdder(x[0], y[0], c[0], soma[0], c[1])

    for i in range(1, n):
        faList[i] = fullAdder(x[i], y[i], c[i], soma[i], c[i+1])

    return instances()

@block
def adderIntbv(x, y, soma, carry):
    @always_comb
    def comb():
        sum = x + y
        soma.next = sum
        if sum > x.max - 1:
            carry.next = 1
        else:
            carry.next = 0

    return comb