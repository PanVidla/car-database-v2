from datetime import datetime

from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from games.need_for_speed.iii_hot_pursuit import blueprint
from games.need_for_speed.iii_hot_pursuit.forms import InstanceNFS3Form, ClassNFS3Form, TuneNFS3Form, EventNFS3Form, \
    TrackNFS3Form, EventRecordNFS3Form
from games.need_for_speed.iii_hot_pursuit.models.events import EventNFS3
from games.need_for_speed.iii_hot_pursuit.models.instance import InstanceNFS3, ClassNFS3, TuneNFS3
from games.need_for_speed.iii_hot_pursuit.models.records import EventRecordNFS3
from games.need_for_speed.iii_hot_pursuit.models.tracks import TrackNFS3
from general import database
from general.forms_info import TextForm, ImageForm
from general.models.instance import InstanceText, InstanceImage


@blueprint.route("/instances/overview", methods=['GET'])
@blueprint.route("/instances/overview/all", methods=['GET'])
def overview_instances():

    instances = InstanceNFS3.query. \
        filter(InstanceNFS3.is_deleted != True) \
        .order_by(InstanceNFS3.id.desc()).all()

    return render_template("nfs3_instances_overview.html",
                           title="Need for Speed III",
                           heading="All Need for Speed III instances",
                           instances=instances,
                           viewing="instances",
                           game="Need for Speed III: Hot Pursuit")


@blueprint.route("/classes/overview", methods=['GET'])
@blueprint.route("/classes/overview/all", methods=['GET'])
def overview_classes():

    classes = ClassNFS3.query.order_by(ClassNFS3.name.asc()).all()

    return render_template("nfs3_classes_overview.html",
                           title="Need for Speed III",
                           heading="All Need for Speed III classes",
                           classes=classes,
                           viewing="classes",
                           game="Need for Speed III: Hot Pursuit")


@blueprint.route("/events/overview", methods=['GET'])
@blueprint.route("/events/overview/all", methods=['GET'])
def overview_events():

    events = EventNFS3.query.order_by(EventNFS3.name.asc()).all()

    return render_template("nfs3_events_overview.html",
                           title="Need for Speed III",
                           heading="All Need for Speed III events",
                           events=events,
                           viewing="events",
                           game="Need for Speed III: Hot Pursuit")


@blueprint.route("/tracks/overview", methods=['GET'])
@blueprint.route("/tracks/overview/all", methods=['GET'])
def overview_tracks():

    tracks = TrackNFS3.query.order_by(TrackNFS3.id.asc()).all()

    return render_template("nfs3_tracks_overview.html",
                           title="Need for Speed III",
                           heading="All Need for Speed III tracks",
                           tracks=tracks,
                           viewing="tracks",
                           game="Need for Speed III: Hot Pursuit")


# Add instance
@blueprint.route("/instances/add-instance/<id>", methods=['GET', 'POST'])
@login_required
def add_instance(id):

    instance = InstanceNFS3.query.get(id)
    form = InstanceNFS3Form()

    if form.validate_on_submit():

        form.populate_obj(instance)
        new_tune = TuneNFS3(instance_id=instance.id)
        instance.set_average()

        try:
            database.session.add(new_tune)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem setting game-specific values for the {}.".format(instance.name_full), "danger")
            return redirect(url_for("need_for_speed.iii_hot_pursuit.overview_instances"))

        flash("Game-specific values have been successfully set for the {}.".format(instance.name_full), "success")
        return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=instance.id))

    return render_template("nfs3_instances_form.html",
                           title="Add instance",
                           heading="Add instance",
                           form=form,
                           viewing="instances",
                           game="Need for Speed III: Hot Pursuit")


@blueprint.route("/classes/add-class", methods=['GET', 'POST'])
@login_required
def add_class():

    form = ClassNFS3Form()

    if form.validate_on_submit():

        new_class = ClassNFS3()
        form.populate_obj(new_class)

        try:
            database.session.add(new_class)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding the {} class to the database.".format(new_class.name), "danger")
            return redirect(url_for("need_for_speed.iii_hot_pursuit.overview_classes"))

        flash("The {} class has been successfully added to the database.".format(new_class.name), "success")
        return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_class", id=new_class.id))

    return render_template("nfs3_classes_form.html",
                           title="Add class",
                           heading="Add class",
                           form=form,
                           viewing="classes",
                           game="Need for Speed III: Hot Pursuit")


@blueprint.route("/events/add-event", methods=['GET', 'POST'])
@login_required
def add_event():

    form = EventNFS3Form()

    if form.validate_on_submit():

        new_event = EventNFS3()
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

    form = TrackNFS3Form()

    if form.validate_on_submit():

        new_track = TrackNFS3(is_fictional=True)
        form.populate_obj(new_track)

        try:
            database.session.add(new_track)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding the {} to the database.".format(new_track.name), "danger")
            return redirect(url_for("need_for_speed.iii_hot_pursuit.overview_tracks"))

        flash("{} has been successfully added to the database.".format(new_track.name), "success")
        return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_track", id=new_track.id))

    return render_template("nfs3_tracks_form.html",
                           title="Add track",
                           heading="Add track",
                           form=form,
                           viewing="tracks",
                           game="Need for Speed III: Hot Pursuit")


# Edit instance (game-specific)
@blueprint.route("/instances/edit-instance/<id>/game-specific", methods=['GET', 'POST'])
@login_required
def edit_instance_game_specific(id):

    instance = InstanceNFS3.query.get(id)

    form = InstanceNFS3Form(obj=instance)

    if form.validate_on_submit():

        form.populate_obj(instance)
        instance.set_average()
        instance.datetime_edited = datetime.utcnow()

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {}.".format(instance.name_full), "danger")
            return redirect(url_for("need_for_speed.iii_hot_pursuit.edit_instance_game_specific", id=instance.id))

        flash("The {} has been successfully edited.".format(instance.name_full), "success")
        return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=instance.id))

    return render_template("nfs3_instances_form.html",
                           title="Edit instance",
                           heading="Edit game-specific information",
                           form=form,
                           viewing="instances",
                           game="Need for Speed III: Hot Pursuit",
                           editing=True)


# Edit class
@blueprint.route("/classes/edit-class/<id>", methods=['GET', 'POST'])
@login_required
def edit_class(id):

    car_class = ClassNFS3.query.get(id)
    form = ClassNFS3Form(obj=car_class)

    if form.validate_on_submit():

        form.populate_obj(car_class)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {} class.".format(car_class.name), "danger")
            return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_class", id=car_class.id))

        flash("The {} class has been successfully edited.".format(car_class.name), "success")
        return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_class", id=car_class.id))

    return render_template("nfs3_classes_form.html",
                           title="Edit class",
                           heading="Edit class",
                           form=form,
                           viewing="classes",
                           game="Need for Speed III: Hot Pursuit",
                           editing=True)


# Edit event
@blueprint.route("/events/edit-event/<id>", methods=['GET', 'POST'])
@login_required
def edit_event(id):

    event = EventNFS3.query.get(id)
    form = EventNFS3Form(obj=event)

    if form.validate_on_submit():

        form.populate_obj(event)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {} event.".format(event.name), "danger")
            return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_event", id=event.id))

        flash("The {} event has been successfully edited.".format(event.name), "success")
        return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_event", id=event.id))

    return render_template("nfs3_events_form.html",
                           title="Edit event",
                           heading="Edit event",
                           form=form,
                           viewing="events",
                           game="Need for Speed III: Hot Pursuit",
                           editing=True)


# Edit event record
@blueprint.route("/event-records/edit-event-record/<id>", methods=['GET', 'POST'])
@login_required
def edit_event_record(id):

    event_record = EventRecordNFS3.query.get(id)
    form = EventRecordNFS3Form(obj=event_record)

    if form.validate_on_submit():

        form.populate_obj(event_record)

        try:
            database.session.add(event_record)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the event record.", "danger")
            return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=event_record.instance.id))

        event_record.set_calculated_values()
        event_record.instance.update_statistics()

        event_record.datetime_edited = datetime.utcnow()

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem calculating values for the event record in the database.", "danger")
            return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=event_record.instance.id))

        flash("Event record no. {} has been successfully edited.".format(
            event_record.no_of_event_record), "success")
        return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=event_record.instance.id))

    return render_template("nfs3_event_records_form.html",
                           title="Edit event record",
                           heading="Edit event record",
                           form=form,
                           viewing="event_records",
                           game="Need for Speed III: Hot Pursuit",
                           editing=True)


# Edit track
@blueprint.route("/tracks/edit-track/<id>", methods=['GET', 'POST'])
@login_required
def edit_track(id):

    track = TrackNFS3.query.get(id)
    form = TrackNFS3Form(obj=track)

    if form.validate_on_submit():

        form.populate_obj(track)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing {}.".format(track.name), "danger")
            return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_track", id=track.id))

        flash("{} event has been successfully edited.".format(track.name), "success")
        return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_track", id=track.id))

    return render_template("nfs3_tracks_form.html",
                           title="Edit track",
                           heading="Edit track",
                           form=form,
                           viewing="tracks",
                           game="Need for Speed III: Hot Pursuit",
                           editing=True)


# Delete class
@blueprint.route("/classes/delete-class/<id>", methods=['GET', 'POST'])
@login_required
def delete_class(id):

    car_class = ClassNFS3.query.get(id)

    try:
        database.session.delete(car_class)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the {} class.".format(car_class.name), "danger")
        return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_class", id=car_class.id))

    flash("Class {} has been successfully deleted.".format(car_class.name), "success")
    return redirect(url_for("need_for_speed.iii_hot_pursuit.overview_classes"))


# Delete event
@blueprint.route("/events/delete-event/<id>", methods=['GET', 'POST'])
@login_required
def delete_event(id):

    event = EventNFS3.query.get(id)

    try:
        database.session.delete(event)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the {}.".format(event.name), "danger")
        return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_event", id=event.id))

    flash("The {} event has been successfully deleted.".format(event.name), "success")
    return redirect(url_for("need_for_speed.iii_hot_pursuit.overview_events"))


# Delete event record
@blueprint.route("/event-records/delete-event-record/<id>", methods=['GET', 'POST'])
@login_required
def delete_event_record(id):

    event_record = EventRecordNFS3.query.get(id)

    event_record.is_deleted = True

    if event_record.is_lap_record == True:
        event_record.track.update_best_lap_time_event_record()

    if event_record.is_track_record == True:
        event_record.track.update_best_track_time_event_record()

    event_record.instance.update_statistics()

    try:
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting event record no. {}.".format(event_record.no_of_event_record), "danger")
        return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=event_record.instance.id))

    flash("Event record no. {} has been successfully deleted.".format(event_record.no_of_event_record), "success")
    return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=event_record.instance.id))


# Delete event
@blueprint.route("/tracks/delete-track/<id>", methods=['GET', 'POST'])
@login_required
def delete_track(id):

    track = TrackNFS3.query.get(id)

    try:
        database.session.delete(track)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting {}.".format(track.name), "danger")
        return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_track", id=track.id))

    flash("{} event has been successfully deleted.".format(track.name), "success")
    return redirect(url_for("need_for_speed.iii_hot_pursuit.overview_tracks"))


# Instance detail
@blueprint.route("/instances/detail/<id>", methods=['GET', 'POST'])
@login_required
def detail_instance(id):

    instance = InstanceNFS3.query.get(id)
    tune = instance.get_tune()
    texts = InstanceText.query \
        .filter(InstanceText.instance_id == instance.id) \
        .order_by(InstanceText.order.asc()) \
        .all()

    add_text_form = TextForm()
    add_image_form = ImageForm()

    edit_tune_form = TuneNFS3Form(obj=tune)
    add_event_record_form = EventRecordNFS3Form()

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
            return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=instance.id))

        flash("The image has been successfully added to {}.".format(instance.name_full), "success")
        return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=instance.id))

    # Edit tune
    if edit_tune_form.submit_edit_tune.data and edit_tune_form.validate():

        if instance.get_tune() is None:

            new_tune = TuneNFS3(instance_id=instance.id)
            edit_tune_form.populate_obj(new_tune)

            try:
                database.session.add(new_tune)
                database.session.commit()
            except RuntimeError:
                flash("There was a problem add a new tune to this instance", "danger")
                return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=instance.id))

            flash("A tune has been successfully added to this instance.", "success")
            return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=instance.id))

        edit_tune_form.populate_obj(tune)
        instance.datetime_edited = datetime.utcnow()

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing this instance's tune.", "danger")
            return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=instance.id))

        flash("The tune has been successfully updated.", "success")
        return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=instance.id))

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
            return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=instance.id))

        new_event_record.set_calculated_values()
        instance.update_statistics()

        instance.datetime_played = datetime.utcnow()

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem calculating values for the new event record in the database.", "danger")
            return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=instance.id))

        flash("Event record no. {} has been successfully added to the database.".format(new_event_record.no_of_event_record), "success")
        return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=instance.id))

    return render_template("nfs3_instances_detail.html",
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
                           game="Need for Speed III: Hot Pursuit")


# Detail class
@blueprint.route("/classes/detail/<id>", methods=['GET', 'POST'])
@login_required
def detail_class(id):

    car_class = ClassNFS3.query.get(id)

    return render_template("nfs3_classes_detail.html",
                           title="{} class".format(car_class.name),
                           heading="{} class".format(car_class.name),
                           car_class=car_class,
                           viewing="classes",
                           game="Need for Speed III: Hot Pursuit")


# Detail event
@blueprint.route("/events/detail/<id>", methods=['GET', 'POST'])
@login_required
def detail_event(id):

    event = EventNFS3.query.get(id)

    return render_template("nfs3_events_detail.html",
                           title="{}".format(event.name),
                           heading="{}".format(event.name),
                           event=event,
                           viewing="events",
                           game="Need for Speed III: Hot Pursuit")


# Detail track
@blueprint.route("/tracks/detail/<id>", methods=['GET', 'POST'])
@login_required
def detail_track(id):

    track = TrackNFS3.query.get(id)

    return render_template("nfs3_tracks_detail.html",
                           title="{}".format(track.name),
                           heading="{}".format(track.name),
                           track=track,
                           viewing="tracks",
                           game="Need for Speed III: Hot Pursuit")
