#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 16:14:19 2019

@author: zanejakobs

AST variance, defined here:
    https://www.sciencedirect.com/science/article/pii/S0304407610000266#fd1
"""
import math

def K(x):
    num = math.gamma((x + 1.0) * 0.5)
    denom = math.sqrt(math.pi * x) * math.gamma(x*0.5)
    return num/denom

def B(a, v1, v2):
    return a * K(v1) + (1-a) * K(v2)

def astAstar(a,v1,v2):
    num = a * K(v1)
    return num/B(a,v1,v2)

def astVar(a, sigma, v1, v2):
    astar = astAstar(a,v1,v2)
    p1 = a*astar*astar * v1 / (v1 - 2) 
    p1 += (1 - a) * (1-astar) * (1-astar) *v2 / (v2-2)
    
    p2 = -1 * astar * astar * v1 / (v1 - 1) + (1-astar) * (1-astar)*v2/(v2-1)
    p2 = p2 * p2
    
    b = B(a,v1,v2)
    
    return sigma * sigma * (4* p1 - 16 * b * b * p2)

def astSD(a, sigma, v1, v2):
    var = astVar(a,sigma,v1,v2)
    return math.sqrt(10*var)/10000
    
    
ssd = astSD( 0.513008,36.8294, 5.4932, 4)
print(ssd)
    
