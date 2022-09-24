#!/bin/python3
import sqlite3, json, os, requests, urllib, pytz
from datetime import datetime
import pandas as pd

from .map import MapHandler


##########


def init_db(here: os.path):
    """
    Creates local DB instance if it doesn't exist already
    """

    print("\n** Initializing DB **\n")

    with sqlite3.connect("./app/nyc.db") as connection:
        with open(os.path.join(here, "schema.sql")) as f:
            connection.executescript(f.read())




def read_db():
    """
    Quick wrapper to read DB as a Pandas DataFrame
    """

    with sqlite3.connect("./app/nyc.db") as connection:
        df = pd.read_sql_query(
            sql="select * from nyc;",
            con=connection
        )

    return df



def push_to_db(address: str, lat: float, lon: float, 
               label: str = None, submitted_by: str = None, 
               comments: str = None, venue_type: str = None) -> None:
    """
    Pushes input from the HTML form to the local DB
    """

    with sqlite3.connect("./app/nyc.db") as connection:
        cursor = connection.cursor()

        cursor.execute("""
        INSERT INTO nyc (address,latitude,longitude,label,venue_type,submitted_by,comments)
        VALUES (?,?,?,?,?,?,?)
        """, (address, lat, lon, label, venue_type, submitted_by, comments))



def validate_input(address: str, label_: str = None, 
                   submitted_by: str = None, comments: str = None,
                   venue_type: str = None) -> dict:
    """
    Cleans up user input submitted via HTML form
    """

    # Get coordinates
    coords = get_coordinates(address=address)
    lon, lat = coords[0], coords[1]

    # Clean up text
    if label_ is None:
        label_ = address

    else:
        label_ = label_.title().strip()

    return {
        "address": address.upper(),
        "label": label_.upper(),
        "latitude": lat,
        "longitude": lon,
        "submitted_by": submitted_by.upper(),
        "comments": comments.upper(),
        "venue_type": venue_type.upper()
    }



def handle_request(address: str, label_: str = None, 
                   submitted_by: str = None, comments: str = None,
                   venue_type: str = None):
    """
    Wraps two of the functions above to validate incoming request
    and push to local DB
    """

    content_store = validate_input(
        address=address, label_=label_, 
        submitted_by=submitted_by,
        comments=comments, venue_type=venue_type
    )

    push_to_db(
        address=content_store["address"],
        lat=content_store["latitude"],
        lon=content_store["longitude"],
        label=content_store["label"],
        submitted_by=content_store["submitted_by"],
        comments=content_store["comments"],
        venue_type=content_store["venue_type"]
    )

    handler = MapHandler()
    handler.build_map()



def get_coordinates(address: str) -> tuple:
    """
    Leverages OpenStreetMap to convert address string
    to longitude and latitude coordinates
    """
    
    # Call to OpenStreetMap
    call = 'https://nominatim.openstreetmap.org/search/' + \
            urllib.parse.quote(address) + '?format=json'

    # Make request + pull JSON information
    r = requests.get(call).json()

    # Return latitude and longitude
    try:
        return (r[0]['lat'], r[0]['lon'])
    except Exception as e:
        raise e
