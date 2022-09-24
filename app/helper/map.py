#!/bin/python3
import folium, os, sqlite3
import pandas as pd


##########


class MapHandler:
    """
    This class contains automations to populate and update
    the WiFi map relevant to this project
    """

    def __init__(self, output_path: os.path = "./app/templates/hotspots.html"):
        self.coords = [40.7128, -74.006]
        self.data_store = self.read_db()
        self.output_path = output_path



    def read_db(self):
        """
        Reads in all values from local DB
        """

        with sqlite3.connect("./app/nyc.db") as connection:
            df = pd.read_sql_query(
                sql="select * from nyc;",
                con=connection
            )

        return df



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

            full_label = f"<b>{label}</b><br>{self.data_store['address'][ix]}".title()
            venue_type = self.data_store["venue_type"][ix]

            if venue_type == "COFFEE":
                color="blue"

            elif venue_type == "HOTEL":
                color="red"

            else:
                color="green"

            folium.Marker(
                location=[
                    self.data_store["longitude"][ix],
                    self.data_store["latitude"][ix]
                ],
                popup=full_label.replace("Ny", "NY"),
                icon=folium.Icon(color=color)
            ).add_to(nyc_map)


        # Write to template directory
        nyc_map.save(outfile=self.output_path)