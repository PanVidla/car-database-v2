from flask import render_template, flash, redirect, url_for

from general import cardb, database
from general.forms_parts import EngineCombustionAddForm, EngineElectricAddForm, EngineCombustionEditForm, \
    EngineElectricEditForm, EngineTypeAddForm, EngineTypeEditForm
from general.models.part import Engine, create_combustion_engine_from_form, create_electric_engine_from_form, \
    EngineCombustion, EngineElectric, CombustionEngineType, ElectricEngineType


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


# Engines types (combustion) overview
@cardb.route("/parts/engines/types/combustion", methods=['GET'])
def overview_engine_types_combustion():

    engine_types = CombustionEngineType.query.order_by(CombustionEngineType.name.asc()).all()

    return render_template("parts_overview_engine_types_combustion.html",
                           title="Engine types",
                           heading="Combustion engine types",
                           engine_types=engine_types,
                           viewing="engine_types")


# Engines types (electric) overview
@cardb.route("/parts/engines/types/electric", methods=['GET'])
def overview_engine_types_electric():

    engine_types = ElectricEngineType.query.order_by(ElectricEngineType.name.asc()).all()

    return render_template("parts_overview_engine_types_electric.html",
                           title="Engine types",
                           heading="Electric engine types",
                           engine_types=engine_types,
                           viewing="engine_types")


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


# Add engine type (combustion)
@cardb.route("/parts/engines/add-engine-type/combustion", methods=['GET', 'POST'])
def add_engine_type_combustion():

    form = EngineTypeAddForm()

    if form.validate_on_submit():

        new_engine_type = CombustionEngineType()
        form.populate_obj(new_engine_type)

        try:
            database.session.add(new_engine_type)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding new engine type to the database.", "danger")
            return redirect(url_for("add_engine_type_combustion"))

        flash("The {} engine type has been successfully added to the database.".format(new_engine_type.name), "success")
        return redirect(url_for("overview_engine_types_combustion"))

    return render_template("parts_form_engine_type.html",
                           title="Add engine type",
                           heading="Add combustion engine type",
                           form=form,
                           viewing="engine_types")


# Add engine type (electric)
@cardb.route("/parts/engines/add-engine-type/electric", methods=['GET', 'POST'])
def add_engine_type_electric():

    form = EngineTypeAddForm()

    if form.validate_on_submit():

        new_engine_type = ElectricEngineType()
        form.populate_obj(new_engine_type)

        try:
            database.session.add(new_engine_type)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding new engine type to the database.", "danger")
            return redirect(url_for("add_engine_type_electric"))

        flash("The {} engine type has been successfully added to the database.".format(new_engine_type.name), "success")
        return redirect(url_for("overview_engine_types_electric"))

    return render_template("parts_form_engine_type.html",
                           title="Add engine type",
                           heading="Add electric engine type",
                           form=form,
                           viewing="engine_types")


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


# Edit engine type (combustion)
@cardb.route("/parts/engines/edit-engine-type/combustion/<id>", methods=['GET', 'POST'])
def edit_engine_type_combustion(id):

    engine_type = CombustionEngineType.query.get(id)
    form = EngineTypeEditForm(obj=engine_type)

    if form.validate_on_submit():

        form.populate_obj(engine_type)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing {} engine type.".format(engine_type.name), "danger")
            return redirect(url_for("edit_engine_type_combustion", id=engine_type.id))

        flash("The engine type {} has been successfully edited.".format(engine_type.name), "success")
        return redirect(url_for("detail_engine_type_combustion", id=engine_type.id))

    return render_template("parts_form_engine_type.html",
                           title="Edit engine type",
                           heading="Edit combustion engine type",
                           form=form,
                           viewing="engines")


# Edit engine type (electric)
@cardb.route("/parts/engines/edit-engine-type/electric/<id>", methods=['GET', 'POST'])
def edit_engine_type_electric(id):

    engine_type = ElectricEngineType.query.get(id)
    form = EngineTypeEditForm(obj=engine_type)

    if form.validate_on_submit():

        form.populate_obj(engine_type)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing {} engine type.".format(engine_type.name), "danger")
            return redirect(url_for("edit_engine_type_electric", id=engine_type.id))

        flash("The engine type {} has been successfully edited.".format(engine_type.name), "success")
        return redirect(url_for("detail_engine_type_electric", id=engine_type.id))

    return render_template("parts_form_engine_type.html",
                           title="Edit engine type",
                           heading="Edit electric engine type",
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


# Delete engine type (combustion)
@cardb.route("/parts/engines/delete-engine-type/combustion/<id>", methods=['GET', 'POST'])
def delete_engine_type_combustion(id):

    engine_type = CombustionEngineType.query.get(id)

    try:
        database.session.delete(engine_type)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the {} engine type.".format(engine_type.name), "danger")
        return redirect(url_for("overview_engine_types_combustion", id=engine_type.id))

    flash("The engine type {} has been successfully deleted.".format(engine_type.name), "success")
    return redirect(url_for("overview_engine_types_combustion"))


# Delete engine type (electric)
@cardb.route("/parts/engines/delete-engine-type/electric/<id>", methods=['GET', 'POST'])
def delete_engine_type_electric(id):

    engine_type = ElectricEngineType.query.get(id)

    try:
        database.session.delete(engine_type)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the {} engine type.".format(engine_type.name), "danger")
        return redirect(url_for("overview_engine_types_electric", id=engine_type.id))

    flash("The engine type {} has been successfully deleted.".format(engine_type.name), "success")
    return redirect(url_for("overview_engine_types_electric"))


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


# Engine type detail (combustion)
@cardb.route("/parts/engines/detail/engine-type/combustion/<id>", methods=['GET', 'POST'])
def detail_engine_type_combustion(id):

    engine_type = CombustionEngineType.query.get(id)

    return render_template("parts_detail_engine_type_combustion.html",
                           title="{}".format(engine_type.name),
                           heading="{}".format(engine_type.name),
                           engine_type=engine_type,
                           viewing="engines")


# Engine type detail (electric)
@cardb.route("/parts/engines/detail/engine-type/electric/<id>", methods=['GET', 'POST'])
def detail_engine_type_electric(id):

    engine_type = ElectricEngineType.query.get(id)

    return render_template("parts_detail_engine_type_electric.html",
                           title="{}".format(engine_type.name),
                           heading="{}".format(engine_type.name),
                           engine_type=engine_type,
                           viewing="engines")
