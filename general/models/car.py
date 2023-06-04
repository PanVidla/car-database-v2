from datetime import datetime

from flask import flash, redirect, url_for
from sqlalchemy.orm import backref

from general import database
from general.models.info import Text, Image
from general.models.misc import Company, Competition
from general.models.part import Engine, EngineCombustion, EngineElectric


# Car
# Represents a real-world car
class Car(database.Model):

    __tablename__ = "cars"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)
    datetime_added = database.Column(database.DateTime, default=datetime.utcnow, index=True, nullable=False)
    datetime_edited = database.Column(database.DateTime, default=datetime.utcnow, index=True, nullable=False)
    is_deleted = database.Column(database.Boolean, default=False, index=True, nullable=False)

    # General
    year = database.Column(database.Integer, index=True, nullable=True)
    manufacturers = database.relationship('Company', secondary="car_manufacturer")
    manufacturers_display = database.Column(database.Unicode, index=True, nullable=False)
    model = database.Column(database.Unicode, index=True, nullable=False)
    name_display = database.Column(database.Unicode, index=True, nullable=False, unique=True)
    name_short = database.Column(database.Unicode, nullable=True)
    country_id = database.Column(database.Integer, database.ForeignKey("countries.id"), nullable=True)
    is_prototype = database.Column(database.Boolean, default=False, index=True, nullable=False)
    is_fictional = database.Column(database.Boolean, default=False, index=True, nullable=False)
    competitions = database.relationship('Competition', secondary="car_competition")
    car_class_id = database.Column(database.Integer, database.ForeignKey("car_classes.id"), index=True, nullable=True)
    body_style_id = database.Column(database.Integer, database.ForeignKey("body_styles.id"), index=True, nullable=False)

    # Technical
    # Engine
    engines = database.relationship('Engine', secondary="car_engine", lazy='dynamic')
    fuel_type_actual_id = database.Column(database.Integer, database.ForeignKey("fuel_types.id"), index=True,
                                          nullable=True)
    max_power_output_kw_actual = database.Column(database.Double, index=True, nullable=True)
    max_power_output_rpm_actual = database.Column(database.Integer, nullable=True)
    max_torque_nm_actual = database.Column(database.Double, index=True, nullable=True)
    max_torque_rpm_actual = database.Column(database.Integer, nullable=True)
    # This refers to the specific car part
    additional_forced_induction_id = database.Column(database.Integer, database.ForeignKey("forced_induction.id"),
                                                     nullable=True)

    # Drivetrain
    # This refers to the actual transmission car part and may backfill the following two values
    transmission_id = database.Column(database.Integer, database.ForeignKey("transmissions.id"), nullable=True)
    transmission_type_actual_id = database.Column(database.Integer, database.ForeignKey("transmission_types.id"),
                                                  nullable=True)
    no_of_gears_actual = database.Column(database.Integer, index=True, nullable=True)
    engine_layout_id = database.Column(database.Integer, database.ForeignKey("engine_layouts.id"), index=True,
                                       nullable=False)
    drivetrain_id = database.Column(database.Integer, database.ForeignKey("drivetrains.id"), index=True, nullable=False)

    # Platform
    suspension_front_id = database.Column(database.Integer, database.ForeignKey("suspension.id"), index=True, nullable=True)
    suspension_rear_id = database.Column(database.Integer, database.ForeignKey("suspension.id"), index=True, nullable=True)
    curb_weight_kg = database.Column(database.Double, index=True, nullable=True)
    weight_distribution = database.Column(database.Double, index=True, nullable=True)
    tires_front = database.Column(database.Unicode, nullable=True)
    tires_rear = database.Column(database.Unicode, nullable=True)

    # Performance
    acceleration_0_to_100_kmh_sec = database.Column(database.Double, index=True, nullable=True)
    maximum_speed_kmh = database.Column(database.Double, index=True, nullable=True)
    power_to_weight_ratio = database.Column(database.Double, index=True, nullable=True)

    # Miscellaneous
    assists = database.relationship('Assist', secondary="car_assist")

    # Statistics
    no_of_instances = database.Column(database.Integer, default=0, index=True, nullable=False)

    # Relationships
    instances = database.relationship('Instance', backref='car', lazy='dynamic')
    texts = database.relationship('CarText', backref='car', lazy='dynamic')
    images = database.relationship('CarImage', backref='car', lazy='dynamic')

    def edit_car_from_form(self, form):

        form.populate_obj(self)

        # Set manufacturers display string
        primary_manufacturer = Company.query.get(form.primary_manufacturer.data)
        secondary_manufacturers = []

        for manufacturer_id in form.secondary_manufacturers.data:
            manufacturer = Company.query.filter(Company.id == manufacturer_id)
            secondary_manufacturers += manufacturer

        manufacturers_display_string = primary_manufacturer.name_display

        for secondary_manufacturer in secondary_manufacturers:
            manufacturers_display_string += " / {}".format(secondary_manufacturer.name_display)

        self.manufacturers_display = manufacturers_display_string

        # If no country is selected
        if form.country_id.data == 0:
            self.country_id = None

    def get_acceleration_0_to_100_kmh_sec(self):
        return "{} s".format(self.acceleration_0_to_100_kmh_sec) if self.acceleration_0_to_100_kmh_sec is not None else "n/a"

    def get_assists(self):

        if self.assists:

            assists = ""
            counter = 1

            for assist in self.assists:

                if counter > 1:
                    assists += ", {}".format(assist.name_short)

                else:
                    assists += "{}".format(assist.name_short)

                counter += 1

            return assists

        else:
            return "none"

    def get_car_class(self):
        return self.car_class.name_custom if self.car_class_id is not None else "n/a"

    def get_competitions(self):

        if self.competitions:

            competitions = ""
            counter = 1

            for competition in self.competitions:

                if counter > 1:
                    competitions += ", {}".format(competition.name_display)

                else:
                    competitions += "{}".format(competition.name_display)

                counter += 1

            return competitions

        else:
            return "none"

    def get_country(self):
        return self.country.name_display if self.country_id is not None else "n/a"

    def get_curb_weight_kg(self):
        return "{} kg".format(self.curb_weight_kg) if self.curb_weight_kg is not None else "n/a"

    def get_datetime_added(self):
        return "{}".format(self.datetime_added.strftime("%d.%m.%Y %H:%M:%S")) if self.datetime_added is not None else "n/a"

    def get_datetime_edited(self):
        return "{}".format(self.datetime_edited.strftime("%d.%m.%Y %H:%M:%S")) if self.datetime_edited is not None else "n/a"

    def get_drivetrain(self):
        return self.drivetrain.name_short if self.drivetrain_id != 0 else "n/a"

    def get_engines(self):

        engines = []

        for engine in self.engines:
            engines.append(engine)

        return engines

    def get_engine_layout(self):
        return self.engine_layout.name if self.engine_layout_id != 0 else "n/a"

    def get_combustion_engines(self):

        engines = self.get_engines()
        combustion_engines = []

        counter = 0

        for engine in engines:
            combustion_engine = EngineCombustion.query.get(engine.id)
            if combustion_engine is not None:
                counter += 1
                combustion_engines.append([combustion_engine, counter])

        return combustion_engines

    def get_electric_engines(self):

        engines = self.get_engines()
        electric_engines = []

        counter = 0

        for engine in engines:
            electric_engine = EngineElectric.query.get(engine.id)
            if electric_engine is not None:
                counter += 1
                electric_engines.append([electric_engine, counter])

        return electric_engines

    def get_fuel_type_name(self):

        if self.fuel_type_actual_id is not None:
            return self.fuel_type.name
        else:
            engines = self.get_engines()
            if engines:
                first_engine = engines[0]
                return first_engine.fuel_type.name
            else:
                return "n/a"

    def get_images(self):

        images = CarImage.query.filter(CarImage.car_id == self.id, CarImage.is_thumbnail == False)
        images = images.order_by(CarImage.order.asc()).all()

        return images

    def get_is_fictional(self):
        return "✓" if self.is_fictional else "x"

    def get_is_prototype(self):
        return "✓" if self.is_prototype else "x"

    def get_manufacturers(self):

        manufacturers = []

        primary_manufacturer = CarManufacturer.query.filter(CarManufacturer.car_id == self.id,
                                                            CarManufacturer.is_primary == True).first()
        secondary_manufacturers = CarManufacturer.query.filter(CarManufacturer.car_id == self.id,
                                                               CarManufacturer.is_primary == False).all()

        manufacturers.append(primary_manufacturer)
        for manufacturer in secondary_manufacturers:
            manufacturers.append(manufacturer)

        return manufacturers

    def get_maximum_power_kw(self):

        maximum_power_string = ""

        if self.max_power_output_kw_actual is not None:
            maximum_power_string += "{} kW".format(self.max_power_output_kw_actual)

            if self.max_power_output_rpm_actual is not None:
                maximum_power_string += " @ {} RPM".format(self.max_power_output_rpm_actual)

        else:
            maximum_power_string = "n/a"

        return maximum_power_string

    def get_maximum_speed_kmh(self):
        return "{} km/h".format(self.maximum_speed_kmh) if self.maximum_speed_kmh is not None else "n/a"

    def get_maximum_torque_nm(self):

        maximum_torque_string = ""

        if self.max_torque_nm_actual is not None:
            maximum_torque_string += "{} N⋅m".format(self.max_torque_nm_actual)

            if self.max_torque_rpm_actual is not None:
                maximum_torque_string += " @ {} RPM".format(self.max_torque_rpm_actual)

        else:
            maximum_torque_string = "n/a"

        return maximum_torque_string

    def get_name_short(self):
        return self.name_short if self.name_short != "" else "n/a"

    def get_no_of_engines(self):
        return len(self.get_engines())

    def get_no_of_combustion_engines(self):
        return len(self.get_combustion_engines())

    def get_no_of_electric_engines(self):
        return len(self.get_electric_engines())

    def get_no_of_gears_actual(self):
        return self.no_of_gears_actual if self.no_of_gears_actual is not None else "n/a"

    def get_power_to_weight_ratio(self):
        return "%.2f" % round(self.power_to_weight_ratio, 2) if self.power_to_weight_ratio is not None else "n/a"

    def get_suspension_front(self):
        return self.front_suspension.name_full if self.suspension_front_id is not None else "n/a"

    def get_suspension_rear(self):
        return self.rear_suspension.name_full if self.suspension_rear_id is not None else "n/a"

    def get_thumbnails(self):

        thumbnails = CarImage.query.filter(Car.car_id == self.id, CarImage.is_thumbnail == True)
        thumbnails = thumbnails.order_by(CarImage.order.asc()).all()

        return thumbnails

    def get_tires_front(self):
        return self.tires_front if self.tires_front != "" else "n/a"

    def get_tires_rear(self):
        return self.tires_rear if self.tires_rear != "" else "n/a"

    def get_transmission_type_actual(self):
        return self.transmission_type.name if self.transmission_type_actual_id is not None else "n/a"

    def get_weight_distribution(self):

        if self.weight_distribution is not None:

            weight_front = self.weight_distribution
            weight_rear = 100 - weight_front
            return "{} / {} %".format(weight_front, weight_rear)

        else:
            return "n/a"

    def get_year(self):
        return self.year if self.year is not None or "" else "n/a"

    def set_assists(self, assists_ids):

        # Delete the old car-assist associations
        car_assist_old = CarAssist.query.filter(CarAssist.car_id == self.id).all()

        for car_assist_association in car_assist_old:

            try:
                database.session.delete(car_assist_association)

            except RuntimeError:
                flash("There was a problem deleting an old association between {} and {}.".format(self.name_display,
                                                                                                  car_assist_association.assist.name_short),
                      "danger")

            database.session.commit()

        # Create new car-asssist associations
        for assist_id in assists_ids:

            try:
                car_assist_association = CarAssist(car_id=self.id, assist_id=assist_id)
                database.session.add(car_assist_association)

            except RuntimeError:
                assist = Assist.query.get(assist_id)
                flash("There was a problem adding a new association between {} and {}.".format(self.name_display,
                                                                                               assist.short),
                      "danger")

        database.session.commit()

        self.datetime_edited = datetime.utcnow()

    def set_engines(self, engine_ids):

        # Delete the old car-engine associations
        car_engine_old = CarEngine.query.filter(CarEngine.car_id == self.id).all()

        for car_engine_association in car_engine_old:

            try:
                database.session.delete(car_engine_association)

            except RuntimeError:
                flash("There was a problem deleting an old association between {} and {}.".format(self.name_display,
                                                                                                  car_engine_association.engine.name_display),
                      "danger")

            database.session.commit()

        # Create new car-engine associations
        for engine_id in engine_ids:

            try:
                car_engine_association = CarEngine(car_id=self.id, engine_id=engine_id)
                database.session.add(car_engine_association)

            except RuntimeError:
                engine = Engine.query.get(engine_id)
                flash("There was a problem adding a new association between {} and {}.".format(self.name_display,
                                                                                               engine.name_display),
                      "danger")

        database.session.commit()

        self.datetime_edited = datetime.utcnow()

    def set_forced_induction(self, forced_induction_id):

        if forced_induction_id == 0:
            self.additional_forced_induction_id = None

        else:
            self.additional_forced_induction_id = forced_induction_id

    def set_competitions(self, competition_ids):

        # Delete the old car-manufacturer associations
        car_competition_old = CarCompetition.query.filter(CarCompetition.car_id == self.id).all()

        for car_competition_association in car_competition_old:

            try:
                database.session.delete(car_competition_association)

            except RuntimeError:
                flash("There was a problem deleting an old association between {} and {}.".format(self.name_display,
                                                                                                  car_competition_association.competition.name_display),
                      "danger")

            database.session.commit()

        # Create new car-competition associations
        for competition_id in competition_ids:

            try:
                car_competition_association = CarCompetition(car_id=self.id, competition_id=competition_id)
                database.session.add(car_competition_association)

            except RuntimeError:
                competition = Competition.query.get(competition_id)
                flash("There was a problem adding a new association between {} and {}.".format(self.name_display,
                                                                                               competition.name_display),
                      "danger")

        database.session.commit()

        self.datetime_edited = datetime.utcnow()

    def set_manufacturers(self, primary_manufacturer_id, secondary_manufacturer_ids):

        # Delete the old car-manufacturer associations
        car_manufacturer_old = CarManufacturer.query.filter(CarManufacturer.car_id == self.id).all()

        for car_manufacturer_association in car_manufacturer_old:

            try:
                database.session.delete(car_manufacturer_association)

            except RuntimeError:
                flash("There was a problem deleting an old association between {} and {}.".format(self.name_display, car_manufacturer_association.manufacturer.name_display), "danger")

            database.session.commit()

        # Create new car-manufacturer associations
        primary_car_manufacturer_association = CarManufacturer(car_id=self.id, company_id=primary_manufacturer_id, is_primary=True)
        database.session.add(primary_car_manufacturer_association)

        for manufacturer_id in secondary_manufacturer_ids:

            try:
                car_manufacturer_association = CarManufacturer(car_id=self.id, company_id=manufacturer_id, is_primary=False)
                database.session.add(car_manufacturer_association)

            except RuntimeError:
                company = Company.query.get(manufacturer_id)
                flash("There was a problem adding a new association between {} and {}.".format(self.name_display,
                                                                                               company.name_display),
                      "danger")

        database.session.commit()

        self.datetime_edited = datetime.utcnow()

    def set_power_to_weight_ratio(self):

        if self.max_power_output_kw_actual is not None:
            power = self.max_power_output_kw_actual
            if self.curb_weight_kg is not None:
                weight = self.curb_weight_kg

                self.power_to_weight_ratio = float(power)/float(weight)

            else:
                self.power_to_weight_ratio = None

        self.datetime_edited = datetime.utcnow()

    def set_suspension(self, form):

        if form.suspension_front_id.data == 0:
            self.suspension_front_id = None
        else:
            self.suspension_front_id = form.suspension_front_id.data

        if form.suspension_rear_id.data == 0:
            self.suspension_rear_id = None
        else:
            self.suspension_rear_id = form.suspension_rear_id.data

        self.datetime_edited = datetime.utcnow()

    def set_transmission(self, form):

        if form.transmission_id.data == 0:
            self.transmission_id = None
            self.transmission_type_actual_id = form.transmission_type_actual_id.data
            self.no_of_gears_actual = form.no_of_gears_actual.data
        else:
            self.transmission_id = form.transmission_id.data
            self.transmission_type_actual_id = None
            self.no_of_gears_actual = None

        self.datetime_edited = datetime.utcnow()


def create_car_from_form(form):

    new_car = Car()
    form.populate_obj(new_car)

    # Set manufacturers display string
    primary_manufacturer = Company.query.get(form.primary_manufacturer.data)
    secondary_manufacturers = []

    for manufacturer_id in form.secondary_manufacturers.data:
        manufacturer = Company.query.filter(Company.id == manufacturer_id)
        secondary_manufacturers += manufacturer

    manufacturers_display_string = primary_manufacturer.name_display

    for secondary_manufacturer in secondary_manufacturers:
        manufacturers_display_string += " / {}".format(secondary_manufacturer.name_display)

    new_car.manufacturers_display = manufacturers_display_string

    # If no country is selected
    if form.country_id.data == 0:
        new_car.country_id = None

    # Temporarily set values to zero, because they cannot be nulled
    new_car.engine_layout_id = 1
    new_car.drivetrain_id = 1

    return new_car


def create_copy_from_car(original_car_id):

    original_car = Car.query.get(original_car_id)
    copy_car = Car()

    # Set general information
    copy_car.year = original_car.year
    copy_car.model = "{} (copy)".format(original_car.model)
    copy_car.name_display = "{} (copy)".format(original_car.name_display)
    copy_car.name_short = original_car.name_short
    copy_car.country_id = original_car.country_id
    copy_car.is_prototype = original_car.is_prototype
    copy_car.is_fictional = original_car.is_fictional
    copy_car.car_class_id = original_car.car_class_id
    copy_car.body_style_id = original_car.body_style_id
    # These two need to be set before the car is put in the database or it will trip a data consistency protection
    copy_car.engine_layout_id = original_car.engine_layout_id
    copy_car.drivetrain_id = original_car.drivetrain_id

    copy_car.manufacturers_display = original_car.manufacturers_display

    try:
        database.session.add(copy_car)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem creating a new car.", "danger")
        return redirect(url_for("detail_car", id=original_car.id))

    # Get original car's manufacturers
    original_car_primary_manufacturer_association = CarManufacturer.query.filter(
                                                                         CarManufacturer.car_id == original_car.id,
                                                                         CarManufacturer.is_primary == True).first()
    original_car_primary_manufacturer_id = original_car_primary_manufacturer_association.company_id

    original_car_secondary_manufacturers_associations = CarManufacturer.query.filter(
                                                                         CarManufacturer.car_id == original_car.id,
                                                                         CarManufacturer.is_primary == False).all()

    secondary_manufacturers_ids = []

    for association in original_car_secondary_manufacturers_associations:
        secondary_manufacturers_ids.append(association.company_id)

    # Set copy car's manufacturers
    copy_car.set_manufacturers(original_car_primary_manufacturer_id, secondary_manufacturers_ids)

    # Get original car's competitions
    original_car_competition_associations = CarCompetition.query.filter(CarCompetition.car_id == original_car.id).all()

    competition_ids = []

    for association in original_car_competition_associations:
        competition_ids.append(association.competition_id)

    # Set copy car's competitions
    copy_car.set_competitions(competition_ids)

    try:
        database.session.commit()

    except RuntimeError:
        flash("There was a problem setting the copy's competition data.", "danger")
        return redirect(url_for("detail_car", id=copy_car.id))

    # Get original car's engine(s)
    original_car_engine_associations = CarEngine.query.filter(CarEngine.car_id == original_car.id).all()

    engine_ids = []

    for association in original_car_engine_associations:
        engine_ids.append(association.engine_id)

    # Set copy car's engine(s)
    copy_car.set_engines(engine_ids)

    try:
        database.session.commit()

    except RuntimeError:
        flash("There was a problem setting the copy's engine data.", "danger")
        return redirect(url_for("detail_car", id=copy_car.id))

    # Set technical data
    # Engine
    copy_car.fuel_type_actual_id = original_car.fuel_type_actual_id
    copy_car.max_power_output_kw_actual = original_car.max_power_output_kw_actual
    copy_car.max_power_output_rpm_actual = original_car.max_power_output_rpm_actual
    copy_car.max_torque_nm_actual = original_car.max_torque_nm_actual
    copy_car.max_torque_rpm_actual = original_car.max_torque_rpm_actual
    copy_car.additional_forced_induction_id = original_car.additional_forced_induction_id

    try:
        database.session.commit()

    except RuntimeError:
        flash("There was a problem setting the copy's engine data.", "danger")
        return redirect(url_for("detail_car", id=copy_car.id))

    # Drivetrain
    copy_car.transmission_id = original_car.transmission_id
    copy_car.transmission_type_actual_id = original_car.transmission_type_actual_id
    copy_car.no_of_gears_actual = original_car.no_of_gears_actual

    try:
        database.session.commit()

    except RuntimeError:
        flash("There was a problem setting the copy's drivetrain data.", "danger")
        return redirect(url_for("detail_car", id=copy_car.id))

    # Platform
    copy_car.suspension_front_id = original_car.suspension_front_id
    copy_car.suspension_rear_id = original_car.suspension_rear_id
    copy_car.curb_weight_kg = original_car.curb_weight_kg
    copy_car.weight_distribution = original_car.weight_distribution
    copy_car.tires_front = original_car.tires_front
    copy_car.tires_rear = original_car.tires_rear

    try:
        database.session.commit()

    except RuntimeError:
        flash("There was a problem setting the copy's platform data.", "danger")
        return redirect(url_for("detail_car", id=copy_car.id))

    # Performance
    copy_car.acceleration_0_to_100_kmh_sec = original_car.acceleration_0_to_100_kmh_sec
    copy_car.maximum_speed_kmh = original_car.maximum_speed_kmh
    copy_car.power_to_weight_ratio = original_car.power_to_weight_ratio

    try:
        database.session.commit()

    except RuntimeError:
        flash("There was a problem setting the copy's performance data.", "danger")
        return redirect(url_for("detail_car", id=copy_car.id))

    # Get original car's assists
    original_car_assist_associations = CarAssist.query.filter(CarAssist.car_id == original_car.id).all()

    assist_ids = []

    for association in original_car_assist_associations:
        assist_ids.append(association.assist_id)

    # Set copy car's assists
    copy_car.set_assists(assist_ids)

    try:
        database.session.commit()

    except RuntimeError:
        flash("There was a problem setting the copy's assist data.", "danger")
        return redirect(url_for("detail_car", id=copy_car.id))

    # Copy text
    for text in original_car.texts:

        new_text = CarText(order=text.order,
                           content=text.content,
                           text_type=text.text_type,
                           car_id=copy_car.id)

        try:
            database.session.add(new_text)
            database.session.commit()

        except RuntimeError:
            flash("There was a problem copying one of the texts from the original car.", "danger")
            return redirect(url_for("detail_car", id=copy_car.id))

    # Copy images
    for image in original_car.images:

        new_image = CarImage(order=image.order,
                             path=image.path,
                             description=image.description,
                             is_thumbnail=image.is_thumbnail,
                             car_id=copy_car.id)

        flash("")

        try:
            database.session.add(new_image)
            database.session.commit()

        except RuntimeError:
            flash("There was a problem copying one of the images from the original car.", "danger")
            return redirect(url_for("detail_car", id=copy_car.id))


class Assist(database.Model):

    __tablename__ = "assists"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name_full = database.Column(database.Unicode, index=True, nullable=False, unique=True)
    name_short = database.Column(database.Unicode, index=True, nullable=False, unique=True)

    cars = database.relationship('Car', secondary="car_assist")
    instances = database.relationship('Instance', secondary="instance_assist")


class BodyStyle(database.Model):

    __tablename__ = "body_styles"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False, unique=True)
    no_of_doors = database.Column(database.Integer, nullable=False)

    cars = database.relationship('Car', backref='body_style', lazy='dynamic')


# Represents a class of cars based on car classification on Wikipedia
class CarClass(database.Model):

    __tablename__ = "car_classes"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name_euro = database.Column(database.Unicode, index=True, nullable=True)
    name_us = database.Column(database.Unicode, index=True, nullable=True)
    name_alternative = database.Column(database.Unicode, index=True, nullable=True)
    name_custom = database.Column(database.Unicode, index=True, nullable=True, unique=True)
    name_short = database.Column(database.Unicode, nullable=True)

    # Relationships
    cars = database.relationship('Car', backref='car_class', lazy='dynamic')


class Drivetrain(database.Model):

    __tablename__ = "drivetrains"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name_full = database.Column(database.Unicode, index=True, nullable=False)
    name_short = database.Column(database.Unicode, index=True, nullable=False)

    # Relationships
    cars = database.relationship('Car', backref='drivetrain', lazy='dynamic')
    instances = database.relationship('Instance', backref='drivetrain', lazy='dynamic')


class EngineLayout(database.Model):

    __tablename__ = "engine_layouts"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False, unique=True)

    # Relationships
    cars = database.relationship('Car', backref='engine_layout', lazy='dynamic')
    instances = database.relationship('Instance', backref='engine_layout', lazy='dynamic')


# Info
class CarText(Text):

    __tablename__ = "texts_cars"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('texts.id'), primary_key=True)

    # General
    car_id = database.Column(database.Integer, database.ForeignKey('cars.id'), primary_key=True)


class CarImage(Image):

    __tablename__ = "images_cars"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('images.id'), primary_key=True)

    # General
    is_thumbnail = database.Column(database.Boolean, default=False, index=True, nullable=False)
    car_id = database.Column(database.Integer, database.ForeignKey('cars.id'), primary_key=True)


# Many-to-many relationships
class CarAssist(database.Model):

    __tablename__ = "car_assist"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)
    car_id = database.Column(database.Integer, database.ForeignKey("cars.id"))
    assist_id = database.Column(database.Integer, database.ForeignKey("assists.id"))
    car = database.relationship('Car', backref=backref("car_assist", cascade="all, delete-orphan"))
    assist = database.relationship('Assist', backref=backref("car_assist", cascade="all, delete-orphan"))


class CarCompetition(database.Model):

    __tablename__ = "car_competition"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)
    car_id = database.Column(database.Integer, database.ForeignKey("cars.id"))
    competition_id = database.Column(database.Integer, database.ForeignKey("competitions.id"))
    car = database.relationship('Car', backref=backref("car_competition", cascade="all, delete-orphan"))
    competition = database.relationship('Competition', backref=backref("car_competition", cascade="all, delete-orphan"))


class CarEngine(database.Model):

    __tablename__ = "car_engine"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)
    car_id = database.Column(database.Integer, database.ForeignKey("cars.id"))
    engine_id = database.Column(database.Integer, database.ForeignKey("engines.id"))
    car = database.relationship('Car', backref=backref("car_engine", cascade="all, delete-orphan"))
    engine = database.relationship('Engine', backref=backref("car_engine", cascade="all, delete-orphan"))


class CarManufacturer(database.Model):

    __tablename__ = "car_manufacturer"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)
    car_id = database.Column(database.Integer, database.ForeignKey("cars.id"))
    company_id = database.Column(database.Integer, database.ForeignKey("companies.id"))
    car = database.relationship('Car', backref=backref("car_manufacturer", cascade="all, delete-orphan"))
    manufacturer = database.relationship('Company', backref=backref("car_manufacturer", cascade="all, delete-orphan"))

    # General
    is_primary = database.Column(database.Boolean, default=True, index=True, nullable=False)
