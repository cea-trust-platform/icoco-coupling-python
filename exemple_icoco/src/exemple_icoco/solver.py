# -*- coding: utf-8 -*-
"""
Two 1D Thermal-hydraulics channel with a "one cell" heated solid in between.
"""
import exemple_icoco.data as data


class solver:
    def __init__(self, num_cells,
                       dz,
                       dy,
                       fluid_1_dx,
                       solid_dx,
                       fluid_2_dx,
                       enthalpy_function,
                       exchange_function_1,
                       exchange_function_2,
                       init_temperature):
        shared_data = data.shared_const_data(dz, dy)
        interface_1 = data.interface_const_data(exchange_function_1)
        interface_2 = data.interface_const_data(exchange_function_2)
        self.fluid_1 = data.fluid_data(num_cells, shared_data, interface_1, fluid_1_dx,
            enthalpy_function)
        self.fluid_2 = data.fluid_data(num_cells, shared_data, interface_2, fluid_2_dx,
            enthalpy_function)
        self.solid = data.solid_data(num_cells, shared_data, interface_1, interface_2,
            solid_dx)
        self.coupling = data.coupling_variable_data()
        self.set_fluid_1_inlet_temperature(init_temperature)
        self.set_fluid_2_inlet_temperature(init_temperature)
        self.initialize_temperature()

    @property
    def num_cells(self):
        return len(self.solid.temperatures_current) - 1

    def set_fluid_1_inlet_temperature(self, value):
        self.fluid_1.temperatures_old[0] = self.fluid_1.temperatures_current[0] = value

    def set_fluid_2_inlet_temperature(self, value):
        self.fluid_2.temperatures_old[0] = self.fluid_2.temperatures_current[0] = value

    def set_powers(self, values):
        if len(values) != self.num_cells:
            raise ValueError(f"We need {self.num_cells} power values and not \
                {len(values)}.")
        self.solid.vol_powers[1:] = [v / (self.solid.dz *
            self.solid.dy * self.solid.dx) for v in values]

    def initialize_temperature(self):
        for i in range(1, self.num_cells + 1):
            self.fluid_1.temperatures_current[i] = self.fluid_1.temperatures_current[0]
        for i in range(1, self.num_cells + 1):
            self.fluid_2.temperatures_current[i] = self.fluid_2.temperatures_current[0]
        for i in range(1, self.num_cells + 1):
            self.solid.temperatures_current[i] = 0.5 * (
                self.fluid_1.temperatures_current[i] + self.fluid_2.temperatures_current[i])

    @staticmethod
    def temperature_from_enthalpy(enthalpy_function, target_enthalpy, init_temperature):
        dtemp = 1.E-2
        precision = 1.E-6
        max_iter = 100
        residual = precision + 1
        temperature = init_temperature
        it = 0
        while residual >= precision and it < max_iter:
            dh = enthalpy_function(temperature + dtemp)
            enthalpy = enthalpy_function(temperature)
            dh -= enthalpy
            residual = abs(enthalpy - target_enthalpy)
            if residual >= precision:
                temperature += (target_enthalpy - enthalpy) * dtemp / dh
            it += 1
        if residual >= precision:
            raise Exception("Non convergence of enthalpy inversion")
        return temperature

    @staticmethod
    def _is_stationary(something, precision):
        residual = 0
        for new_temp, old_temp in zip(something.temperatures_current, something.temperatures_old):
            if abs(new_temp - old_temp) > residual:
                residual = abs(new_temp - old_temp)
        return residual <= precision

    def _solve_fluid_time_step(self, dt, fluid):
        exchange_values = [fluid.get_exchange_coef(t) / fluid.dx
            for t in self.solid.temperatures_current]
        enthalpies_old = [fluid.enthalpy_function(t) for t in fluid.temperatures_old]
        enthalpies = [h for h in enthalpies_old]

        precision = fluid.precision
        max_iter = fluid.max_iter
        residual = precision + 1
        it = 0
        while residual >= precision and it < max_iter:
            residual = 0
            for i in range(1, len(enthalpies)):
                enthalpies[i] = enthalpies_old[i] + dt / fluid.density * (
                    - fluid.speed * fluid.density * (enthalpies_old[i] - enthalpies_old[i-1])
                    / fluid.dz + exchange_values[i] * (self.solid.temperatures_current[i] -
                    fluid.temperatures_current[i]))
                new_T = self.temperature_from_enthalpy(fluid.enthalpy_function, enthalpies[i],
                    fluid.temperatures_current[i])
                if abs(new_T - fluid.temperatures_current[i]) > residual:
                    residual = abs(new_T - fluid.temperatures_current[i])
                fluid.temperatures_current[i] = new_T
            it += 1
        fluid.residual = residual

    def solve_fluid_1_time_step(self, dt):
        self._solve_fluid_time_step(dt, self.fluid_1)

    def solve_fluid_2_time_step(self, dt):
        self._solve_fluid_time_step(dt, self.fluid_2)

    def _solve_fluid_stationary(self, fluid):
        exchange_values = [fluid.get_exchange_coef(t) / fluid.dx
            for t in self.solid.temperatures_current]
        enthalpies = [fluid.enthalpy_function(t) for t in fluid.temperatures_current]

        precision = fluid.precision
        max_iter = fluid.max_iter
        residual = precision + 1
        it = 0
        while residual >= precision and it < max_iter:
            residual = 0
            for i in range(1, len(enthalpies)):
                enthalpies[i] = enthalpies[i-1] + fluid.dz / (fluid.speed * fluid.density) * (
                    exchange_values[i] * (self.solid.temperatures_current[i] -
                    fluid.temperatures_current[i]))
                new_T = self.temperature_from_enthalpy(fluid.enthalpy_function, enthalpies[i],
                    fluid.temperatures_current[i])
                if abs(new_T - fluid.temperatures_current[i]) > residual:
                    residual = abs(new_T - fluid.temperatures_current[i])
                fluid.temperatures_current[i] = new_T
            it += 1
        fluid.residual = residual

    def solve_fluid_1_stationary(self):
        self._solve_fluid_stationary(self.fluid_1)

    def solve_fluid_2_stationary(self):
        self._solve_fluid_stationary(self.fluid_2)

    def validate_fluid_1(self):
        self.fluid_1.temperatures_old[:] = self.fluid_1.temperatures_current[:]

    def validate_fluid_2(self):
        self.fluid_2.temperatures_old[:] = self.fluid_2.temperatures_current[:]

    def is_stationary_fluid_1(self, precision):
        return self._is_stationary(self.fluid_1, precision)

    def is_stationary_fluid_2(self, precision):
        return self._is_stationary(self.fluid_2, precision)

    def solve_solid_time_step(self, dt):
        precision = self.solid.precision
        max_iter = self.solid.max_iter
        residual = precision + 1
        it = 0
        while residual >= precision and it < max_iter:
            residual = 0
            for i in range(1, self.num_cells + 1):
                h1 = self.solid.get_exchange_coef_1(self.solid.temperatures_current[i])
                h1 /= self.solid.dx
                h2 = self.solid.get_exchange_coef_2(self.solid.temperatures_current[i])
                h2 /= self.solid.dx
                denom = 1 + dt / self.solid.vol_heat_capacity * (h1 + h2)
                new_T = (self.solid.temperatures_old[i] + dt / self.solid.vol_heat_capacity *
                    (h1 * self.fluid_1.temperatures_current[i] +
                     h2 * self.fluid_2.temperatures_current[i] +
                     self.solid.vol_powers[i])) / denom
                if abs(new_T - self.solid.temperatures_current[i]) > residual:
                    residual = abs(new_T - self.solid.temperatures_current[i])
                self.solid.temperatures_current[i] = new_T
            it += 1
        self.solid.residual = residual

    def solve_solid_stationary(self):
        precision = self.solid.precision
        max_iter = self.solid.max_iter
        residual = precision + 1
        it = 0
        while residual >= precision and it < max_iter:
            residual = 0
            for i in range(1, self.num_cells + 1):
                h1 = self.solid.get_exchange_coef_1(self.solid.temperatures_current[i])
                h1 /= self.solid.dx
                h2 = self.solid.get_exchange_coef_2(self.solid.temperatures_current[i])
                h2 /= self.solid.dx
                new_T = (h1 * self.fluid_1.temperatures_current[i] +
                    h2 * self.fluid_2.temperatures_current[i] + self.solid.vol_powers[i]) / (
                        h1 + h2)
                if abs(new_T - self.solid.temperatures_current[i]) > residual:
                    residual = abs(new_T - self.solid.temperatures_current[i])
                self.solid.temperatures_current[i] = new_T
            it += 1
        self.solid.residual = residual

    def validate_solid(self):
        self.solid.temperatures_old[:] = self.solid.temperatures_current[:]

    def is_stationary_solid(self, precision):
        return self._is_stationary(self.solid, precision)

    def solve_time_step(self, dt):
        precision = self.coupling.precision
        max_iter = self.coupling.max_iter
        residual = precision + 1
        it = 0
        previous_temperature_solid = [0.] * (self.num_cells + 1)
        while residual >= precision and it < max_iter:
            residual = 0
            previous_temperature_solid[:] = self.solid.temperatures_current[:]
            self.solve_fluid_1_time_step(dt)
            self.solve_fluid_2_time_step(dt)
            self.solve_solid_time_step(dt)
            for previous_temp, current_temp in zip(previous_temperature_solid,
                                                   self.solid.temperatures_current):
                if abs(previous_temp - current_temp) > residual:
                    residual = abs(previous_temp - current_temp)
            it += 1
        self.coupling.residual = residual

    def solve_stationary(self):
        precision = self.coupling.precision
        max_iter = self.coupling.max_iter
        residual = precision + 1
        it = 0
        previous_temperature_solid = [0.] * (self.num_cells + 1)
        while residual >= precision and it < max_iter:
            residual = 0
            previous_temperature_solid[:] = self.solid.temperatures_current[:]
            self.solve_fluid_1_stationary()
            self.solve_fluid_2_stationary()
            self.solve_solid_stationary()
            for previous_temp, current_temp in zip(previous_temperature_solid,
                                                   self.solid.temperatures_current):
                if abs(previous_temp - current_temp) > residual:
                    residual = abs(previous_temp - current_temp)
            it += 1
        self.coupling.residual = residual

    def is_stationary(self, precision):
        return (self._is_stationary(self.fluid_1, precision) and
                self._is_stationary(self.fluid_2, precision) and
                self._is_stationary(self.solid, precision))

    def validate(self):
        self.validate_fluid_1()
        self.validate_fluid_2()
        self.validate_solid()
