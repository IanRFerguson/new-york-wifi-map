#!/bin/python3
import os, pathlib
from time import sleep
from flask import (render_template, request, 
                   Flask, redirect, send_file,
                   url_for, flash, after_this_request)

from .helper.map import MapHandler
from .helper.db import (handle_request, init_db, read_db)


##########


app = Flask(__name__)
app_path = pathlib.Path(__file__).parent

if not os.path.exists(os.path.join(app_path, "nyc.db")):
    init_db(here=app_path)

print("\n** App Running **\n")


##########


@app.route("/", methods=["GET", "POST"])
def index():

    if not os.path.exists("./app/templates/hotspots.html"):
        dummy = open("./app/templates/hotspots.html", "w")
        dummy.close()

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

        try:
            handle_request(
                address=address_string,
                label_=venue_,
                submitted_by=submitted_by,
                comments=comments,
                venue_type=venue_type_
            )

        except Exception as e:
            flash(e)
            return redirect(url_for('index'))

        return render_template(
            "success.html",
            address=address_string.upper()
        )

    return render_template("add.html")



@app.route("/view_hotpots", methods=["GET", "POST"])
def view():
    data = read_db()

    return render_template("view.html", data=data.values.tolist())



@app.route("/hotspots", methods=["GET", "POST"])
def hotspots():
    return render_template("hotspots.html")



@app.route("/download_csv", methods=["GET", "POST"])
def download_csv():
    data = read_db()

    output_path = os.path.join("./.temp_cache")
    pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)

    data.to_csv(
        os.path.join(output_path, "NYC_WIFI_HOTSPOTS.csv"),
        index=False
    )


    @after_this_request
    def remove_output(response_):
        os.remove(
            os.path.join(output_path, "NYC_WIFI_HOTSPOTS.csv")
        )


    return send_file(
        os.path.join(output_path, "NYC_WIFI_HOTSPOTS.csv"),
        as_attachment=True
    )


##########


if __name__ == "__main__":
    app.run(debug=True)
