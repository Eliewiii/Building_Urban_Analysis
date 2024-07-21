from bua.utils.utils_import_simulation_steps_and_config_var import *

# Create urban_canopy
urban_canopy_object = SimulationCommonMethods.create_or_load_urban_canopy_object(
    path_simulation_folder=default_path_simulation_folder)


path_gis = r"C:\Users\eliem\OneDrive - Technion\Ministry of Energy Research\IBPSA US conference\Buildings"
# add GIS
SimulationLoadBuildingOrGeometry.add_2D_GIS_to_urban_canopy(urban_canopy=urban_canopy_object,
                                                            path_gis=path_gis,
                                                            path_additional_gis_attribute_key_dict=
                                                            None,
                                                            unit="deg")

# Move building to origin
SimulationBuildingManipulationFunctions.move_buildings_to_origin(urban_canopy_object=urban_canopy_object)
#

path_folder_json = r"C:\Users\eliem\OneDrive - Technion\Ministry of Energy Research\IBPSA US conference\hbjson_2\var_sub_optimal\merged_or"

# # Load Buildings from json
# path_folder_json = None
path_file_json = None
# path_folder_json = "C:\\Users\\elie-medioni\\OneDrive\\OneDrive - Technion\\BUA\\Elie\\Samples\\hb_model"
# # path_file_json = "C:\Users\elie-medioni\OneDrive\OneDrive - Technion\BUA\Hilany\Samples\model_with_shades_small_win_corr.hbjson"
# path_file_json = "C:\\Users\\alejandro.s\\Technion\\Elie Medioni - BUA\\Samples\\Elie\\hb_model\\complex_hb_model.hbjson"
#

SimulationLoadBuildingOrGeometry.add_buildings_from_hbjson_to_urban_canopy(
    urban_canopy_object=urban_canopy_object,
    path_folder_hbjson=path_folder_json,
    path_file_hbjson=path_file_json,
    are_buildings_targets=True)

# # Move building to origin
# SimulationBuildingManipulationFunctions.move_buildings_to_origin(urban_canopy_object=urban_canopy_object)



# Export urban_canopy to pickle
SimulationCommonMethods.save_urban_canopy_object_to_pickle(urban_canopy_object=urban_canopy_object,
                                                           path_simulation_folder=default_path_simulation_folder)
# Export urban_canopy to json
SimulationCommonMethods.save_urban_canopy_to_json(urban_canopy_object=urban_canopy_object,
                                                  path_simulation_folder=default_path_simulation_folder)

