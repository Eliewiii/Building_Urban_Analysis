"""
Functions used to load bipvs and to perfom  the simulation of the energy harvested
"""

import logging

from honeybee_radiance.sensorgrid import SensorGrid

from bua.bipv.bipv_panel import BipvPanel
from bua.bipv.bipv_technology import BipvTechnology

user_logger = logging.getLogger("user")
dev_logger = logging.getLogger("dev")


def init_bipv_on_sensor_grid(sensor_grid: SensorGrid, pv_technology_obj, bipv_transportation_obj,
                             annual_panel_irradiance_list,
                             minimum_panel_eroi):
    """
    Initialize the bipvs on the sensor_grid and return a list of the bipvs.
    The function will check if the area of the faces of the sensor_grid is big enough to contain the bipvs
    and if the eroi of the bipvs is above the threshold set by the user.
    If the area is not big enough, it will raise a warning and the bipvs will not be initialized in those face of the mesh.
    :param sensor_grid: Honeybee SensorGrid object
    :param pv_technology_obj: PVPanelTechnology object
    :param annual_panel_irradiance_list: list of floats: annual irradiance on each face of the sensor_grid
    :param minimum_panel_eroi: float: minimum energy return on investment of the PV, (Default=1.2)
    electricity for the grid (Default=1.)

    :return panel_obj_list
    """
    # initialize the list of the panel objects
    panel_obj_list = []
    # Extract the parameters from the Sensorgrid qbd the pv_technology_obj
    lb_mesh_obj = sensor_grid.mesh
    mesh_face_area_list = list(lb_mesh_obj.face_areas)  # face_areas is a tuple
    # Initialize the flags
    area_flag_warning = False
    eroi_flag_warning = False

    for face_index, face in enumerate(lb_mesh_obj.faces):
        # Calculate the energy harvested by the panel
        """ We need to differentiate the different cases of efficiency functions, this part is just 
        an approximation, overestimating th energy harvested by the panel, we cannot compute for panels that 
        require hourly timestep """
        if pv_technology_obj.efficiency_function == BipvTechnology.constant_efficiency or \
                pv_technology_obj.efficiency_function == BipvTechnology.degrading_rate_efficiency_loss:
            energy_harvested = sum(
                [pv_technology_obj.estimate_yearly_energy_harvested_by_panel_not_considering_inverter(
                    irradiance=annual_panel_irradiance_list[face_index], age=year) for year in
                    range(pv_technology_obj.weibull_law_failure_parameters["lifetime"])])
        else:
            """ If the efficiency function is not constant_efficiency of"""
            energy_harvested = sum(
                [pv_technology_obj.estimate_yearly_energy_harvested_by_panel_not_considering_inverter(
                    irradiance=annual_panel_irradiance_list[face_index], age=year,
                    efficiency_function=BipvTechnology.constant_efficiency) for
                    year in range(pv_technology_obj.weibull_law_failure_parameters["lifetime"])])

        gtg_transportation_dict, recycling_dict = pv_technology_obj.compute_transportation_lca_and_cost(
            bipv_transportation_obj=bipv_transportation_obj)
        primary_energy_transportation = gtg_transportation_dict["primary_energy"]
        primary_energy_recycling = recycling_dict["primary_energy"]
        primary_energy_inverter_estimated = pv_technology_obj.estimated_primary_energy_inverter

        primary_energy = \
            pv_technology_obj.primary_energy_manufacturing + primary_energy_transportation + primary_energy_recycling + \
            primary_energy_inverter_estimated
        panel_eroi = energy_harvested / primary_energy
        """
        Note that it is not exactly the reql eroi thqt is computed here, we assume that the panel will last for 
        the average lifetime of the weibull law.
        """
        # Check if the area is big enough and if the eroi is above the threshold
        if mesh_face_area_list[face_index] < pv_technology_obj.panel_area:
            area_flag_warning = True
        # Check if the eroi of teh panel is above the threshold
        elif panel_eroi <= minimum_panel_eroi:
            eroi_flag_warning = True
        else:
            new_panel = BipvPanel(face_index, pv_technology_obj)
            new_panel.initialize_or_replace_panel()
            panel_obj_list.append(new_panel)
    # raise flag if needed
    if area_flag_warning:
        user_logger.warning(
            "Some faces of the sensor grid are too small to contain a PV panel, no panel will be initialized in those faces")
        dev_logger.warning(
            "Some faces of the sensor grid are too small to contain a PV panel, no panel will be initialized in those faces")
    if eroi_flag_warning:
        user_logger.warning(
            "Some PV panels have an eroi below the threshold, no panel will be initialized in those faces")
        dev_logger.warning(
            "Some PV panels have an eroi below the threshold, no panel will be initialized in those faces")

    return panel_obj_list


def simulate_bipv_yearly_energy_harvesting(pv_panel_obj_list,
                                           hourly_solar_irradiance_table,
                                           inverter_capacity,
                                           start_year, current_study_duration_in_years,
                                           uc_start_year,
                                           uc_end_year, replacement_scenario,
                                           pv_tech_obj=None, **kwargs):
    """
    Loop over every year of the study duration to get the energy harvested, the energy used and the dmfa waste harvested
    every year
    :param pv_panel_obj_list: list of panel objects
    :param hourly_solar_irradiance_table: list of floats: table (list of list) with the hourly solar irradiance
    in Wh/m2, of all the faces of the sensor grid
    :param inverter_capacity: float: capacity of the inverter in kW
    :param start_year: int: year when the simulation starts
    :param current_study_duration_in_years: int: duration of the study in years
    :param uc_start_year: int: year when the uc starts
    :param uc_end_year: int: year when the uc ends
    :param pv_tech_obj: PVPanelTechnology object
    :param replacement_scenario: string: replacement scenario chosen between
    "replace_failed_panels_every_X_year" and "replace_all_panels_every_X_year", "no_replacement", "uc_replace_failed_panels_every_X_years", "uc_replace_all_panels_every_X_years"
    Default="replace_failed_panels_every_X_year"
    :param kwargs: dictionary of the parameters for the replacement scenario, keys are
        "replacement_frequency_in_years" : int: frequency of the replacement in years
        "panel_replacement_min_age": int: minimum age of the panel to be replaced
        "infrastructure_replacement_last_year": int: last year of the panel to be replaced, for instance, if
        the whole infrastructure is older the infrastructure_replacement_last_year, no replacement will be
        done anymore.
    :return energy_production_per_year_list: list of floats in kWh/year
    :return nb_of_panels_installed_list: list of int: list of the number of panels installed each year
    """
    # Check that all the inputs are given:
    if replacement_scenario == "replace_failed_panels_every_X_years" or replacement_scenario == "uc_replace_failed_panels_every_X_years":
        if "replacement_frequency_in_years" not in kwargs:
            user_logger.error(
                "The replacement frequency in years is not given, please provide the replacement frequency in years")
            raise ValueError("The replacement frequency in years is not given")

    # Initialize the lists
    energy_production_per_year_list = []
    nb_of_panels_installed_per_year_list = []
    # Loop over the years
    iteration_start_year = start_year + current_study_duration_in_years

    # todo: make sure that we don't simulate the current year twice
    if iteration_start_year < uc_end_year:
        for year in range(iteration_start_year, uc_end_year):
            # initialize
            annual_energy_harvested = 0.
            nb_of_new_panels = 0
            if "infrastructure_replacement_last_year" in kwargs \
                    and year - start_year > kwargs["infrastructure_replacement_last_year"]:
                None
            # Initialize panels for the first year they are installed
            elif (start_year - year) == 0:
                for panel_obj in pv_panel_obj_list:
                    panel_obj.initialize_or_replace_panel(pv_tech_obj=pv_tech_obj)
                    nb_of_new_panels += 1
            # Panel replacement according to replacement scenario
            elif replacement_scenario == "replace_failed_panels_every_X_years":
                replacement_frequency_in_years = kwargs["replacement_frequency_in_years"]
                if (year - start_year) % replacement_frequency_in_years == 0:
                    for panel_obj in pv_panel_obj_list:
                        if not panel_obj.is_panel_working():
                            panel_obj.initialize_or_replace_panel(pv_tech_obj=pv_tech_obj)
                            nb_of_new_panels += 1
            elif replacement_scenario == "replace_all_panels_every_X_years":
                replacement_frequency_in_years = kwargs["replacement_frequency_in_years"]
                if (year - start_year) % replacement_frequency_in_years == 0:
                    for panel_obj in pv_panel_obj_list:
                        if (not panel_obj.is_panel_working() or "panel_replacement_min_age" not in kwargs
                                or panel_obj.age >= kwargs["panel_replacement_min_age"]):
                            panel_obj.initialize_or_replace_panel(pv_tech_obj=pv_tech_obj)
                            nb_of_new_panels += 1

            elif replacement_scenario == "uc_replace_failed_panels_every_X_years":
                replacement_frequency_in_years = kwargs["replacement_frequency_in_years"]
                if (year - uc_start_year) % replacement_frequency_in_years == 0:
                    for panel_obj in pv_panel_obj_list:
                        if not panel_obj.is_panel_working():
                            panel_obj.initialize_or_replace_panel(pv_tech_obj=pv_tech_obj)
                            nb_of_new_panels += 1

            elif replacement_scenario == "uc_replace_all_panels_every_X_years":
                replacement_frequency_in_years = kwargs["replacement_frequency_in_years"]
                if (year - uc_start_year) % replacement_frequency_in_years == 0:
                    for panel_obj in pv_panel_obj_list:
                        if (not panel_obj.is_panel_working() or "panel_replacement_min_age" not in kwargs
                                or panel_obj.age >= kwargs["panel_replacement_min_age"]):
                            panel_obj.initialize_or_replace_panel(pv_tech_obj=pv_tech_obj)
                            nb_of_new_panels += 1

            elif replacement_scenario == "no_replacement":
                pass

            # Loop over all the sun hours
            nb_of_sun_hours = len(
                hourly_solar_irradiance_table[0])  # Number of sun hours in the year, same for all faces
            hourly_power_generation_by_panels_table = [panel_obj.get_hourly_power_generation_over_a_year(
                hourly_irradiance_list=hourly_solar_irradiance_table[panel_obj.index], **kwargs) for panel_obj
                in
                pv_panel_obj_list]
            for i in range(nb_of_sun_hours):
                total_power = sum(
                    [hourly_power_generation_by_panels_table[j][i] for j in range(len(pv_panel_obj_list))])
                if total_power > inverter_capacity:
                    total_power = inverter_capacity
                # Energy in kWh/h is power in kW * 1h
                annual_energy_harvested += total_power
            for panel_obj in pv_panel_obj_list:
                panel_obj.increment_age_by_one_year()

            energy_production_per_year_list.append(annual_energy_harvested / 1000)  # convert Wh to kWh
            nb_of_panels_installed_per_year_list.append(nb_of_new_panels)

    return energy_production_per_year_list, nb_of_panels_installed_per_year_list


def compute_lca_and_cost_for_gtg(nb_of_panels_installed_yearly_list, pv_tech_obj, roof_or_facades):
    """
    Take the results from function loop_over_the_years_for_solar_panels and use the pv_tech_obj info to transform it to data
    :param nb_of_panels_installed_yearly_list: list of int: list of the number of panels installed each year
    :param pv_tech_obj: PVPanelTechnology object
    :param roof_or_facades: string: "roof" or "facades"
    :return gtg_result_dict: dictionary of the gtg results
    """
    # Primary energy
    primary_energy_material_extraction_and_manufacturing_yearly_list = [
        i * pv_tech_obj.primary_energy_manufacturing for
        i in nb_of_panels_installed_yearly_list]

    # Carbon footprint
    carbon_material_extraction_and_manufacturing_yearly_list = [i * pv_tech_obj.ghg_manufacturing for i in
                                                                nb_of_panels_installed_yearly_list]

    # Economic cost
    cost_investement_yearly_list = [i * pv_tech_obj.cost_investment for i in
                                    nb_of_panels_installed_yearly_list]

    # Economic revenues
    if roof_or_facades == "roof":
        revenue_substituted_construction_material_yearly_list = [
            i * pv_tech_obj.revenue_substituted_construction_material_roof for i in
            nb_of_panels_installed_yearly_list]
    else:
        revenue_substituted_construction_material_yearly_list = [
            i * pv_tech_obj.revenue_substituted_construction_material_facades for i in
            nb_of_panels_installed_yearly_list]

    gtg_result_dict = {
        "primary_energy": primary_energy_material_extraction_and_manufacturing_yearly_list,
        "ghg": carbon_material_extraction_and_manufacturing_yearly_list,
        "cost": {
            "investment": cost_investement_yearly_list,
            "revenue": {
                "substituted_construction_material": revenue_substituted_construction_material_yearly_list}
        }
    }

    return gtg_result_dict


def compute_lca_cost_and_dmfa_for_recycling(nb_of_panels_installed_yearly_list, pv_tech_obj):
    """
    Take the results from function loop_over_the_years_for_solar_panels and use the pv_tech_obj info to transform it to data
    :param nb_of_panels_installed_yearly_list: list of int: list of the number of panels installed each year
    :param pv_tech_obj: PVPanelTechnology object
    :return recycling_dict: dictionary of the recycling results
    """
    # Primary energy
    primary_energy_recycling_yearly_list = [i * pv_tech_obj.primary_energy_recycling for i in
                                            nb_of_panels_installed_yearly_list]
    # Carbon footprint
    carbon_recycling_yearly_list = [i * pv_tech_obj.ghg_recycling for i in
                                    nb_of_panels_installed_yearly_list]
    # Compute DMFA waste in kg for each year
    dmfa_waste_yearly_list = [i * pv_tech_obj.weight for i in
                              nb_of_panels_installed_yearly_list]

    # Economic cost
    cost_recycling_yearly_list = [i * pv_tech_obj.cost_recycling for i in
                                  nb_of_panels_installed_yearly_list]
    # Economic revenues
    revenue_material_recovery_yearly_list = [i * pv_tech_obj.revenue_material_recovery for i in
                                             nb_of_panels_installed_yearly_list]

    recycling_dict = {
        "primary_energy": primary_energy_recycling_yearly_list,
        "ghg": carbon_recycling_yearly_list,
        "cost": {
            "investment": cost_recycling_yearly_list,
            "revenue": {"material_recovery": revenue_material_recovery_yearly_list}
        },
        "dmfa": dmfa_waste_yearly_list
    }

    return recycling_dict


def compute_lca_and_cost_for_maintenance(panel_list, start_year, current_study_duration_in_years,
                                         uc_end_year):
    """
    Compute the LCA and cost of the maintenance of the panels over the simulated years
    :param panel_list: list of BipvPanel objects
    :param start_year: int: year when the simulation starts
    :param current_study_duration_in_years: int: duration of the study in years
    :param uc_end_year: int: year when the uc ends
    :return maintenance_result_dict: dictionary of the maintenance results
    """
    primary_energy_maintenance_yearly_list = []
    ghg_maintenance_yearly_list = []
    cost_maintenance_yearly_list = []
    # Loop over the years
    iteration_start_year = start_year + current_study_duration_in_years
    if iteration_start_year < uc_end_year:
        for year in range(iteration_start_year, uc_end_year):
            primary_energy_maintenance_yearly_list.append(
                sum([panel_obj.panel_technology_object.primary_energy_annual_maintenance for panel_obj in
                     panel_list]))
            ghg_maintenance_yearly_list.append(
                sum([panel_obj.panel_technology_object.ghg_annual_maintenance for panel_obj in panel_list]))
            cost_maintenance_yearly_list.append(
                sum([panel_obj.panel_technology_object.cost_annual_maintenance for panel_obj in panel_list]))

    maintenance_result_dict = {
        "primary_energy": primary_energy_maintenance_yearly_list,
        "ghg": ghg_maintenance_yearly_list,
        "cost": cost_maintenance_yearly_list
    }

    return maintenance_result_dict


def compute_lca_and_cost_for_transportation(nb_of_panels_installed_yearly_list, pv_tech_obj,
                                            transportation_obj):
    """
    Take the results from function loop_over_the_years_for_solar_panels and use the pv_tech_obj info to transform it to data
    :param nb_of_panels_installed_yearly_list: list of int: list of the number of panels installed each year
    :param pv_tech_obj: PVPanelTechnology object
    :param transportation_obj: BipvTransportation object
    :return transport_result_dict: dictionary of the transportation results
    """
    # Transportation values
    gtg_transportation_dict, recycling_dict = pv_tech_obj.compute_transportation_lca_and_cost(
        bipv_transportation_obj=transportation_obj)
    # Primary energy
    primary_energy_transport_gtg_yearly_list = [i * gtg_transportation_dict["primary_energy"] for i in
                                                nb_of_panels_installed_yearly_list]
    primary_energy_transport_recycling_yearly_list = [i * recycling_dict["primary_energy"] for i in
                                                      nb_of_panels_installed_yearly_list]
    # Carbon footprint
    carbon_transport_gtg_yearly_list = [i * gtg_transportation_dict["ghg"] for i in
                                        nb_of_panels_installed_yearly_list]
    carbon_transport_recycling_yearly_list = [i * recycling_dict["ghg"] for i in
                                              nb_of_panels_installed_yearly_list]
    # Economic cost
    cost_transport_gtg_yearly_list = [i * gtg_transportation_dict["cost"] for i in
                                      nb_of_panels_installed_yearly_list]
    cost_transport_recycling_yearly_list = [i * recycling_dict["cost"] for i in
                                            nb_of_panels_installed_yearly_list]

    transport_result_dict = {
        "primary_energy": {
            "gtg": primary_energy_transport_gtg_yearly_list,
            "recycling": primary_energy_transport_recycling_yearly_list
        },
        "ghg": {
            "gtg": carbon_transport_gtg_yearly_list,
            "recycling": carbon_transport_recycling_yearly_list
        },
        "cost": {
            "gtg": cost_transport_gtg_yearly_list,
            "recycling": cost_transport_recycling_yearly_list
        }
    }

    return transport_result_dict


def compute_lca_and_cost_for_inverter(inverter_obj, inverter_sub_capacities, start_year,
                                      current_study_duration_in_years, uc_end_year):
    """
    Compute the LCA and cost of the inverter(s) over the simulated years
    :param inverter_obj: BipvInverter object
    :param inverter_sub_capacities: list of float: list of the individual sizes of the inverters used if necessary in kWp
    :param start_year: int: year when the simulation starts
    :param current_study_duration_in_years: int: duration of the study in years
    :param uc_end_year: int: year when the uc ends
    :return inverter_result_dict: dictionary of the inverter results
    """
    inverter_primary_energy_yearly_list = []
    inverter_ghg_yearly_list = []
    inverter_cost_yearly_list = []

    # Loop over the years
    iteration_start_year = start_year + current_study_duration_in_years
    if iteration_start_year < uc_end_year:
        for year in range(iteration_start_year, uc_end_year):
            if (year - start_year) % inverter_obj.replacement_frequency == 0:
                primary_energy_list, ghg_emission_list, cost_list = inverter_obj.get_primary_energy_ghg_and_cost_for_capacity_list(
                    inverter_sub_capacities)
                inverter_primary_energy_yearly_list.append(primary_energy_list)
                inverter_ghg_yearly_list.append(ghg_emission_list)
                inverter_cost_yearly_list.append(cost_list)
            else:
                inverter_primary_energy_yearly_list.append(0.)
                inverter_ghg_yearly_list.append(0.)
                inverter_cost_yearly_list.append(0.)

    inverter_result_dict = {
        "primary_energy": inverter_primary_energy_yearly_list,
        "ghg": inverter_ghg_yearly_list,
        "cost": inverter_cost_yearly_list
    }

    return inverter_result_dict
