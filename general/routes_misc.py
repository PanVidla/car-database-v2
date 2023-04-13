# Overviews
from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from general import cardb, database
from general.forms_info import TextForm
from general.forms_misc import CountryAddForm, CountryEditForm, CompetitionAddForm, CompetitionEditForm
from general.models.car import Car
from general.models.misc import Country, Competition, CompetitionText, CountryText


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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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


# Delete competition text
@cardb.route("/misc/competitions/text/delete-text/<id>", methods=['GET', 'POST'])
@login_required
def delete_competition_text(id):

    text = CompetitionText.query.get(id)

    try:
        database.session.delete(text)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the text.", "danger")
        return redirect(url_for("detail_competition", id=text.competition_id))

    flash("The text has been successfully deleted.", "success")
    return redirect(url_for("detail_competition", id=text.competition_id))


# Delete country text
@cardb.route("/misc/countries/text/delete-text/<id>", methods=['GET', 'POST'])
@login_required
def delete_country_text(id):

    text = CountryText.query.get(id)

    try:
        database.session.delete(text)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the text.", "danger")
        return redirect(url_for("detail_country", id=text.country_id))

    flash("The text has been successfully deleted.", "success")
    return redirect(url_for("detail_country", id=text.country_id))


# Competition detail
@cardb.route("/misc/competitions/detail/<id>", methods=['GET', 'POST'])
@login_required
def detail_competition(id):

    competition = Competition.query.get(id)
    cars = Car.query \
        .filter(Car.is_deleted != True) \
        .filter(Car.competitions.any(id=competition.id)) \
        .order_by(Car.manufacturers_display.asc(), Car.year.asc(), Car.model.asc()) \
        .all()
    texts = CompetitionText.query \
        .filter(CompetitionText.competition_id == competition.id) \
        .order_by(CompetitionText.order.asc()) \
        .all()
    add_text_form = TextForm()

    # Add text
    if add_text_form.submit_add_text.data and add_text_form.validate():

        new_text = CompetitionText()
        add_text_form.populate_obj(new_text)
        new_text.order = len(competition.texts.all()) + 1
        new_text.competition_id = competition.id

        try:
            database.session.add(new_text)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding text to {}.".format(competition.name_display), "danger")
            return redirect(url_for("detail_competition", id=competition.id))

        flash("The text has been successfully added to {}.".format(competition.name_display), "success")
        return redirect(url_for("detail_competition", id=competition.id))

    return render_template("misc_competitions_detail.html",
                           title="{}".format(competition.name_display),
                           heading="{}".format(competition.name_full),
                           competition=competition,
                           cars=cars,
                           texts=texts,
                           add_text_form=add_text_form)


# Country detail
@cardb.route("/misc/countries/detail/<id>", methods=['GET', 'POST'])
@login_required
def detail_country(id):

    country = Country.query.get(id)
    cars = Car.query \
        .filter(Car.is_deleted != True) \
        .filter(Car.country_id == country.id) \
        .order_by(Car.manufacturers_display.asc(), Car.year.asc(), Car.model.asc()) \
        .all()
    texts = CountryText.query \
        .filter(CountryText.country_id == country.id) \
        .order_by(CountryText.order.asc()) \
        .all()
    locations = country.locations.all()
    add_text_form = TextForm()

    # Add text
    if add_text_form.submit_add_text.data and add_text_form.validate():

        new_text = CountryText()
        add_text_form.populate_obj(new_text)
        new_text.order = len(country.texts.all()) + 1
        new_text.country_id = country.id

        try:
            database.session.add(new_text)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding text to {}.".format(country.name_display), "danger")
            return redirect(url_for("detail_country", id=country.id))

        flash("The text has been successfully added to {}.".format(country.name_display), "success")
        return redirect(url_for("detail_country", id=country.id))

    return render_template("misc_countries_detail.html",
                           title="{}".format(country.name_display),
                           heading="{}".format(country.name_full),
                           country=country,
                           texts=texts,
                           cars=cars,
                           locations=locations,
                           add_text_form=add_text_form)
