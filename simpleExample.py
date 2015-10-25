""" Example of creating a point using BiotMag software.
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

""" Example of a current point which contributes to the B field
    (x,y,z,
    Ix,Iy,Iz)"""
point = core.bCurrent.currentPoint(     5.0, 5.0, 0.0, 
                                        0.0, 1.0, 0.0)


""" Add the current point to the grid object. This is essentially
    the calculation of the field in all the cells of the grid
    due to that particular current object. Multiple current
    objects can be imposed on the same grid """
Grid.addEffectiveBField(point.currentElements)


""" Plots the graph interactively using ROOT and is saved locally """
Grid.Plot2D("simpleExample.root")