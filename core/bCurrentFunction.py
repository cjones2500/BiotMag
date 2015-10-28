""" This module contains a set of current functions that can be used to vary
    the current along a line or a set of vectors defined by either a line
    or a curve segment"""
import ROOT
import math as m

def constantCurrent(vector,radialVector):
    return vector.Unit()

def reverseConstantCurrent(vector,radialVector):
    return -1.0*vector.Unit()
    
def effectiveTokamakCurrent(vector,radialVector):
    """Calculate the theta of this vector"""
    radius = m.sqrt(radialVector.X()*radialVector.X() + radialVector.Y()*radialVector.Y())
    majorRadius = radius*1.0
    theta = m.acos(radialVector.X()/radius)
    currentVectorMag = (vector.Mag())/(2.0*m.pi*(majorRadius + radius*(1.0+m.cos(theta))))
    vector.SetMag(currentVectorMag)
    return vector
