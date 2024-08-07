"""Convert a list of closed breps to Laadybug geometry Polyface3D object stored in a json file (mostly to send them to the urban canopy)
    Inputs:
        _close_brep_list: List of closed breps to convert to Polyface3D stored in a json file
        (mostly to send them to the urban canopy)
        _prefix: Prefix to add to the identifier of the Polyface3D object. Make sure it is unique to this project
        _file_name_ : Name of the json file to create without extension (Default: polyface3d)
        _path_folder_: Path to the location where the file will be generated. If None, the file will be generated in the default simulation folder.
            It is recommended to specify a folder if you are not using the default simulation folder.
        _run: Plug in a button to run the component
    Output:
        path_polyface3d_json_file: path to the json file containing the polyface3d object"""

__author__ = "elie-medioni"
__version__ = "2024.06.04"

ghenv.Component.Name = "BUA Convert Breps To Polyface3D Json"
ghenv.Component.NickName = 'ConvertBrepsToPolyface3DJson'
ghenv.Component.Message = '1.2.0'
ghenv.Component.Category = 'BUA'
ghenv.Component.SubCategory = '1 :: Load Buildings'

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

from ladybug_rhino.togeometry import to_polyface3d


def clean_path(path):
    path = path.replace("\\", "/")
    return (path)


# Get Appdata\local folder
local_appdata = os.environ['LOCALAPPDATA']
path_tool = os.path.join(local_appdata, "Building_urban_analysis")
name_folder_temporary_files = "temporary_files"
default_file_name = "polyface3d"

if _file_name_ is None or _file_name_ == "":
    _file_name_ = default_file_name
if _path_folder_ is None or _path_folder_ == "":
    _path_folder_ = os.path.join(path_tool, "Simulation_temp", name_folder_temporary_files)
    if not os.path.isdir(_path_folder_):
        os.makedirs(_path_folder_)
elif os.path.isdir(_path_folder_) is False:
    raise ValueError("The path folder does not exist, enter a valid path")

if _close_brep_list is not None and not _close_brep_list == []:
    for brep in _close_brep_list:
        if not brep.IsSolid:
            raise ValueError("At least one of the Brep is not closed, only close Brep can be loaded")

path_polyface3d_json_file = os.path.join(_path_folder_, _file_name_ + ".json")

if _run:
    # Check the inputs
    if _close_brep_list is None or _close_brep_list == []:
        raise ValueError("The list of breps is empty")
    if _prefix is None or _prefix == "":
        raise ValueError("The prefix is empty")



    # Create the temparary simulation folder if it does not exist if needed
    if not os.path.exists(_path_folder_):
        os.makedirs(_path_folder_)

    # Initialize the list of polyface3d
    polyface3d_dict = {}
    # Convert the closed breps to polyface3d
    for index, brep in enumerate(_close_brep_list):
        polyface3d_dict["{}_{}".format(_prefix, index)] = to_polyface3d(brep).to_dict()
    # Create the json file
    with open(path_polyface3d_json_file, 'w') as outfile:
        json.dump(polyface3d_dict, outfile)
