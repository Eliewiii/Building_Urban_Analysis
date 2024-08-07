"""Plot the bounding boxes of the buildings inside the Urban Canopy. For the context selection algorithm.
    Inputs:
        path_simulation_folder_: Path to the folder. By default, the code will be run in
                                Appdata\Local\Building_urban_analysis\Simulation_temp
        building_id_list_: List of building ids to display. If empty, all the buildings will be displayed.
        _run : Plug a boolean toggle to True to run the code and display the results.
    Output:
        bounding_box_list : Brep of the bounding_boxes of the target building
        building_id_list : List of the ids of the buildings
"""

__author__ = "elie-medioni"
__version__ = "2023.12.22"

ghenv.Component.Name = "BUA Plot Bounding Boxes"
ghenv.Component.NickName = 'PlotBoundingBoxes'
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

import json
import os

from ladybug_rhino.fromgeometry import from_polyface3d
from ladybug_geometry.geometry3d.polyface import Polyface3D


def clean_path(path):
    path = path.replace("\\", "/")
    return (path)


# Get Appdata\local folder
local_appdata = os.environ['LOCALAPPDATA']
path_tool = os.path.join(local_appdata, "Building_urban_analysis")

# set default value for the simulation folder if not provided
if path_simulation_folder_ is None:
    path_simulation_folder_ = os.path.join(path_tool, "Simulation_temp")

path_json = os.path.join(path_simulation_folder_, "urban_canopy.json")

# Run the code if the _run input is set to True
if _run and os.path.isfile(path_json):

    # Read the json file
    with open(path_json, 'r') as json_file:
        urban_canopy_dict = json.load(json_file)

    # Get the list of the building ids to display
    if _building_id_list == [] or _building_id_list is None:
        _building_id_list = list(urban_canopy_dict["buildings"].keys())
    else: # Check if the building ids are in the json file
        for building_id in _building_id_list:
            try :
                urban_canopy_dict["buildings"][building_id]
            except KeyError:
                raise KeyError("Building with ID '{}' not found in the dictionary.".format(building_id))

    # Init
    bounding_box_list = []

    for building_id in _building_id_list:
        # Check if the building has a bounding box
        if urban_canopy_dict["buildings"][building_id]["lb_polyface3d_oriented_bounding_box"] is not None:
            # Convert the dictionnary to a polyface3d then to a brep
            bounding_box_list.append(from_polyface3d(
                Polyface3D.from_dict(urban_canopy_dict["buildings"][building_id]["lb_polyface3d_oriented_bounding_box"])))
    if len(bounding_box_list) == 0:
        print("No bounding box was found. The bounding boxes were not generated. "
              "Generate them with the dedicated component or run context filtering if needed, "
              "it generates the bounding boxes automatically.")

    # Set the ids of teh buildings as output, to know which building is which
    building_id_list = _building_id_list

if not os.path.isfile(path_json):
    print("The json file of the urban canopy does not exist")
