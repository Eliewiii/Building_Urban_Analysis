"""

"""
from mains_tool.utils_general import *

class SimulationBuildingManipulationFunctions:
    @staticmethod
    def move_buildings_to_origin(urban_canopy,move_buildings_to_origin):
        """
        Move buildings to the origin of the plan (put the average elevation to 0)
        :param move_buildings_to_origin:
        :param urban_canopy:
        :return:
        """
        if move_buildings_to_origin or urban_canopy.moving_vector_to_origin is not None:
            urban_canopy.move_buildings_to_origin()
            logging.info("Buildings have been moved to origin successfully")

    @staticmethod
    def remove_building_list_from_urban_canopy(urban_canopy,building_list):
        """
        Remove a list of buildings from the urban canopy
        :param urban_canopy:
        :param building_list:
        :return:
        """
        for building_id in building_list:
            urban_canopy.remove_building_from_dict(building_id)
        logging.info("Building(s) removed from the urban canopy successfully")