import logging

user_logger = logging.getLogger("user")  
dev_logger = logging.getLogger("dev")  


class SolarOrPanelSimulation:

    @staticmethod
    def solar_radiation_simulation(urban_canopy_object, path_simulation_folder, path_weather_file, list_id,
                                   grid_size, offset_dist, on_roof, on_facades):
        """
        Run solar radiation simulation
        """

        urban_canopy_object.radiation_simulation_urban_canopy(path_simulation_folder, path_weather_file,
                                                              list_id, grid_size, offset_dist, on_roof,
                                                              on_facades)
        user_logger.info("The solar radiation simulation was run on the buildings of the urban canopy")
        dev_logger.info("The solar radiation simulation was run on the buildings of the urban canopy")


    @staticmethod
    def panel_simulation(urban_canopy_object, path_simulation_folder, path_pv_tech_dictionary_json,
                         id_pv_tech_roof, id_pv_tech_facades,
                         minimum_ratio_energy_harvested_on_primary_energy,
                         performance_ratio, study_duration_in_years, replacement_scenario, **kwargs):
        """
        Run panel simulation
        """

        urban_canopy_object.run_panel_simulation(path_simulation_folder, path_pv_tech_dictionary_json,
                                                 id_pv_tech_roof, id_pv_tech_facades,
                                                 minimum_ratio_energy_harvested_on_primary_energy,
                                                 performance_ratio, study_duration_in_years,
                                                 replacement_scenario, **kwargs)
        user_logger.info("The panel simulation was run on the buildings of the urban canopy")
        dev_logger.info("The panel simulation was run on the buildings of the urban canopy")



