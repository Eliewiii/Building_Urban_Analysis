"""

"""

from mains_tool.utils_main_import_packages import *

# Get Appdata\local folder
local_appdata = os.environ['LOCALAPPDATA']
path_tool = os.path.join(local_appdata, "Building_urban_analysis")
# Path of the different folders in the tool
path_scripts_tool = os.path.join(path_tool, "Scripts")
path_libraries_tool = os.path.join(path_tool, "Libraries")
# Name of the folders generated by the tool
name_folder_gh_components_logs = "gh_components_logs"
name_folder_temporary_files = "temporary_files"
# Name of the files generated by the tool
name_urban_canopy_envelop_hbjson = "urban_canopy_envelop.hbjson"  # todo @Elie: change the name in the rest of the code and GH
name_bounding_box_file_hbjson = "bounding_boxes.hbjson"

# Default values for the simulations - General
default_path_folder_simulation = os.path.join(path_tool, "Simulation_temp")
default_move_buildings_to_origin = False
default_make_hb_model_envelops = False

# Default values for the simulations - GIS
default_path_gis = os.path.join(path_libraries_tool, "GIS", "gis_typo_id_extra_small")
default_building_id_key_gis = "idbinyan"
default_gis_attribute_key_dict = {
    "building_id_key_gis": "none",
    "name": ["name", "full_name_"],
    "age": ["age", "date", "year"],
    "typology": ["typo", "typology", "type", "Typology"],
    "elevation": ["minheight"],
    "height": ["height", "Height", "govasimple"],
    "number of floor": ["number_floor", "nb_floor", "mskomot"],
    "group": ["group"]
}
default_unit_gis = "m"
default_move_buildings_to_origin = False

# Default values for the simulations - Building manipulation
default_is_target_building = True
default_is_simulated_building = True  # target building is always simulated

# default values for when using Honeybee, dragonfly and Ladybug libraries
default_tolerance_value = 0.01

# Default values for the simulations - Context filter
default_minimum_vf_criterion_context_filter_first_pass_shading = 0.01
default_number_of_rays_context_filter_second_pass = 3
# todo @Elie: add when coded
# Default values for the simulations - Solar radiation calculation
default_name_radiation_simulation_folder = 'Radiation Simulation'
default_path_weather_file = os.path.join(path_tool, "Libraries", "EPW", "IS_5280_A_Haifa.epw")
default_grid_size = 1.5  # todo check it !
default_offset_dist = 0.1
default_on_roof = True
default_on_facades = True

# Default values for panel simulation

default_path_pv_tech_dictionary = os.path.join(path_tool, "Libraries", "Solar_panels", "pv_technologies.json")
default_id_pv_tech_roof = "mitrex_roof c-Si"
default_id_pv_tech_facades = "metsolar_facades c-Si"
default_study_duration_years = 50
default_replacement_scenario = "yearly"
default_evey_X_years = 5
# Exports
urban_canopy_export_file_name = "urban_canopy"
urban_canopy_export_file_name_pkl = urban_canopy_export_file_name + ".pkl"
urban_canopy_export_file_name_json = urban_canopy_export_file_name + ".json"

# Export to json file
default_tree_structure_per_building_urban_canopy_json_dict = {
    "Is_target_building": False,  # Maybe add all the other attributes (height,age,typology,etc.)
    "Is_to_simulate": False,
    "Age": None,
    "Typology": None,
    "HB_model": {},
    "HB_room_envelop": {},
    "Context_surfaces": {
        "First_pass_filter": {},
        "Second_pass_filter": {}
    },
    "Solar_radiation": {
        "Sensor_grids_dict": {"Roof": None, "Facades": None},
        "Path_results": {
            "Annual": {"Roof": None, "Facades": None},
            "Timestep": {"Roof": None, "Facades": None}
        },
        "Panels_results": {
            "Roof": {
                "energy_produced": {"list": None, "total": None},
                "lca_energy": {"list": None, "total": None},
                "lca_carbon": {"list": None, "total": None},
                "dmfa": {"list": None, "total": None},
                "recycling_energy": {"list": None, "total": None}
            },
            "Facades": {
                "energy_produced": {"list": None, "total": None},
                "lca_energy": {"list": None, "total": None},
                "lca_carbon": {"list": None, "total": None},
                "dmfa": {"list": None, "total": None},
                "recycling_energy": {"list": None, "total": None}
            },
            "Total": {
                "energy_produced": {"list": None, "total": None},
                "lca_energy": {"list": None, "total": None},
                "lca_carbon": {"list": None, "total": None},
                "dmfa": {"list": None, "total": None},
                "recycling_energy": {"list": None, "total": None}
            },
        }
    }
}
