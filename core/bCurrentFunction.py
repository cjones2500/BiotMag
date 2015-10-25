""" This module contains a set of current functions that can be used to vary
    the current along a line or a set of vectors defined by either a line
    or a curve segement"""
import ROOT

def constantCurrent(vector):
    return vector.Unit()

def reverseConstantCurrent(vector):
    return -1.0*vector.Unit()
    
