""" Example of creating a line using BiotMag software.
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

""" Define two points for a line """
pointA = ROOT.TVector3(5.0,3.0,0.0)
pointB = ROOT.TVector3(5.0,7.0,0.0)

""" Example of a line current"""
line = core.bCurrent.currentLine(   pointA,
                                    pointB,
                                    fct.constantCurrent,10)

""" Add a point the effective field projected onto the grid """
Grid.addEffectiveBField(line.currentElements)

""" Plots the graph interactively using ROOT and is saved locally """
Grid.Plot2D("lineExample.root")