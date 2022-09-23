#!/bin/python3
from re import sub
from flask import render_template, request, Flask
from .helper.db import (init_db, read_db, 
                        validate_input, push_to_db)
from .helper.map import MapHandler
import os, pathlib

##########

app = Flask(__name__)
app_path = pathlib.Path(__file__).parent

if not os.path.exists(os.path.join(app_path, "nyc.db")):
    init_db(here=app_path)

print("\n** App Running **\n")

handler = MapHandler()
handler.build_map()

##########

@app.route("/", methods=["GET", "POST"])
def index():

    return render_template("index.html")



@app.route("/add_hotspot", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        venue_ = request.form["venue_name"]
        address_ = request.form["street_address"]
        city_ = request.form["city"]
        venue_type_ = request.form["venue_type"]
        submitted_by = request.form["submitted_by"]
        comments = request.form["comments"]

        address_string = f"{address_}, {city_}, NY"

        validate_input(
            address=address_string,
            label_=venue_,
            submitted_by=submitted_by,
            comments=comments,
            push_directly=True
        )

    return render_template("add.html")


@app.route("/view_hotpots", methods=["GET", "POST"])
def view():

    data = read_db()

    if len(data) == 0:
        data = None

    return render_template("view.html", data=data)



@app.route("/hotspots", methods=["GET", "POST"])
def hotspots():
    return render_template("hotspots.html")



# --- Run
if __name__ == "__main__":
    app.run(debug=True)
