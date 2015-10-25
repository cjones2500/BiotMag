""" Example of creating a coil-like field using BiotMag software.
    Note that:
        - magnetic field is given in units of T
        - distance is given in units of cm """

import ROOT
import core.bGrid
import core.bCurrent
import core.bCurrentFunction as fct

""" Defined a grid with a certain size, only a square grid is defined
    with a length and a number of cells in that grid """
Grid = core.bGrid.bGrid2D(10.0,10000)

"""Center of a 10x10 Grid"""
centerPoint = ROOT.TVector3(5.0,5.0,0.0)
radius = 2.5
circle = core.bCurrent.currentCoil(centerPoint,radius,fct.constantCurrent,100)
Grid.addEffectiveBField(circle.currentElements)
Grid.Plot2D("circleExample.root")