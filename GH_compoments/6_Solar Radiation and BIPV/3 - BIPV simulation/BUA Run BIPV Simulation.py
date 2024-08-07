"""Run the BIPV simulation for the selected buildings.
    Inputs:
        path_simulation_folder_: Path to the simulation folder.
            (Default = user\appdata\Local\Building_urban_analysis\Simulation_temp)
        building_id_list_: list of the identifier of the buildings that should be simulated. The buildings
            need to be target buildings to be simulated (Default = "all")
        _bipv_simulation_identifier_: Identifier of the simulation that should be simulated. The results of each
            simulation saved in a separate folder. (Default = "new_uc_scenario")
        _bipv_panels_parameters : Parameters of the BIPV simulation. to be defined from the BIPVParameters component.
        _replacement_scenario_parameters: Parameters of the replacement scenario. to be defined from the
            ReplacementScenarioParameters component.
        _start_year: Year from which the simulation should start. (Default: current year)
        _end_year: Year from which the simulation should end. For instance, if the start year is 2023 and the end year
         2026, the simulation will be run for 3 years: 2023,2024 and 2025 (Default: current year+50)
        _overwrite_: bool: True if the existing simulation should be overwritten. (Default: True)
        update_panel_technology_: Set to True if the panel technology should be updated to the inputted one when replaced.
        _run: Plug in a button to run the component
    Output:
        report: report
        path_simulation_folder_: Path to the folder."""

__author__ = "Elie"
__version__ = "2024.04.07"

ghenv.Component.Name = "BUA Run BIPV Simulation"
ghenv.Component.NickName = 'RunBIPVSimulation'
ghenv.Component.Message = '1.2.0'
ghenv.Component.Category = 'BUA'
ghenv.Component.SubCategory = '6 :: Solar Radiation and BIPV'

import rhinoscriptsyntax as rs
def get_rhino_version():
    return rs.ExeVersion()
rhino_version = get_rhino_version()
if rhino_version > 7:
    import ghpythonlib as ghlib
    c = ghlib.component._get_active_component()
    c.ToggleObsolete(False)

import os
import json


def clean_path(path):
    path = path.replace("\\", "/")
    return (path)


def read_logs(path_simulation_folder):
    path_log_file = os.path.join(path_simulation_folder_, "gh_components_logs",
                                 ghenv.Component.NickName + ".log")
    if os.path.isfile(path_log_file):
        with open(path_log_file, 'r') as log_file:
            log_data = log_file.read()
        return (log_data)
    else:
        return ("No log found")


# Get Appdata\local folder
local_appdata = os.environ['LOCALAPPDATA']
path_tool = os.path.join(local_appdata, "Building_urban_analysis")
path_bat_file = os.path.join(path_tool, "Scripts","bua", "mains_tool", "run_BUA.bat")

# Check path_simulation_folder_
if path_simulation_folder_ is not None and os.path.isdir(path_simulation_folder_) is False:
    raise ValueError("The simulation folder does not exist, enter a valid path")

# Check _bipv_panels_parameters
if _bipv_panels_parameters is not None:
    try:  # try to load the json
        bipv_panel_parameters_dict = json.loads(_bipv_panels_parameters)
    except:
        raise ValueError("The BIPV parameters are not valid, use the BIPV Parameters component as input")
    if (isinstance(bipv_panel_parameters_dict, dict) is False
            or "roof_pv_tech_id" not in bipv_panel_parameters_dict.keys()
            or "facades_pv_tech_id" not in bipv_panel_parameters_dict.keys()
            or "roof_pv_transport_id" not in bipv_panel_parameters_dict.keys()
            or "facades_pv_transport_id" not in bipv_panel_parameters_dict.keys()
            or "roof_pv_inverter_id" not in bipv_panel_parameters_dict.keys()
            or "facades_pv_inverter_id" not in bipv_panel_parameters_dict.keys()
            or "roof_inverter_sizing_ratio" not in bipv_panel_parameters_dict.keys()
            or "facades_inverter_sizing_ratio" not in bipv_panel_parameters_dict.keys()
            or "minimum_panel_eroi" not in bipv_panel_parameters_dict.keys()):

        raise ValueError("The BIPV parameters are not valid, use the BIPV Parameters component as input")
    else:
        roof_pv_tech_id = bipv_panel_parameters_dict["roof_pv_tech_id"]
        facades_pv_tech_id = bipv_panel_parameters_dict["facades_pv_tech_id"]
        roof_pv_transport_id = bipv_panel_parameters_dict["roof_pv_transport_id"]
        facades_pv_transport_id = bipv_panel_parameters_dict["facades_pv_transport_id"]
        roof_pv_inverter_id = bipv_panel_parameters_dict["roof_pv_inverter_id"]
        facades_pv_inverter_id = bipv_panel_parameters_dict["facades_pv_inverter_id"]
        roof_inverter_sizing_ratio = bipv_panel_parameters_dict["roof_inverter_sizing_ratio"]
        facades_inverter_sizing_ratio = bipv_panel_parameters_dict["facades_inverter_sizing_ratio"]
        minimum_panel_eroi = bipv_panel_parameters_dict["minimum_panel_eroi"]
else:
    roof_pv_tech_id = None
    facades_pv_tech_id = None
    roof_pv_transport_id = None
    facades_pv_transport_id = None
    roof_pv_inverter_id = None
    facades_pv_inverter_id = None
    roof_inverter_sizing_ratio = None
    facades_inverter_sizing_ratio = None
    minimum_panel_eroi = None

# Check _replacement_scenario_parameters
if _replacement_scenario_parameters is not None:
    try:  # try to load the json
        replacement_scenario_parameters_dict = json.loads(_replacement_scenario_parameters)
    except:
        raise ValueError("The BIPV parameters are not valid, use the BIPV Parameters component as input")
    if isinstance(replacement_scenario_parameters_dict,
                  dict) is False or "replacement_scenario_id" not in replacement_scenario_parameters_dict.keys() or "replacement_frequency" not in replacement_scenario_parameters_dict.keys() or "minimal_panel_age" not in replacement_scenario_parameters_dict.keys():
        raise ValueError(
            "The replacement scenario parameters are not valid, use the Replacement Scenario Parameters component as input")
    else:
        replacement_scenario_id = replacement_scenario_parameters_dict["replacement_scenario_id"]
        replacement_frequency = replacement_scenario_parameters_dict["replacement_frequency"]
        minimal_panel_age = replacement_scenario_parameters_dict["minimal_panel_age"]
else:
    replacement_scenario_id = None
    replacement_frequency = None
    minimal_panel_age = None

# Set _overwrite_ to True if it is not provided
if _overwrite_ is None:
    _overwrite_ = True

# Check _start_year and _end_year
if _start_year is None and _end_year is None:
    pass
elif _start_year is None:
    raise ValueError("The start year and the end year must be defined")
elif _start_year is not None and _end_year is not None and _start_year >= _end_year:
    raise ValueError("The start year must be lower than the end year")

if _run:
    # Write the command
    command = path_bat_file
    # Steps to execute
    argument = " "
    argument = argument + "--make_simulation_folder 1 " + "--create_or_load_urban_canopy_object 1 " + "--run_bipv_harvesting_and_lca_simulation 1 " + " --overwrite 1 " + "--save_urban_canopy_object_to_pickle 1 " + "--save_urban_canopy_object_to_json 1 "
    # OPtionnal argument of the bat file/Python script
    if path_simulation_folder_ is not None:
        argument = argument + ' -f "{}"'.format(path_simulation_folder_)
    if building_id_list_ is not None and building_id_list_ != []:
        argument = argument + ' --building_id_list "{}"'.format(building_id_list_)
    if _bipv_simulation_identifier_ is not None:
        argument = argument + ' --bipv_scenario_identifier "{}"'.format(_bipv_simulation_identifier_)
    if roof_pv_tech_id is not None:
        argument = argument + ' --id_pv_tech_roof "{}"'.format(roof_pv_tech_id)
    if facades_pv_tech_id is not None:
        argument = argument + ' --id_pv_tech_facades "{}"'.format(facades_pv_tech_id)
    if roof_pv_transport_id is not None:
        argument = argument + ' --roof_transport_id "{}"'.format(roof_pv_transport_id)
    if facades_pv_transport_id is not None:
        argument = argument + ' --facades_transport_id "{}"'.format(facades_pv_transport_id)
    if roof_pv_inverter_id is not None:
        argument = argument + ' --roof_inverter_id "{}"'.format(roof_pv_inverter_id)
    if facades_pv_inverter_id is not None:
        argument = argument + ' --facades_inverter_id "{}"'.format(facades_pv_inverter_id)
    if roof_inverter_sizing_ratio is not None:
        argument = argument + " --roof_inverter_sizing_ratio {}".format(roof_inverter_sizing_ratio)
    if facades_inverter_sizing_ratio is not None:
        argument = argument + " --facades_inverter_sizing_ratio {}".format(facades_inverter_sizing_ratio)
    if minimum_panel_eroi is not None:
        argument = argument + " --minimum_panel_eroi {}".format(minimum_panel_eroi)
    if replacement_scenario_id is not None:
        argument = argument + ' --replacement_scenario "{}"'.format(replacement_scenario_id)
    if replacement_frequency is not None:
        argument = argument + " --replacement_frequency {}".format(replacement_frequency)
    if minimal_panel_age is not None:
        argument = argument + " --minimal_panel_age {}".format(minimal_panel_age)
    if _start_year is not None:
        argument = argument + " --start_year {}".format(_start_year)
    if _end_year is not None:
        argument = argument + " --end_year {}".format(_end_year)
    if _overwrite_ is not None:
        argument = argument + " --overwrite {}".format(int(_overwrite_))
    if update_panel_technology_ is not None:
        argument = argument + " --update_panel_technology {}".format(int(update_panel_technology_))

    # Add the name of the component to the argument
    argument = argument + " -c {}".format(ghenv.Component.NickName)
    # Run the bat file
    output = os.system(command + argument)

# set default value for the simulation folder if not provided
if path_simulation_folder_ is None:
    path_simulation_folder_ = os.path.join(path_tool, "Simulation_temp")

# Path to the results of the simulation
name_radiation_simulation_folder = 'Irradiance and BIPV Simulation'
path_bipv_simulation_results_folder = os.path.join(path_simulation_folder_, name_radiation_simulation_folder)

# Check if the simulation folder exists
if os.path.isdir(path_bipv_simulation_results_folder):
    pass
else:
    path_bipv_simulation_results_folder = None

# Read the log file
report = read_logs(path_simulation_folder_)
