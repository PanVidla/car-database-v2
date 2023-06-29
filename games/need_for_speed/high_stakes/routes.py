from datetime import datetime

from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from games.need_for_speed.high_stakes import blueprint
from games.need_for_speed.high_stakes.forms import InstanceNFS4Form, ClassNFS4Form, TuneNFS4Form, TrackNFS4Form, \
    ArcadeEventNFS4Form
from games.need_for_speed.high_stakes.models.event import EventNFS4, create_new_arcade_event_from_form, ArcadeEventNFS4
from games.need_for_speed.high_stakes.models.instance import InstanceNFS4, TuneNFS4, ClassNFS4
from games.need_for_speed.high_stakes.models.track import TrackNFS4
from general import database
from general.forms_info import TextForm, ImageForm
from general.models.instance import InstanceText, InstanceImage


# Instances overview
@blueprint.route("/instances/overview", methods=['GET'])
@blueprint.route("/instances/overview/all", methods=['GET'])
def overview_instances():

    instances = InstanceNFS4.query. \
        filter(InstanceNFS4.is_deleted != True) \
        .order_by(InstanceNFS4.id.desc()).all()

    return render_template("nfs4_instances_overview.html",
                           title="Need for Speed: High Stakes",
                           heading="All Need for Speed: High Stakes instances",
                           instances=instances,
                           viewing="instances",
                           game="Need for Speed: High Stakes")


@blueprint.route("/classes/overview", methods=['GET'])
@blueprint.route("/classes/overview/all", methods=['GET'])
def overview_classes():

    classes = ClassNFS4.query.order_by(ClassNFS4.name.asc()).all()

    return render_template("nfs4_classes_overview.html",
                           title="Need for Speed: High Stakes",
                           heading="All Need for Speed: High Stakes classes",
                           classes=classes,
                           viewing="classes",
                           game="Need for Speed: High Stakes")


@blueprint.route("/events/overview", methods=['GET'])
@blueprint.route("/events/overview/all", methods=['GET'])
def overview_events_all():

    events = EventNFS4.query.order_by(EventNFS4.id.desc()).all()

    return render_template("nfs4_events_overview_all.html",
                           title="Need for Speed: High Stakes",
                           heading="All Need for Speed: High Stakes events",
                           events=events,
                           viewing="events",
                           game="Need for Speed: High Stakes")


@blueprint.route("/events/arcade/overview", methods=['GET'])
@blueprint.route("/events/arcade/overview/all", methods=['GET'])
def overview_events_arcade():

    arcade_events = ArcadeEventNFS4.query.order_by(ArcadeEventNFS4.id.desc()).all()

    return render_template("nfs4_events_overview_arcade.html",
                           title="Need for Speed: High Stakes",
                           heading="All Need for Speed: High Stakes arcade events",
                           arcade_events=arcade_events,
                           viewing="events_arcade",
                           game="Need for Speed: High Stakes")


@blueprint.route("/tracks/overview", methods=['GET'])
@blueprint.route("/tracks/overview/all", methods=['GET'])
def overview_tracks():

    tracks = TrackNFS4.query.order_by(TrackNFS4.id.asc()).all()

    return render_template("nfs4_tracks_overview.html",
                           title="Need for Speed: High Stakes",
                           heading="All Need for Speed: High Stakes tracks",
                           tracks=tracks,
                           viewing="tracks",
                           game="Need for Speed: High Stakes")


# Add instance
@blueprint.route("/instances/add-instance/<id>", methods=['GET', 'POST'])
@login_required
def add_instance(id):

    instance = InstanceNFS4.query.get(id)
    form = InstanceNFS4Form()

    if form.validate_on_submit():

        form.populate_obj(instance)
        new_tune = TuneNFS4(instance_id=instance.id)

        try:
            database.session.add(new_tune)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem setting game-specific values for the {}.".format(instance.name_full), "danger")
            return redirect(url_for("need_for_speed.high_stakes.overview_instances"))

        flash("Game-specific values have been successfully set for the {}.".format(instance.name_full), "success")
        return redirect(url_for("need_for_speed.high_stakes.detail_instance", id=instance.id))

    return render_template("nfs4_instances_form.html",
                           title="Add instance",
                           heading="Add instance",
                           form=form,
                           viewing="instances",
                           game="Need for Speed: High Stakes")


# Add class
@blueprint.route("/classes/add-class", methods=['GET', 'POST'])
@login_required
def add_class():

    form = ClassNFS4Form()

    if form.validate_on_submit():

        new_class = ClassNFS4()
        form.populate_obj(new_class)

        try:
            database.session.add(new_class)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding the {} class to the database.".format(new_class.name), "danger")
            return redirect(url_for("need_for_speed.high_stakes.overview_classes"))

        flash("The {} class has been successfully added to the database.".format(new_class.name), "success")
        return redirect(url_for("need_for_speed.high_stakes.detail_class", id=new_class.id))

    return render_template("nfs4_classes_form.html",
                           title="Add class",
                           heading="Add class",
                           form=form,
                           viewing="classes",
                           game="Need for Speed: High Stakes")


@blueprint.route("/events/add-event/arcade", methods=['GET', 'POST'])
@login_required
def add_event_arcade():

    form = ArcadeEventNFS4Form()

    if form.validate_on_submit():

        attempt_at_creating_new_arcade_event = create_new_arcade_event_from_form(form)

        error_code = attempt_at_creating_new_arcade_event[0]
        arcade_event = attempt_at_creating_new_arcade_event[1]
        message = attempt_at_creating_new_arcade_event[2]

        if (error_code >= 1) and (error_code <= 3):
            flash(message, "warning")
            return redirect(url_for("need_for_speed.high_stakes.add_event_arcade"))

        elif error_code != 0:
            flash("There was an unknown error when creating the new arcade event.", "danger")
            return redirect(url_for("need_for_speed.high_stakes.add_event_arcade"))

        else:

            try:
                database.session.add(arcade_event)
                database.session.commit()
            except RuntimeError:
                flash("There was a problem adding the arcade event \"{}\" event to the database.".format(arcade_event.name), "danger")
                return redirect(url_for("need_for_speed.high_stakes.add_event_arcade"))

        flash("The arcade event \"{}\" has been successfully added to the database.".format(arcade_event.name), "success")
        # TODO: Should actually redirect to the detail view of the event
        return redirect(url_for("need_for_speed.high_stakes.overview_events_all"))

    return render_template("nfs4_events_form_arcade.html",
                           title="Add arcade event",
                           heading="Add arcade event",
                           form=form,
                           viewing="events",
                           game="Need for Speed: High Stakes")


@blueprint.route("/events/add-event/career", methods=['GET', 'POST'])
@login_required
def add_event_career():

    form = EventNFS4CareerForm()

    if form.validate_on_submit():

        new_event = EventNFS()
        form.populate_obj(new_event)

        try:
            database.session.add(new_event)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding the \"{}\" event to the database.".format(new_event.name), "danger")
            return redirect(url_for("need_for_speed.iii_hot_pursuit.overview_events"))

        flash("The \"{}\" event has been successfully added to the database.".format(new_event.name), "success")
        return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_event", id=new_event.id))

    return render_template("nfs3_events_form.html",
                           title="Add event",
                           heading="Add event",
                           form=form,
                           viewing="events",
                           game="Need for Speed III: Hot Pursuit")


# Add track
@blueprint.route("/tracks/add-track", methods=['GET', 'POST'])
@login_required
def add_track():

    form = TrackNFS4Form()

    if form.validate_on_submit():

        new_track = TrackNFS4(is_fictional=True)
        form.populate_obj(new_track)

        try:
            database.session.add(new_track)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding the {} to the database.".format(new_track.name), "danger")
            return redirect(url_for("need_for_speed.high_stakes.overview_tracks"))

        flash("{} has been successfully added to the database.".format(new_track.name), "success")
        return redirect(url_for("need_for_speed.high_stakes.detail_track", id=new_track.id))

    return render_template("nfs4_tracks_form.html",
                           title="Add track",
                           heading="Add track",
                           form=form,
                           viewing="tracks",
                           game="Need for Speed: High Stakes")


# Edit instance (game-specific)
@blueprint.route("/instances/edit-instance/<id>/game-specific", methods=['GET', 'POST'])
@login_required
def edit_instance_game_specific(id):

    instance = InstanceNFS4.query.get(id)

    form = InstanceNFS4Form(obj=instance)

    if form.validate_on_submit():

        form.populate_obj(instance)
        instance.datetime_edited = datetime.utcnow()

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {}.".format(instance.name_full), "danger")
            return redirect(url_for("need_for_speed.high_stakes.edit_instance_game_specific", id=instance.id))

        flash("The {} has been successfully edited.".format(instance.name_full), "success")
        return redirect(url_for("need_for_speed.high_stakes.detail_instance", id=instance.id))

    return render_template("nfs4_instances_form.html",
                           title="Edit instance",
                           heading="Edit game-specific information",
                           form=form,
                           viewing="instances",
                           game="Need for Speed: High Stakes",
                           editing=True)


# Edit class
@blueprint.route("/classes/edit-class/<id>", methods=['GET', 'POST'])
@login_required
def edit_class(id):

    car_class = ClassNFS4.query.get(id)
    form = ClassNFS4Form(obj=car_class)

    if form.validate_on_submit():

        form.populate_obj(car_class)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {} class.".format(car_class.name), "danger")
            return redirect(url_for("need_for_speed.high_stakes.detail_class", id=car_class.id))

        flash("The {} class has been successfully edited.".format(car_class.name), "success")
        return redirect(url_for("need_for_speed.high_stakes.detail_class", id=car_class.id))

    return render_template("nfs4_classes_form.html",
                           title="Edit class",
                           heading="Edit class",
                           form=form,
                           viewing="classes",
                           game="Need for Speed: High Stakes",
                           editing=True)


# Edit track
@blueprint.route("/tracks/edit-track/<id>", methods=['GET', 'POST'])
@login_required
def edit_track(id):

    track = TrackNFS4.query.get(id)
    form = TrackNFS4Form(obj=track)

    if form.validate_on_submit():

        form.populate_obj(track)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing {}.".format(track.name), "danger")
            return redirect(url_for("need_for_speed.high_stakes.detail_track", id=track.id))

        flash("{} event has been successfully edited.".format(track.name), "success")
        return redirect(url_for("need_for_speed.high_stakes.detail_track", id=track.id))

    return render_template("nfs4_tracks_form.html",
                           title="Edit track",
                           heading="Edit track",
                           form=form,
                           viewing="tracks",
                           game="Need for Speed: High Stakes",
                           editing=True)


# Delete event
@blueprint.route("/tracks/delete-track/<id>", methods=['GET', 'POST'])
@login_required
def delete_track(id):

    track = TrackNFS4.query.get(id)

    try:
        database.session.delete(track)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting {}.".format(track.name), "danger")
        return redirect(url_for("need_for_speed.high_stakes.detail_track", id=track.id))

    flash("{} event has been successfully deleted.".format(track.name), "success")
    return redirect(url_for("need_for_speed.high_stakes.overview_tracks"))


# Delete class
@blueprint.route("/classes/delete-class/<id>", methods=['GET', 'POST'])
@login_required
def delete_class(id):

    car_class = ClassNFS4.query.get(id)

    try:
        database.session.delete(car_class)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the {} class.".format(car_class.name), "danger")
        return redirect(url_for("need_for_speed.high_stakes.detail_class", id=car_class.id))

    flash("Class {} has been successfully deleted.".format(car_class.name), "success")
    return redirect(url_for("need_for_speed.high_stakes.overview_classes"))


# Instance detail
@blueprint.route("/instances/detail/<id>", methods=['GET', 'POST'])
@login_required
def detail_instance(id):

    instance = InstanceNFS4.query.get(id)
    tune = instance.get_tune()
    texts = InstanceText.query \
        .filter(InstanceText.instance_id == instance.id) \
        .order_by(InstanceText.order.asc()) \
        .all()

    add_text_form = TextForm()
    add_image_form = ImageForm()

    edit_tune_form = TuneNFS4Form(obj=tune)
    # add_event_record_form = EventRecordNFS3Form()

    # Add text
    if add_text_form.submit_add_text.data and add_text_form.validate():

        whole_text = add_text_form.content.data

        for paragraph in whole_text.splitlines():

            if paragraph == "":
                continue

            else:

                new_text = InstanceText()
                new_text.content = paragraph
                new_text.text_type = add_text_form.text_type.data
                new_text.order = len(instance.texts.all()) + 1
                new_text.instance_id = instance.id

                instance.datetime_edited = datetime.utcnow()

                try:
                    database.session.add(new_text)
                    database.session.commit()
                except RuntimeError:
                    flash("There was a problem adding text to {}.".format(instance.name_display), "danger")
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

        instance.datetime_edited = datetime.utcnow()

        try:
            database.session.add(new_image)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding an image to {}.".format(instance.name_full), "danger")
            return redirect(url_for("need_for_speed.high_stakes.detail_instance", id=instance.id))

        flash("The image has been successfully added to {}.".format(instance.name_full), "success")
        return redirect(url_for("need_for_speed.high_stakes.detail_instance", id=instance.id))

    # Edit tune
    if edit_tune_form.submit_edit_tune.data and edit_tune_form.validate():

        if instance.get_tune() is None:

            new_tune = TuneNFS4(instance_id=instance.id)
            edit_tune_form.populate_obj(new_tune)

            try:
                database.session.add(new_tune)
                database.session.commit()
            except RuntimeError:
                flash("There was a problem add a new tune to this instance", "danger")
                return redirect(url_for("need_for_speed.high_stakes.detail_instance", id=instance.id))

            flash("A tune has been successfully added to this instance.", "success")
            return redirect(url_for("need_for_speed.high_stakes.detail_instance", id=instance.id))

        edit_tune_form.populate_obj(tune)
        instance.datetime_edited = datetime.utcnow()

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing this instance's tune.", "danger")
            return redirect(url_for("need_for_speed.high_stakes.detail_instance", id=instance.id))

        flash("The tune has been successfully updated.", "success")
        return redirect(url_for("need_for_speed.high_stakes.detail_instance", id=instance.id))

    # Add event record
    if add_event_record_form.submit_add_event_record.data and add_event_record_form.validate():

        new_event_record = EventRecordNFS3(instance_id=instance.id,
                                           datetime_added=datetime.utcnow(),
                                           datetime_edited=datetime.utcnow(),
                                           no_of_event_record=len(instance.get_event_records()) + 1)
        add_event_record_form.populate_obj(new_event_record)

        try:
            database.session.add(new_event_record)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding a new event record to the database.", "danger")
            return redirect(url_for("need_for_speed.high_stakes.detail_instance", id=instance.id))

        new_event_record.set_calculated_values()
        instance.update_statistics()

        instance.datetime_played = datetime.utcnow()

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem calculating values for the new event record in the database.", "danger")
            return redirect(url_for("need_for_speed.high_stakes.detail_instance", id=instance.id))

        flash("Event record no. {} has been successfully added to the database.".format(new_event_record.no_of_event_record), "success")
        return redirect(url_for("need_for_speed.high_stakes.detail_instance", id=instance.id))

    return render_template("nfs4_instances_detail.html",
                           title="{}".format(instance.name_nickname),
                           heading="{}".format(instance.name_full),
                           instance=instance,
                           tune=tune,
                           texts=texts,
                           add_text_form=add_text_form,
                           add_image_form=add_image_form,
                           edit_tune_form=edit_tune_form,
                           add_event_record_form=add_event_record_form,
                           viewing="instances",
                           game="Need for Speed: High Stakes")


# Detail class
@blueprint.route("/classes/detail/<id>", methods=['GET', 'POST'])
@login_required
def detail_class(id):

    car_class = ClassNFS4.query.get(id)

    return render_template("nfs4_classes_detail.html",
                           title="{} class".format(car_class.name),
                           heading="{} class".format(car_class.name),
                           car_class=car_class,
                           viewing="classes",
                           game="Need for Speed: High Stakes")


# Detail track
@blueprint.route("/tracks/detail/<id>", methods=['GET', 'POST'])
@login_required
def detail_track(id):

    track = TrackNFS4.query.get(id)

    return render_template("nfs4_tracks_detail.html",
                           title="{}".format(track.name),
                           heading="{}".format(track.name),
                           track=track,
                           viewing="tracks",
                           game="Need for Speed: High Stakes")
