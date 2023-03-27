from flask import render_template, flash, redirect, url_for

from general import cardb, database
from general.forms_parts import EngineCombustionAddForm, EngineElectricAddForm, EngineCombustionEditForm, \
    EngineElectricEditForm
from general.models.part import Engine, create_combustion_engine_from_form, create_electric_engine_from_form, \
    EngineCombustion, EngineElectric


# Engines overview
@cardb.route("/parts/engines", methods=['GET'])
@cardb.route("/parts/engines/all", methods=['GET'])
def overview_engines():

    engines = Engine.query.order_by(Engine.fuel_type_id.asc(), Engine.name_display.asc()).all()

    return render_template("parts_overview_engines.html",
                           title="Engines",
                           heading="All engines",
                           engines=engines,
                           viewing="engines")


# Add engine (combustion)
@cardb.route("/parts/engines/add-engine/combustion", methods=['GET', 'POST'])
def add_engine_combustion():

    form = EngineCombustionAddForm()

    if form.validate_on_submit():

        new_engine = create_combustion_engine_from_form(form)

        try:
            database.session.add(new_engine)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding new engine to the database.", "danger")
            return redirect(url_for("add_engine_combustion"))

        flash("The {} has been successfully added to the database.".format(new_engine.name_display), "success")
        return redirect(url_for("overview_engines"))

    return render_template("parts_form_engine_combustion.html",
                           title="Add engine",
                           heading="Add combustion engine",
                           form=form,
                           viewing="engines")


# Add engine (electric)
@cardb.route("/parts/engines/add-engine/electric", methods=['GET', 'POST'])
def add_engine_electric():

    form = EngineElectricAddForm()

    if form.validate_on_submit():

        new_engine = create_electric_engine_from_form(form)

        try:
            database.session.add(new_engine)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding new engine to the database.", "danger")
            return redirect(url_for("add_engine_electric"))

        flash("The {} has been successfully added to the database.".format(new_engine.name_display), "success")
        return redirect(url_for("overview_engines"))

    return render_template("parts_form_engine_electric.html",
                           title="Add engine",
                           heading="Add electric engine",
                           form=form,
                           viewing="engines")


# Edit engine (combustion)
@cardb.route("/parts/engines/edit-engine/combustion/<id>", methods=['GET', 'POST'])
def edit_engine_combustion(id):

    engine = EngineCombustion.query.get(id)
    form = EngineCombustionEditForm(obj=engine)

    if form.validate_on_submit():

        engine.edit_combustion_engine_from_form(form)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing {}.".format(engine.name_display), "danger")
            return redirect(url_for("edit_engine_combustion", id=engine.id))

        flash("{} has been successfully edited.".format(engine.name_display), "success")
        return redirect(url_for("detail_engine_combustion", id=engine.id))

    return render_template("parts_form_engine_combustion.html",
                           title="Edit engine",
                           heading="Edit combustion engine",
                           form=form,
                           viewing="engines")


# Edit engine (electric)
@cardb.route("/parts/engines/edit-engine/electric/<id>", methods=['GET', 'POST'])
def edit_engine_electric(id):

    engine = EngineElectric.query.get(id)
    form = EngineElectricEditForm(obj=engine)

    if form.validate_on_submit():

        engine.edit_electric_engine_from_form(form)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing {}.".format(engine.name_display), "danger")
            return redirect(url_for("edit_engine_electric", id=engine.id))

        flash("{} has been successfully edited.".format(engine.name_display), "success")
        return redirect(url_for("detail_engine_electric", id=engine.id))

    return render_template("parts_form_engine_electric.html",
                           title="Edit engine",
                           heading="Edit electric engine",
                           form=form,
                           viewing="engines")


# Delete engine
@cardb.route("/parts/engines/delete-engine/<id>", methods=['GET', 'POST'])
def delete_engine(id):

    engine = Engine.query.get(id)

    try:
        database.session.delete(engine)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting {}.".format(engine.name_display), "danger")
        return redirect(url_for("overview_engines", id=engine.id))

    flash("{} has been successfully deleted.".format(engine.name_display), "success")
    return redirect(url_for("overview_engines"))


# Engine detail (combustion)
@cardb.route("/parts/engines/detail/combustion/<id>", methods=['GET', 'POST'])
def detail_engine_combustion(id):

    engine = EngineCombustion.query.get(id)

    return render_template("parts_detail_engine_combustion.html",
                           title="{}".format(engine.name_display),
                           heading="{}".format(engine.name_display),
                           engine=engine,
                           viewing="engines")


# Engine detail (electric)
@cardb.route("/parts/engines/detail/electric/<id>", methods=['GET', 'POST'])
def detail_engine_electric(id):

    engine = EngineElectric.query.get(id)

    return render_template("parts_detail_engine_electric.html",
                           title="{}".format(engine.name_display),
                           heading="{}".format(engine.name_display),
                           engine=engine,
                           viewing="engines")
