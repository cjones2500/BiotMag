import numpy as np
import math as m
import ROOT

""" This is an abstract object for a generic current object.
    Any features specific to a generic current object should
    be included here"""
class currentObj(object):
    
    """Initialize the current object"""
    def __init__(self,numberOfElements):
        self.numberOfElements = int(numberOfElements)
        
        """ Initialize a numpy array with a sufficient description
            for the current source object where the different
            elements are (x,y,z,b_x,b_y,b_z)"""
        self.currentElements = np.zeros( (self.numberOfElements, 6) )
            
    """Return a description of the current object"""    
    def __str__(self):
        return  "Abstract Current Object seen as a summation of many current sources"

"""Class defines a simple current point"""
class currentPoint(currentObj):
    
    def __init__(self, x, y, z, ix, iy, iz, numberOfElements=1.0):
        currentObj.__init__(self,numberOfElements)
        self.x = x
        self.y = y
        self.z = z 
        self.ix = ix
        self.iy = iy
        self.iz = iz
        
        self.currentElements[0][0] = self.x
        self.currentElements[0][1] = self.y
        self.currentElements[0][2] = self.z
        self.currentElements[0][3] = self.ix
        self.currentElements[0][4] = self.iy
        self.currentElements[0][5] = self.iz
