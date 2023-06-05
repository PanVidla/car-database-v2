from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from sqlalchemy import or_

from general import cardb, database
from general.forms_info import TextForm, ImageForm
from general.forms_parts import EngineCombustionAddForm, EngineElectricAddForm, EngineCombustionEditForm, \
    EngineElectricEditForm, EngineTypeAddForm, EngineTypeEditForm, ForcedInductionAddForm, ForcedInductionEditForm, \
    SuspensionAddForm, TransmissionAddForm, TransmissionTypeAddForm, SuspensionEditForm, TransmissionEditForm, \
    TransmissionTypeEditForm
from general.models.car import Car
from general.models.instance import Instance
from general.models.part import Engine, create_combustion_engine_from_form, create_electric_engine_from_form, \
    EngineCombustion, EngineElectric, CombustionEngineType, ElectricEngineType, ForcedInduction, \
    create_forced_induction_from_form, Transmission, TransmissionType, Suspension, create_transmission_from_form, \
    EngineText, ForcedInductionText, SuspensionText, TransmissionText, EngineImage, ForcedInductionImage, \
    SuspensionImage, TransmissionImage, create_copy_from_combustion_engine, create_copy_from_electric_engine


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


# Forced induction overview
@cardb.route("/parts/forced-induction", methods=['GET'])
@cardb.route("/parts/forced-induction/all", methods=['GET'])
def overview_forced_induction():

    forced_induction_parts = ForcedInduction.query.order_by(ForcedInduction.name_display.asc()).all()

    return render_template("parts_overview_forced_induction.html",
                           title="Forced induction",
                           heading="All forced induction",
                           forced_induction_parts=forced_induction_parts,
                           viewing="forced_induction")


# Transmissions overview
@cardb.route("/parts/transmission", methods=['GET'])
@cardb.route("/parts/transmission/all", methods=['GET'])
def overview_transmissions():

    transmissions = Transmission.query.order_by(Transmission.name_display.asc()).all()

    return render_template("parts_overview_transmissions.html",
                           title="Transmissions",
                           heading="All transmissions",
                           transmissions=transmissions,
                           viewing="transmissions")


# Transmission types overview
@cardb.route("/parts/transmission/types", methods=['GET'])
@cardb.route("/parts/transmission/types/all", methods=['GET'])
def overview_transmission_types():

    transmission_types = TransmissionType.query.order_by(TransmissionType.name.asc()).all()

    return render_template("parts_overview_transmission_types.html",
                           title="Transmission types",
                           heading="All transmission types",
                           transmission_types=transmission_types,
                           viewing="transmission_types")


# Suspensions overview
@cardb.route("/parts/suspension", methods=['GET'])
@cardb.route("/parts/suspension/all", methods=['GET'])
def overview_suspensions():

    suspensions = Suspension.query.order_by(Suspension.name_full.asc()).all()

    return render_template("parts_overview_suspensions.html",
                           title="Suspension",
                           heading="All suspension",
                           suspensions=suspensions,
                           viewing="suspensions")


# Add engine (combustion)
@cardb.route("/parts/engines/add-engine/combustion", methods=['GET', 'POST'])
@login_required
def add_engine_combustion():

    form = EngineCombustionAddForm()

    if form.validate_on_submit():

        # Check if an engine of the same display name already exists in the database
        existing_combustion_engine = EngineCombustion.query.filter(EngineCombustion.name_display == form.name_display.data).first()

        if existing_combustion_engine is not None:
            flash("The {} already exists in the database.".format(existing_combustion_engine.name_display), "warning")
            return redirect(url_for("overview_engines"))

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
@login_required
def add_engine_electric():

    form = EngineElectricAddForm()

    if form.validate_on_submit():

        # Check if an engine of the same display name already exists in the database
        existing_electric_engine = EngineElectric.query.filter(
            EngineElectric.name_display == form.name_display.data).first()

        if existing_electric_engine is not None:
            flash("The {} already exists in the database.".format(existing_electric_engine.name_display), "warning")
            return redirect(url_for("overview_engines"))

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
@login_required
def add_engine_type_combustion():

    form = EngineTypeAddForm()

    if form.validate_on_submit():

        # Check if an engine type of the same name already exists in the database
        existing_combustion_engine_type = CombustionEngineType.query.filter(
            CombustionEngineType.name == form.name.data).first()

        if existing_combustion_engine_type is not None:
            flash("The \"{}\" engine type already exists in the database.".format(existing_combustion_engine_type.name), "warning")
            return redirect(url_for("overview_engine_types_combustion"))

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
@login_required
def add_engine_type_electric():

    form = EngineTypeAddForm()

    if form.validate_on_submit():

        # Check if an engine type of the same name already exists in the database
        existing_electric_engine_type = ElectricEngineType.query.filter(
            ElectricEngineType.name == form.name.data).first()

        if existing_electric_engine_type is not None:
            flash("The \"{}\" engine type already exists in the database.".format(existing_electric_engine_type.name),
                  "warning")
            return redirect(url_for("overview_engine_types_electric"))

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


# Add forced induction
@cardb.route("/parts/forced-induction/add-forced-induction", methods=['GET', 'POST'])
@login_required
def add_forced_induction():

    form = ForcedInductionAddForm()

    if form.validate_on_submit():

        # Check if forced induction of the same display name already exists in the database
        existing_forced_induction = ForcedInduction.query.filter(
            ForcedInduction.name_display == form.name_display.data).first()

        if existing_forced_induction is not None:
            flash("The {} already exists in the database.".format(existing_forced_induction.name_display), "warning")
            return redirect(url_for("overview_forced_induction"))

        new_forced_induction = create_forced_induction_from_form(form)

        try:
            database.session.add(new_forced_induction)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding new forced induction to the database.", "danger")
            return redirect(url_for("add_forced_induction"))

        flash("The {} has been successfully added to the database.".format(new_forced_induction.name_display), "success")
        return redirect(url_for("overview_forced_induction"))

    return render_template("parts_form_forced_induction.html",
                           title="Add forced induction",
                           heading="Add forced induction",
                           form=form,
                           viewing="forced_induction")


# Add suspension
@cardb.route("/parts/suspension/add-suspension", methods=['GET', 'POST'])
@login_required
def add_suspension():

    form = SuspensionAddForm()

    if form.validate_on_submit():

        # Check if suspension of the same name or with the same shortcut already exists in the database
        existing_suspension = Suspension.query.filter(or_(Suspension.name_full == form.name_full.data,
                                                          Suspension.name_short == form.name_short.data)).first()

        if existing_suspension is not None:
            flash("This kind of suspension or suspension with the same shortcut already exists in the database.", "warning")
            return redirect(url_for("overview_suspensions"))

        new_suspension = Suspension()
        form.populate_obj(new_suspension)

        try:
            database.session.add(new_suspension)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding new suspension to the database.", "danger")
            return redirect(url_for("add_suspension"))

        flash("The {} has been successfully added to the database.".format(new_suspension.name_full), "success")
        return redirect(url_for("overview_suspensions"))

    return render_template("parts_form_suspension.html",
                           title="Add suspension",
                           heading="Add suspension",
                           form=form,
                           viewing="suspensions")


# Add transmission
@cardb.route("/parts/transmission/add-transmission", methods=['GET', 'POST'])
@login_required
def add_transmission():

    form = TransmissionAddForm()

    if form.validate_on_submit():

        # Check if transmission of the same display name already exists in the database
        existing_transmission = Transmission.query.filter(
            Transmission.name_display == form.name_display.data).first()

        if existing_transmission is not None:
            flash("The {} already exists in the database.".format(existing_transmission.name_display), "warning")
            return redirect(url_for("overview_transmissions"))

        new_transmission = create_transmission_from_form(form)

        try:
            database.session.add(new_transmission)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding new transmission to the database.", "danger")
            return redirect(url_for("add_transmission"))

        flash("The {} has been successfully added to the database.".format(new_transmission.name_display), "success")
        return redirect(url_for("overview_transmissions"))

    return render_template("parts_form_transmission.html",
                           title="Add transmission",
                           heading="Add transmission",
                           form=form,
                           viewing="transmissions")


# Add transmission type
@cardb.route("/parts/transmission/add-transmission-type", methods=['GET', 'POST'])
@login_required
def add_transmission_type():

    form = TransmissionTypeAddForm()

    if form.validate_on_submit():

        # Check if transmission type of the same name already exists in the database
        existing_transmission_type = TransmissionType.query.filter(
            TransmissionType.name == form.name.data).first()

        if existing_transmission_type is not None:
            flash("The \"{}\" transmission type already exists in the database.".format(existing_transmission_type.name), "warning")
            return redirect(url_for("overview_transmission_types"))

        new_transmission_type = TransmissionType()
        form.populate_obj(new_transmission_type)

        try:
            database.session.add(new_transmission_type)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding a new transmission type to the database.", "danger")
            return redirect(url_for("add_transmission_type"))

        flash("The {} transmission type has been successfully added to the database.".format(new_transmission_type.name), "success")
        return redirect(url_for("overview_transmission_types"))

    return render_template("parts_form_transmission_type.html",
                           title="Add transmission type",
                           heading="Add transmission type",
                           form=form,
                           viewing="transmission_types")


# Edit engine (combustion)
@cardb.route("/parts/engines/edit-engine/combustion/<id>", methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
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
@login_required
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


# Edit forced induction
@cardb.route("/parts/forced-induction/edit-forced-induction/<id>", methods=['GET', 'POST'])
@login_required
def edit_forced_induction(id):

    forced_induction = ForcedInduction.query.get(id)
    form = ForcedInductionEditForm(obj=forced_induction)

    if form.validate_on_submit():

        forced_induction.edit_forced_induction_from_form(form)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing {}.".format(forced_induction.name_display), "danger")
            return redirect(url_for("edit_forced_induction", id=forced_induction.id))

        flash("The {} has been successfully edited.".format(forced_induction.name_display), "success")
        return redirect(url_for("detail_forced_induction", id=forced_induction.id))

    return render_template("parts_form_forced_induction.html",
                           title="Edit forced induction",
                           heading="Edit forced induction",
                           form=form,
                           viewing="forced_induction")


# Edit suspension
@cardb.route("/parts/suspension/edit-suspension/<id>", methods=['GET', 'POST'])
@login_required
def edit_suspension(id):

    suspension = Suspension.query.get(id)
    form = SuspensionEditForm(obj=suspension)

    if form.validate_on_submit():

        form.populate_obj(suspension)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {} suspension.".format(suspension.name_full), "danger")
            return redirect(url_for("edit_suspension", id=suspension.id))

        flash("The {} suspension has been successfully edited.".format(suspension.name_full), "success")
        return redirect(url_for("detail_suspension", id=suspension.id))

    return render_template("parts_form_suspension.html",
                           title="Edit suspension",
                           heading="Edit suspension",
                           form=form,
                           viewing="suspensions")


# Edit transmission
@cardb.route("/parts/transmission/edit-transmission/<id>", methods=['GET', 'POST'])
@login_required
def edit_transmission(id):

    transmission = Transmission.query.get(id)
    form = TransmissionEditForm(obj=transmission)

    if form.validate_on_submit():

        transmission.edit_transmission_from_form(form)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {} transmission.".format(transmission.name_display), "danger")
            return redirect(url_for("edit_transmission", id=transmission.id))

        flash("The {} transmission has been successfully edited.".format(transmission.name_display), "success")
        return redirect(url_for("detail_transmission", id=transmission.id))

    return render_template("parts_form_transmission.html",
                           title="Edit transmission",
                           heading="Edit transmission",
                           form=form,
                           viewing="transmissions")


# Edit transmission type
@cardb.route("/parts/transmission/edit-transmission-type/<id>", methods=['GET', 'POST'])
@login_required
def edit_transmission_type(id):

    transmission_type = TransmissionType.query.get(id)
    form = TransmissionTypeEditForm(obj=transmission_type)

    if form.validate_on_submit():

        form.populate_obj(transmission_type)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {} transmission type.".format(transmission_type.name), "danger")
            return redirect(url_for("edit_transmission_type", id=transmission_type.id))

        flash("The {} transmission type has been successfully edited.".format(transmission_type.name), "success")
        return redirect(url_for("detail_transmission_type", id=transmission_type.id))

    return render_template("parts_form_transmission_type.html",
                           title="Edit transmission type",
                           heading="Edit transmission type",
                           form=form,
                           viewing="transmission_types")


# Delete engine
@cardb.route("/parts/engines/delete-engine/<id>", methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
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


# Delete forced induction
@cardb.route("/parts/forced-induction/delete-forced-induction/<id>", methods=['GET', 'POST'])
@login_required
def delete_forced_induction(id):

    forced_induction = ForcedInduction.query.get(id)

    try:
        database.session.delete(forced_induction)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the {}.".format(forced_induction.name_display), "danger")
        return redirect(url_for("overview_forced_induction", id=forced_induction.id))

    flash("The {} has been successfully deleted.".format(forced_induction.name_display), "success")
    return redirect(url_for("overview_forced_induction"))


# Delete suspension
@cardb.route("/parts/suspension/delete-suspension/<id>", methods=['GET', 'POST'])
@login_required
def delete_suspension(id):

    suspension = Suspension.query.get(id)

    try:
        database.session.delete(suspension)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the {} suspension.".format(suspension.name_full), "danger")
        return redirect(url_for("overview_suspensions", id=suspension.id))

    flash("The {} suspension has been successfully deleted.".format(suspension.name_full), "success")
    return redirect(url_for("overview_suspensions"))


# Delete transmission
@cardb.route("/parts/transmission/delete-transmission/<id>", methods=['GET', 'POST'])
@login_required
def delete_transmission(id):

    transmission = Transmission.query.get(id)

    try:
        database.session.delete(transmission)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the {} transmission.".format(transmission.name_display), "danger")
        return redirect(url_for("overview_transmissions", id=transmission.id))

    flash("The {} transmission has been successfully deleted.".format(transmission.name_display), "success")
    return redirect(url_for("overview_transmissions"))


# Delete transmission type
@cardb.route("/parts/transmission/delete-transmission-type/<id>", methods=['GET', 'POST'])
@login_required
def delete_transmission_type(id):

    transmission_type = TransmissionType.query.get(id)

    try:
        database.session.delete(transmission_type)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the {} transmission type.".format(transmission_type.name), "danger")
        return redirect(url_for("overview_transmission_types", id=transmission_type.id))

    flash("The {} transmission type has been successfully deleted.".format(transmission_type.name), "success")
    return redirect(url_for("overview_transmission_types"))


# Delete engine text
@cardb.route("/parts/engines/text/delete-text/<id>", methods=['GET', 'POST'])
@login_required
def delete_engine_text(id):

    text = EngineText.query.get(id)

    try:
        database.session.delete(text)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the text.", "danger")
        return redirect(url_for("detail_engine", id=text.engine_id))

    flash("The text has been successfully deleted.", "success")
    return redirect(url_for("detail_engine", id=text.engine_id))


# Delete engine image
@cardb.route("/parts/engines/image/delete-image/<id>", methods=['GET', 'POST'])
@login_required
def delete_engine_image(id):

    image = EngineImage.query.get(id)

    try:
        database.session.delete(image)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the image.", "danger")
        return redirect(url_for("overview_engines", id=image.engine_id))

    flash("The image has been successfully deleted.", "success")

    # Re-align the order of images so that there is an image with order no. 1
    engine = Engine.query.get(image.engine_id)
    remaining_images = engine.get_images()

    counter = 1

    try:
        for image in remaining_images:

            image.order = counter
            counter += 1

            database.session.commit()

    except RuntimeError:
        flash("There was a problem with resetting the order of the remaining images.", "danger")
        return redirect(url_for("overview_engines", id=image.engine_id))

    flash("The remaining images had their order successfully reset.", "success")
    return redirect(url_for("overview_engines", id=image.engine_id))


# Delete forced induction text
@cardb.route("/parts/forced_induction/text/delete-text/<id>", methods=['GET', 'POST'])
@login_required
def delete_forced_induction_text(id):

    text = ForcedInductionText.query.get(id)

    try:
        database.session.delete(text)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the text.", "danger")
        return redirect(url_for("detail_forced_induction", id=text.forced_induction_id))

    flash("The text has been successfully deleted.", "success")
    return redirect(url_for("detail_forced_induction", id=text.forced_induction_id))


# Delete forced induction image
@cardb.route("/parts/forced_induction/image/delete-image/<id>", methods=['GET', 'POST'])
@login_required
def delete_forced_induction_image(id):

    image = ForcedInductionImage.query.get(id)

    try:
        database.session.delete(image)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the image.", "danger")
        return redirect(url_for("detail_forced_induction", id=image.forced_induction_id))

    flash("The image has been successfully deleted.", "success")

    # Re-align the order of images so that there is an image with order no. 1
    forced_induction = ForcedInduction.query.get(image.forced_induction_id)
    remaining_images = forced_induction.get_images()

    counter = 1

    try:
        for image in remaining_images:

            image.order = counter
            counter += 1

            database.session.commit()

    except RuntimeError:
        flash("There was a problem with resetting the order of the remaining images.", "danger")
        return redirect(url_for("detail_forced_induction", id=image.forced_induction_id))

    flash("The remaining images had their order successfully reset.", "success")
    return redirect(url_for("detail_forced_induction", id=image.forced_induction_id))


# Delete suspension text
@cardb.route("/parts/suspension/text/delete-text/<id>", methods=['GET', 'POST'])
@login_required
def delete_suspension_text(id):

    text = SuspensionText.query.get(id)

    try:
        database.session.delete(text)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the text.", "danger")
        return redirect(url_for("detail_suspension", id=text.suspension_id))

    flash("The text has been successfully deleted.", "success")
    return redirect(url_for("detail_suspension", id=text.suspension_id))


# Delete suspension image
@cardb.route("/parts/suspension/image/delete-image/<id>", methods=['GET', 'POST'])
@login_required
def delete_suspension_image(id):

    image = SuspensionImage.query.get(id)

    try:
        database.session.delete(image)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the image.", "danger")
        return redirect(url_for("detail_suspension", id=image.suspension_id))

    flash("The image has been successfully deleted.", "success")

    # Re-align the order of images so that there is an image with order no. 1
    suspension = Suspension.query.get(image.suspension_id)
    remaining_images = suspension.get_images()

    counter = 1

    try:
        for image in remaining_images:

            image.order = counter
            counter += 1

            database.session.commit()

    except RuntimeError:
        flash("There was a problem with resetting the order of the remaining images.", "danger")
        return redirect(url_for("detail_suspension", id=image.suspension_id))

    flash("The remaining images had their order successfully reset.", "success")
    return redirect(url_for("detail_suspension", id=image.suspension_id))


# Delete transmission text
@cardb.route("/parts/transmission/text/delete-text/<id>", methods=['GET', 'POST'])
@login_required
def delete_transmission_text(id):

    text = TransmissionText.query.get(id)

    try:
        database.session.delete(text)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the text.", "danger")
        return redirect(url_for("detail_transmission", id=text.transmission_id))

    flash("The text has been successfully deleted.", "success")
    return redirect(url_for("detail_transmission", id=text.transmission_id))


# Delete transmission image
@cardb.route("/parts/transmission/image/delete-image/<id>", methods=['GET', 'POST'])
@login_required
def delete_transmission_image(id):

    image = TransmissionImage.query.get(id)

    try:
        database.session.delete(image)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the image.", "danger")
        return redirect(url_for("detail_transmission", id=image.transmission_id))

    flash("The image has been successfully deleted.", "success")

    # Re-align the order of images so that there is an image with order no. 1
    transmission = Transmission.query.get(image.transmission_id)
    remaining_images = transmission.get_images()

    counter = 1

    try:
        for image in remaining_images:

            image.order = counter
            counter += 1

            database.session.commit()

    except RuntimeError:
        flash("There was a problem with resetting the order of the remaining images.", "danger")
        return redirect(url_for("detail_transmission", id=image.transmission_id))

    flash("The remaining images had their order successfully reset.", "success")
    return redirect(url_for("detail_transmission", id=image.transmission_id))


# Engine detail
@cardb.route("/parts/engines/detail/<id>", methods=['GET', 'POST'])
def detail_engine(id):

    # Try to get a combustion engine
    combustion_engine = EngineCombustion.query.filter(EngineCombustion.id == id).first()

    if combustion_engine is not None:
        return redirect(url_for("detail_engine_combustion", id=combustion_engine.id))

    # Try to get an electric engine
    electric_engine = EngineElectric.query.filter(EngineElectric.id == id).first()

    if electric_engine is not None:
        return redirect(url_for("detail_engine_electric", id=electric_engine.id))

    # Redirect back to the overview, if neither type is found
    else:
        flash("No engine with that ID was found.", "warning")
        return redirect(url_for("overview_engines"))


# Engine detail (combustion)
@cardb.route("/parts/engines/detail/combustion/<id>", methods=['GET', 'POST'])
@login_required
def detail_engine_combustion(id):

    engine = EngineCombustion.query.get(id)
    texts = EngineText.query \
        .filter(EngineText.engine_id == engine.id) \
        .order_by(EngineText.order.asc()) \
        .all()
    cars = Car.query \
        .filter(Car.is_deleted != True) \
        .filter(Car.engines.any(id=engine.id)) \
        .order_by(Car.manufacturers_display.asc(), Car.year.asc(), Car.model.asc()) \
        .all()
    instances = Instance.query \
        .filter(Instance.is_deleted != True) \
        .filter(Instance.assists.any(id=engine.id)) \
        .order_by(Instance.name_full) \
        .all()
    add_text_form = TextForm()
    add_image_form = ImageForm()

    # Add text
    if add_text_form.submit_add_text.data and add_text_form.validate():

        whole_text = add_text_form.content.data

        for paragraph in whole_text.splitlines():

            if paragraph == "":
                continue

            else:

                new_text = EngineText()
                new_text.content = paragraph
                new_text.text_type = add_text_form.text_type.data
                new_text.order = len(engine.texts.all()) + 1
                new_text.engine_id = engine.id

                try:
                    database.session.add(new_text)
                    database.session.commit()
                except RuntimeError:
                    flash("There was a problem adding text to {}.".format(engine.name_display), "danger")
                    return redirect(url_for("detail_engine_combustion", id=engine.id))

        flash("The text has been successfully added to {}.".format(engine.name_display), "success")
        return redirect(url_for("detail_engine_combustion", id=engine.id))

    # Add image
    if add_image_form.submit_add_image.data and add_image_form.validate():

        new_image = EngineImage()
        add_image_form.populate_obj(new_image)
        new_image.order = len(engine.images.all()) + 1
        new_image.engine_id = engine.id

        try:
            database.session.add(new_image)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding an image to {}.".format(engine.name_display), "danger")
            return redirect(url_for("detail_engine_combustion", id=engine.id))

        flash("The image has been successfully added to {}.".format(engine.name_display), "success")
        return redirect(url_for("detail_engine_combustion", id=engine.id))

    return render_template("parts_detail_engine_combustion.html",
                           title="{}".format(engine.name_display),
                           heading="{}".format(engine.name_display),
                           engine=engine,
                           texts=texts,
                           cars=cars,
                           instances=instances,
                           add_text_form=add_text_form,
                           add_image_form=add_image_form,
                           viewing="engines")


# Engine detail (electric)
@cardb.route("/parts/engines/detail/electric/<id>", methods=['GET', 'POST'])
@login_required
def detail_engine_electric(id):

    engine = EngineElectric.query.get(id)
    texts = EngineText.query \
        .filter(EngineText.engine_id == engine.id) \
        .order_by(EngineText.order.asc()) \
        .all()
    cars = Car.query \
        .filter(Car.is_deleted != True) \
        .filter(Car.engines.any(id=engine.id)) \
        .order_by(Car.manufacturers_display.asc(), Car.year.asc(), Car.model.asc()) \
        .all()
    instances = Instance.query \
        .filter(Instance.is_deleted != True) \
        .filter(Instance.assists.any(id=engine.id)) \
        .order_by(Instance.name_full) \
        .all()
    add_text_form = TextForm()
    add_image_form = ImageForm()

    # Add text
    if add_text_form.submit_add_text.data and add_text_form.validate():

        whole_text = add_text_form.content.data

        for paragraph in whole_text.splitlines():

            if paragraph == "":
                continue

            else:

                new_text = EngineText()
                new_text.content = paragraph
                new_text.text_type = add_text_form.text_type.data
                new_text.order = len(engine.texts.all()) + 1
                new_text.engine_id = engine.id

                try:
                    database.session.add(new_text)
                    database.session.commit()
                except RuntimeError:
                    flash("There was a problem adding text to {}.".format(engine.name_display), "danger")
                    return redirect(url_for("detail_engine_electric", id=engine.id))

        flash("The text has been successfully added to {}.".format(engine.name_display), "success")
        return redirect(url_for("detail_engine_electric", id=engine.id))

    # Add image
    if add_image_form.submit_add_image.data and add_image_form.validate():

        new_image = EngineImage()
        add_image_form.populate_obj(new_image)
        new_image.order = len(engine.images.all()) + 1
        new_image.engine_id = engine.id

        try:
            database.session.add(new_image)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding an image to {}.".format(engine.name_display), "danger")
            return redirect(url_for("detail_engine_electric", id=engine.id))

        flash("The image has been successfully added to {}.".format(engine.name_display), "success")
        return redirect(url_for("detail_engine_electric", id=engine.id))

    return render_template("parts_detail_engine_electric.html",
                           title="{}".format(engine.name_display),
                           heading="{}".format(engine.name_display),
                           engine=engine,
                           texts=texts,
                           cars=cars,
                           instances=instances,
                           add_text_form=add_text_form,
                           add_image_form=add_image_form,
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


# Forced induction detail
@cardb.route("/parts/forced-induction/detail/<id>", methods=['GET', 'POST'])
@login_required
def detail_forced_induction(id):

    forced_induction = ForcedInduction.query.get(id)
    texts = ForcedInductionText.query \
        .filter(ForcedInductionText.forced_induction_id == forced_induction.id) \
        .order_by(ForcedInductionText.order.asc()) \
        .all()
    cars = Car.query \
        .filter(Car.is_deleted != True) \
        .filter(Car.additional_forced_induction_id == forced_induction.id) \
        .order_by(Car.manufacturers_display.asc(), Car.year.asc(), Car.model.asc()) \
        .all()
    instances = Instance.query \
        .filter(Instance.is_deleted != True) \
        .filter(Instance.additional_forced_induction_id == forced_induction.id) \
        .order_by(Instance.name_full.asc()) \
        .all()
    add_text_form = TextForm()
    add_image_form = ImageForm()

    # Add text
    if add_text_form.submit_add_text.data and add_text_form.validate():

        whole_text = add_text_form.content.data

        for paragraph in whole_text.splitlines():

            if paragraph == "":
                continue

            else:

                new_text = ForcedInductionText()
                new_text.content = paragraph
                new_text.text_type = add_text_form.text_type.data
                new_text.order = len(forced_induction.texts.all()) + 1
                new_text.forced_induction_id = forced_induction.id

                try:
                    database.session.add(new_text)
                    database.session.commit()
                except RuntimeError:
                    flash("There was a problem adding text to {}.".format(forced_induction.name_display), "danger")
                    return redirect(url_for("detail_forced_induction", id=forced_induction.id))

        flash("The text has been successfully added to {}.".format(forced_induction.name_display), "success")
        return redirect(url_for("detail_forced_induction", id=forced_induction.id))

    # Add image
    if add_image_form.submit_add_image.data and add_image_form.validate():

        new_image = ForcedInductionImage()
        add_image_form.populate_obj(new_image)
        new_image.order = len(forced_induction.images.all()) + 1
        new_image.forced_induction_id = forced_induction.id

        try:
            database.session.add(new_image)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding an image to {}.".format(forced_induction.name_display), "danger")
            return redirect(url_for("detail_forced_induction", id=forced_induction.id))

        flash("The image has been successfully added to {}.".format(forced_induction.name_display), "success")
        return redirect(url_for("detail_forced_induction", id=forced_induction.id))

    return render_template("parts_detail_forced_induction.html",
                           title="{}".format(forced_induction.name_display),
                           heading="{}".format(forced_induction.name_display),
                           forced_induction=forced_induction,
                           texts=texts,
                           cars=cars,
                           instances=instances,
                           add_text_form=add_text_form,
                           add_image_form=add_image_form,
                           viewing="forced_induction")


# Suspension detail
@cardb.route("/parts/suspension/detail/<id>", methods=['GET', 'POST'])
@login_required
def detail_suspension(id):

    suspension = Suspension.query.get(id)
    texts = SuspensionText.query \
        .filter(SuspensionText.suspension_id == suspension.id) \
        .order_by(SuspensionText.order.asc()) \
        .all()
    cars_front = Car.query \
        .filter(Car.is_deleted != True) \
        .filter(Car.suspension_front_id == suspension.id) \
        .order_by(Car.manufacturers_display.asc(), Car.year.asc(), Car.model.asc()) \
        .all()
    cars_rear = Car.query \
        .filter(Car.is_deleted != True) \
        .filter(Car.suspension_rear_id == suspension.id) \
        .order_by(Car.manufacturers_display.asc(), Car.year.asc(), Car.model.asc()) \
        .all()
    instances_front = Instance.query \
        .filter(Instance.is_deleted != True) \
        .filter(Instance.suspension_front_id == suspension.id) \
        .order_by(Instance.name_full.asc()) \
        .all()
    instances_rear = Instance.query \
        .filter(Instance.is_deleted != True) \
        .filter(Instance.suspension_rear_id == suspension.id) \
        .order_by(Instance.name_full.asc()) \
        .all()
    add_text_form = TextForm()
    add_image_form = ImageForm()

    # Add text
    if add_text_form.submit_add_text.data and add_text_form.validate():

        whole_text = add_text_form.content.data

        for paragraph in whole_text.splitlines():

            if paragraph == "":
                continue

            else:

                new_text = SuspensionText()
                new_text.content = paragraph
                new_text.text_type = add_text_form.text_type.data
                new_text.order = len(suspension.texts.all()) + 1
                new_text.suspension_id = suspension.id

                try:
                    database.session.add(new_text)
                    database.session.commit()
                except RuntimeError:
                    flash("There was a problem adding text to {}.".format(suspension.name_full), "danger")
                    return redirect(url_for("detail_suspension", id=suspension.id))

        flash("The text has been successfully added to {}.".format(suspension.name_full), "success")
        return redirect(url_for("detail_suspension", id=suspension.id))

    # Add image
    if add_image_form.submit_add_image.data and add_image_form.validate():

        new_image = SuspensionImage()
        add_image_form.populate_obj(new_image)
        new_image.order = len(suspension.images.all()) + 1
        new_image.suspension_id = suspension.id

        try:
            database.session.add(new_image)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding an image to {}.".format(suspension.name_full), "danger")
            return redirect(url_for("detail_suspension", id=suspension.id))

        flash("The image has been successfully added to {}.".format(suspension.name_full), "success")
        return redirect(url_for("detail_suspension", id=suspension.id))

    return render_template("parts_detail_suspension.html",
                           title="{}".format(suspension.name_full),
                           heading="{}".format(suspension.name_full),
                           suspension=suspension,
                           texts=texts,
                           cars_front=cars_front,
                           cars_rear=cars_rear,
                           instances_front=instances_front,
                           instances_rear=instances_rear,
                           add_text_form=add_text_form,
                           add_image_form=add_image_form,
                           viewing="suspensions")


# Transmission detail
@cardb.route("/parts/transmission/detail/<id>", methods=['GET', 'POST'])
@login_required
def detail_transmission(id):

    transmission = Transmission.query.get(id)
    texts = TransmissionText.query \
        .filter(TransmissionText.transmission_id == transmission.id) \
        .order_by(TransmissionText.order.asc()) \
        .all()
    cars = Car.query \
        .filter(Car.is_deleted != True) \
        .filter(Car.transmission_id == transmission.id) \
        .order_by(Car.manufacturers_display.asc(), Car.year.asc(), Car.model.asc()) \
        .all()
    instances = Instance.query \
        .filter(Instance.is_deleted != True) \
        .filter(Instance.transmission_id == transmission.id) \
        .order_by(Instance.name_full.asc()) \
        .all()
    add_text_form = TextForm()
    add_image_form = ImageForm()

    # Add text
    if add_text_form.submit_add_text.data and add_text_form.validate():

        whole_text = add_text_form.content.data

        for paragraph in whole_text.splitlines():

            if paragraph == "":
                continue

            else:

                new_text = TransmissionText()
                new_text.content = paragraph
                new_text.text_type = add_text_form.text_type.data
                new_text.order = len(transmission.texts.all()) + 1
                new_text.transmission_id = transmission.id

                try:
                    database.session.add(new_text)
                    database.session.commit()
                except RuntimeError:
                    flash("There was a problem adding text to {}.".format(transmission.name_display), "danger")
                    return redirect(url_for("detail_transmission", id=transmission.id))

        flash("The text has been successfully added to {}.".format(transmission.name_display), "success")
        return redirect(url_for("detail_transmission", id=transmission.id))

    # Add image
    if add_image_form.submit_add_image.data and add_image_form.validate():

        new_image = TransmissionImage()
        add_image_form.populate_obj(new_image)
        new_image.order = len(transmission.images.all()) + 1
        new_image.transmission_id = transmission.id

        try:
            database.session.add(new_image)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding an image to {}.".format(transmission.name_display), "danger")
            return redirect(url_for("detail_transmission", id=transmission.id))

        flash("The image has been successfully added to {}.".format(transmission.name_display), "success")
        return redirect(url_for("detail_transmission", id=transmission.id))

    return render_template("parts_detail_transmission.html",
                           title="{}".format(transmission.name_display),
                           heading="{}".format(transmission.name_display),
                           transmission=transmission,
                           texts=texts,
                           cars=cars,
                           instances=instances,
                           add_text_form=add_text_form,
                           add_image_form=add_image_form,
                           viewing="transmissions")


# Transmission type detail
@cardb.route("/parts/transmission/type/detail/<id>", methods=['GET', 'POST'])
def detail_transmission_type(id):

    transmission_type = TransmissionType.query.get(id)

    return render_template("parts_detail_transmission_type.html",
                           title="{}".format(transmission_type.name),
                           heading="{}".format(transmission_type.name),
                           transmission_type=transmission_type,
                           viewing="transmission_types")


# Combustion engine copy
@cardb.route("/parts/engines/copy-engine-combustion/<id>", methods=['GET', 'POST'])
@login_required
def copy_engine_combustion(id):

    create_copy_from_combustion_engine(id)

    flash("A copy of the combustion engine has been successfully created.", "success")
    return redirect(url_for("overview_engines"))


# Electric engine copy
@cardb.route("/parts/engines/copy-engine-electric/<id>", methods=['GET', 'POST'])
@login_required
def copy_engine_electric(id):

    create_copy_from_electric_engine(id)

    flash("A copy of the electric engine has been successfully created.", "success")
    return redirect(url_for("overview_engines"))
