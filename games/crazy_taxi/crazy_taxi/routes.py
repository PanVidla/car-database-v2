from flask import render_template, redirect, url_for

from games.crazy_taxi.crazy_taxi import crazy_taxi_1
from games.crazy_taxi.crazy_taxi.models.instance import InstanceCT
from general.models.car import Car
from general.models.instance import Instance


@crazy_taxi_1.route("/instances/overview", methods=['GET'])
@crazy_taxi_1.route("/instances/overview/all", methods=['GET'])
def overview_instances():

    instances = InstanceCT.query. \
        filter(InstanceCT.is_deleted != True) \
        .order_by(InstanceCT.name_full.desc()).all()

    return render_template("ct1_instances_overview.html",
                           title="Crazy Taxi",
                           heading="All Crazy Taxi instances",
                           instances=instances)


@crazy_taxi_1.route("/instances/add-instance", methods=['GET', 'POST'])
def add_instance():

    return redirect(url_for("crazy_taxi.crazy_taxi_1.overview_instances"))


# Instance detail
@crazy_taxi_1.route("/instances/detail/<id>", methods=['GET', 'POST'])
def detail_instance(id):

    instance = Instance.query.get(id)

    return render_template("instances_detail.html",
                           title="{}".format(instance.name_nickname),
                           heading="{}".format(instance.name_full),
                           instance=instance,
                           viewing="instances")
