from flask import render_template, flash, redirect, url_for

from general import cardb, database
from general.forms_cars import AssistAddForm, AssistEditForm
from general.models.car import Car, Assist


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


# Assist detail
@cardb.route("/cars/assists/detail/<id>", methods=['GET', 'POST'])
def detail_assist(id):

    assist = Assist.query.get(id)

    return render_template("cars_detail_assists.html",
                           title="{}".format(assist.name_short),
                           heading="{}".format(assist.name_full),
                           assist=assist,
                           viewing="assists")
