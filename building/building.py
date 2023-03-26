"""
BuildingBasic class, representing one building in an urban canopy.
"""

import logging

import shapely

from math import sqrt, isnan
from ladybug_geometry.geometry3d import Point3D, Face3D, Vector3D

from libraries_addons.hb_rooms_addons import LB_face_footprint_to_elevated_HB_room_envelop

default_gis_attribute_key_dict = {
    "building_id_key_gis": [],
    "name": ["name", "full_name_"],
    "age": ["age", "date"],
    "typology": ["typo", "typology", "type", "Typology"],
    "elevation": ["minheight"],
    "height": ["height", "Height", "govasimple"],
    "number of floor": ["number_floor", "nb_floor", "mskomot"],
    "group": ["group"]
}


class BuildingBasic:
    """BuildingBasic class, representing one building in an urban canopy."""

    def __init__(self, identifier, LB_face_footprint, urban_canopy=None, building_index_in_GIS=None):
        """Initialize a building obj"""
        # urban canopy and key to access to the object from building_dict
        self.urban_canopy = urban_canopy
        self.id = identifier  # id of the building in the urban canopy building_dict
        # GIS specific
        self.index_in_GIS = building_index_in_GIS  # id in the shp file
        # Properties
        self.name = None  # name of the building (if available in the GIS)
        self.group = None  # group/neighbourhood of the building (if available in the GIS)
        self.age = None  # year the building was built
        self.typology = None  # typology of the building
        self.height = None  # height of the building in meter
        self.num_floor = None  # number of floor of the building
        self.elevation = 0  # elevation of the building in meter
        self.floor_height = None  # height of the floors in meter
        # Geometry
        self.LB_face_footprint = LB_face_footprint  # footprint of the building, including the holes in the LB geometry face format
        # Position
        self.moved_to_origin = False  # boolean to know if the building has been moved

    def load_HB_attributes(self):
        """ Load the attributes that cannot be pickled from equivalent attribute dict. """
        # for BuildingBasic not relevant yet, so nothing to do
        None

    def pickle_HB_attributes(self):
        """ Pickle the attributes that cannot be pickled. """
        # for BuildingBasic not relevant yet, so nothing to do
        None

    @classmethod
    def make_buildingbasic_from_LB_footprint(cls, LB_face_footprint, identifier, urban_canopy=None, building_index_in_GIS=None):
        """Generate a BuildingBasic from a Ladybug footprint."""
        return cls(identifier, LB_face_footprint, urban_canopy, building_index_in_GIS)

    @classmethod
    def make_buildingbasic_from_shapely_polygon(cls, polygon, identifier, unit, urban_canopy=None, building_index_in_GIS=None):
        """Generate a BuildingBasic from a shapely polygon."""
        LB_face_footprint = polygon_to_LB_footprint(polygon, unit)
        if LB_face_footprint is not None:
            return cls(identifier, LB_face_footprint, urban_canopy, building_index_in_GIS)
        else:
            return None

    @classmethod
    def make_buildingbasic_from_GIS(cls, urban_canopy, GIS_file, building_index_in_GIS, building_id_key_gis, unit):
        """
            Generate a building from a shp file.
            Can Eventually return multiple buildings if the footprint is a multipolygon.

            :param urban_canopy:
            :param GIS_file: GIS file
            :param building_index_in_GIS: id of the building in the shp file
            :param building_id_key_gis: key of the building id in the shp file
            :param unit: unit of the shp file
            :return: list of building ids and list of building objects
        """
        # Initialize the outputs
        building_id_list, building_obj_list = [], []
        # get the building id
        if building_id_key_gis is None:
            # if the building identifier is not specified in the shp file, use the index of the building in the shp file
            # todo: maybe convert into a string, the results are weird in GH, but not problematic
            building_id = building_index_in_GIS
        else:
            building_id = GIS_file[building_id_key_gis][building_index_in_GIS]
        # get the footprint of the building
        footprint = GIS_file['geometry'][building_index_in_GIS]

        # if the building footprint is a multipolygon
        if isinstance(footprint, shapely.geometry.polygon.Polygon):
            try:
                polygon_to_LB_footprint(footprint, unit)

            except:
                logging.warning(f"The footprint of the building id {building_id} in the GIS file could not be converted"
                                f" to a Ladybug footprint. The building will be ignored.")
            else:
                building_obj = cls.make_buildingbasic_from_shapely_polygon(polygon=footprint, identifier=building_id, unit=unit,
                                                urban_canopy=urban_canopy,
                                                building_index_in_GIS=building_index_in_GIS)
                if building_obj is not None:
                    building_id_list.append(building_id)
                    building_obj_list.append(building_obj)


        # if the building footprint is a multipolygon
        elif isinstance(footprint, shapely.geometry.multipolygon.MultiPolygon):
            for i, polygon in enumerate(footprint.geoms):
                sub_building_id = f"{building_id}_{i}"
                try:
                    polygon_to_LB_footprint(polygon, unit)
                except:
                    logging.warning(
                        f"The footprint of the building id {sub_building_id} in the GIS file could not be converted"
                        f" to a Ladybug footprint. The building will be ignored.")
                else:
                    building_obj = cls.make_buildingbasic_from_shapely_polygon(polygon=footprint, identifier=sub_building_id,
                                                    urban_canopy=urban_canopy,
                                                    building_index_in_GIS=building_index_in_GIS)
                    if building_obj is not None:
                        building_id_list.append(sub_building_id)
                        building_obj_list.append(building_obj)

        return building_id_list, building_obj_list

    def extract_building_attributes_from_GIS(self, GIS_file, additional_gis_attribute_key_dict=None):
        """
        Affect the properties of the building from a shp file.
        :param GIS_file: shp file
        :param additional_gis_attribute_key_dict: dictionary of additional keys to look for in the shp file
        """
        gis_attribute_key_dict = add_additional_attribute_keys_to_dict(default_gis_attribute_key_dict,
                                                                       additional_gis_attribute_key_dict)

        ## age ##
        for attribute_key in gis_attribute_key_dict["age"]:  # loop on all the possible name
            try:  # check if the property name exist
                int(GIS_file[attribute_key][self.index_in_GIS])
            except:  # if it doesn't, don't do anything
                None
            else:  # if it does, assign the information to the building_zon then break = get out of the loop
                if not isnan(int(GIS_file[attribute_key][self.index_in_GIS])):
                    self.age = int(GIS_file[attribute_key][self.index_in_GIS])
                    break
        ## name ##
        for attribute_key in gis_attribute_key_dict["name"]:
            try:
                str(GIS_file[attribute_key][self.index_in_GIS])
            except:
                None
            else:
                self.name = str(GIS_file[attribute_key][self.index_in_GIS])
                break
        ## group ##
        for attribute_key in gis_attribute_key_dict["group"]:
            try:
                str(GIS_file[attribute_key][self.index_in_GIS])
            except:
                None
            else:
                self.group = str(GIS_file[attribute_key][self.index_in_GIS])
                break
        ## height ##
        for attribute_key in gis_attribute_key_dict["height"]:
            try:
                float(GIS_file[attribute_key][self.index_in_GIS])
            except:
                None
            else:
                if not isnan(float(GIS_file[attribute_key][self.index_in_GIS])):
                    self.height = float(GIS_file[attribute_key][self.index_in_GIS])
                    break
        ## elevation ##
        for attribute_key in gis_attribute_key_dict["elevation"]:
            try:
                float(GIS_file[attribute_key][self.index_in_GIS])
            except:
                None
            else:
                if not isnan(float(GIS_file[attribute_key][self.index_in_GIS])):
                    self.elevation = float(GIS_file[attribute_key][self.index_in_GIS])

                    break
        ## number of floor ##
        for attribute_key in gis_attribute_key_dict["number of floor"]:
            try:
                int(GIS_file[attribute_key][self.index_in_GIS])
            except:
                None
            else:
                if not isnan(int(GIS_file[attribute_key][self.index_in_GIS])):
                    self.num_floor = int(GIS_file[attribute_key][self.index_in_GIS])
                    break

        ## typology ##
        for attribute_key in gis_attribute_key_dict["typology"]:
            try:
                str(GIS_file[attribute_key][self.index_in_GIS])
            except:
                None
            else:
                self.typology = str(GIS_file[attribute_key][self.index_in_GIS])
                break

        # check the property of the building, correct and assign default value if needed
        self.check_and_correct_property()

    def check_and_correct_property(self):
        """ check if there is enough information about the building"""
        # no valid height and no valid number of floor
        if ((type(self.height) != int or type(self.height) != float) or (
                self.height < 3)) and (type(self.num_floor) != int or self.num_floor < 1):
            self.height = 9.
            self.num_floor = 3
            self.floor_height = 3.
        # no valid height but valid number of floor
        elif ((type(self.height) != int or type(self.height) != float) or (
                self.height < 3)) and type(self.num_floor) == int and self.num_floor > 0:  # assume 3m floor height
            self.height = 3. * self.num_floor
            self.floor_height = 3.
        # no number of floor but valid height
        elif (type(self.num_floor) != int or self.num_floor < 1) and (
                type(self.height) == int or type(self.height) == float) and self.height >= 3:
            # assume approximately 3m floor height
            self.num_floor = self.height // 3.
            self.floor_height = self.height / float(self.num_floor)
        # both height and number of floor
        elif (type(self.height) == int or type(self.height) == float) and (type(
                self.num_floor) == int and self.num_floor > 0):  # both height and number of floor
            if 5. <= self.height / float(self.num_floor) <= 2.5:  # then ok
                self.floor_height = self.height / float(self.num_floor)
            else:  # prioritize the height
                self.num_floor = self.height // 3.
                self.floor_height = self.height / float(self.num_floor)
        else:  # not the proper format
            self.height = 9.
            self.num_floor = 3
            self.floor_height = 3.

    def move(self, vector):
        """
        Move the building to a new location
        :param vector: [x,y,z]
        """
        # move the LB footprint
        self.LB_face_footprint = self.LB_face_footprint.move(Vector3D(vector[0], vector[1], 0))
        # adjust the elevation
        self.elevation = self.elevation + vector[2]
        # make it moved
        self.moved_to_origin = True

    def export_building_to_elevated_HB_room_envelop (self):
        """
        Convert the building to HB Room object showing the envelop of the building for plotting purposes
        or for context filtering
        :return: HB Room envelop
        """
        # convert the envelop of the building to a HB Room
        HB_room_envelop = LB_face_footprint_to_elevated_HB_room_envelop(LB_face_footprint=self.LB_face_footprint,
                                                                        building_id=self.id,
                                                                        height=self.height,
                                                                        elevation=self.elevation)
        return HB_room_envelop

    def to_HB_model(self, layout_from_typology=False, automatic_subdivision=True, properties_from_typology=True):
        """ Convert the building to HB model
        :param properties_from_typology: If True, the properties of the building will be assigned based on the typology
        :param layout_from_typology: If True, the layout of the building will be assigned based on the typology
        :param automatic_subdivision: If True, and if the layout is not taken from the typology, footprint of
        the building will be subdivided automatically into apartments and cores based on the typology"""
        # todo: under construction @Elie
        if layout_from_typology:
            # todo: develop this feature later on,
            #  we'll only have one Room per floor or the automatic subdivision for now
            None
            # todo: maybe have it in a separate function
            # Load and copy the layout (footprint,apartment and cores) from the typology

            # move them to the location of the building (match the center of the footprints)

            # resize the layout to the size of the building footprint

            # rotate the layout to the orientation of the building centered on the centroid
            # (use a criteria with maximum intersection between the two footprints)

            # update the new footprint of the building

            # make the HB model with the new layout (windows,HVAC,etc.)
            # todo: consider building on pillars or with unconditioned ground floor if mentioned in the typology.
            #  in the future
        else:

            if automatic_subdivision: # then divide the footprint into apartments and cores with Dragonfly
                None  # todo @Elie, not top priority
            else:  # then just create one room per floor with the actual LB_face_footprint
                None  # todo @Elie

        if properties_from_typology:  # Apply all the properties from the self.typology to the HB model
            None
        else: # Apply the default properties to the HB model from the Typology "default"
            None  # todo @Elie

        HB_model = None  # todo @Elie: remove later, just not to show an error
        return HB_model


def polygon_to_LB_footprint(polygon_obj, unit, tolerance=0.01):
    """
        Transform a Polygon object to a Ladybug footprint.
        Args:
            polygon_obj: A Polygon object.
            unit: Unit of the shp file.
        Returns:
            LB_face_footprint:A Ladybug footprint.
    """

    # Convert the exterior of the polygon to a list of points
    point_list_outline = [list(point) for point in polygon_obj.exterior.__geo_interface__['coordinates']]
    # if there is less than 3 points, the geometry is not valid, then return None
    if len(point_list_outline) < 3:
        return None
    # Reverse the list of points to have the right orientation (facing down)
    point_list_outline.reverse()
    # Scale the point list according to the unit of the shp file
    scale_point_list_according_to_unit(point_list_outline, unit)
    # Remove redundant vertices (maybe not necessary, already included in Ladybug)
    # remove_redundant_vertices(point_list_outline, tol=tolerance)

    # Convert the list of points to a list of Ladybug Point3D
    point_3d_list_outline = [Point3D(point[0], point[1], 0) for point in point_list_outline]

    # Convert the exterior of the polygon to a list of points
    # Check if the polygon has holes
    try:
        polygon_obj.interiors  # Check if the polygon has holes
    except:
        interior_holes_pt_list = None
    else:
        interior_holes_pt_list = []
        for hole in polygon_obj.interiors:
            if hole.__geo_interface__['coordinates'] != None:
                if len(hole) == 1:
                    hole = hole[0]
                list_point_hole = [list(point) for point in hole]
                # if their is less than 3 points in the geometry, then the geometry is not valid =>
                if len(list_point_hole) < 3:
                    return None
                list_point_hole.reverse()

                interior_holes_pt_list.append(list_point_hole)
        if interior_holes_pt_list == [None]:
            interior_holes_pt_list = []
        for holes in interior_holes_pt_list:
            scale_point_list_according_to_unit(holes, unit)
            # remove_redundant_vertices(holes,tol = tolerance)  #(maybe not necessary, already included in Ladybug)

        interior_holes_pt_3d_list = []
        for hole in interior_holes_pt_list:
            interior_holes_pt_3d_list.append([Point3D(point[0], point[1], 0) for point in hole])

    # Convert the list of points to a Ladybug footprint
    LB_face_footprint = Face3D(boundary=point_3d_list_outline, holes=interior_holes_pt_3d_list, enforce_right_hand=True)
    # Remove collinear vertices
    LB_face_footprint = LB_face_footprint.remove_colinear_vertices(tolerance=tolerance)

    return LB_face_footprint


def scale_point_list_according_to_unit(point_list, unit):
    """
    Scale the point list according to the unit of the shp file.
    :param point_list: list of points, a point is a list of two coordinates
    :param unit: unit of the shp file, usually degree or meter
    """
    if unit == "deg":
        factor = 111139  # conversion factor, but might be a bit different, it depends on the altitude, but the
        # deformation induced should be small if it's not on a very high mountain
        for point in point_list:
            point[0] = point[0] * factor
            point[1] = point[1] * factor
    # a priori the only units re degrees and meters. For meter not need to scale
    else:
        None


def remove_redundant_vertices(point_list, tol=0.5):
    """
    Check if the points of the footprint are too close to each other. If yes, delete one of the points.
    :param point_list: list of points, a point is a list of two coordinates
    :param tol: tolerance in meter. if the distance between 2 consecutive point is lower than this value, one of the point is deleted
    """
    # Number of points in the point list
    number_of_points = len(point_list)
    # Initialize the index
    i = 0
    while i <= number_of_points - 1:  # go over all points
        if distance(point_list[i], point_list[i + 1]) < tol:
            point_list.pop(i + 1)
        else:
            i += 1
        if i >= len(
                point_list) - 1:  # if we reach the end of the footprint, considering some points were removed, the loop ends
            break
    if distance(point_list[0],
                point_list[-1]) < tol:  # check also with the first and last points in the footprint
        point_list.pop(-1)


def distance(pt_1, pt_2):
    """
    :param pt_1: list for the point 1
    :param pt_2: list for the point 2
    :return: distance between the 2 points
    """

    return sqrt((pt_1[0] - pt_2[0]) ** 2 + (pt_1[1] - pt_2[1]) ** 2)


def add_additional_attribute_keys_to_dict(attribute_key_dict, additional_attribute_key_dict):
    """
    Add additional attribute keys to the attribute key dictionary.
    :param attribute_key_dict: dictionary of attribute keys
    :param additional_attribute_key_dict: dictionary of additional attribute keys
    :return: dictionary of attribute keys
    """
    if additional_attribute_key_dict is None:
        # if there is no additional attribute key dictionary, return the default attribute key dictionary
        return attribute_key_dict
    else:
        concatenated_attribute_key_dict = {}  # initialize the concatenated attribute key dictionary
        for key in additional_attribute_key_dict.keys():
            # sum the list = concatenating the attribute keys
            concatenated_attribute_key_dict[key] = attribute_key_dict[key] + additional_attribute_key_dict[key]
        return concatenated_attribute_key_dict
