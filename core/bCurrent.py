import numpy as np
import math as m
import ROOT

""" This is an abstract object for a generic current object.
    Any features specific to a generic current object should
    be included here"""
class currentObj(object):
    
    """Initialize the current object"""
    def __init__(self,numberOfElements,sizeOfCurrent):
        self.numberOfElements = int(numberOfElements)
        self.sizeOfCurrent = sizeOfCurrent
        
        """ Initialize a numpy array with a sufficient description
            for the current source object where the different
            elements are (x,y,z,b_x,b_y,b_z)"""
        self.currentElements = np.zeros( (self.numberOfElements, 6) )
            
    """Return a description of the current object"""    
    def __str__(self):
        return  "Abstract Current Object seen as a summation of many current sources"

"""Class defines a simple current point and inherits from a currentObj"""
class currentPoint(currentObj):
    
    def __init__(self, x, y, z, ix, iy, iz, numberOfElements=1.0):
        currentObj.__init__(self,numberOfElements,sizeOfCurrent=1.0)
        self.x = x
        self.y = y
        self.z = z
    
        self.ix = ix
        self.iy = iy
        self.iz = iz
        
        """Override the size of the current """
        self.sizeOfCurrent = m.sqrt(self.ix*self.ix + self.iy*self.iy + self.iz*self.iz)
        
        self.currentElements[0][0] = self.x
        self.currentElements[0][1] = self.y
        self.currentElements[0][2] = self.z
        self.currentElements[0][3] = self.ix
        self.currentElements[0][4] = self.iy
        self.currentElements[0][5] = self.iz

""" Class defines a stright wire with a certain number of elements and takes a TVector3 as an argument.
    This current class can be used to define the current in three dimensions"""
class currentLine(currentObj):
    """ Initialized by defining two points to draw the line and a currentVectorFunction() is
        also provided to generate the current vector at a given point """
    def __init__(self,pointA,pointB,currentVectorFunction,numberOfElements,sizeOfCurrent=1.0):
        currentObj.__init__(self,numberOfElements,sizeOfCurrent)
        self.numberOfElements = int(numberOfElements)
        
        """Check that a TVector3 has been given to this class """
        if (not isinstance(pointA, ROOT.TVector3)) or (not isinstance(pointB, ROOT.TVector3)) :
            raise TypeError("Points on the line must be a TVector3")
        self.pointA = pointA
        self.pointB = pointB
        
        """Divide each length into equal parts """
        widthInX = (self.pointB.X() - self.pointA.X())/float(self.numberOfElements)
        widthInY = (self.pointB.Y() - self.pointA.Y())/float(self.numberOfElements)
        widthInZ = (self.pointB.Z() - self.pointA.Z())/float(self.numberOfElements)
        
        """Loop over all the points and calculate the straight line path """
        for iPoint in range(0,self.numberOfElements):
            self.currentElements[iPoint][0] = self.pointA.X() + widthInX*iPoint
            self.currentElements[iPoint][1] = self.pointA.Y() + widthInY*iPoint
            self.currentElements[iPoint][2] = self.pointA.Z() + widthInZ*iPoint
            
            """ Hand a TVector3 to the currentVectorFunction, this follows the path of the
                current by default and nay manipulations are added """
            iCurrentVector = ROOT.TVector3( widthInX,
                                            widthInY,
                                            widthInZ)
            
            """Update to reflect the current direction and size at a given point """
            iCurrentVector = currentVectorFunction(iCurrentVector)*self.sizeOfCurrent
            
            """Calculate the current Vector at each point from the current vector function """
            self.currentElements[iPoint][3] = iCurrentVector.X()          
            self.currentElements[iPoint][4] = iCurrentVector.Y()
            self.currentElements[iPoint][5] = iCurrentVector.Z()
                
"""Class to define a circle of current that represents a coil """
class currentCoil(currentObj):
    def __init__(self,centerPoint,radius,currentVectorFunction,numberOfElements,sizeOfCurrent=1.0):
        currentObj.__init__(self,numberOfElements,sizeOfCurrent)
        self.numberOfElements = int(numberOfElements)
        
        """Check that a TVector3 has been given to this class """
        if (not isinstance(centerPoint, ROOT.TVector3)):
            raise TypeError("Points on the line must be a TVector3")
        
        segmentDivision =  (2.0*m.pi)/self.numberOfElements
        for iPoint in xrange(0,self.numberOfElements):
            theta = segmentDivision*iPoint*1.0
            self.currentElements[iPoint][0] = centerPoint.X() + radius*m.cos(theta) 
            self.currentElements[iPoint][1] = centerPoint.Y() + radius*m.sin(theta)
            self.currentElements[iPoint][2] = centerPoint.Z()
            
            """ Hand a TVector3 to the currentVectorFunction, this follows the path of the
                current by default and nay manipulations are added """
            iCurrentVector = ROOT.TVector3( radius*m.cos(theta),
                                            radius*m.sin(theta),
                                            centerPoint.Z())
            
            """Always choose the vector the is orthogonal to the direction from the center of the coil"""
            iCurrentVector = (iCurrentVector.Orthogonal())*self.sizeOfCurrent
            
            """Define a radial vector from the center of the coil """
            radiusVector = ROOT.TVector3(   self.currentElements[iPoint][0],
                                            self.currentElements[iPoint][1],
                                            self.currentElements[iPoint][2])
        
            """Update to reflect the current direction and size at a given point """
            iCurrentVector = currentVectorFunction(iCurrentVector,radiusVector)
        
            """Calculate the current Vector at each point from the current vector function """
            self.currentElements[iPoint][3] = iCurrentVector.X()          
            self.currentElements[iPoint][4] = iCurrentVector.Y()
            self.currentElements[iPoint][5] = iCurrentVector.Z()
                