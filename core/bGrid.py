import numpy as np
import math as m
import ROOT

""" This is an abstract object of a grid of NxN size for
    projecting the effective magnetic field within a
    given cell. It is composed of a number of cells and
    is defined to have equal lengths in N dimensions"""
class bGrid(object):
    
    """Initialize the grid object"""
    def __init__(self,length,numberOfCells,truncation):
        self.length = length
        self.numberOfCells = int(numberOfCells)
        """ Defined the the number of parameters per cell as
            (x, y, z, b_x, b_y, b_z) in additional to the position
            of the cell """
        self.parametersPerCell = 6
        self.cellsInGrid = np.zeros( (self.numberOfCells,self.parametersPerCell))
        
        """ Tructation of the magnetic field density
            as is approached a point current source"""
        self.truncation = truncation 

    """Return a description of the grid object"""    
    def __str__(self):
        return  "Abstract Grid Object to add magnetic fields"
    
    """ add the field from a current object to the grid object """
    def addEffectiveBField(self,currentObject):
    
        """Loop through all the cells in the grid object"""
        for iCell in range(0,len(self.cellsInGrid)):
    
            """Initialise the sum of all the current elements for a given cell in the grid """
            vectorSumOfBFields = ROOT.TVector3(0.0,0.0,0.0)
            
            """Loop through all the current point sources for a given cell"""
            for iElement in range(0,len(currentObject)):
    
                """ Make a TVector3 for the current element in the line
                    z component is zero for the moment"""
                distanceVector = ROOT.TVector3( currentObject[iElement][0] - self.cellsInGrid[iCell][0],
                                                currentObject[iElement][1] - self.cellsInGrid[iCell][1],
                                                currentObject[iElement][2] - self.cellsInGrid[iCell][2])
                
                """ unit direction of the current element"""
                currentElementVector = ROOT.TVector3(   currentObject[iElement][3],
                                                        currentObject[iElement][4],
                                                        currentObject[iElement][5])
                
                """Make sure the current vector is a unit vector"""
                currentElementUnitDirection = currentElementVector.Unit()
                
                """Calculate the cross product for biot-savart function"""
                crossProductUnitVector = currentElementUnitDirection.Cross(distanceVector.Unit())
                
                radialDistanceInCm = distanceVector.Mag()*0.01
                """ Calculate the size of the field at Point P from a
                    specific current point source. Since point sources
                    are being used a truncation is given when the center
                    of the cell is close to the current source"""
                if(radialDistanceInCm < self.truncation):
                    multiplicationFactor = float(currentElementVector.Mag()*crossProductUnitVector.Mag()/(self.truncation*self.truncation))
                else:
                    multiplicationFactor = float(currentElementVector.Mag()*crossProductUnitVector.Mag()/(radialDistanceInCm*radialDistanceInCm))
    
                """Calculate the total effect of different all the current sources on a particular cell"""
                vectorSumOfBFields = vectorSumOfBFields + 0.0000001*crossProductUnitVector*multiplicationFactor

            
            self.cellsInGrid[iCell][3] = self.cellsInGrid[iCell][3] + vectorSumOfBFields.X()
            self.cellsInGrid[iCell][4] = self.cellsInGrid[iCell][4] + vectorSumOfBFields.Y()
            self.cellsInGrid[iCell][5] = self.cellsInGrid[iCell][5] + vectorSumOfBFields.Z()
    
"""This is a class to build a 2D grid object and has 2X2 dimensions"""
class bGrid2D(bGrid):
    
    def __init__(self,length,numberOfCells,truncation=0.000001):
        bGrid.__init__(self,length,numberOfCells,truncation)
        self.dimensions = 2
        self.numberInLength  = int(m.pow(self.numberOfCells,(1.0/float(self.dimensions))))
        self.cellWidth  = self.length/self.numberInLength
        iPoint = 0.0
        """Initialize the (x,y,z=0) center coordinates for the grid"""
        for xPoint in range(0,self.numberInLength):
            xValue = (xPoint+0.5)*self.cellWidth
            for yPoint in range(0,self.numberInLength):
                self.cellsInGrid[iPoint][0] = xValue
                self.cellsInGrid[iPoint][1] = (yPoint+0.5)*self.cellWidth
                self.cellsInGrid[iPoint][2] = 0.0
                iPoint = iPoint + 1.0
    
    def Plot2D(self,saveFileName):
        canvas = ROOT.TCanvas()
        histogram = ROOT.TH2F("histogram","",self.numberInLength,0.0,self.length,self.numberInLength,0.0,self.length);
        histogram.SetDirectory(0)
        """Loop through all the cells and plot these to a histogram """
        for i in range(0,len(self.cellsInGrid)):
            magOfVector = m.sqrt(   self.cellsInGrid[i,3]*self.cellsInGrid[i,3] +
                                    self.cellsInGrid[i,4]*self.cellsInGrid[i,4] +
                                    self.cellsInGrid[i,5]*self.cellsInGrid[i,5] )
            histogram.Fill(self.cellsInGrid[i,0],self.cellsInGrid[i,1],magOfVector)
            
        canvas.SetLogz()
        histogram.SetStats(0)
        histogram.Draw("CONT4z")
        canvas.SaveAs(saveFileName)
        canvas.Update()
        raw_input("\nPress Enter to continue...")

        

        
    
    
    
