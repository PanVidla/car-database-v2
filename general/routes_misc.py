# Overviews
from flask import render_template, flash, redirect, url_for

from general import cardb, database
from general.forms_misc import CountryAddForm, CountryEditForm, CompetitionAddForm, CompetitionEditForm
from general.models.misc import Country, Competition


@cardb.route("/misc/competitions", methods=['GET'])
@cardb.route("/misc/competitions/all", methods=['GET'])
def overview_competitions():

    competitions = Competition.query.order_by(Competition.name_display.asc(), Competition.date_started.asc()).all()

    return render_template("misc_competitions_overview.html",
                           title="Competitions",
                           heading="All competitions",
                           competitions=competitions)


@cardb.route("/misc/countries", methods=['GET'])
@cardb.route("/misc/countries/all", methods=['GET'])
def overview_countries():

    countries = Country.query.order_by(Country.name_display.asc()).all()

    return render_template("misc_countries_overview.html",
                           title="Countries",
                           heading="All countries",
                           countries=countries)


# Add competition
@cardb.route("/misc/competitions/add-competition", methods=['GET', 'POST'])
def add_competition():

    form = CompetitionAddForm()

    if form.validate_on_submit():

        new_competition = Competition()
        form.populate_obj(new_competition)

        try:
            database.session.add(new_competition)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding a new competition to the database.", "danger")
            return redirect(url_for("add_competition"))

        flash("{} ({}, {}) has been successfully added to the database.".format(new_competition.name_display,
                                                                                new_competition.name_full,
                                                                                new_competition.name_short), "success")
        return redirect(url_for("overview_competitions"))

    return render_template("misc_competitions_form.html",
                           title="Add competition",
                           heading="Add competition",
                           form=form)


# Add country
@cardb.route("/misc/countries/add-country", methods=['GET', 'POST'])
def add_country():

    form = CountryAddForm()

    if form.validate_on_submit():

        new_country = Country()
        form.populate_obj(new_country)

        try:
            database.session.add(new_country)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding a new country to the database.", "danger")
            return redirect(url_for("add_country"))

        flash("{} ({}, {}) has been successfully added to the database.".format(new_country.name_display,
                                                                                new_country.name_full,
                                                                                new_country.get_name_short()), "success")
        return redirect(url_for("overview_countries"))

    return render_template("misc_countries_form.html",
                           title="Add country",
                           heading="Add country",
                           form=form)


# Edit competition
@cardb.route("/misc/competition/edit-competition/<id>", methods=['GET', 'POST'])
def edit_competition(id):

    competition = Competition.query.get(id)
    form = CompetitionEditForm(obj=competition)

    if form.validate_on_submit():

        form.populate_obj(competition)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing {} ({}, {}).".format(competition.name_display,
                                                                    competition.name_full,
                                                                    competition.name_short), "danger")
            return redirect(url_for("edit_competition", id=competition.id))

        flash("{} ({}, {}) has been successfully edited.".format(competition.name_display,
                                                                 competition.name_full,
                                                                 competition.name_short), "success")
        return redirect(url_for("detail_competition", id=competition.id))

    return render_template("misc_competitions_form.html",
                           title="Edit competition",
                           heading="Edit competition",
                           form=form)


# Edit country
@cardb.route("/misc/countries/edit-country/<id>", methods=['GET', 'POST'])
def edit_country(id):

    country = Country.query.get(id)
    form = CountryEditForm(obj=country)

    if form.validate_on_submit():

        form.populate_obj(country)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing {}.".format(country.name_display), "danger")
            return redirect(url_for("edit_country", id=country.id))

        flash("{} ({}, {}) has been successfully edited.".format(country.name_display,
                                                                 country.name_full,
                                                                 country.get_name_short()), "success")
        return redirect(url_for("detail_country", id=country.id))

    return render_template("misc_countries_form.html",
                           title="Edit country",
                           heading="Edit country",
                           form=form)


# Delete competition
@cardb.route("/misc/competition/delete-competition/<id>", methods=['GET', 'POST'])
def delete_competition(id):

    competition = Competition.query.get(id)

    try:
        database.session.delete(competition)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting {} ({}, {}).".format(competition.name_display,
                                                                      competition.name_full,
                                                                      competition.name_short), "danger")
        return redirect(url_for("detail_competition", id=competition.id))

    flash("{} ({}, {}) has been successfully deleted.".format(competition.name_display,
                                                              competition.name_full,
                                                              competition.name_short), "success")
    return redirect(url_for("overview_competitions"))


# Delete country
@cardb.route("/misc/countries/delete-country/<id>", methods=['GET', 'POST'])
def delete_country(id):

    country = Country.query.get(id)

    try:
        database.session.delete(country)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting {}.".format(country.name_display), "danger")
        return redirect(url_for("detail_country", id=country.id))

    flash("{} ({}, {}) has been successfully deleted.".format(country.name_display,
                                                              country.name_full,
                                                              country.get_name_short()), "success")
    return redirect(url_for("overview_countries"))


# Competition detail
@cardb.route("/misc/competitions/detail/<id>", methods=['GET', 'POST'])
def detail_competition(id):

    competition = Competition.query.get(id)

    return render_template("misc_competitions_detail.html",
                           title="{}".format(competition.name_display),
                           heading="{}".format(competition.name_full),
                           competition=competition)


# Country detail
@cardb.route("/misc/countries/detail/<id>", methods=['GET', 'POST'])
def detail_country(id):

    country = Country.query.get(id)
    cars = country.cars.all()
    locations = country.locations.all()

    return render_template("misc_countries_detail.html",
                           title="{}".format(country.name_display),
                           heading="{}".format(country.name_full),
                           country=country,
                           cars=cars,
                           locations=locations)
