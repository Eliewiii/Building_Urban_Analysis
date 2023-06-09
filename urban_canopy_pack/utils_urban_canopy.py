
import numpy
import matplotlib.pyplot as plt
import numpy as np

from mains_tool.utils_general import *

from honeybee.model import Model
from honeybee.room import Room

from building.building_basic import BuildingBasic
from building.building_modeled import BuildingModeled

from libraries_addons.extract_gis_files import extract_gis

from typology.typology import Typology

from urban_canopy_pack.urban_canopy_additional_functions import UrbanCanopyAdditionalFunction

from solar_panel.pv_panel import PvPanel
from solar_panel.pv_panel_technology import PvPanelTechnology

from libraries_addons.solar_panels.useful_functions_solar_panel import load_panels_on_sensor_grid, \
    loop_over_the_years_for_solar_panels, beginning_end_of_life_lca_results_in_lists, results_from_lists_to_dict, \
    get_cumul_values, add_elements_of_two_lists, transform_to_linear_function, find_intersection_functions, \
    generate_step_function

# Default values
default_minimum_vf_criterion_for_shadow_calculation = 0.01  # minimum view factor between surfaces to be considered
# as context surfaces in the first pass of the algorithm for shading computation
