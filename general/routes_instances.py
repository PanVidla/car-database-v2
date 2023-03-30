from flask import render_template, redirect, url_for

from general import cardb
from general.forms_instance import SelectGameForm
from general.models.instance import Instance


# Overview instances
@cardb.route("/instances", methods=['GET'])
@cardb.route("/instances/all", methods=['GET'])
def overview_instances():

    instances = Instance.query.order_by(Instance.id).all()

    return render_template("instances_overview.html",
                           title="Instances",
                           heading="All instances",
                           instances=instances)


# Add instance
@cardb.route("/instances/add-instance", methods=['GET', 'POST'])
def add_instance():

    form = SelectGameForm()

    if form.validate_on_submit():

        game_name_full = form.game_name_full.data
        car_id = form.car_id.data

        if game_name_full == "Crazy Taxi":
            return redirect(url_for("crazy_taxi.crazy_taxi_1.add_instance", id=car_id))

    return render_template("instances_form.html",
                           title="Add instance",
                           heading="Add instance",
                           form=form)
