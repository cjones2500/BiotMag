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
    
    """Save a grid object to file"""
    def saveGrid(self,fileToSave):
        np.savetxt(fileToSave,self.cellsInGrid)
    
    """Read a grid object from a file """
    def loadGrid(self,readFile):
        self.cellsInGrid = np.loadtxt(readFile)
        
    """Add anothergrid object to this Grid object """
    def addGrid(self,gridObject):
        """TODO:    check the grid objects are the same size
                    otherwise change them such that they are
                    the same size """
        self.cellsInGrid = self.cellsInGrid + gridObject.cellsInGrid
        
    
    """ add the field from a current object to the grid object """
    def addEffectiveBField(self,currentObject):
    
        """Loop through all the cells in the grid object"""
        for iCell in xrange(0,len(self.cellsInGrid)):
    
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
    
                """ Calculate the total effect of different all the current sources on a particular cell.
                    The 0.0000001 factor comes from the 10^-7 in Biot-Savart law from mu_0.
                    Units are given in cm so an extra factor of 0.01*0.01 is added.
                    FIXME: Not sure if there should be an extra factor of 0.01*0.01 here
                """
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
    
    """Plot the projection on X of the magnetic field about a point in Y and in an x range """
    def PlotXProjection(self,yLineValue,saveFileName,xLow,xHigh,yBandWidth=0.1):
        canvas = ROOT.TCanvas("canvas","Projection on X (set Y)",200,10,700,500);
        counter = 0
        
        """Find out how many values are within a Y band width"""
        for iCell in range(0,self.numberOfCells):
            if( (self.cellsInGrid[iCell][1] + yBandWidth > yLineValue) and (self.cellsInGrid[iCell][1] - yBandWidth < yLineValue)  ):
                counter = counter + 1
        
        bList = np.zeros(counter)
        xList = np.zeros(counter)
    
        counter = 0
        for iCell in range(0,self.numberOfCells):
            if( (self.cellsInGrid[iCell][1] + yBandWidth > yLineValue) and (self.cellsInGrid[iCell][1] - yBandWidth < yLineValue)  ):
                
                """Only look in the region where you are interested in the x dependence of the field """
                if( ( self.cellsInGrid[iCell][0] > xLow) and  (self.cellsInGrid[iCell][0] < xHigh) ):
                    xList[counter] = self.cellsInGrid[iCell][0]
                    bList[counter] = m.sqrt(    self.cellsInGrid[iCell][3]*self.cellsInGrid[iCell][3] +
                                                self.cellsInGrid[iCell][4]*self.cellsInGrid[iCell][4] +
                                                self.cellsInGrid[iCell][5]*self.cellsInGrid[iCell][5]   )
                    counter = counter + 1
        
        gr = ROOT.TGraph(len(xList),xList,bList)
        gr.SetTitle("Projection of X on the line Y = " + str(yLineValue))
        gr.GetXaxis().SetRangeUser(xLow,xHigh)
        gr.GetXaxis().SetTitle("X position [cm]")
        gr.GetYaxis().SetTitle("B field Strength [T]")
        gr.GetXaxis().CenterTitle()
        gr.GetYaxis().CenterTitle()
        gr.Draw("AP*")
        canvas.SaveAs(saveFileName)
        canvas.Update()
        raw_input("\nPress Enter to continue...")

        

        
    
    
    
