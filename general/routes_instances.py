from datetime import datetime

from flask import render_template, redirect, url_for, flash

from general import cardb, database
from general.forms_cars import Car21Form, Car3Form, Car4Form, Car5Form, Car6Form, Car7Form, Car8Form
from general.forms_instance import SelectGameForm, InstanceTypeAddForm, InstanceTypeEditForm, SpecializationAddForm, \
    SpecializationEditForm, InstanceGeneralForm
from general.helpers import create_instance_based_on_game, return_redirect_to_details_based_on_game
from general.models.car import Car
from general.models.game import Game
from general.models.instance import Instance, InstanceType, InstanceSpecialization, InstanceEngine, InstanceAssist


# Overview instances
@cardb.route("/instances", methods=['GET'])
@cardb.route("/instances/all", methods=['GET'])
def overview_instances():

    instances = Instance.query.\
        filter(Instance.is_deleted != True).\
        order_by(Instance.id.desc()).all()

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


# Overview instance specialization
@cardb.route("/instances/specialization", methods=['GET'])
@cardb.route("/instances/specialization/all", methods=['GET'])
def overview_specialization():

    specialization = InstanceSpecialization.query.order_by(InstanceSpecialization.name_full.asc()).all()

    return render_template("instances_overview_specialization.html",
                           title="Instance specialization",
                           heading="All instance specialization",
                           specializations=specialization,
                           viewing="specialization")


# Add instance (game & car)
@cardb.route("/instances/add-instance", methods=['GET', 'POST'])
def add_instance_game_car():

    form = SelectGameForm()

    if form.validate_on_submit():

        game_id = form.game_name_full.data
        car_id = form.car_id.data

        return redirect(url_for("add_instance_general", car_id=car_id, game_id=game_id))

    return render_template("instances_form_1_game_select.html",
                           title="Add instance",
                           heading="Add instance",
                           form=form,
                           viewing="instances")


# Add instance (general)
@cardb.route("/instances/add-instance/<car_id>/<game_id>/general", methods=['GET', 'POST'])
def add_instance_general(car_id, game_id):

    car = Car.query.get(car_id)
    game = Game.query.get(game_id)
    form = InstanceGeneralForm(obj=car,
                               name_full=car.name_display)

    if form.validate_on_submit():

        new_instance = create_instance_based_on_game(game)
        new_instance.set_type_and_specialization(form)
        form.populate_obj(new_instance)

        new_instance.car_id = car.id
        new_instance.game_id = game.id

        try:
            database.session.add(new_instance)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding the new instance to the database.", "danger")
            return redirect(url_for("add_instance_general"))

        flash("The {} has been successfully added to the database.".format(new_instance.name_full), "success")

        car.refresh_no_of_instances()
        database.session.commit()

        return redirect(url_for("add_instance_engine", instance_id=new_instance.id))

    return render_template("instances_form_2_general.html",
                           title="Add instance",
                           heading="Add instance",
                           form=form,
                           viewing="instances")


# Add instance (general)
@cardb.route("/instances/add-instance/<instance_id>/engine", methods=['GET', 'POST'])
def add_instance_engine(instance_id):

    instance = Instance.query.get(instance_id)
    car = Car.query.get(instance.car_id)

    # Get engines
    engines_ids = []
    for engine in car.get_engines():
        engines_ids.append(engine.id)

    form = Car21Form(engines=engines_ids)

    if form.validate_on_submit():

        instance.set_engines(form.engines.data)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem assigning engine(s) to the {}.".format(instance.name_full), "danger")
            return redirect(url_for("add_instance_engine"))

        flash("The engines have been successfully assigned to the {}.".format(instance.name_full), "success")

        return redirect(url_for("add_instance_forced_induction", instance_id=instance.id))

    return render_template("instances_form_3_engine.html",
                           title="Add instance",
                           heading="Add instance",
                           form=form,
                           viewing="instances")


# Add instance (forced induction)
@cardb.route("/instances/add-instance/<instance_id>/forced-induction", methods=['GET', 'POST'])
def add_instance_forced_induction(instance_id):

    instance = Instance.query.get(instance_id)
    car = Car.query.get(instance.car_id)

    form = Car3Form(additional_forced_induction_id=car.additional_forced_induction_id)

    if form.validate_on_submit():

        instance.set_forced_induction(form.additional_forced_induction_id.data)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem assigning forced induction to the {}.".format(instance.name_full), "danger")
            return redirect(url_for("add_instance_forced_induction"))

        flash("Forced induction has been successfully assigned to the {}.".format(instance.name_full), "success")

        return redirect(url_for("add_instance_power_values", instance_id=instance.id))

    return render_template("instances_form_4_forced_induction.html",
                           title="Add instance",
                           heading="Add instance",
                           form=form,
                           viewing="instances")


# Add instance (power values)
@cardb.route("/instances/add-instance/<instance_id>/power-values", methods=['GET', 'POST'])
def add_instance_power_values(instance_id):

    instance = Instance.query.get(instance_id)
    car = Car.query.get(instance.car_id)

    form = Car4Form(obj=car)

    if form.validate_on_submit():

        form.populate_obj(instance)
        instance.datetime_edited = datetime.utcnow()

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem assigning power values to the {}.".format(instance.name_full), "danger")
            return redirect(url_for("add_instance_power_values"))

        flash("Power values have been successfully assigned to the {}.".format(instance.name_full), "success")

        return redirect(url_for("add_instance_transmission", instance_id=instance.id))

    return render_template("instances_form_5_power_values.html",
                           title="Add instance",
                           heading="Add instance",
                           form=form,
                           viewing="instances")


# Add instance (transmission)
@cardb.route("/instances/add-instance/<instance_id>/transmission", methods=['GET', 'POST'])
def add_instance_transmission(instance_id):

    instance = Instance.query.get(instance_id)
    car = Car.query.get(instance.car_id)

    form = Car5Form(obj=car)

    if form.validate_on_submit():

        form.populate_obj(instance)
        instance.set_transmission(form)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem assigning transmission to the {}.".format(instance.name_full), "danger")
            return redirect(url_for("add_instance_transmission"))

        flash("Transmission has been successfully assigned to the {}.".format(instance.name_full), "success")

        return redirect(url_for("add_instance_platform", instance_id=instance.id))

    return render_template("instances_form_6_transmission.html",
                           title="Add instance",
                           heading="Add instance",
                           form=form,
                           viewing="instances")


# Add instance (platform)
@cardb.route("/instances/add-instance/<instance_id>/platform", methods=['GET', 'POST'])
def add_instance_platform(instance_id):

    instance = Instance.query.get(instance_id)
    car = Car.query.get(instance.car_id)

    form = Car6Form(obj=car)

    if form.validate_on_submit():

        form.populate_obj(instance)
        instance.set_suspension(form)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem setting Platform for the {}.".format(instance.name_full), "danger")
            return redirect(url_for("add_instance_platform"))

        flash("Platform has been successfully set for the {}.".format(instance.name_full), "success")

        return redirect(url_for("add_instance_performance", instance_id=instance.id))

    return render_template("instances_form_7_platform.html",
                           title="Add instance",
                           heading="Add instance",
                           form=form,
                           viewing="instances")


# Add instance (performance)
@cardb.route("/instances/add-instance/<instance_id>/performance", methods=['GET', 'POST'])
def add_instance_performance(instance_id):

    instance = Instance.query.get(instance_id)
    car = Car.query.get(instance.car_id)

    form = Car7Form(obj=car)

    if form.validate_on_submit():

        form.populate_obj(instance)
        instance.set_power_to_weight_ratio()

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem setting performance for the {}.".format(instance.name_full), "danger")
            return redirect(url_for("add_instance_performance"))

        flash("Performance has been successfully set for the {}.".format(instance.name_full), "success")

        return redirect(url_for("add_instance_assists", instance_id=instance.id))

    return render_template("instances_form_8_performance.html",
                           title="Add instance",
                           heading="Add instance",
                           form=form,
                           viewing="instances")


# Add instance (assists)
@cardb.route("/instances/add-instance/<instance_id>/assists", methods=['GET', 'POST'])
def add_instance_assists(instance_id):

    instance = Instance.query.get(instance_id)
    car = Car.query.get(instance.car_id)

    # Get assists
    assists_ids = car.get_assists()

    form = Car8Form(assists=assists_ids)

    if form.validate_on_submit():

        instance.set_assists(form.assists_select.data)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem setting assists for the {}.".format(instance.name_full), "danger")
            return redirect(url_for("add_instance_assists"))

        flash("Assists have been successfully set for the {}.".format(instance.name_full), "success")

        return redirect(url_for("add_instance_game_specific", instance_id=instance.id))

    return render_template("instances_form_9_assists.html",
                           title="Add instance",
                           heading="Add instance",
                           form=form,
                           viewing="instances")


# Add instance (game-specific)
@cardb.route("/instances/add-instance/<instance_id>/game-specific", methods=['GET', 'POST'])
def add_instance_game_specific(instance_id):

    instance = Instance.query.get(instance_id)

    if instance.game.name_full == "Crazy Taxi":
        return redirect(url_for("crazy_taxi.crazy_taxi_1.add_instance"))


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


# Add specialization
@cardb.route("/instances/specialization/add-specialization", methods=['GET', 'POST'])
def add_specialization():

    form = SpecializationAddForm()

    if form.validate_on_submit():

        new_specialization = InstanceSpecialization()
        form.populate_obj(new_specialization)

        try:
            database.session.add(new_specialization)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding the new specialization to the database.", "danger")
            return redirect(url_for("add_specialization"))

        flash("The specialization \"{}\" has been successfully added to the database.".format(
            new_specialization.name_full), "success")
        return redirect(url_for("overview_specialization"))

    return render_template("instances_form_specialization.html",
                           title="Add specialization",
                           heading="Add specialization",
                           form=form,
                           viewing="specialization")


# Edit instance (general)
@cardb.route("/instances/edit-instance/<id>/general", methods=['GET', 'POST'])
def edit_instance_general(id):

    instance = Instance.query.get(id)

    form = InstanceGeneralForm(obj=instance)

    if form.validate_on_submit():

        form.populate_obj(instance)
        instance.set_type_and_specialization(form)
        instance.datetime_edited = datetime.utcnow()

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {}.".format(instance.name_full), "danger")
            return redirect(url_for("edit_instance_general", id=instance.id))

        flash("The {}  has been successfully edited.".format(instance.name_full), "success")
        return redirect(url_for("detail_instance", id=instance.id))

    return render_template("instances_form_2_general.html",
                           title="Edit instance",
                           heading="Edit general information",
                           form=form,
                           viewing="instances",
                           editing=True)


# Edit instance (engine)
@cardb.route("/instances/edit-instance/<id>/engine", methods=['GET', 'POST'])
def edit_instance_engine(id):

    instance = Instance.query.get(id)

    # Get engine(s) for the multiple select form
    engines = InstanceEngine.query.filter(InstanceEngine.instance_id == instance.id).all()
    engine_ids = []

    for engine in engines:
        engine_ids += str(engine.engine_id)

    form = Car21Form(engines=engine_ids)

    if form.validate_on_submit():

        instance.set_engines(form.engines.data)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {}.".format(instance.name_full), "danger")
            return redirect(url_for("edit_instance_engine", id=instance.id))

        flash("The {}  has been successfully edited.".format(instance.name_full), "success")
        return redirect(url_for("detail_instance", id=instance.id))

    return render_template("instances_form_3_engine.html",
                           title="Edit instance",
                           heading="Edit engine(s)",
                           form=form,
                           viewing="instances",
                           editing=True)


# Edit instance (forced induction)
@cardb.route("/instances/edit-instance/<id>/forced-induction", methods=['GET', 'POST'])
def edit_instance_forced_induction(id):

    instance = Instance.query.get(id)

    form = Car3Form(obj=instance)

    if form.validate_on_submit():

        instance.set_forced_induction(form.additional_forced_induction_id.data)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {}.".format(instance.name_full), "danger")
            return redirect(url_for("edit_instance_forced_induction", id=instance.id))

        flash("The {} has been successfully edited.".format(instance.name_full), "success")
        return redirect(url_for("detail_instance", id=instance.id))

    return render_template("instances_form_4_forced_induction.html",
                           title="Edit instance",
                           heading="Edit forced induction",
                           form=form,
                           viewing="instances",
                           editing=True)


# Edit instance (power values)
@cardb.route("/instances/edit-instance/<id>/power-values", methods=['GET', 'POST'])
def edit_instance_power_values(id):

    instance = Instance.query.get(id)

    form = Car4Form(obj=instance)

    if form.validate_on_submit():

        form.populate_obj(instance)
        instance.set_power_to_weight_ratio()

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {}.".format(instance.name_full), "danger")
            return redirect(url_for("edit_instance_power_values", id=instance.id))

        flash("The {} has been successfully edited.".format(instance.name_full), "success")
        return redirect(url_for("detail_instance", id=instance.id))

    return render_template("instances_form_5_power_values.html",
                           title="Edit instance",
                           heading="Edit power values",
                           form=form,
                           viewing="instances",
                           editing=True)


# Edit instance (transmission)
@cardb.route("/instances/edit-instance/<id>/transmission", methods=['GET', 'POST'])
def edit_instance_transmission(id):

    instance = Instance.query.get(id)

    form = Car5Form(obj=instance)

    if form.validate_on_submit():

        form.populate_obj(instance)
        instance.set_transmission(form)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {}.".format(instance.name_full), "danger")
            return redirect(url_for("edit_instance_transmission", id=instance.id))

        flash("The {} has been successfully edited.".format(instance.name_full), "success")
        return redirect(url_for("detail_instance", id=instance.id))

    return render_template("instances_form_6_transmission.html",
                           title="Edit instance",
                           heading="Edit transmission",
                           form=form,
                           viewing="instances",
                           editing=True)


# Edit instance (platform)
@cardb.route("/cars/edit-instance/<id>/platform", methods=['GET', 'POST'])
def edit_instance_platform(id):

    instance = Instance.query.get(id)

    form = Car6Form(obj=instance)

    if form.validate_on_submit():

        form.populate_obj(instance)
        instance.set_power_to_weight_ratio()
        instance.set_suspension(form)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {}.".format(instance.name_full), "danger")
            return redirect(url_for("edit_instance_platform", id=instance.id))

        flash("The {} has been successfully edited.".format(instance.name_full), "success")
        return redirect(url_for("detail_instance", id=instance.id))

    return render_template("instances_form_7_platform.html",
                           title="Edit instance",
                           heading="Edit platform",
                           form=form,
                           viewing="instances",
                           editing=True)


# Edit instance (performance)
@cardb.route("/instances/edit-instance/<id>/performance", methods=['GET', 'POST'])
def edit_instance_performance(id):

    instance = Instance.query.get(id)

    form = Car7Form(obj=instance)

    if form.validate_on_submit():

        form.populate_obj(instance)
        instance.datetime_edited = datetime.utcnow()

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {}.".format(instance.name_full), "danger")
            return redirect(url_for("edit_instance_performance", id=instance.id))

        flash("The {} has been successfully edited.".format(instance.name_full), "success")
        return redirect(url_for("detail_instance", id=instance.id))

    return render_template("instances_form_8_performance.html",
                           title="Edit instance",
                           heading="Edit performance",
                           form=form,
                           viewing="instances",
                           editing=True)


# Edit instance (assists)
@cardb.route("/cars/edit-instance/<id>/assists", methods=['GET', 'POST'])
def edit_instance_assists(id):

    instance = Instance.query.get(id)

    # Get assists for the multiple select form
    assists = InstanceAssist.query.filter(InstanceAssist.instance_id == instance.id).all()
    assists_ids = []

    for assist in assists:
        assists_ids += str(assist.assist_id)

    form = Car8Form(assists_select=assists_ids)

    if form.validate_on_submit():

        instance.set_assists(form.assists_select.data)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {}.".format(instance.name_full), "danger")
            return redirect(url_for("edit_instance_assists", id=instance.id))

        flash("The {} has been successfully edited.".format(instance.name_full), "success")
        return redirect(url_for("detail_instance", id=instance.id))

    return render_template("instances_form_9_assists.html",
                           title="Edit instance",
                           heading="Edit assists",
                           form=form,
                           viewing="instances",
                           editing=True)


# Delete instance
@cardb.route("/cars/delete-instance/<id>", methods=['GET', 'POST'])
def delete_instance(id):

    instance = Instance.query.get(id)
    instance.is_deleted = True

    try:
        database.session.delete(instance)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the {}.".format(instance.name_full), "danger")
        return redirect(url_for("detail_instance", id=instance.id))

    flash("The {} has been successfully deleted.".format(instance.name_full), "success")
    return redirect(url_for("overview_instances"))


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


# Edit specialization
@cardb.route("/instances/specialization/edit-specialization/<id>", methods=['GET', 'POST'])
def edit_specialization(id):

    specialization = InstanceSpecialization.query.get(id)
    form = SpecializationEditForm(obj=specialization)

    if form.validate_on_submit():

        form.populate_obj(specialization)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the specialization \"{}\".".format(specialization.name_full), "danger")
            return redirect(url_for("edit_specialization", id=specialization.id))

        flash("The specialization \"{}\" has been successfully edited.".format(specialization.name_full), "success")
        return redirect(url_for("detail_specialization", id=specialization.id))

    return render_template("instances_form_specialization.html",
                           title="Edit specialization",
                           heading="Edit specialization",
                           form=form,
                           viewing="specialization")


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


# Delete specialization
@cardb.route("/instances/specialization/delete-specialization/<id>", methods=['GET', 'POST'])
def delete_specialization(id):

    specialization = InstanceSpecialization.query.get(id)

    try:
        database.session.delete(specialization)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the \"{}\" specialization.".format(specialization.name_full), "danger")
        return redirect(url_for("detail_specialization", id=specialization.id))

    flash("The specialization \"{}\" has been successfully deleted.".format(specialization.name_full), "success")
    return redirect(url_for("overview_instance_specialization"))


# Instance type detail
@cardb.route("/instances/types/detail/<id>", methods=['GET', 'POST'])
def detail_instance(id):

    instance = Instance.query.get(id)
    game = Game.query.get(instance.game_id)

    return return_redirect_to_details_based_on_game(game, id)


# Instance type detail
@cardb.route("/instances/types/detail/<id>", methods=['GET', 'POST'])
def detail_instance_type(id):

    instance_type = InstanceType.query.get(id)

    return render_template("instances_detail_instance_type.html",
                           title="{}".format(instance_type.name_short),
                           heading="{}".format(instance_type.name_full),
                           instance_type=instance_type,
                           viewing="instance_types")


# Specialization detail
@cardb.route("/instances/specialization/detail/<id>", methods=['GET', 'POST'])
def detail_specialization(id):

    specialization = InstanceSpecialization.query.get(id)

    return render_template("instances_detail_specialization.html",
                           title="{}".format(specialization.name_short),
                           heading="{}".format(specialization.name_full),
                           specialization=specialization,
                           viewing="specialization")
