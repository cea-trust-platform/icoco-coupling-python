# -*- coding: utf-8 -*-
"""
Two 1D Thermal-hydraulics channel with a "one cell" heated solid in between.
"""
import copy

class shared_const_data:
    def __init__(self, dz, dy):
        self.dz = dz
        self.dy = dy


class interface_const_data:
    def __init__(self, exchange_function):
        self.exchange_function = exchange_function


class fluid_variable_data:
    def __init__(self, num_cells):
        self.temperatures_current = [0.]*(num_cells + 1)
        self.temperatures_old = [0.]*(num_cells + 1)
        self.density = 1.
        self.speed = 1.
        self.precision = 1.E-6
        self.max_iter = 100
        self.residual = 0.
        self.presentTime = 0.


class fluid_data:
    def __init__(self, num_cells, shared, interface, dx, enthalpy_function):
        self._variable_data = fluid_variable_data(num_cells)
        self._shared = shared
        self._interface = interface
        self.dx = dx
        self.enthalpy_function = enthalpy_function

    def get_exchange_coef(self, solid_temperature):
        return self._interface.exchange_function(solid_temperature)

    def get_variable_data(self):
        return copy.deepcopy(self._variable_data)

    def set_variable_data(self, variable_data):
        self._variable_data = variable_data

    @property
    def dz(self):
        return self._shared.dz

    @property
    def dy(self):
        return self._shared.dy

    @property
    def temperatures_current(self):
        return self._variable_data.temperatures_current

    @property
    def temperatures_old(self):
        return self._variable_data.temperatures_old

    @property
    def density(self):
        return self._variable_data.density

    @density.setter
    def density(self, value):
         self._variable_data.density = value

    @property
    def speed(self):
        return self._variable_data.speed

    @speed.setter
    def speed(self, value):
         self._variable_data.speed = value

    @property
    def precision(self):
        return self._variable_data.precision

    @precision.setter
    def precision(self, value):
         self._variable_data.precision = value

    @property
    def max_iter(self):
        return self._variable_data.max_iter

    @max_iter.setter
    def max_iter(self, value):
         self._variable_data.max_iter = value

    @property
    def residual(self):
        return self._variable_data.residual

    @residual.setter
    def residual(self, value):
         self._variable_data.residual = value

    @property
    def presentTime(self):
        return self._variable_data.presentTime

    @presentTime.setter
    def presentTime(self, value):
         self._variable_data.presentTime = value


class solid_variable_data:
    def __init__(self, num_cells):
        self.temperatures_current = [0.]*(num_cells+1)
        self.temperatures_old = [0.]*(num_cells+1)
        self.vol_heat_capacity = 1.
        self.vol_powers = [0.]*(num_cells+1)
        self.precision = 1.E-6
        self.max_iter = 100
        self.residual = 0.
        self.presentTime = 0.


class solid_data:
    def __init__(self, num_cells, shared, interface_1, interface_2, dx):
        self._variable_data = solid_variable_data(num_cells)
        self._shared = shared
        self._interface_1 = interface_1
        self._interface_2 = interface_2
        self.dx = dx

    def get_exchange_coef_1(self, solid_temperature):
        return self._interface_1.exchange_function(solid_temperature)

    def get_exchange_coef_2(self, solid_temperature):
        return self._interface_2.exchange_function(solid_temperature)

    def get_variable_data(self):
        return copy.deepcopy(self._variable_data)

    def set_variable_data(self, variable_data):
        self._variable_data = variable_data

    @property
    def dz(self):
        return self._shared.dz

    @property
    def dy(self):
        return self._shared.dy

    @property
    def temperatures_current(self):
        return self._variable_data.temperatures_current

    @property
    def temperatures_old(self):
        return self._variable_data.temperatures_old

    @property
    def vol_heat_capacity(self):
        return self._variable_data.vol_heat_capacity

    @vol_heat_capacity.setter
    def vol_heat_capacity(self, value):
         self._variable_data.vol_heat_capacity = value

    @property
    def vol_powers(self):
        return self._variable_data.vol_powers

    @property
    def precision(self):
        return self._variable_data.precision

    @precision.setter
    def precision(self, value):
         self._variable_data.precision = value

    @property
    def max_iter(self):
        return self._variable_data.max_iter

    @max_iter.setter
    def max_iter(self, value):
         self._variable_data.max_iter = value

    @property
    def residual(self):
        return self._variable_data.residual

    @residual.setter
    def residual(self, value):
         self._variable_data.residual = value

    @property
    def presentTime(self):
        return self._variable_data.presentTime

    @presentTime.setter
    def presentTime(self, value):
         self._variable_data.presentTime = value


class coupling_variable_data:
    def __init__(self):
        self.precision = 1.E-6
        self.max_iter = 100
        self.residual = 0.

    def get_variable_data(self):
        return copy.deepcopy(self)

    def set_variable_data(self, variable_data):
        self.precision = variable_data.precision
        self.max_iter = variable_data.max_iter
        self.residual = variable_data.residual
