from flask import render_template

from general import cardb
from general.models.car import Car


@cardb.route("/", methods=['GET'])
@cardb.route("/cars", methods=['GET'])
def overview_cars():

    cars = Car.query.order_by(Car.manufacturers_display.asc(), Car.year.asc(), Car.model.asc()).all()

    return render_template("cars_overview.html",
                           title="All cars",
                           heading="All cars",
                           cars=cars,
                           viewing="cars")
