"""Generate the bounding boxes buildings for context selection algorithm.
    Inputs:
        path_simulation_folder_: Path to the simulation folder. Default = Appdata\Local\Building_urban_analysis\Simulation_temp
        _overwrite_: Set to True to overwrite the existing bounding boxes. Default = False
        _run: Plug in a button to run the component
    Output:
        report: logs
        path_simulation_folder_: Path to the folder."""


__author__ = "elie-medioni"
__version__ = "2023.12.27"

ghenv.Component.Name = "BUA Generate Bounding Boxes"
ghenv.Component.NickName = 'GenerateBoundingBoxes'
ghenv.Component.Message = '1.2.0'
ghenv.Component.Category = 'BUA'
ghenv.Component.SubCategory = '4 :: Context Selection'

import rhinoscriptsyntax as rs
def get_rhino_version():
    return rs.ExeVersion()
rhino_version = get_rhino_version()
if rhino_version > 7:
    import ghpythonlib as ghlib
    c = ghlib.component._get_active_component()
    c.ToggleObsolete(False)

import os


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
        return ("No log file found")


# Check path_simulation_folder_
if path_simulation_folder_ is not None and os.path.isdir(path_simulation_folder_) is False:
    raise ValueError("The simulation folder does not exist, enter a valid path")

# Get Appdata\local folder
local_appdata = os.environ['LOCALAPPDATA']
path_tool = os.path.join(local_appdata, "Building_urban_analysis")
path_bat_file = os.path.join(path_tool, "Scripts","bua", "mains_tool", "run_BUA.bat")

if _run:
    # Write the command
    command = path_bat_file
    # Steps to execute
    argument = " "
    argument = argument + "--make_simulation_folder 1 " + "--create_or_load_urban_canopy_object 1 " + "--save_urban_canopy_object_to_pickle 1 " + "--save_urban_canopy_object_to_json 1 " + "--generate_bounding_boxes 1 "
    # OPtionnal argument of the bat file/Python script
    if path_simulation_folder_ is not None:
        argument = argument + ' -f "{}"'.format(path_simulation_folder_)
    if overwrite_ is not None:
        argument = argument + " --overwrite {}".format(int(overwrite_))

    # Add the name of the component to the argument
    argument = argument + " -c {}".format(ghenv.Component.NickName)
    # Run the bat file
    output = os.system(command + argument)

# set default value for the simulation folder if not provided
if path_simulation_folder_ is None:
    path_simulation_folder_ = os.path.join(path_tool, "Simulation_temp")

# Read the log file
report = read_logs(path_simulation_folder_)