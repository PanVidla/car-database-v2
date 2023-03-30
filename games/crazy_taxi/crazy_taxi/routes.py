from flask import render_template

from games.crazy_taxi.crazy_taxi import crazy_taxi_1
from games.crazy_taxi.crazy_taxi.models.instance import InstanceCT
from general.forms_instance import InstanceForm
from general.models.car import Car


@crazy_taxi_1.route("/instances/overview", methods=['GET'])
@crazy_taxi_1.route("/instances/overview/all", methods=['GET'])
def overview_instances():

    instances = InstanceCT.query. \
        filter(InstanceCT.is_deleted != True) \
        .order_by(InstanceCT.name_full.asc()).all()

    return render_template("ct1_instances_overview.html",
                           title="Crazy Taxi",
                           heading="All Crazy Taxi instances",
                           instances=instances)


@crazy_taxi_1.route("/instances/add-instance/<id>", methods=['GET', 'POST'])
def add_instance(id):

    car = Car.query.get(id)
    form = InstanceForm(name_full=car.name_display)



