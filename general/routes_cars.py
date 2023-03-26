from flask import render_template, flash, redirect, url_for

from general import cardb, database
from general.forms_cars import AssistAddForm, AssistEditForm, BodyStyleAddForm, BodyStyleEditForm, CarClassAddForm, \
    CarClassEditForm, DrivetrainAddForm, DrivetrainEditForm, EngineLayoutAddForm, EngineLayoutEditForm, FuelAddForm, \
    FuelEditForm
from general.models.car import Car, Assist, BodyStyle, CarClass, Drivetrain, EngineLayout
from general.models.part import FuelType


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


# Car classes overview
@cardb.route("/cars/car-classes", methods=['GET'])
@cardb.route("/cars/car-classes/all", methods=['GET'])
def overview_car_classes():

    car_classes = CarClass.query.order_by(CarClass.name_custom.asc()).all()

    return render_template("cars_overview_car_classes.html",
                           title="All car classes",
                           heading="All car classes",
                           car_classes=car_classes,
                           viewing="car_classes")


# Drivetrains overview
@cardb.route("/cars/drivetrains", methods=['GET'])
@cardb.route("/cars/drivetrains/all", methods=['GET'])
def overview_drivetrains():

    drivetrains = Drivetrain.query.order_by(Drivetrain.name_full.asc()).all()

    return render_template("cars_overview_drivetrains.html",
                           title="Drivetrains",
                           heading="Drivetrains",
                           drivetrains=drivetrains,
                           viewing="drivetrains")


# Engine layouts overview
@cardb.route("/cars/engine-layouts", methods=['GET'])
@cardb.route("/cars/engine-layouts/all", methods=['GET'])
def overview_engine_layouts():

    engine_layouts = EngineLayout.query.order_by(EngineLayout.name.asc()).all()

    return render_template("cars_overview_engine_layouts.html",
                           title="Engine layouts",
                           heading="Engine layouts",
                           engine_layouts=engine_layouts,
                           viewing="engine_layouts")


# Engine fuels
@cardb.route("/cars/fuels", methods=['GET'])
@cardb.route("/cars/fuels/all", methods=['GET'])
def overview_fuels():

    fuels = FuelType.query.order_by(FuelType.name.asc()).all()

    return render_template("cars_overview_fuels.html",
                           title="Fuels",
                           heading="Fuel types",
                           fuels=fuels,
                           viewing="fuels")


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


# Add car class
@cardb.route("/cars/car-classes/add-car-class", methods=['GET', 'POST'])
def add_car_class():

    form = CarClassAddForm()

    if form.validate_on_submit():

        new_car_class = CarClass()
        form.populate_obj(new_car_class)

        try:
            database.session.add(new_car_class)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding a new car class to the database.", "danger")
            return redirect(url_for("add_car_class"))

        flash("Car class \"{}\" has been successfully added to the database.".format(new_car_class.name_custom), "success")
        return redirect(url_for("overview_car_classes"))

    return render_template("cars_form_car_class.html",
                           title="Add car class",
                           heading="Add car class",
                           form=form,
                           viewing="car_classes")


# Add drivetrain
@cardb.route("/cars/drivetrains/add-drivetrain", methods=['GET', 'POST'])
def add_drivetrain():

    form = DrivetrainAddForm()

    if form.validate_on_submit():

        drivetrain = Drivetrain()
        form.populate_obj(drivetrain)

        try:
            database.session.add(drivetrain)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding a new drivetrain to the database.", "danger")
            return redirect(url_for("add_drivetrain"))

        flash("Drivetrain \"{}\" ({}) has been successfully added to the database.".format(drivetrain.name_full, drivetrain.name_short), "success")
        return redirect(url_for("overview_drivetrains"))

    return render_template("cars_form_drivetrain.html",
                           title="Drivetrains",
                           heading="Drivetrains",
                           form=form,
                           viewing="drivetrains")


# Add engine layout
@cardb.route("/cars/engine-layouts/add-engine-layout", methods=['GET', 'POST'])
def add_engine_layout():

    form = EngineLayoutAddForm()

    if form.validate_on_submit():

        new_engine_layout = EngineLayout()
        form.populate_obj(new_engine_layout)

        try:
            database.session.add(new_engine_layout)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding a new engine layout to the database.", "danger")
            return redirect(url_for("add_engine_layout"))

        flash("Engine layout \"{}\" has been successfully added to the database.".format(new_engine_layout.name), "success")
        return redirect(url_for("overview_engine_layouts"))

    return render_template("cars_form_engine_layout.html",
                           title="Add engine layout",
                           heading="Add engine layout",
                           form=form,
                           viewing="engine_layouts")


# Add fuel type
@cardb.route("/cars/fuels/add-fuel", methods=['GET', 'POST'])
def add_fuel():

    form = FuelAddForm()

    if form.validate_on_submit():

        new_fuel_type = FuelType()
        form.populate_obj(new_fuel_type)

        try:
            database.session.add(new_fuel_type)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding a new fuel type to the database.", "danger")
            return redirect(url_for("add_fuel"))

        flash("Fuel type \"{}\" has been successfully added to the database.".format(new_fuel_type.name), "success")
        return redirect(url_for("overview_fuels"))

    return render_template("cars_form_fuel.html",
                           title="Add fuel",
                           heading="Add fuel type",
                           form=form,
                           viewing="fuels")


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


# Edit car class
@cardb.route("/cars/car-classes/edit-car-class/<id>", methods=['GET', 'POST'])
def edit_car_class(id):

    car_class = CarClass.query.get(id)
    form = CarClassEditForm(obj=car_class)

    if form.validate_on_submit():

        form.populate_obj(car_class)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the \"{}\" car class.".format(car_class.name_custom), "danger")
            return redirect(url_for("edit_car_class", id=car_class.id))

        flash("The car class \"{}\" has been successfully edited.".format(car_class.name_custom), "success")
        return redirect(url_for("detail_car_class", id=car_class.id))

    return render_template("cars_form_car_class.html",
                           title="Edit car class",
                           heading="Edit car class",
                           form=form,
                           viewing="car_classes")


# Edit drivetrain
@cardb.route("/cars/drivetrains/edit-drivetrain/<id>", methods=['GET', 'POST'])
def edit_drivetrain(id):

    drivetrain = Drivetrain.query.get(id)
    form = DrivetrainEditForm(obj=drivetrain)

    if form.validate_on_submit():

        form.populate_obj(drivetrain)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the \"{}\" drivetrain.".format(drivetrain.name_full), "danger")
            return redirect(url_for("edit_drivetrain", id=drivetrain.id))

        flash("The drivetrain \"{}\" has been successfully edited.".format(drivetrain.name_full), "success")
        return redirect(url_for("detail_drivetrain", id=drivetrain.id))

    return render_template("cars_form_drivetrain.html",
                           title="Edit drivetrain",
                           heading="Edit drivetrain",
                           form=form,
                           viewing="drivetrains")


# Edit engine layout
@cardb.route("/cars/engine-layouts/edit-engine-layout/<id>", methods=['GET', 'POST'])
def edit_engine_layout(id):

    engine_layout = EngineLayout.query.get(id)
    form = EngineLayoutEditForm(obj=engine_layout)

    if form.validate_on_submit():

        form.populate_obj(engine_layout)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the \"{}\" engine layout.".format(engine_layout.name), "danger")
            return redirect(url_for("edit_engine_layout", id=engine_layout.id))

        flash("The engine layout \"{}\" has been successfully edited.".format(engine_layout.name), "success")
        return redirect(url_for("detail_engine_layout", id=engine_layout.id))

    return render_template("cars_form_engine_layout.html",
                           title="Edit engine layout",
                           heading="Edit engine layout",
                           form=form,
                           viewing="engine_layouts")


# Edit fuel type
@cardb.route("/cars/fuels/edit-fuel/<id>", methods=['GET', 'POST'])
def edit_fuel(id):

    fuel = FuelType.query.get(id)
    form = FuelEditForm(obj=fuel)

    if form.validate_on_submit():

        form.populate_obj(fuel)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the fuel \"{}\".".format(fuel.name), "danger")
            return redirect(url_for("edit_fuel", id=fuel.id))

        flash("The fuel \"{}\" has been successfully edited.".format(fuel.name), "success")
        return redirect(url_for("detail_fuel", id=fuel.id))

    return render_template("cars_form_fuel.html",
                           title="Edit fuel",
                           heading="Edit fuel type",
                           form=form,
                           viewing="fuels")


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


# Delete car class
@cardb.route("/cars/car-classes/delete-car-class/<id>", methods=['GET', 'POST'])
def delete_car_class(id):

    car_class = CarClass.query.get(id)

    try:
        database.session.delete(car_class)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the car class \"{}\".".format(car_class.name_custom), "danger")
        return redirect(url_for("detail_car_class", id=car_class.id))

    flash("The car class \"{}\" has been successfully deleted.".format(car_class.name_custom), "success")
    return redirect(url_for("overview_car_classes"))


# Delete drivetrain
@cardb.route("/cars/drivetrains/delete-drivetrain/<id>", methods=['GET', 'POST'])
def delete_drivetrain(id):

    drivetrain = Drivetrain.query.get(id)

    try:
        database.session.delete(drivetrain)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the drivetrain \"{}\".".format(drivetrain.name_full), "danger")
        return redirect(url_for("detail_drivetrain", id=drivetrain.id))

    flash("The drivetrain \"{}\" has been successfully deleted.".format(drivetrain.name_full), "success")
    return redirect(url_for("overview_drivetrains"))


# Delete engine layout
@cardb.route("/cars/engine-layouts/delete-engine-layout/<id>", methods=['GET', 'POST'])
def delete_engine_layout(id):

    engine_layout = EngineLayout.query.get(id)

    try:
        database.session.delete(engine_layout)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the engine layout \"{}\".".format(engine_layout.name), "danger")
        return redirect(url_for("detail_engine_layout", id=engine_layout.id))

    flash("The engine layout \"{}\" has been successfully deleted.".format(engine_layout.name), "success")
    return redirect(url_for("overview_engine_layout"))


# Delete fuel
@cardb.route("/cars/fuels/delete-fuel/<id>", methods=['GET', 'POST'])
def delete_fuel(id):

    fuel = FuelType.query.get(id)

    try:
        database.session.delete(fuel)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting \"{}\".".format(fuel.name), "danger")
        return redirect(url_for("detail_fuel", id=fuel.id))

    flash("The fuel \"{}\" has been successfully deleted.".format(fuel.name), "success")
    return redirect(url_for("overview_fuels"))


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


# Car class detail
@cardb.route("/cars/car-classes/detail/<id>", methods=['GET', 'POST'])
def detail_car_class(id):

    car_class = CarClass.query.get(id)

    return render_template("cars_detail_car_class.html",
                           title="{}".format(car_class.name_custom),
                           heading="{}".format(car_class.name_custom),
                           car_class=car_class,
                           viewing="car_classes")


# Drivetrain detail
@cardb.route("/cars/drivetrains/detail/<id>", methods=['GET', 'POST'])
def detail_drivetrain(id):

    drivetrain = Drivetrain.query.get(id)

    return render_template("cars_detail_drivetrain.html",
                           title="{}".format(drivetrain.name_short),
                           heading="{}".format(drivetrain.name_full),
                           drivetrain=drivetrain,
                           viewing="drivetrains")


# Engine layout detail
@cardb.route("/cars/engine-layouts/detail/<id>", methods=['GET', 'POST'])
def detail_engine_layout(id):

    engine_layout = EngineLayout.query.get(id)

    return render_template("cars_detail_engine_layout.html",
                           title="{}".format(engine_layout.name),
                           heading="{}".format(engine_layout.name),
                           engine_layout=engine_layout,
                           viewing="engine_layouts")


# Fuel type detail
@cardb.route("/cars/fuels/detail/<id>", methods=['GET', 'POST'])
def detail_fuel(id):

    fuel = FuelType.query.get(id)

    return render_template("cars_detail_fuel.html",
                           title="{}".format(fuel.name),
                           heading="{}".format(fuel.name),
                           fuel=fuel,
                           viewing="fuels")
