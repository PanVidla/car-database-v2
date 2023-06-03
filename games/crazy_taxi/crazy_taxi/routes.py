from flask import render_template, redirect, url_for, flash
from flask_login import login_required

from games.crazy_taxi.crazy_taxi import crazy_taxi_1
from games.crazy_taxi.crazy_taxi.models.instance import InstanceCT
from general import database
from general.forms_info import TextForm, ImageForm
from general.models.car import Car
from general.models.instance import Instance, InstanceText, InstanceImage


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
@login_required
def detail_instance(id):

    instance = Instance.query.get(id)
    texts = InstanceText.query \
        .filter(InstanceText.instance_id == instance.id) \
        .order_by(InstanceText.order.asc()) \
        .all()

    add_text_form = TextForm()
    add_image_form = ImageForm()

    # Add text
    if add_text_form.submit_add_text.data and add_text_form.validate():

        new_text = InstanceText()
        add_text_form.populate_obj(new_text)
        new_text.order = len(instance.texts.all()) + 1
        new_text.instance_id = instance.id

        try:
            database.session.add(new_text)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding text to {}.".format(instance.name_full), "danger")
            return redirect(url_for("detail_instance", id=instance.id))

        flash("The text has been successfully added to {}.".format(instance.name_full), "success")
        return redirect(url_for("detail_instance", id=instance.id))

    # Add image
    if add_image_form.submit_add_image.data and add_image_form.validate():

        new_image = InstanceImage()
        add_image_form.populate_obj(new_image)
        new_image.order = len(instance.images.all()) + 1
        new_image.instance_id = instance.id
        new_image.is_thumbnail = False

        try:
            database.session.add(new_image)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding an image to {}.".format(instance.name_full), "danger")
            return redirect(url_for("crazy_taxi.crazy_taxi_1.detail_instance", id=instance.id))

        flash("The image has been successfully added to {}.".format(instance.name_full), "success")
        return redirect(url_for("crazy_taxi.crazy_taxi_1.detail_instance", id=instance.id))

    return render_template("instances_detail.html",
                           title="{}".format(instance.name_nickname),
                           heading="{}".format(instance.name_full),
                           instance=instance,
                           texts=texts,
                           add_text_form=add_text_form,
                           add_image_form=add_image_form,
                           viewing="instances")
