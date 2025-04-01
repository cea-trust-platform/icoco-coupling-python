# -*- coding: utf-8 -*-
"""
Two 1D Thermal-hydraulics channel with a "one cell" heated solid in between.
"""
import exemple_icoco.solver
import exemple_icoco.medbuilder
import exemple_icoco.algebraic_list
from exemple_icoco.mode import Mode

import icoco
import pyTHEDI as thedi
import medcoupling


class ValueType:
    Double = 0
    Int = 1
    String = 2


class ContextType:
    NONE = 0
    TIME_STEP_DEFINED = 1
    STATIONARY_DEFINED = 2


class Problem:
    def __init__(self):
        self.problemName = "exemple_icoco"
        self._clean_state()

    def _clean_state(self):
        self._dt = None
        self._solver = None
        self._med_mesh = None
        self._data_for_abort = {}
        self._data_for_save = {}
        self._stationaryMode = False
        self._mode = Mode(Mode.All)
        self._last_error_message = ""
        self._initialized = False
        self._solved = {Mode.Fluid_1 : False, Mode.Fluid_2 : False, Mode.Solid : False}
        self._context = ContextType.NONE


    @staticmethod
    def GetICoCoMajorVersion():
        return 3

    def getMEDCouplingMajorVersion(self):
        return medcoupling.MEDCouplingVersionMajMinRel()[0]

    def isMEDCoupling64Bits(self):
        return medcoupling.MEDCouplingSizeOfIDs() == 64

    def initialize(self):
        if self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="initialize",
                precondition="cannot be called multiple times. Use terminate() before calling" +
                " initialize() again.")
        try:
            self._clean_state()

            dz = 0.1
            dy = 1.
            num_cells = 20
            fluid_1_dx = 0.01
            fluid_2_dx = 0.03
            total_power = 1.E6
            input_temperature = 300. + 273.15
            pressure = 155.E5
            speed_1 = 1.
            speed_2 = 1./ 3.
            density_1 = 1000. #No choice.
            density_2 = 1000. #No choice.
            solid_dx = 0.01
            h_coef_1 = 1.E3
            h_coef_2 = 2.E3
            materiau = thedi.UO2_REP()

            def enthalpy(temperature):
                return thedi.EAU_TPT_incompressible.HL(temperature, pressure)

            def exchange_1(temperature):
                h_mat = materiau.Get_lambda(temperature, [])[0] * 2. / solid_dx
                return (h_mat * h_coef_1) / (h_mat + h_coef_1)

            def exchange_2(temperature):
                h_mat = materiau.Get_lambda(temperature, [])[0] * 2. / solid_dx
                return (h_mat * h_coef_2) / (h_mat + h_coef_2)

            self._solver = exemple_icoco.solver.solver(num_cells,
                                                        dz,
                                                        dy,
                                                        fluid_1_dx,
                                                        solid_dx,
                                                        fluid_2_dx,
                                                        enthalpy,
                                                        exchange_1,
                                                        exchange_2,
                                                        input_temperature)

            self._solver.fluid_1.density = density_1
            self._solver.fluid_2.density = density_2
            self._solver.fluid_1.speed = speed_1
            self._solver.fluid_2.speed = speed_2
            self._solver.solid.vol_heat_capacity = materiau.Get_rhocp(input_temperature, [])[0]

            self._med_mesh = exemple_icoco.medbuilder.build_1D_mesh(num_cells, dz)

            self._initialized = True

            return True
        except Exception as error:
            self._last_error_message = error.__str__()
            return False

    def terminate(self):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="terminate",
                precondition="cannot be called before initialize().")
        if self._context != ContextType.NONE:
            raise icoco.WrongContext(prob=self.problemName, method="terminate",
                precondition="cannot be called inside the CALCULATION_DEFINED context.")
        self._clean_state()
        self._initialized = False

    def getLastErrorMessage(self):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getLastErrorMessage",
                precondition="cannot be called before initialize().")
        return self._last_error_message

    def presentTime(self):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="presentTime",
                precondition="cannot be called before initialize().")
        if self._mode.is_activated(Mode.Fluid_1):
            return self._solver.fluid_1.presentTime
        if self._mode.is_activated(Mode.Fluid_2):
            return self._solver.fluid_2.presentTime
        return self._solver.solid.presentTime

    def computeTimeStep(self):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="computeTimeStep",
                precondition="cannot be called before initialize().")
        if self._context == ContextType.STATIONARY_DEFINED:
            raise icoco.WrongContext(prob=self.problemName, method="computeTimeStep",
                precondition="cannot be called inside the STATIONARY_DEFINED context.")
        dt = 1.E30
        if self._mode.is_activated(Mode.Fluid_1):
            dt = self._solver.fluid_1.dz / self._solver.fluid_1.speed
        if self._mode.is_activated(Mode.Fluid_2):
            dt = min(self._solver.fluid_2.dz / self._solver.fluid_2.speed, dt)
        if self._context == ContextType.TIME_STEP_DEFINED and dt >= self._dt:
            dt = self._dt / 2.
        return dt, False

    def _validateSolver(self):
        if self._mode.is_activated(Mode.Fluid_1):
            self._solver.validate_fluid_1()
        if self._mode.is_activated(Mode.Fluid_2):
            self._solver.validate_fluid_2()
        if self._mode.is_activated(Mode.Solid):
            self._solver.validate_solid()

    def initTimeStep(self, dt):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="initTimeStep",
                precondition="cannot be called before initialize().")
        if self._context != ContextType.NONE:
            raise icoco.WrongContext(prob=self.problemName, method="initTimeStep",
                precondition="cannot be called inside the CALCULATION_DEFINED context.")
        if dt <= 0.:
            raise icoco.WrongArgument(prob=self.problemName, method="initTimeStep", arg='dt',
                condition="dt must be > 0.")
        self._context = ContextType.TIME_STEP_DEFINED
        self._dt = dt
        self._data_for_abort["mode"] = Mode(self._mode.mode)
        if self._mode.is_activated(Mode.Fluid_1):
            self._data_for_abort[Mode.Fluid_1] = self._solver.fluid_1.get_variable_data()
        if self._mode.is_activated(Mode.Fluid_2):
            self._data_for_abort[Mode.Fluid_2] = self._solver.fluid_2.get_variable_data()
        if self._mode.is_activated(Mode.Solid):
            self._data_for_abort[Mode.Solid] = self._solver.solid.get_variable_data()
        self._validateSolver()
        dt_code, _ = self.computeTimeStep()
        return dt <= dt_code

    def solveTimeStep(self):
        if self._context != ContextType.TIME_STEP_DEFINED:
            raise icoco.WrongContext(prob=self.problemName, method="solveTimeStep",
                precondition="cannot be called outside the TIME_STEP_DEFINED context.")
        for mode in self._mode.get_elementary_modes():
            if self._solved[mode]:
                raise icoco.WrongContext(prob=self.problemName, method="solveTimeStep",
                    precondition=f"cannot be called twice for the same elementary mode ({mode}).")
        succeeded, converged = self.iterateTimeStep()
        if not converged:
            self._last_error_message = "Non convergence of solveTimeStep()"
        return succeeded and converged

    def iterateTimeStep(self):
        if self._context != ContextType.TIME_STEP_DEFINED:
            raise icoco.WrongContext(prob=self.problemName, method="iterateTimeStep",
                precondition="cannot be called outside the TIME_STEP_DEFINED context.")
        vol_heat_capacity = self._solver.solid.vol_heat_capacity
        if self._stationaryMode:
            self._solver.solid.vol_heat_capacity = vol_heat_capacity * 1.E-3
        try:
            if self._mode == Mode.All:
                self._solver.solve_time_step(self._dt)
            else:
                if self._mode.is_activated(Mode.Fluid_1):
                    self._solver.solve_fluid_1_time_step(self._dt)
                if self._mode.is_activated(Mode.Fluid_2):
                    self._solver.solve_fluid_2_time_step(self._dt)
                if self._mode.is_activated(Mode.Solid):
                    self._solver.solve_solid_time_step(self._dt)
            for mode in self._mode.get_elementary_modes():
                self._solved[mode] = True
            residual = self.getOutputDoubleValue("residual")
            required_precision = self.getOutputDoubleValue("precision")
            converged = residual <= required_precision
            return True, converged
        except Exception as error:
            self._last_error_message = error.__str__()
            return False, False
        finally:
            self._solver.solid.vol_heat_capacity = vol_heat_capacity

    def validateTimeStep(self):
        if self._context != ContextType.TIME_STEP_DEFINED:
            raise icoco.WrongContext(prob=self.problemName, method="validateTimeStep",
                precondition="cannot be called outside the TIME_STEP_DEFINED context.")
        if self._mode != self._data_for_abort["mode"]:
            raise icoco.WrongContext(prob=self.problemName, method="validateTimeStep",
                precondition=f"the method was called in mode {self._mode} whereas initTimeStep\
                was called in mode {self._data_for_abort["mode"]}.")
        for mode in self._mode.get_elementary_modes():
            if not self._solved[mode]:
                raise icoco.WrongContext(prob=self.problemName, method="validateTimeStep",
                    precondition=f"elementary mode ({mode}) was not solved.")
        self._data_for_abort["mode"] = 0
        self._context = ContextType.NONE
        for mode in self._mode.get_elementary_modes():
            self._solved[mode] = False
        if self._mode.is_activated(Mode.Fluid_1):
            self._solver.fluid_1.presentTime += self._dt
        if self._mode.is_activated(Mode.Fluid_2):
            self._solver.fluid_2.presentTime += self._dt
        if self._mode.is_activated(Mode.Solid):
            self._solver.solid.presentTime += self._dt

    def setStationaryMode(self, stationaryMode):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="setStationaryMode",
                precondition="cannot be called before initialize().")
        if self._context != ContextType.NONE:
            raise icoco.WrongContext(prob=self.problemName, method="setStationaryMode",
                precondition="cannot be called inside the CALCULATION_DEFINED context.")
        self._stationaryMode = stationaryMode

    def getStationaryMode(self):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getStationaryMode",
                precondition="cannot be called before initialize().")
        if self._context != ContextType.NONE:
            raise icoco.WrongContext(prob=self.problemName, method="getStationaryMode",
                precondition="cannot be called inside the CALCULATION_DEFINED context.")
        return self._stationaryMode

    def isStationary(self):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="isStationary",
                precondition="cannot be called before initialize().")
        if self._context != ContextType.NONE:
            raise icoco.WrongContext(prob=self.problemName, method="isStationary",
                precondition="cannot be called inside the CALCULATION_DEFINED context.")
        if self._mode == Mode.All:
            return self._solver.is_stationary(1.E-3 * self._dt)
        if self._mode == Mode.Fluid:
            return (self._solver.is_stationary_fluid_1(1.E-3 * self._dt) and
                    self._solver.is_stationary_fluid_2(1.E-3 * self._dt))
        if self._mode == Mode.Fluid_1:
            return self._solver.is_stationary_fluid_1(1.E-3 * self._dt)
        if self._mode == Mode.Fluid_2:
            return self._solver.is_stationary_fluid_2(1.E-3 * self._dt)
        return self._solver.is_stationary_solid(1.E-3 * self._dt)

    def abortTimeStep(self):
        if self._context != ContextType.TIME_STEP_DEFINED:
            raise icoco.WrongContext(prob=self.problemName, method="abortTimeStep",
                precondition="cannot be called outside the TIME_STEP_DEFINED context.")
        if self._mode != self._data_for_abort["mode"]:
            raise icoco.WrongContext(prob=self.problemName, method="abortTimeStep",
                precondition=f"the method was called in mode {self._mode} whereas initTimeStep\
                was called in mode {self._data_for_abort["mode"]}.")
        self._data_for_abort["mode"] = 0
        self._context = ContextType.NONE
        for mode in self._mode.get_elementary_modes():
            self._solved[mode] = False
        if self._mode.is_activated(Mode.Fluid_1):
            self._solver.fluid_1.set_variable_data(self._data_for_abort[Mode.Fluid_1])
        if self._mode.is_activated(Mode.Fluid_2):
            self._solver.fluid_2.set_variable_data(self._data_for_abort[Mode.Fluid_2])
        if self._mode.is_activated(Mode.Solid):
            self._solver.solid.set_variable_data(self._data_for_abort[Mode.Solid])

    def resetTime(self, time):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="resetTime",
                precondition="cannot be called before initialize().")
        if self._context != ContextType.NONE:
            raise icoco.WrongContext(prob=self.problemName, method="resetTime",
                precondition="cannot be called inside the CALCULATION_DEFINED context.")
        if self._mode.is_activated(Mode.Fluid_1):
            self._solver.fluid_1.presentTime = time
        if self._mode.is_activated(Mode.Fluid_2):
            self._solver.fluid_2.presentTime = time
        if self._mode.is_activated(Mode.Solid):
            self._solver.solid.presentTime = time

    def initStationary(self):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="initStationary",
                precondition="cannot be called before initialize().")
        if self._context != ContextType.NONE:
            raise icoco.WrongContext(prob=self.problemName, method="initStationary",
                precondition="cannot be called inside the CALCULATION_DEFINED context.")
        self._context = ContextType.STATIONARY_DEFINED
        self._data_for_abort["mode"] = Mode(self._mode.mode)
        if self._mode.is_activated(Mode.Fluid_1):
            self._data_for_abort[Mode.Fluid_1] = self._solver.fluid_1.get_variable_data()
        if self._mode.is_activated(Mode.Fluid_2):
            self._data_for_abort[Mode.Fluid_2] = self._solver.fluid_2.get_variable_data()
        if self._mode.is_activated(Mode.Solid):
            self._data_for_abort[Mode.Solid] = self._solver.solid.get_variable_data()

    def solveStationary(self):
        if self._context != ContextType.STATIONARY_DEFINED:
            raise icoco.WrongContext(prob=self.problemName, method="solveStationary",
                precondition="cannot be called outside the STATIONARY_DEFINED context.")
        for mode in self._mode.get_elementary_modes():
            if self._solved[mode]:
                raise icoco.WrongContext(prob=self.problemName, method="solveStationary",
                    precondition=f"cannot be called twice for the same elementary mode ({mode}).")
        succeeded, converged = self.iterateStationary()
        if not converged:
            self._last_error_message = "Non convergence of solveStationary()"
        return succeeded and converged

    def iterateStationary(self):
        if self._context != ContextType.STATIONARY_DEFINED:
            raise icoco.WrongContext(prob=self.problemName, method="iterateStationary",
                precondition="cannot be called outside the STATIONARY_DEFINED context.")
        try:
            if self._mode == Mode.All:
                self._solver.solve_stationary()
            else:
                if self._mode.is_activated(Mode.Fluid_1):
                    self._solver.solve_fluid_1_stationary()
                if self._mode.is_activated(Mode.Fluid_2):
                    self._solver.solve_fluid_2_stationary()
                if self._mode.is_activated(Mode.Solid):
                    self._solver.solve_solid_stationary()
            for mode in Mode(Mode.All).get_elementary_modes():
                self._solved[mode] = True
            residual = self.getOutputDoubleValue("residual")
            required_precision = self.getOutputDoubleValue("precision")
            converged = residual <= required_precision
            return True, converged
        except Exception as error:
            self._last_error_message = error.__str__()
            return False, False

    def validateStationary(self):
        if self._context != ContextType.STATIONARY_DEFINED:
            raise icoco.WrongContext(prob=self.problemName, method="validateStationary",
                precondition="cannot be called outside the STATIONARY_DEFINED context.")
        if self._mode != self._data_for_abort["mode"]:
            raise icoco.WrongContext(prob=self.problemName, method="validateStationary",
                precondition=f"the method was called in mode {self._mode} whereas initStationary\
                was called in mode {self._data_for_abort["mode"]}.")
        for mode in self._mode.get_elementary_modes():
            if not self._solved[mode]:
                raise icoco.WrongContext(prob=self.problemName, method="validateStationary",
                    precondition=f"elementary mode ({mode}) was not solved.")
        self._data_for_abort["mode"] = 0
        self._context = ContextType.NONE
        for mode in self._mode.get_elementary_modes():
            self._solved[mode] = False

    def abortStationary(self):
        if self._context != ContextType.STATIONARY_DEFINED:
            raise icoco.WrongContext(prob=self.problemName, method="abortStationary",
                precondition="cannot be called outside the STATIONARY_DEFINED context.")
        if self._mode != self._data_for_abort["mode"]:
            raise icoco.WrongContext(prob=self.problemName, method="abortStationary",
                precondition=f"the method was called in mode {self._mode} whereas initStationary\
                was called in mode {self._data_for_abort["mode"]}.")
        self._data_for_abort["mode"] = 0
        self._context = ContextType.NONE
        for mode in self._mode.get_elementary_modes():
            self._solved[mode] = False
        if self._mode.is_activated(Mode.Fluid_1):
            self._solver.fluid_1.set_variable_data(self._data_for_abort[Mode.Fluid_1])
        if self._mode.is_activated(Mode.Fluid_2):
            self._solver.fluid_2.set_variable_data(self._data_for_abort[Mode.Fluid_2])
        if self._mode.is_activated(Mode.Solid):
            self._solver.solid.set_variable_data(self._data_for_abort[Mode.Solid])

    def save(label, method, content):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="save",
                precondition="cannot be called before initialize().")
        if self._context != ContextType.NONE:
            raise icoco.WrongContext(prob=self.problemName, method="save",
                precondition="cannot be called inside the CALCULATION_DEFINED context.")
        if method != "memory":
            raise icoco.WrongArgument(prob=self.problemName, method="save", arg='method',
                condition="method must be 'memory'.")
        if content not in ["all", "temperatures"]:
            raise icoco.WrongArgument(prob=self.problemName, method="save", arg='content',
                condition="content must be either 'all' or 'temperatures'.")
        self._data_for_save[label] = {}
        if self._mode.is_activated(Mode.Fluid_1):
            self._data_for_save[label][Mode.Fluid_1] = self._solver.fluid_1.get_variable_data() if \
                content == "all" else copy.deepcopy(self._solver.fluid_1.temperatures_current)
        if self._mode.is_activated(Mode.Fluid_2):
            self._data_for_save[label][Mode.Fluid_2] = self._solver.fluid_2.get_variable_data() if \
                content == "all" else copy.deepcopy(self._solver.fluid_2.temperatures_current)
        if self._mode.is_activated(Mode.Solid):
            self._data_for_save[label][Mode.Solid] = self._solver.solid.get_variable_data() if \
                content == "all" else copy.deepcopy(self._solver.solid.temperatures_current)

    def restore(label, method, content):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="restore",
                precondition="cannot be called before initialize().")
        if self._context != ContextType.NONE:
            raise icoco.WrongContext(prob=self.problemName, method="restore",
                precondition="cannot be called inside the CALCULATION_DEFINED context.")
        if method != "memory":
            raise icoco.WrongArgument(prob=self.problemName, method="restore", arg='method',
                condition="method must be 'memory'.")
        if content not in ["all", "temperatures"]:
            raise icoco.WrongArgument(prob=self.problemName, method="restore", arg='content',
                condition="content must be either 'all' or 'temperatures'.")
        if label not in self._data_for_save:
            raise icoco.WrongArgument(prob=self.problemName, method="restore", arg='label',
             condition=f"label {label} is unknown. Available labels: {self._data_for_save.keys()}.")
        if self._mode.is_activated(Mode.Fluid_1):
            if content == "all":
                self._solver.fluid_1.set_variable_data(self._data_for_save[label][Mode.Fluid_1])
            else:
                self._solver.fluid_1.temperatures_current[:] = \
                    self._data_for_save[label][Mode.Fluid_1][:]
        if self._mode.is_activated(Mode.Fluid_2):
            if content == "all":
                self._solver.fluid_2.set_variable_data(self._data_for_save[label][Mode.Fluid_2])
            else:
                self._solver.fluid_2.temperatures_current[:] = \
                    self._data_for_save[label][Mode.Fluid_2][:]
        if self._mode.is_activated(Mode.Solid):
            if content == "all":
                self._solver.solid.set_variable_data(self._data_for_save[label][Mode.Solid])
            else:
                self._solver.solid.temperatures_current[:] = \
                    self._data_for_save[label][Mode.Solid][:]

    def forget(label, method):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="forget",
                precondition="cannot be called before initialize().")
        if method != "memory":
            raise icoco.WrongArgument(prob=self.problemName, method="forget", arg='method',
                condition="method must be 'memory'.")
        if content not in ["all", "temperatures"]:
            raise icoco.WrongArgument(prob=self.problemName, method="forget", arg='content',
                condition="content must be either 'all' or 'temperatures'.")
        if label in self._data_for_save:
            del self._data_for_save[label]

    def getInputFieldsNames(self):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getInputFieldsNames",
                precondition="cannot be called before initialize().")
        return ["power"]

    def getOutputFieldsNames(self):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getOutputFieldsNames",
                precondition="cannot be called before initialize().")
        return ["temperature_fluid_1", "temperature_fluid_2", "temperature_solid"]

    def getFieldType(self, name):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getFieldType",
                precondition="cannot be called before initialize().")
        return Value.Double

    def getMeshUnit(self):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getMeshUnit",
                precondition="cannot be called before initialize().")
        return 'm'

    def getFieldUnit(self, name):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getFieldUnit",
                precondition="cannot be called before initialize().")
        if name == "power":
            return 'W'
        else:
            return 'K'

    def getFieldTimeSemantics(self, name):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getFieldTimeSemantics",
                precondition="cannot be called before initialize().")
        if name == "power":
            return "constant"
        else:
            return "end_of_time_step"

    def getNameOfFieldUnderlyingMesh(self, name):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getNameOfFieldUnderlyingMesh",
                precondition="cannot be called before initialize().")
        return "1DMesh"

    def getInputMEDDoubleFieldTemplate(self, name):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getInputMEDDoubleFieldTemplate",
                precondition="cannot be called before initialize().")
        return exemple_icoco.medbuilder.build_1D_field(self._med_mesh,
                                                       [0.]*self._solver.num_cells,
                                                       medcoupling.ExtensiveMaximum)

    def setInputMEDDoubleField(self, name, field):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="setInputMEDDoubleField",
                precondition="cannot be called before initialize().")
        if name == "power":
            array = field.getArray()
            self._solver.solid.set_powers([array.getIJ(i, 0) for i in range(len(array))])
        else:
            raise icoco.WrongArgument(prob=self.problemName, method="setInputMEDDoubleField",
                arg='name',
                condition=f"unknown field name {name}. Only 'power' is available.")

    def getOutputMEDDoubleField(self, name):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getOutputMEDDoubleField",
                precondition="cannot be called before initialize().")
        if name == "temperature_fluid_1":
            values = self._solver.fluid_1.temperatures_current[1:]
        elif name == "temperature_fluid_2":
            values = self._solver.fluid_2.temperatures_current[1:]
        elif name == "temperature_solid":
            values = self._solver.solid.temperatures_current[1:]
        else:
            raise icoco.WrongArgument(prob=self.problemName, method="getOutputMEDDoubleField",
                arg='name',
                condition=f"unknown field name {name}. Only {self.getOutputFieldsNames()}" +
                    "are available.")
        return exemple_icoco.medbuilder.build_1D_field(self._med_mesh,
                                                       values,
                                                       medcoupling.IntensiveMaximum)

    def getAlgebraicDataNames(self):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getAlgebraicDataNames",
                precondition="cannot be called before initialize().")
        return ["temperature_fluid_1", "temperature_fluid_2", "temperature_solid"]

    def getAlgebraicDataTimeSemantics(self):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getAlgebraicDataTimeSemantics",
                precondition="cannot be called before initialize().")
        return "end_of_time_step"

    def setAlgebraicData(self, name, data):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="setAlgebraicData",
                precondition="cannot be called before initialize().")
        if name == "temperature_fluid_1":
            self._solver.fluid_1.temperatures_current[1:] = data.get_data()[:]
        elif name == "temperature_fluid_2":
            self._solver.fluid_2.temperatures_current[1:] = data.get_data()[:]
        elif name == "temperature_solid":
            self._solver.solid.temperatures_current[1:] = data.get_data()[:]

    def getAlgebraicData(self, name):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getAlgebraicData",
                precondition="cannot be called before initialize().")
        if name == "temperature_fluid_1":
            return exemple_icoco.algebraic_list.Algebraic_list(
                self._solver.fluid_1.temperatures_current[1:])
        elif name == "temperature_fluid_2":
            return exemple_icoco.algebraic_list.Algebraic_list(
                self._solver.fluid_2.temperatures_current[1:])
        elif name == "temperature_solid":
            return exemple_icoco.algebraic_list.Algebraic_list(
                self._solver.solid.temperatures_current[1:])

    def getInputValuesNames(self):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getInputValuesNames",
                precondition="cannot be called before initialize().")
        return ["mode", "precision", "max_iter"]

    def getOutputValuesNames(self):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getOutputValuesNames",
                precondition="cannot be called before initialize().")
        return ["mode", "precision", "max_iter", "residual"]

    def getValueType(self, name):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getValueType",
                precondition="cannot be called before initialize().")
        if name == "mode":
            return ValueType.Int
        if name in ["residual", "precision"]:
            return ValueType.Double
        raise icoco.WrongArgument(prob=self.problemName, method="getValueType",
                arg='name',
                condition=f"unknown value name {name}.")

    def getValueUnit(self):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getValueUnit",
                precondition="cannot be called before initialize().")
        return "NA"

    def getValueTimeSemantics(self):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getValueTimeSemantics",
                precondition="cannot be called before initialize().")
        return "NA"

    def setInputIntValue(self, name, value):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="setInputIntValue",
                precondition="cannot be called before initialize().")
        if name == "mode":
            if not value in Mode.get_modes():
                raise icoco.WrongArgument(prob=self.problemName, method="setInputIntValue",
                    arg='value',
                    condition=f"unknown provided mode {value}.")
            input_mode = Mode(value)
            elem_modes = input_mode.get_elementary_modes()
            if self._data_for_abort["mode"] != 0: #We are inside CALCULATION_DEFINED context
                previous_mode = self._data_for_abort["mode"]
                included_mode = True
                for e_mode in elem_modes:
                    included_mode = included_mode and previous_mode.is_activated(e_mode)
                if not included_mode:
                    raise icoco.WrongArgument(prob=self.problemName, method="setInputIntValue",
                        arg='value',
                        condition=f"the provided mode {input_mode} is not included in the " +
                        f"mode activated when the current CALCULATION_DEFINED context was opened" +
                        f" ({previous_mode}).")
            times = []
            if Mode.Fluid_1 in elem_modes:
                times.append(self._solver.fluid_1.presentTime)
            if Mode.Fluid_2 in elem_modes:
                times.append(self._solver.fluid_2.presentTime)
            if Mode.Solid in elem_modes:
                times.append(self._solver.solid.presentTime)
            for t in times[1:]:
                if abs(t - times[0]) > 1.E-10:
                    raise icoco.WrongArgument(prob=self.problemName, method="setInputIntValue",
                        arg='value',
                        condition=f"all elementary modes of the compound provided mode " +
                        f"{input_mode} are not synchronized (there presentTime are different).")
            self._mode = input_mode
        else:
            raise icoco.WrongArgument(prob=self.problemName, method="setInputIntValue",
                arg='name',
                condition=f"unknown value name {name}.")

    def getOutputIntValue(self, name):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getOutputIntValue",
                precondition="cannot be called before initialize().")
        if name == "mode":
            return self._mode.mode
        raise icoco.WrongArgument(prob=self.problemName, method="getOutputIntValue",
            arg='name',
            condition=f"unknown value name {name}.")

    def setInputDoubleValue(self, name, value):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="setInputDoubleValue",
                precondition="cannot be called before initialize().")
        if name == "precision":
            if self._mode. == Mode.All:
                self._solver.coupling.precision = value
            else:
                if self._mode.is_activated(Mode.Fluid_1):
                    self._solver.fluid_1.precision = value
                if self._mode.is_activated(Mode.Fluid_2):
                    self._solver.fluid_2.precision = value
                if self._mode.is_activated(Mode.Solid):
                    self._solver.solid.precision = value
        elif name == "max_iter":
            if self._mode. == Mode.All:
                self._solver.coupling.max_iter = value
            else:
                if self._mode.is_activated(Mode.Fluid_1):
                    self._solver.fluid_1.max_iter = value
                if self._mode.is_activated(Mode.Fluid_2):
                    self._solver.fluid_2.max_iter = value
                if self._mode.is_activated(Mode.Solid):
                    self._solver.solid.max_iter = value
        else:
            raise icoco.WrongArgument(prob=self.problemName, method="setInputDoubleValue",
                arg='name',
                condition=f"unknown value name {name}.")

    def getOutputDoubleValue(self, name):
        if not self._initialized:
            raise icoco.WrongContext(prob=self.problemName, method="getOutputDoubleValue",
                precondition="cannot be called before initialize().")
        if name == "precision":
            if self._mode. == Mode.All
                return self._solver.coupling.precision
            if self._mode.is_activated(Mode.Fluid_1):
                return self._solver.fluid_1.precision
            if self._mode.is_activated(Mode.Fluid_2):
                return self._solver.fluid_2.precision
            if self._mode.is_activated(Mode.Solid):
                return self._solver.solid.precision
        elif name == "max_iter":
            if self._mode. == Mode.All
                return self._solver.coupling.max_iter
            if self._mode.is_activated(Mode.Fluid_1):
                return self._solver.fluid_1.max_iter
            if self._mode.is_activated(Mode.Fluid_2):
                return self._solver.fluid_2.max_iter
            if self._mode.is_activated(Mode.Solid):
                return self._solver.solid.max_iter
        elif name == "residual":
            if self._mode. == Mode.All
                return self._solver.coupling.residual
            if self._mode.is_activated(Mode.Fluid_1):
                return self._solver.fluid_1.residual
            if self._mode.is_activated(Mode.Fluid_2):
                return self._solver.fluid_2.residual
            if self._mode.is_activated(Mode.Solid):
                return self._solver.solid.residual
        else:
            raise icoco.WrongArgument(prob=self.problemName, method="getOutputDoubleValue",
                arg='name',
                condition=f"unknown value name {name}.")
