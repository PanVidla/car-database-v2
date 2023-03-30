from flask import render_template, redirect, url_for, flash

from general import cardb, database
from general.forms_instance import SelectGameForm, InstanceTypeAddForm, InstanceTypeEditForm
from general.models.instance import Instance, InstanceType


# Overview instances
@cardb.route("/instances", methods=['GET'])
@cardb.route("/instances/all", methods=['GET'])
def overview_instances():

    instances = Instance.query.order_by(Instance.id).all()

    return render_template("instances_overview.html",
                           title="Instances",
                           heading="All instances",
                           instances=instances,
                           viewing="instances")


# Overview instance types
@cardb.route("/instances/types", methods=['GET'])
@cardb.route("/instances/types/all", methods=['GET'])
def overview_instance_types():

    instance_types = InstanceType.query.order_by(InstanceType.name_full.asc()).all()

    return render_template("instances_overview_instance_types.html",
                           title="Instance types",
                           heading="All instance types",
                           instance_types=instance_types,
                           viewing="instance_types")


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


# Add instance type
@cardb.route("/instances/types/add-type", methods=['GET', 'POST'])
def add_instance_type():

    form = InstanceTypeAddForm()

    if form.validate_on_submit():

        new_instance_type = InstanceType()
        form.populate_obj(new_instance_type)

        try:
            database.session.add(new_instance_type)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding the new instance type to the database.", "danger")
            return redirect(url_for("add_instance_type"))

        flash("The instance type \"{}\" has been successfully added to the database.".format(new_instance_type.name_full),
              "success")
        return redirect(url_for("overview_instance_types"))

    return render_template("instances_form_instance_type.html",
                           title="Add instance type",
                           heading="Add instance type",
                           form=form,
                           viewing="instance_types")


# Edit instance type
@cardb.route("/instances/types/edit-type/<id>", methods=['GET', 'POST'])
def edit_instance_type(id):

    instance_type = InstanceType.query.get(id)
    form = InstanceTypeEditForm(obj=instance_type)

    if form.validate_on_submit():

        form.populate_obj(instance_type)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the instance type \"{}\".".format(instance_type.name_full), "danger")
            return redirect(url_for("edit_instance_type", id=instance_type.id))

        flash("The instance type \"{}\" has been successfully edited.".format(instance_type.name_full), "success")
        return redirect(url_for("detail_instance_type", id=instance_type.id))

    return render_template("instances_form_instance_type.html",
                           title="Edit instance type",
                           heading="Edit instance type",
                           form=form,
                           viewing="instance_types")


# Delete instance type
@cardb.route("/instances/types/delete-type/<id>", methods=['GET', 'POST'])
def delete_instance_type(id):

    instance_type = InstanceType.query.get(id)

    try:
        database.session.delete(instance_type)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the \"{}\" instance type.".format(instance_type.name_full), "danger")
        return redirect(url_for("detail_instance_type", id=instance_type.id))

    flash("The instance type \"{}\" has been successfully deleted.".format(instance_type.name_full), "success")
    return redirect(url_for("overview_instance_types"))


# Instance detail
@cardb.route("/instances/types/detail/<id>", methods=['GET', 'POST'])
def detail_instance_type(id):

    instance_type = InstanceType.query.get(id)

    return render_template("instances_detail_instance_type.html",
                           title="{}".format(instance_type.name_short),
                           heading="{}".format(instance_type.name_full),
                           instance_type=instance_type,
                           viewing="instance_types")
