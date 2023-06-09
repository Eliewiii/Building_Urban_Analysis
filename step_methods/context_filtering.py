"""
Functions for the context filtering step.
For both shading and LWR.
"""

from mains_tool.utils_general import *
from step_methods.utils_step_methods import *

from mains_tool.utils_default_values_user_parameters import *


class SimulationContextFiltering:
    """ todo   """

    @classmethod
    def perform_context_filtering_on_building(cls,
                                              urban_canopy_object,
                                              min_VF_criterion=default_mvfc_context_shading_selection,
                                              number_of_rays=default_number_of_rays,
                                              building_id_list=None, on_building_to_simulate=True,
                                              automatic_floor_subdivision_for_new_BuildingModeled=default_automatic_floor_subdivision_for_new_BuildingModeled,
                                              use_layout_from_typology_for_new_BuildingModeled=default_use_layout_from_typology_for_new_BuildingModeled,
                                              use_properties_from_typology_for_new_BuildingModeled=default_use_properties_from_typology_for_new_BuildingModeled,
                                              make_new_BuildingModeled_simulated=default_make_new_BuildingModeled_simulated):
        """
        Perform the 2 context filtering pass on buildings
        :param urban_canopy_object:
        :param min_VF_criterion:
        :param number_of_rays:
        :param building_id_list:
        :param on_building_to_simulate:
        :param automatic_floor_subdivision_for_new_BuildingModeled:
        :param use_layout_from_typology_for_new_BuildingModeled:
        :param use_properties_from_typology_for_new_BuildingModeled:
        :param make_new_BuildingModeled_simulated:
        :return:
        """

        # Initialize the BuildingShadingContext obj if needed
        urban_canopy_object.initialize_shading_context_obj_of_buildings_to_simulate(min_VF_criterion, number_of_rays)
        # Perform the first pass of context filtering
        building_id_list_to_convert_to_BuildingModeled = cls.perform_first_pass_of_context_filtering_on_buildings(
            urban_canopy_object, min_VF_criterion=default_mvfc_context_shading_selection,
            number_of_rays=default_number_of_rays, building_id_list=None, on_building_to_simulate=True)
        # Convert the context buildings in BuildingModeled objects
        urban_canopy_object.convert_list_of_buildings_to_BuildingModeled(building_id_list_to_convert_to_BuildingModeled,
                                                                         automatic_floor_subdivision=automatic_floor_subdivision_for_new_BuildingModeled,
                                                                         layout_from_typology=use_layout_from_typology_for_new_BuildingModeled,
                                                                         properties_from_typology=use_properties_from_typology_for_new_BuildingModeled,
                                                                         are_simulated=make_new_BuildingModeled_simulated)
        # Perform the second pass of context filtering
        cls.perform_second_pass_of_context_filtering_on_buildings(urban_canopy_object)

    @ staticmethod
    def perform_first_pass_of_context_filtering_on_buildings(urban_canopy_object,
                                                             min_VF_criterion=default_mvfc_context_shading_selection,
                                                             number_of_rays=default_number_of_rays,
                                                             building_id_list=None, on_building_to_simulate=True,
                                                             automatic_floor_subdivision_for_new_BuildingModeled=default_automatic_floor_subdivision_for_new_BuildingModeled,
                                                             use_layout_from_typology_for_new_BuildingModeled=default_use_layout_from_typology_for_new_BuildingModeled,
                                                             use_properties_from_typology_for_new_BuildingModeled=default_use_properties_from_typology_for_new_BuildingModeled,
                                                             make_new_BuildingModeled_simulated=default_make_new_BuildingModeled_simulated):
        """
        Perform first pass of context filtering on buildings
        :param urban_canopy_object: UrbanCanopy object, the urban canopy
        :param min_VF_criterion: float, minimum view factor criterion
        :param number_of_rays: int, number of rays to use for the view factor calculation
        :param building_id_list: list of str, list of building IDs to perform the context filtering on (optionnal)
        :param on_building_to_simulate: bool, if True, perform the context filtering on all the building to simulate
        :return:
        """

        # Perform first pass of context filtering on buildings
        return urban_canopy_object.perform_first_pass_context_filtering_on_buildings(
            building_id_list=building_id_list,
            on_building_to_simulate=on_building_to_simulate)


    @staticmethod
    def perform_second_pass_of_context_filtering_on_buildings(urban_canopy_object):
        """ todo """
        pass # todo @ Elie
