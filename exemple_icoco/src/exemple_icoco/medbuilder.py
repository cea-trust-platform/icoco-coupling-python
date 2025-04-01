# -*- coding: utf-8 -*-
"""
Two 1D Thermal-hydraulics channel with a "one cell" heated solid in between.
"""
import medcoupling as mc

def build_1D_mesh(num_cells, dz):
    coordzbas = 0.
    coord = coordzbas
    coords = []
    for i in range(num_cells + 1):
        coords.append(coord)
        coord += dz
    array = mc.DataArrayDouble(coords)
    array.setInfoOnComponent(0, "X [m]")
    mesh = mc.MEDCouplingCMesh("1DMesh")
    mesh.setCoords(array)
    return mesh

def build_1D_field(mesh, values, nature):
    field = mc.MEDCouplingFieldDouble.New(mc.ON_CELLS)
    field.setMesh(mesh)
    array = mc.DataArrayDouble(values)
    field.setArray(array)
    field.setName("1DField")
    field.setNature(nature)
    return field

