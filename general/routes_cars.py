from datetime import datetime

from flask import render_template, flash, redirect, url_for

from general import cardb, database
from general.forms_cars import AssistAddForm, AssistEditForm, BodyStyleAddForm, BodyStyleEditForm, CarClassAddForm, \
    CarClassEditForm, DrivetrainAddForm, DrivetrainEditForm, EngineLayoutAddForm, EngineLayoutEditForm, FuelAddForm, \
    FuelEditForm, AspirationEditForm, AspirationAddForm, Car1Form, Car21Form, Car22Form, Car3Form, \
    Car4Form, Car5Form, Car6Form, Car7Form, Car8Form, CarAdd1Form, CarEdit1Form
from general.forms_info import TextForm
from general.models.car import Car, Assist, BodyStyle, CarClass, Drivetrain, EngineLayout, create_car_from_form, \
    CarManufacturer, CarCompetition, CarEngine, CarAssist, CarText
from general.models.part import FuelType, Aspiration


# Cars overview
@cardb.route("/cars", methods=['GET'])
@cardb.route("/cars/all", methods=['GET'])
def overview_cars():

    cars = Car.query.\
        filter(Car.is_deleted != True)\
        .order_by(Car.manufacturers_display.asc(), Car.year.asc(), Car.model.asc()).all()

    return render_template("cars_overview.html",
                           title="All cars",
                           heading="All cars",
                           cars=cars,
                           viewing="cars")


# Aspiration overview
@cardb.route("/cars/aspiration", methods=['GET'])
@cardb.route("/cars/aspiration/all", methods=['GET'])
def overview_aspiration():

    aspiration = Aspiration.query.order_by(Aspiration.id.asc()).all()

    return render_template("cars_overview_aspiration.html",
                           title="Aspiration",
                           heading="Aspiration",
                           aspiration_types=aspiration,
                           viewing="aspiration")


# Assists overview
@cardb.route("/cars/assists", methods=['GET'])
@cardb.route("/cars/assists/all", methods=['GET'])
def overview_assists():

    assists = Assist.query.order_by(Assist.name_short.asc()).all()

    return render_template("cars_overview_assists.html",
                           title="Assists",
                           heading="Assists",
                           assists=assists,
                           viewing="assists")


# Body styles overview
@cardb.route("/cars/body-styles", methods=['GET'])
@cardb.route("/cars/body-styles/all", methods=['GET'])
def overview_body_styles():

    body_styles = BodyStyle.query.order_by(BodyStyle.name.asc()).all()

    return render_template("cars_overview_body_styles.html",
                           title="Body styles",
                           heading="Body styles",
                           body_styles=body_styles,
                           viewing="body_styles")


# Car classes overview
@cardb.route("/cars/car-classes", methods=['GET'])
@cardb.route("/cars/car-classes/all", methods=['GET'])
def overview_car_classes():

    car_classes = CarClass.query.order_by(CarClass.name_custom.asc()).all()

    return render_template("cars_overview_car_classes.html",
                           title="Car classes",
                           heading="Car classes",
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


# Add car
# General information
@cardb.route("/cars/add-car/1", methods=['GET', 'POST'])
def add_car_1():

    form = CarAdd1Form()

    if form.validate_on_submit():

        new_car = create_car_from_form(form)

        try:
            database.session.add(new_car)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding the new car to the database.", "danger")
            return redirect(url_for("add_car_1"))

        flash("The {} has been successfully added to the database.".format(new_car.name_display), "success")

        new_car.set_manufacturers(form.primary_manufacturer.data, form.secondary_manufacturers.data)
        new_car.set_competitions(form.competitions_select.data)

        return redirect(url_for("add_car_2", id=new_car.id))

    return render_template("cars_form_1_general.html",
                           title="Add car",
                           heading="Add car",
                           form=form,
                           viewing="cars")


# Engine
@cardb.route("/cars/add-car/2/<id>", methods=['GET', 'POST'])
def add_car_2(id):

    car = Car.query.get(id)
    form_1_engine = Car21Form()
    form_2_skip = Car22Form()

    if form_1_engine.submit_existing_engine.data and form_1_engine.validate():

        car.set_engines(form_1_engine.engines.data)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem assigning engine(s) to the car.", "danger")
            return redirect(url_for("add_car_2"))

        flash("The selected engine(s) has been successfully assigned to the car.", "success")
        return redirect(url_for("add_car_3", id=car.id))

    if form_2_skip.submit_skip_engine.data:

        flash("Engine selection for this car has been skipped.", "info")
        return redirect(url_for("add_car_3", id=car.id))

    return render_template("cars_form_2_engine.html",
                           title="Add car",
                           heading="Add car",
                           form_1_engine=form_1_engine,
                           form_2_skip=form_2_skip,
                           viewing="cars")


# Forced induction
@cardb.route("/cars/add-car/3/<id>", methods=['GET', 'POST'])
def add_car_3(id):

    car = Car.query.get(id)
    form = Car3Form()

    if form.validate_on_submit():

        car.set_forced_induction(form.additional_forced_induction_id.data)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem assigning additional forced induction to the car.", "danger")
            return redirect(url_for("add_car_3"))

        flash("The selected forced induction has been successfully assigned to the car.", "success")
        return redirect(url_for("add_car_4", id=car.id))

    return render_template("cars_form_3_forced_induction.html",
                           title="Add car",
                           heading="Add car",
                           form=form,
                           viewing="cars")


# Actual power and torque output
@cardb.route("/cars/add-car/4/<id>", methods=['GET', 'POST'])
def add_car_4(id):

    car = Car.query.get(id)
    engines = car.engines.all()

    if engines:
        first_engine = engines[0]
        form = Car4Form(fuel_type_actual_id=first_engine.fuel_type_id,
                        max_power_output_kw_actual=first_engine.max_power_output_kw,
                        max_power_output_rpm_actual=first_engine.max_power_output_rpm,
                        max_torque_nm_actual=first_engine.max_torque_nm,
                        max_torque_rpm_actual=first_engine.max_torque_rpm)

    else:
        form = Car4Form()

    if form.validate_on_submit():

        form.populate_obj(car)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem assigning power values of the car.", "danger")
            return redirect(url_for("add_car_4"))

        flash("The values have been successfully assigned to the car.", "success")
        return redirect(url_for("add_car_5", id=car.id))

    return render_template("cars_form_4_power_values.html",
                           title="Add car",
                           heading="Add car",
                           form=form,
                           viewing="cars")


# Transmission and drivetrain
@cardb.route("/cars/add-car/5/<id>", methods=['GET', 'POST'])
def add_car_5(id):

    car = Car.query.get(id)
    form = Car5Form()

    if form.validate_on_submit():

        form.populate_obj(car)
        car.set_transmission(form)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem assigning transmission data of the car.", "danger")
            return redirect(url_for("add_car_5"))

        flash("The transmission for this car has been successfully set..", "success")
        return redirect(url_for("add_car_6", id=car.id))

    return render_template("cars_form_5_transmission.html",
                           title="Add car",
                           heading="Add car",
                           form=form,
                           viewing="cars")


# Platform
@cardb.route("/cars/add-car/6/<id>", methods=['GET', 'POST'])
def add_car_6(id):

    car = Car.query.get(id)
    form = Car6Form()

    if form.validate_on_submit():

        form.populate_obj(car)
        car.set_suspension(form)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem assigning platform to the car.", "danger")
            return redirect(url_for("add_car_6"))

        flash("The platform for this car has been successfully set.", "success")
        return redirect(url_for("add_car_7", id=car.id))

    return render_template("cars_form_6_platform.html",
                           title="Add car",
                           heading="Add car",
                           form=form,
                           viewing="cars")


# Performance
@cardb.route("/cars/add-car/7/<id>", methods=['GET', 'POST'])
def add_car_7(id):

    car = Car.query.get(id)
    form = Car7Form()

    if form.validate_on_submit():

        form.populate_obj(car)
        car.set_power_to_weight_ratio()

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem assigning performance data to the car.", "danger")
            return redirect(url_for("add_car_7"))

        flash("The performance data has been successfully set.", "success")
        return redirect(url_for("add_car_8", id=car.id))

    return render_template("cars_form_7_performance.html",
                           title="Add car",
                           heading="Add car",
                           form=form,
                           viewing="cars")


# Assists
@cardb.route("/cars/add-car/8/<id>", methods=['GET', 'POST'])
def add_car_8(id):

    car = Car.query.get(id)
    form = Car8Form()

    if form.validate_on_submit():

        car.set_assists(form.assists_select.data)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem assigning assists to the car.", "danger")
            return redirect(url_for("add_car_8"))

        flash("The creation of {} has been successfully completed.".format(car.name_display), "success")
        return redirect(url_for("overview_cars"))

    return render_template("cars_form_8_assists.html",
                           title="Add car",
                           heading="Add car",
                           form=form,
                           viewing="cars")


# Add aspiration
@cardb.route("/cars/aspiration/add-aspiration", methods=['GET', 'POST'])
def add_aspiration():

    form = AspirationAddForm()

    if form.validate_on_submit():

        new_aspiration = Aspiration()
        form.populate_obj(new_aspiration)

        try:
            database.session.add(new_aspiration)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding new aspiration to the database.", "danger")
            return redirect(url_for("add_aspiration"))

        flash("Aspiration \"{}\" has been successfully added to the database.".format(new_aspiration.name), "success")
        return redirect(url_for("overview_aspiration"))

    return render_template("cars_form_aspiration.html",
                           title="Add aspiration",
                           heading="Add aspiration",
                           form=form,
                           viewing="aspiration")


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


# Edit car (general)
@cardb.route("/cars/edit-car/<id>/general", methods=['GET', 'POST'])
def edit_car_general(id):

    car = Car.query.get(id)

    # Get manufacturers for the multiple select form
    primary_manufacturer = CarManufacturer.query.filter(CarManufacturer.car_id == car.id,
                                                        CarManufacturer.is_primary == True).first()
    secondary_manufacturers = CarManufacturer.query.filter(CarManufacturer.car_id == car.id,
                                                           CarManufacturer.is_primary == False).all()
    secondary_manufacturer_ids = []

    for secondary_manufactuer in secondary_manufacturers:
        secondary_manufacturer_ids += str(secondary_manufactuer.company_id)

    # Get competitions for the multiple select form
    competitions = CarCompetition.query.filter(CarCompetition.car_id == car.id).all()
    competition_ids = []

    for competition in competitions:
        competition_ids += str(competition.competition_id)

    form = CarEdit1Form(obj=car,
                        primary_manufacturer=primary_manufacturer.manufacturer.id,
                        secondary_manufacturers=secondary_manufacturer_ids,
                        competitions_select=competition_ids)

    if form.validate_on_submit():

        car.edit_car_from_form(form)
        car.set_manufacturers(form.primary_manufacturer.data, form.secondary_manufacturers.data)
        car.set_competitions(form.competitions_select.data)
        car.datetime_edited = datetime.utcnow()

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {}.".format(car.name_display), "danger")
            return redirect(url_for("edit_car_general", id=car.id))

        flash("The {}  has been successfully edited.".format(car.name_display), "success")
        return redirect(url_for("detail_car", id=car.id))

    return render_template("cars_form_1_general.html",
                           title="Edit car",
                           heading="Edit general information",
                           form=form,
                           viewing="car",
                           editing=True)


# Edit car (engine)
@cardb.route("/cars/edit-car/<id>/engine", methods=['GET', 'POST'])
def edit_car_engine(id):

    car = Car.query.get(id)

    # Get engine(s) for the multiple select form
    engines = CarEngine.query.filter(CarEngine.car_id == car.id).all()
    engine_ids = []

    for engine in engines:
        engine_ids += str(engine.engine_id)

    form = Car21Form(engines=engine_ids)

    if form.validate_on_submit():

        car.set_engines(form.engines.data)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {}.".format(car.name_display), "danger")
            return redirect(url_for("edit_car_engine", id=car.id))

        flash("The {}  has been successfully edited.".format(car.name_display), "success")
        return redirect(url_for("detail_car", id=car.id))

    return render_template("cars_form_2_engine.html",
                           title="Edit car",
                           heading="Edit engine(s)",
                           form_1_engine=form,
                           viewing="car",
                           editing=True)


# Edit car (forced induction)
@cardb.route("/cars/edit-car/<id>/forced-induction", methods=['GET', 'POST'])
def edit_car_forced_induction(id):

    car = Car.query.get(id)

    form = Car3Form(obj=car)

    if form.validate_on_submit():

        car.set_forced_induction(form.additional_forced_induction_id.data)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {}.".format(car.name_display), "danger")
            return redirect(url_for("edit_car_forced_induction", id=car.id))

        flash("The {} has been successfully edited.".format(car.name_display), "success")
        return redirect(url_for("detail_car", id=car.id))

    return render_template("cars_form_3_forced_induction.html",
                           title="Edit car",
                           heading="Edit forced induction",
                           form=form,
                           viewing="car",
                           editing=True)


# Edit car (power values)
@cardb.route("/cars/edit-car/<id>/power-values", methods=['GET', 'POST'])
def edit_car_power_values(id):

    car = Car.query.get(id)

    form = Car4Form(obj=car)

    if form.validate_on_submit():

        form.populate_obj(car)
        car.set_power_to_weight_ratio()

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {}.".format(car.name_display), "danger")
            return redirect(url_for("edit_car_power_values", id=car.id))

        flash("The {} has been successfully edited.".format(car.name_display), "success")
        return redirect(url_for("detail_car", id=car.id))

    return render_template("cars_form_4_power_values.html",
                           title="Edit car",
                           heading="Edit power values",
                           form=form,
                           viewing="car",
                           editing=True)


# Edit car (transmission)
@cardb.route("/cars/edit-car/<id>/transmission", methods=['GET', 'POST'])
def edit_car_transmission(id):

    car = Car.query.get(id)

    form = Car5Form(obj=car)

    if form.validate_on_submit():

        form.populate_obj(car)
        car.set_transmission(form)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {}.".format(car.name_display), "danger")
            return redirect(url_for("edit_car_transmission", id=car.id))

        flash("The {} has been successfully edited.".format(car.name_display), "success")
        return redirect(url_for("detail_car", id=car.id))

    return render_template("cars_form_5_transmission.html",
                           title="Edit car",
                           heading="Edit transmission",
                           form=form,
                           viewing="car",
                           editing=True)


# Edit car (platform)
@cardb.route("/cars/edit-car/<id>/platform", methods=['GET', 'POST'])
def edit_car_platform(id):

    car = Car.query.get(id)

    form = Car6Form(obj=car)

    if form.validate_on_submit():

        form.populate_obj(car)
        car.set_power_to_weight_ratio()
        car.set_suspension(form)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {}.".format(car.name_display), "danger")
            return redirect(url_for("edit_car_platform", id=car.id))

        flash("The {}  has been successfully edited.".format(car.name_display), "success")
        return redirect(url_for("detail_car", id=car.id))

    return render_template("cars_form_6_platform.html",
                           title="Edit car",
                           heading="Edit platform",
                           form=form,
                           viewing="car",
                           editing=True)


# Edit car (performance)
@cardb.route("/cars/edit-car/<id>/performance", methods=['GET', 'POST'])
def edit_car_performance(id):

    car = Car.query.get(id)

    form = Car7Form(obj=car)

    if form.validate_on_submit():

        form.populate_obj(car)
        car.datetime_edited = datetime.utcnow()

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {}.".format(car.name_display), "danger")
            return redirect(url_for("edit_car_performance", id=car.id))

        flash("The {} has been successfully edited.".format(car.name_display), "success")
        return redirect(url_for("detail_car", id=car.id))

    return render_template("cars_form_7_performance.html",
                           title="Edit car",
                           heading="Edit performance",
                           form=form,
                           viewing="car",
                           editing=True)


# Edit car (assists)
@cardb.route("/cars/edit-car/<id>/assists", methods=['GET', 'POST'])
def edit_car_assists(id):

    car = Car.query.get(id)

    # Get assists for the multiple select form
    assists = CarAssist.query.filter(CarAssist.car_id == car.id).all()
    assists_ids = []

    for assist in assists:
        assists_ids += str(assist.assist_id)

    form = Car8Form(assists_select=assists_ids)

    if form.validate_on_submit():

        car.set_assists(form.assists_select.data)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the {}.".format(car.name_display), "danger")
            return redirect(url_for("edit_car_assists", id=car.id))

        flash("The {} has been successfully edited.".format(car.name_display), "success")
        return redirect(url_for("detail_car", id=car.id))

    return render_template("cars_form_8_assists.html",
                           title="Edit car",
                           heading="Edit assists",
                           form=form,
                           viewing="car",
                           editing=True)


# Edit aspiration
@cardb.route("/cars/aspiration/edit-aspiration/<id>", methods=['GET', 'POST'])
def edit_aspiration(id):

    aspiration = Aspiration.query.get(id)
    form = AspirationEditForm(obj=aspiration)

    if form.validate_on_submit():

        form.populate_obj(aspiration)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing aspiration \"{}\".".format(aspiration.name), "danger")
            return redirect(url_for("edit_aspiration", id=aspiration.id))

        flash("Aspiration \"{}\" has been successfully edited.".format(aspiration.name), "success")
        return redirect(url_for("detail_aspiration", id=aspiration.id))

    return render_template("cars_form_aspiration.html",
                           title="Edit aspiration",
                           heading="Edit aspiration",
                           form=form,
                           viewing="aspiration")


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


# Delete car
@cardb.route("/cars/delete-car/<id>", methods=['GET', 'POST'])
def delete_car(id):

    car = Car.query.get(id)
    car.is_deleted = True

    try:
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the {}.".format(car.name_display), "danger")
        return redirect(url_for("detail_car", id=car.id))

    flash("The {} has been successfully deleted.".format(car.name_display), "success")
    return redirect(url_for("overview_cars"))


# Delete aspiration
@cardb.route("/cars/aspiration/delete-aspiration/<id>", methods=['GET', 'POST'])
def delete_aspiration(id):

    aspiration = Aspiration.query.get(id)

    try:
        database.session.delete(aspiration)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting aspiration \"{}\".".format(aspiration.name), "danger")
        return redirect(url_for("detail_aspiration", id=aspiration.id))

    flash("Aspiration \"{}\" has been successfully deleted.".format(aspiration.name), "success")
    return redirect(url_for("overview_aspiration"))


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


# Delete car text
@cardb.route("/cars/text/delete-text/<id>", methods=['GET', 'POST'])
def delete_car_text(id):

    text = CarText.query.get(id)

    try:
        database.session.delete(text)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the text.", "danger")
        return redirect(url_for("detail_car", id=text.car_id))

    flash("The text has been successfully deleted.", "success")
    return redirect(url_for("detail_car", id=text.car_id))


# Car detail
@cardb.route("/cars/detail/<id>", methods=['GET', 'POST'])
def detail_car(id):

    car = Car.query.get(id)
    add_text_form = TextForm()

    # Add text
    if add_text_form.submit_add_text.data and add_text_form.validate():

        new_text = CarText()
        add_text_form.populate_obj(new_text)
        new_text.order = len(car.texts.all()) + 1
        new_text.car_id = car.id

        car.datetime_edited = datetime.utcnow()

        try:
            database.session.add(new_text)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding text to {}.".format(car.name_display), "danger")
            return redirect(url_for("detail_car", id=car.id))

        flash("The text has been successfully added to {}.".format(car.name_display), "success")
        return redirect(url_for("detail_car", id=car.id))

    return render_template("cars_detail.html",
                           title="{}".format(car.name_display),
                           heading="{}".format(car.name_display),
                           car=car,
                           add_text_form=add_text_form,
                           viewing="cars")


# Aspiration detail
@cardb.route("/cars/aspiration/detail/<id>", methods=['GET', 'POST'])
def detail_aspiration(id):

    aspiration = Aspiration.query.get(id)

    return render_template("cars_detail_aspiration.html",
                           title="{}".format(aspiration.name),
                           heading="{}".format(aspiration.name),
                           aspiration=aspiration,
                           viewing="aspiration")


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
