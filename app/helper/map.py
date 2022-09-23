#!/bin/python3
from .db import read_db
import urllib, requests, os
import folium

##########

class MapHandler:
    """
    This class contains automations to populate and update
    the WiFi map relevant to this project
    """

    def __init__(self, output_path: os.path = "./app/templates/hotspots.html"):
        self.coords = [40.7128, -74.006]
        self.data_store = read_db()
        self.output_path = output_path


    def build_map(self):
        """
        Updates and writes an HTML map to the templates folder
        """

        # Instantiate map
        nyc_map = folium.Map(
            location=self.coords,
            zoom_start=12
        )

        # Loop through and drop pins
        for ix, label in enumerate(self.data_store["label"]):
            folium.Marker(
                location=[
                    self.data_store["latitude"][ix],
                    self.data_store["longitude"][ix]
                ],
                popup=label
            ).add_to(nyc_map)


        # Write to template directory
        nyc_map.save(outfile=self.output_path)