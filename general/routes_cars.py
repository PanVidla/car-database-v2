from flask import render_template, flash, redirect, url_for

from general import cardb, database
from general.forms_cars import AssistAddForm, AssistEditForm, BodyStyleAddForm, BodyStyleEditForm
from general.models.car import Car, Assist, BodyStyle


# Cars overview
@cardb.route("/cars", methods=['GET'])
@cardb.route("/cars/all", methods=['GET'])
def overview_cars():

    cars = Car.query.order_by(Car.manufacturers_display.asc(), Car.year.asc(), Car.model.asc()).all()

    return render_template("cars_overview.html",
                           title="All cars",
                           heading="All cars",
                           cars=cars,
                           viewing="cars")


# Assists overview
@cardb.route("/cars/assists", methods=['GET'])
@cardb.route("/cars/assists/all", methods=['GET'])
def overview_assists():

    assists = Assist.query.order_by(Assist.name_short.asc()).all()

    return render_template("cars_overview_assists.html",
                           title="All assists",
                           heading="All assists",
                           assists=assists,
                           viewing="assists")


# Body styles overview
@cardb.route("/cars/body-styles", methods=['GET'])
@cardb.route("/cars/body-styles/all", methods=['GET'])
def overview_body_styles():

    body_styles = BodyStyle.query.order_by(BodyStyle.name.asc()).all()

    return render_template("cars_overview_body_styles.html",
                           title="All body styles",
                           heading="All body styles",
                           body_styles=body_styles,
                           viewing="body_styles")


# Add assist
@cardb.route("/cars/assists/add-assist", methods=['GET', 'POST'])
def add_assist():

    form = AssistAddForm()

    if form.validate_on_submit():

        new_assist = Assist()
        form.populate_obj(new_assist)

        try:
            database.session.add(new_assist)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding a new assist to the database.", "danger")
            return redirect(url_for("add_assist"))

        flash("{} ({}) has been successfully added to the database.".format(new_assist.name_full,
                                                                            new_assist.name_short), "success")
        return redirect(url_for("overview_assists"))

    return render_template("cars_form_assists.html",
                           title="Add assist",
                           heading="Add assist",
                           form=form,
                           viewing="assists")


# Add body style
@cardb.route("/cars/body-styles/add-body-style", methods=['GET', 'POST'])
def add_body_style():

    form = BodyStyleAddForm()

    if form.validate_on_submit():

        new_body_style = BodyStyle()
        form.populate_obj(new_body_style)

        try:
            database.session.add(new_body_style)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding a new body style to the database.", "danger")
            return redirect(url_for("add_body_style"))

        flash("Body style \"{}\" has been successfully added to the database.".format(new_body_style.name), "success")
        return redirect(url_for("overview_body_styles"))

    return render_template("cars_form_body_style.html",
                           title="Add body style",
                           heading="Add body style",
                           form=form,
                           viewing="body_styles")


# Edit assist
@cardb.route("/cars/assists/edit-assist/<id>", methods=['GET', 'POST'])
def edit_assist(id):

    assist = Assist.query.get(id)
    form = AssistEditForm(obj=assist)

    if form.validate_on_submit():

        form.populate_obj(assist)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing {} ({}).".format(assist.name_full,
                                                                assist.name_short), "danger")
            return redirect(url_for("edit_assist", id=assist.id))

        flash("{} ({}) has been successfully edited.".format(assist.name_full,
                                                             assist.name_short), "success")
        return redirect(url_for("detail_assist", id=assist.id))

    return render_template("cars_form_assists.html",
                           title="Edit assist",
                           heading="Edit assist",
                           form=form,
                           viewing="assists")


# Edit body style
@cardb.route("/cars/body-styles/edit-body-style/<id>", methods=['GET', 'POST'])
def edit_body_style(id):

    body_style = BodyStyle.query.get(id)
    form = BodyStyleEditForm(obj=body_style)

    if form.validate_on_submit():

        form.populate_obj(body_style)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the body style \"{}\".".format(body_style.name), "danger")
            return redirect(url_for("edit_body_style", id=body_style.id))

        flash("The body style \"{}\" has been successfully edited.".format(body_style.name), "success")
        return redirect(url_for("detail_body_style", id=body_style.id))

    return render_template("cars_form_body_style.html",
                           title="Edit body style",
                           heading="Edit body style",
                           form=form,
                           viewing="body_styles")


# Delete assist
@cardb.route("/cars/assists/delete-assist/<id>", methods=['GET', 'POST'])
def delete_assist(id):

    assist = Assist.query.get(id)

    try:
        database.session.delete(assist)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting {} ({}).".format(assist.name_full,
                                                                  assist.name_short), "danger")
        return redirect(url_for("detail_assist", id=assist.id))

    flash("{} ({}) has been successfully deleted.".format(assist.name_full,
                                                          assist.name_short), "success")
    return redirect(url_for("overview_assists"))


# Delete body_style
@cardb.route("/cars/body-styles/delete-body-style/<id>", methods=['GET', 'POST'])
def delete_body_style(id):

    body_style = BodyStyle.query.get(id)

    try:
        database.session.delete(body_style)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting body style \"{}\".".format(body_style.name), "danger")
        return redirect(url_for("detail_body_style", id=body_style.id))

    flash("The body style \"{}\" has been successfully deleted.".format(body_style.name), "success")
    return redirect(url_for("overview_body_styles"))


# Assist detail
@cardb.route("/cars/assists/detail/<id>", methods=['GET', 'POST'])
def detail_assist(id):

    assist = Assist.query.get(id)

    return render_template("cars_detail_assists.html",
                           title="{}".format(assist.name_short),
                           heading="{}".format(assist.name_full),
                           assist=assist,
                           viewing="assists")


# Body style detail
@cardb.route("/cars/body-styles/detail/<id>", methods=['GET', 'POST'])
def detail_body_style(id):

    body_style = BodyStyle.query.get(id)

    return render_template("cars_detail_body_style.html",
                           title="{}".format(body_style.name),
                           heading="{}".format(body_style.name),
                           body_style=body_style,
                           viewing="body_styles")
