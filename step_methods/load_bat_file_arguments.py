"""
Class to load the arguments from the command line to the main script with the values sent from Grasshopper
"""

from utils.utils_default_values_user_parameters import *


class LoadArguments:
    """ """

    @staticmethod
    def add_user_parameters_to_parser(parser):
        """
        Get the user parameters from the command line
        :param parser: parser object containing the user parameters
        :return parser: parser object with the argument added
        """
        # Configuration
        parser.add_argument("-f", "--path_simulation_folder", help="path to the simulation folder", nargs='?',
                            default=default_path_simulation_folder)
        parser.add_argument("-c", "--gh_component_name",
                            help="name of the component in gh that execute the code",
                            nargs='?',
                            default=None)
        # General
        parser.add_argument("--path_folder",
                            help="path to a folder that will be useful for the simulation", nargs='?',
                            default=None)
        parser.add_argument("--path_file",
                            help="path to a single file that will be useful for the simulation", nargs='?',
                            default=None)
        parser.add_argument("-l", "--building_id_list",
                            help="list of the names of the buildings in the urban canopy "
                                 "we want to run the simulation on", nargs='?', default=None)
        parser.add_argument("--silent", help="if True run the simulation without opening the terminal",
                            nargs='?', default=False)
        parser.add_argument("--overwrite", help="if True overwrite the previous simulation",
                            nargs='?', default=False)
        # Building manipulation
        parser.add_argument("-t", "--are_buildings_target",
                            help="boolean (here '0' or '1') telling if the buildings inputed in the component are "
                                 "target ", nargs='?', default=False)
        parser.add_argument("--on_building_to_simulate",
                            help="boolean (0 or 1), telling of the simulation should be performed on building_to_simulate",
                            nargs='?', default=False)

        # Extract Geometry GIS
        parser.add_argument("-g", "--path_gis_folder",
                            help="path to gis folder containing all the sub gis files",
                            nargs='?', default=default_path_gis)
        parser.add_argument("-u", "--gis_unit", help="unit of the GIS", nargs='?', default=default_unit_gis)
        parser.add_argument("-d", "--path_dic_additional_gis_attribute_keys",
                            help="path to the additional key dictionary of the attributes in the GIS file",
                            nargs='?', default=None)
        # Extract Geometry frpm json
        parser.add_argument("--typology",
                            help="name of the typology of that should be applied to the buildings",
                            nargs='?', default=None)
        # Building model generation parameters
        parser.add_argument("--keep_context",
                            help="boolean (here '0' or '1') telling if the context should be kept",
                            nargs='?', default=False)
        parser.add_argument("--run_on_building_to_simulate",
                            help="boolean (here '0' or '1') telling if it should be run on all buildings to simulate",
                            nargs='?', default=False)
        parser.add_argument("--automatic_floor_subdivision",
                            help="boolean (here '0' or '1') telling if it should be run on all buildings to simulate",
                            nargs='?', default=False)
        parser.add_argument("--use_layout_from_typology",
                            help="boolean (here '0' or '1') telling if it should be run on all buildings to simulate",
                            nargs='?', default=False)
        parser.add_argument("--use_properties_from_typology",
                            help="boolean (here '0' or '1') telling if it should be run on all buildings to simulate",
                            nargs='?', default=False)
        # Merge HB model faces parameters
        parser.add_argument("--orient_roof_according_to_building_orientation",
                            help="True if the roof mesh should be oriented according to the building orientation, else False",
                            default=True)
        # Context filter algorithm parameters
        parser.add_argument("--min_vf_criterion",
                            help="float, value of the minimum view factor criterion", nargs='?',
                            default=default_mvfc_context_shading_selection)
        parser.add_argument("--number_of_rays",
                            help="int, number of rays used for the raytracing", nargs='?',
                            default=default_shading_number_of_rays_context_filter_second_pass)
        parser.add_argument("--consider_windows",
                            help=f"boolean (here '0' or '1') telling if the windows should be considered in "
                                 f"the context filtering", nargs='?', default=False)
        parser.add_argument("--keep_shades_from_user",
                            help=f"boolean (here '0' or '1') telling if the shades from the user should be kept "
                                 f"in the context filtering", nargs='?', default=False)
        parser.add_argument("--no_ray_tracing",
                            help=f"boolean (here '0' or '1') telling if the ray tracing should be performed "
                                 f"(used for testing purposes)", nargs='?', default=False)
        parser.add_argument("--keep_discarded_faces",
                            help=f"boolean (here '0' or '1') telling if the discarded faces should be kept "
                                 f"(used for testing purposes)", nargs='?', default=False)
        # Simulation general
        parser.add_argument("-w", "--path_weather_file", help="path to the weather file used",
                            default=default_path_weather_file)
        parser.add_argument("--north_angle",
                            help="angle of the north in degree", default=0)
        # Sensorgrid
        parser.add_argument("--on_roof", help="True if the simulation is to be run on the roof, else False",
                            default=default_on_roof)
        parser.add_argument("--on_facades",
                            help="True if the simulation is to be run on the facades, else False",
                            default=default_on_facades)
        parser.add_argument("--grid_size",
                            help="size of the grid of the mesh for the buildings, it should be about "
                                 "the size of a panel + BOS",
                            default=default_grid_size)  # todo to delete when new version working
        parser.add_argument("--roof_grid_size_x",
                            help="size of the grid of the mesh for the buildings in the x direction, "
                                 "it should be about the size of a panel + BOS",
                            default=default_roof_grid_size_x)
        parser.add_argument("--roof_grid_size_y",
                            help="size of the grid of the mesh for the buildings in the y direction, "
                                 "it should be about the size of a panel + BOS",
                            default=default_roof_grid_size_y)
        parser.add_argument("--facades_grid_size_x",
                            help="size of the grid of the mesh for the buildings in the x direction, "
                                 "it should be about the size of a panel + BOS",
                            default=default_facades_grid_size_x)
        parser.add_argument("--facades_grid_size_y",
                            help="size of the grid of the mesh for the buildings in the y direction, "
                                 "it should be about the size of a panel + BOS",
                            default=default_facades_grid_size_y)
        parser.add_argument("--offset_dist",
                            help="Number for the distance to move points from the surfaces of the "
                                 "geometry of the model", default=default_offset_dist)
        # BIPV
        parser.add_argument("--bipv_scenario_identifier",
                            help="Identifier of the BIPV scenario", default=default_bipv_scenario_identifier)
        parser.add_argument("--path_pv_tech_dictionary_folder",
                            help="path to the folder containing the json with PVPanelTechnologies",
                            default=default_path_pv_tech_dictionary_folder)
        parser.add_argument("--id_pv_tech_roof", help="name of the pv tech used on the roof",
                            default=default_id_pv_tech_roof)
        parser.add_argument("--id_pv_tech_facades", help="name of the pv tech used on the facades",
                            default=default_id_pv_tech_facades)
        parser.add_argument("--start_year", help="Start year of the simulation",
                            default=default_start_year)
        parser.add_argument("--end_year", help="End year of the simulation",
                            default=default_end_year)
        parser.add_argument("--minimum_panel_eroi",
                            help="minimum energy production during the first year for the panel to be installed",
                            default=default_minimum_panel_eroi)
        parser.add_argument("--efficiency_computation_method",
                            help="Method used to compute the efficiency of the panel",
                            default=default_efficiency_computation_method)
        parser.add_argument("--replacement_scenario",
                            help="replacement scenario chosen for the failed panels",
                            default=default_replacement_scenario)
        parser.add_argument("--replacement_frequency_in_years", help="replacement every x years scenario",
                            default=default_replacement_frequency_in_years)
        parser.add_argument("--update_panel_technology",
                            help="Update the panel technology with the new values", default=False)
        # todo: take care of tehe last one
        parser.add_argument("--country_ghe_cost",
                            help="Cost in gCO2eq per kWh depending on the country energy mix",
                            default=default_country_ghe_cost)

    @staticmethod
    def add_user_simulation_features_to_parser(parser):
        """
        Get the simulation steps to run from the command line
        :param parser:
        :return:
        """
        # General features
        parser.add_argument("--make_simulation_folder",
                            help="create the simulation folder if it doesn't exist",
                            nargs='?',
                            default=False)
        parser.add_argument("--create_or_load_urban_canopy_object",
                            help="Load or create urban canopy objects",
                            nargs='?', default=False)
        parser.add_argument("--save_urban_canopy_object_to_pickle",
                            help="Save the urban canopy object to pickle file",
                            nargs='?', default=False)
        parser.add_argument("--save_urban_canopy_object_to_json",
                            help="Save some of the attributes of the urban canopy object to pickle file",
                            nargs='?',
                            default=False)

        # geometry extraction features
        parser.add_argument("--extract_gis", help="Extract GIS file and add it to the urban canopy object",
                            nargs='?', default=False)
        parser.add_argument("--extract_buildings_from_hbjson_models",
                            help="Extract buildings from hbjson files and add them to the urban canopy object",
                            nargs='?', default=False)
        parser.add_argument("--extract_buildings_from_polyface3d_json",
                            help="Extract buildings from polyface3d json files and add them to the urban canopy object",
                            nargs='?', default=False)

        # Building manipulation features
        parser.add_argument("--move_buildings_to_origin",
                            help="Move all the buildings to the origin of the plan",
                            nargs='?', default=False)
        parser.add_argument("--remove_building_list_from_urban_canopy",
                            help="Remove a list of building from the urban canopy object", nargs='?',
                            default=False)
        parser.add_argument("--make_merged_faces_hb_model",
                            help="Make a HB model with the faces merged.", nargs='?',
                            default=False)

        # Context filtering features
        parser.add_argument("--generate_bounding_boxes", help="Generate bounding boxes for the buildings",
                            nargs='?', default=False)
        parser.add_argument("--run_full_context_filtering", help="Perform the full context filtering for buildings",
                            nargs='?', default=False)
        parser.add_argument("--run_first_pass_context_filtering",
                            help="Perform teh first pass of the context filtering for buildings",
                            nargs='?', default=False)
        parser.add_argument("--run_second_pass_context_filtering",
                            help="Perform teh second pass of the context filtering for buildings",
                            nargs='?', default=False)
        # Generate objects for visualization
        parser.add_argument("--generate_model_with_building_envelop",
                            help="Make a HB model containing the envelop of all the buildings in the urban canopy "
                                 "object that will be stored in the json dic of the urban canopy object",
                            nargs='?', default=False)
        # Solar radiation and BIPV simulation
        parser.add_argument("--generate_sensorgrids_on_buildings",
                            help="Perform the generation of the mesh on the buildings", default=False)
        parser.add_argument("--run_annual_solar_irradiance_simulation",
                            help="Perform the generation of the mesh on the buildings", default=False)
        parser.add_argument("--run_bipv_harvesting_and_lca_simulation",
                            help="Perform the generation of the mesh on the buildings", default=False)

        # Post-processing
        parser.add_argument("--generate_panels_results_in_csv",
                            help="Generate the csv file containing all the useful "
                                 "data calculated by the simulation", default=False)
        parser.add_argument("--plot_graph_results_building_panel_simulation",
                            help="Plot and save the graphs for each building", default=False)
        parser.add_argument("--plot_graph_results_urban_canopy",
                            help="Plot and save the graphs of the urban canopy",
                            default=False)

    @staticmethod
    def parse_arguments_and_add_them_to_variable_dict(parser):
        """
        Parse the arguments
        :param parser:
        :return:
        """
        # Parse the parser with the added arguments
        args = parser.parse_args()

        # post process of some arguments
        buildings_id_list = parse_and_clean_building_id_list_from_argument_parser(args.building_id_list)

        # Create a dictionary with the arguments and the name of their variable that will be imported in the main script
        arguments_dictionary = {
            # Configuration
            "path_simulation_folder": args.path_simulation_folder,
            "gh_component_name": args.gh_component_name,
            # General
            "path_folder": args.path_folder,
            "path_file": args.path_file,
            "building_id_list": buildings_id_list,
            "silent": bool(int(args.silent)),
            "overwrite": bool(int(args.overwrite)),
            # Building manipulation
            "are_buildings_target": bool(int(args.are_buildings_target)),
            "on_building_to_simulate": bool(int(args.on_building_to_simulate)),
            # Extract geometry
            "path_gis": args.path_gis_folder,
            "unit_gis": args.gis_unit,
            "path_additional_gis_attribute_key_dict": args.path_dic_additional_gis_attribute_keys,
            # Extract geometry from json
            "typology": args.typology,
            # Building model generation parameters
            "keep_context": bool(int(args.keep_context)),
            # Mesh faces parameters
            "orient_roof_according_to_building_orientation": bool(
                int(args.orient_roof_according_to_building_orientation)),
            # Context filter algorithm parameters
            "min_vf_criterion": float(args.min_vf_criterion),
            "number_of_rays": int(args.number_of_rays),
            "consider_windows": bool(int(args.consider_windows)),
            "keep_shades_from_user": bool(int(args.keep_shades_from_user)),
            "no_ray_tracing": bool(int(args.no_ray_tracing)),
            "keep_discarded_faces": bool(int(args.keep_discarded_faces)),
            # Simulation general
            "path_weather_file": args.path_weather_file,
            "north_angle": float(args.north_angle),
            # Sensorgrid
            "on_roof": bool(int(args.on_roof)),
            "on_facades": bool(int(args.on_facades)),
            "roof_grid_size_x": float(args.roof_grid_size_x),
            "facades_grid_size_x": float(args.facades_grid_size_x),
            "roof_grid_size_y": float(args.roof_grid_size_y),
            "facades_grid_size_y": float(args.facades_grid_size_y),
            "offset_dist": float(args.offset_dist),
            # BIPV
            "bipv_scenario_identifier": args.bipv_scenario_identifier,
            "path_pv_tech_dictionary": args.path_pv_tech_dictionary_folder,
            "roof_id_pv_tech": args.id_pv_tech_roof,
            "facades_id_pv_tech": args.id_pv_tech_facades,
            "start_year": int(args.start_year),
            "end_year": int(args.end_year),
            "minimum_panel_eroi": float(args.minimum_panel_eroi),
            "efficiency_computation_method": args.efficiency_computation_method,
            "replacement_scenario": args.replacement_scenario,
            "replacement_frequency_in_years": int(args.replacement_frequency_in_years),
            "update_panel_technology": bool(int(args.update_panel_technology)),
            "country_ghe_cost": float(args.country_ghe_cost),
        }

        # Create a dictionary with the arguments and the name of their variable that will be imported in the main script
        step_dictionary = {
            # Initialization and wrapping
            "run_make_simulation_folder": bool(int(args.make_simulation_folder)),
            "run_create_or_load_urban_canopy_object": bool(int(args.create_or_load_urban_canopy_object)),
            "run_save_urban_canopy_object_to_pickle": bool(int(args.save_urban_canopy_object_to_pickle)),
            "run_save_urban_canopy_object_to_json": bool(int(args.save_urban_canopy_object_to_json)),
            # Import geometry
            "run_extract_gis": bool(int(args.extract_gis)),
            "run_extract_buildings_from_hbjson_models": bool(int(args.extract_buildings_from_hbjson_models)),
            "run_extract_buildings_from_polyface3d_json": bool(int(args.extract_buildings_from_polyface3d_json)),
            # Building manipulation
            "run_move_buildings_to_origin": bool(int(args.move_buildings_to_origin)),
            "run_remove_building_list_from_urban_canopy": bool(
                int(args.remove_building_list_from_urban_canopy)),
            "run_make_merged_faces_hb_model": bool(int(args.make_merged_faces_hb_model)),
            "run_generate_bounding_boxes": bool(int(args.generate_bounding_boxes)),
            "run_generate_model_with_building_envelop": bool(int(args.generate_model_with_building_envelop)),
            # Context filtering
            "run_context_filtering": bool(int(args.run_full_context_filtering)),
            "run_first_pass_context_filtering": bool(int(args.run_first_pass_context_filtering)),
            "run_second_pass_context_filtering": bool(int(args.run_second_pass_context_filtering)),
            # Solar and BIPV simulation
            "run_generate_sensorgrids_on_buildings": bool(int(args.generate_sensorgrids_on_buildings)),
            "run_annual_solar_irradiance_simulation": bool(int(args.run_annual_solar_irradiance_simulation)),
            "run_bipv_harvesting_and_lca_simulation": bool(int(args.run_bipv_harvesting_and_lca_simulation)),
            "generate_panels_results_in_csv": bool(int(args.generate_panels_results_in_csv)),
            "plot_graph_results_building_panel_simulation": bool(
                int(args.plot_graph_results_building_panel_simulation)),  # todo outdated
            "plot_graph_results_urban_canopy": bool(int(args.plot_graph_results_urban_canopy))  # todo outdated
        }

        return arguments_dictionary, step_dictionary


def parse_and_clean_building_id_list_from_argument_parser(building_id_list_form_argument_parser):
    """
    Parse the building id list from the argument parser
    :param building_id_list_form_argument_parser: str : list of building id seperated by spaces
    :return:
    """
    # return None if None
    if building_id_list_form_argument_parser is None:
        return None
    else:
        # return a list of id, ignore the empty string if there is any
        return [id for id in building_id_list_form_argument_parser.split(" ") if id != '']
