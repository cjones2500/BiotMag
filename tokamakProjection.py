""" Example of creating a coil-like field using BiotMag software.
    Note that:
        - magnetic field is given in units of T
        - current is assumed in units of A
        - distance is given in units of cm """

import ROOT
import core.bGrid
import core.bCurrent
import core.bCurrentFunction as fct

""" Defined a grid with a certain size, only a square grid is defined
    with a length and a number of cells in that grid """
Grid = core.bGrid.bGrid2D(10.0,1000)

"""Center of a circle"""
centerPoint = ROOT.TVector3(5.0,5.0,0.0)
radiusMin = 2.0
thicknessOfWire = 0.01
iMax = 10
for i in range(0,iMax):
    """Set a width of the current wire"""
    radius = radiusMin + thicknessOfWire*(1.0*i)/(iMax*1.0)
    """Use a circular current coil with an effective radius"""
    tokamakBField = core.bCurrent.currentCoil(centerPoint,radius,fct.effectiveTokamakCurrent,100,sizeOfCurrent=1.0)
    """Add the tokamakBField to the Grid"""
    Grid.addEffectiveBField(tokamakBField.currentElements)

Grid.Plot2D("tokamakProjection.root")
"""Plot the inner 90% field at 0.9 of the radius, ignoring edge effects """
xLow = centerPoint.X() - 0.9*radiusMin 
xHigh = centerPoint.X() + 0.9*radiusMin
Grid.PlotXProjection(centerPoint.X(),"xTokmakaProjection.root",xLow,xHigh)
gridToSave = "tokamakGrid.out"
Grid.saveGrid(gridToSave)