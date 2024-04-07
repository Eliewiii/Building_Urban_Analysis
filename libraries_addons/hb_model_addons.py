"""
Additional functions to apply on honeybee model
"""

import logging

# Dragonfly
from dragonfly.building import Building
# Honeybee
from honeybee.room import Room
from honeybee_energy.lib.constructionsets import construction_set_by_identifier
from honeybee_energy.lib.programtypes import program_type_by_identifier
from ladybug_geometry.geometry3d.pointvector import Vector3D



dev_logger = logging.getLogger("dev")
user_logger = logging.getLogger("user")

class HbAddons:

    @staticmethod
    def elevation_and_height_from_HB_model(HB_model):
        """
        Extract the elevation of the building from the hb model
        :param HB_model: honeybee Model
        :return: elevation, height
        """
        elevation = min([room.min.z for room in HB_model.rooms])
        height = max([room.max.z for room in HB_model.rooms]) - elevation
        return elevation, height

    @staticmethod
    def make_LB_face_footprint_from_HB_model(HB_model,elevation):
        """
        Extract the footprint of the building from the hb model
        :param HB_model:
        :return:
        """
        # todo @Elie : finish the function (and check if it works)
        # turn into dragonfly building
        dragonfly_building = Building.from_honeybee(HB_model)
        # get the footprint
        lb_footprint_list = dragonfly_building.footprint()
        if len(lb_footprint_list) > 1:
            user_logger.warning("The HB model has more than one footprint, an oriented bounded box will be used to represent the footprint")
            dev_logger.warning("The HB model has more than one footprint, an oriented bounded box will be used to represent the footprint")
            # todo : @Elie : convert the function that makes the oriented bounded box from LB

        elif len(lb_footprint_list) == 0:
            user_logger.warning("The HB model has no footprint")
            dev_logger.warning("The HB model has no footprint")
            # todo : @Elie : convert the function that makes the oriented bounded box from LB
        else:
            # Move the footprint to elevation 0
            lb_footprint = lb_footprint_list[0].move(Vector3D(0., 0., - elevation))
            return lb_footprint


    @staticmethod
    def get_LB_faces_with_ground_bc_from_HB_model(HB_model):
        """
        Extract LB geometry faces 3D that have ground boundary condition from the HB model
        todo: not relevant if the building is on pillar...
        :param HB_model:
        :return:
        """
        # Init the list of LB geometry faces 3D that have ground boundary condition
        LB_face_ground_bc_list = []
        # Loop through the rooms of the HB model
        for room in HB_model.rooms:
            for face in room.faces:
                if face.boundary_condition.boundary_condition == "Ground":
                    LB_face_ground_bc_list.append(face.geometry)

        return LB_face_ground_bc_list


    # todo: @Elie : from mow on not

    @staticmethod
    def LB_footprint_to_HB_model(lb_face_footprint, height, elevation, typology_layout=False,core_to_floor_area_ratio=0.15):
        """
        Create a honeybee model with extruded footprints of the building
        :param lb_face_footprint:
        :param height:
        :param elevation:
        :param typology_layout: if True, it will use the layout of the building typology to build the building
        :param core_to_floor_area_ratio:
        :return:
        """
        # todo: @Elie : finish the function (and check if it works)
        if typology_layout:
            None
        if not typology_layout:  # Automatic subdivision of the building on cores an apartments
            HB_model = Room.from_footprint("building", lb_face_footprint, height, elevation)
        return None

    @staticmethod
    def HB_model_apply_constructionset(HB_model, constructions_set_id):
        """
        Assign construction set and program type to each room of the model
        """
        # todo: @Elie : finish the function (and check if it works)
        for room in HB_model.rooms:
            ## assign construction set
            room.properties.energy.construction_set = construction_set_by_identifier(constructions_set_id)
            ## assign program

    @staticmethod
    def HB_model_apply_programs(HB_model, program_type_apartment_id, program_type_core_id):
        """
        Assign construction set and program type to each room of the model
        """
        # todo: @Elie : finish the function (and check if it works)
        for room in HB_model.rooms:
            ## assign program
            if room.properties.energy.is_conditioned:
                # if conditioned => apartment
                room.properties.energy.program_type = program_type_by_identifier(program_type_apartment_id)
            else:
                room.properties.energy.program_type = program_type_by_identifier(program_type_core_id)

    @staticmethod
    def HB_model_window_by_facade_ratio_per_direction(HB_model, ratio_per_direction, min_length_wall_for_window=2.,only_conditioned=True):
        """
        Assign window to each room of the model
        """
        # todo: @Elie : finish the function (and check if it works)
        for room in HB_model.rooms:
            if room.properties.energy.is_conditioned or only_conditioned==False:
                for face in room.faces:
                # get the length of the surface => projection of the face on the XY plane
                    pt_a , pt_b = room.min, room.max # extreme points of the
