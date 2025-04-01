# -*- coding: utf-8 -*-

import exemple_icoco.solver
import pyTHEDI as thedi
import pytest

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

def run_thedi():
    thedi.EAU_TPT_incompressible.Init("/volatile/catA/cpatricot/THEDI/ressources/Tables/Eau.10-210bar_PT",
                                      force_reecriture=True)

    canal1 = thedi.CANAL(thedi.Solveur_thermohydraulique.SOLVEUR_QUATRE_EQUATIONS_1D,
                        thedi.Equations_detat_fluide.EOS_EAU_TPT_incompressible)
    canal2 = thedi.CANAL(thedi.Solveur_thermohydraulique.SOLVEUR_QUATRE_EQUATIONS_1D,
                        thedi.Equations_detat_fluide.EOS_EAU_TPT_incompressible)

    blasius_perso = thedi.Correlations_specifications(0., 0.,
                            thedi.Correlation_frottement.BLASIUS_PERSONNALISE_1,
                            thedi.Correlation_frottement.BLASIUS_PERSONNALISE_1)

    canal1.Init([dz]*num_cells, [dy * fluid_1_dx]*num_cells, [0.01]*num_cells, [],
        input_temperature, pressure, ["canal1"]*num_cells, [blasius_perso]*num_cells)
    canal2.Init([dz]*num_cells, [dy * fluid_2_dx]*num_cells, [0.01]*num_cells, [],
        input_temperature, pressure, ["canal1"]*num_cells, [blasius_perso]*num_cells)

    canal1.Get_thermohydro_1D().Init_frottements_Blasius_personnalise_1([0]*num_cells, [0.], [1.])
    canal2.Get_thermohydro_1D().Init_frottements_Blasius_personnalise_1([0]*num_cells, [0.], [1.])

    canal1.Set_cos_theta(0.001)
    canal2.Set_cos_theta(0.001)

    canal1.Get_thermohydro_1D().Set_utilisation_puissance_decalee(False)
    canal2.Get_thermohydro_1D().Set_utilisation_puissance_decalee(False)

    solid = thedi.CONNEXION_THERMIQUE()
    solid.Init(canal1, canal2)

    nusselt1 = thedi.Correlations_specifications(
        0., 0., thedi.Correlation_Nusselt.ECHANGE_CONSTANT,
        thedi.Correlation_Nusselt.ECHANGE_CONSTANT)
    nusselt2 = thedi.Correlations_specifications(
        0., 0., thedi.Correlation_Nusselt.ECHANGE_CONSTANT,
        thedi.Correlation_Nusselt.ECHANGE_CONSTANT)

    canal1.Get_thermohydro_1D().Init_Nusselt_coef_echange_thermique_constant([0]*num_cells,
                                                                             [h_coef_1])
    canal2.Get_thermohydro_1D().Init_Nusselt_coef_echange_thermique_constant([0]*num_cells,
                                                                             [h_coef_2])

    materiau = thedi.UO2_REP()

    solid.Ajoute_thermique(thedi.Geometrie_thermique.PLAN, list(range(num_cells)), "solid", dy,
                    [solid_dx], [materiau], ["solid"], 1., nusselt1, nusselt2)

    power_lin = [total_power / (num_cells * dz)]*num_cells
    solid.Get_thermique_multi_1D().Set_puissance_lin(
                    power_lin, ["solid"], "solid")

    canal1.Set_P_haut(pressure)
    canal2.Set_P_haut(pressure)
    canal1.Set_Q_bas(speed_1 * density_1 * fluid_1_dx * dy)
    canal2.Set_Q_bas(speed_2 * density_2 * fluid_2_dx * dy)
    canal1.Set_T_bas(input_temperature)
    canal2.Set_T_bas(input_temperature)

    systeme = thedi.SYSTEME()
    systeme.Ajoute_composants([canal1, canal2])
    systeme.Ajoute_connexion_thermique(solid)

    systeme.Calcule_pas_de_temps(-1.)

    print("THEDI :")
    print(canal1.Get_thermohydro_1D().Get_T_liquide())
    print(canal2.Get_thermohydro_1D().Get_T_liquide())
    print(solid.Get_thermique_multi_1D().Get_T_effective(
        thedi.Definition_temperature_moyenne.MOYENNE_VOLUMIQUE, ["solid"], "solid"))

    return (canal1.Get_thermohydro_1D().Get_T_liquide(),
            canal2.Get_thermohydro_1D().Get_T_liquide(),
            solid.Get_thermique_multi_1D().Get_T_effective(
                thedi.Definition_temperature_moyenne.MOYENNE_VOLUMIQUE, ["solid"], "solid"))

def run_solver():
    thedi.EAU_TPT_incompressible.Init("/volatile/catA/cpatricot/THEDI/ressources/Tables/Eau.10-210bar_PT",
                                      force_reecriture=True)

    materiau = thedi.UO2_REP()

    def enthalpy(temperature):
        return thedi.EAU_TPT_incompressible.HL(temperature, pressure)

    def exchange_1(temperature):
        h_mat = materiau.Get_lambda(temperature, [])[0] * 2. / solid_dx
        return (h_mat * h_coef_1) / (h_mat + h_coef_1)

    def exchange_2(temperature):
        h_mat = materiau.Get_lambda(temperature, [])[0] * 2. / solid_dx
        return (h_mat * h_coef_2) / (h_mat + h_coef_2)

    my_solver = exemple_icoco.solver.solver(num_cells,
                                            dz,
                                            dy,
                                            fluid_1_dx,
                                            solid_dx,
                                            fluid_2_dx,
                                            enthalpy,
                                            exchange_1,
                                            exchange_2,
                                            input_temperature)

    my_solver.fluid_1.density = density_1
    my_solver.fluid_2.density = density_2
    my_solver.fluid_1.speed = speed_1
    my_solver.fluid_2.speed = speed_2
    my_solver.solid.vol_heat_capacity = materiau.Get_rhocp(input_temperature, [])[0]
    my_solver.set_powers([total_power / num_cells] * num_cells)

    my_solver.solve_stationary()
    my_solver.validate()

    print("SOLVER :")
    print(my_solver.fluid_1.temperatures_current)
    print(my_solver.fluid_2.temperatures_current)
    print(my_solver.solid.temperatures_current)

    return (my_solver.fluid_1.temperatures_current, my_solver.fluid_2.temperatures_current,
        my_solver.solid.temperatures_current)

thedi_temperature_fluid_1, thedi_temperature_fluid_2, thedi_temperature_solid = run_thedi()
temperature_fluid_1, temperature_fluid_2, temperature_solid = run_solver()

for resu_thedi, resu_solver in zip(thedi_temperature_fluid_1, temperature_fluid_1[1:]):
    assert pytest.approx(resu_solver, abs=1.E-1) == resu_thedi
for resu_thedi, resu_solver in zip(thedi_temperature_fluid_2, temperature_fluid_2[1:]):
    assert pytest.approx(resu_solver, abs=1.E-1) == resu_thedi
for resu_thedi, resu_solver in zip(thedi_temperature_solid, temperature_solid[1:]):
    assert pytest.approx(resu_solver, abs=1.E-1) == resu_thedi
