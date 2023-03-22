from flask import render_template

from general import cardb
from general.models.car import Car
from general.models.game import Game
from general.models.instance import Instance
from general.models.misc import Company
from general.strings import *


# Overviews
@cardb.route("/", methods=['GET'])
@cardb.route("/cars", methods=['GET'])
def overview_cars():

    cars = Car.query.order_by(Car.manufacturers_display.asc(), Car.year.asc(), Car.model.asc()).all()

    return render_template("overview_cars.html",
                           title=title_cars,
                           overview_heading=overview_heading_cars,
                           cars=cars)


@cardb.route("/instances", methods=['GET'])
def overview_instances():

    instances = Instance.query.order_by(Instance.id).all()

    return render_template("overview_instances.html",
                           title=title_instances,
                           overview_heading=overview_heading_instances,
                           instances=instances)
