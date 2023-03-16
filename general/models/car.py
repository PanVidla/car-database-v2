from datetime import datetime

from sqlalchemy.orm import backref

from general import database


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
    model = database.Column(database.Unicode, index=True, nullable=False)
    name_display = database.Column(database.Unicode, index=True, nullable=False)
    name_short = database.Column(database.Unicode, nullable=True)
    is_prototype = database.Column(database.Boolean, default=False, index=True, nullable=False)
    is_fictional = database.Column(database.Boolean, default=False, index=True, nullable=False)
    competitions = database.relationship('Competition', secondary="car_competition")
    car_class_id = database.Column(database.Integer, database.ForeignKey("car_classes.id"), index=True, nullable=True)
    body_style_id = database.Column(database.Integer, database.ForeignKey("body_styles.id"), index=True, nullable=False)

    # Technical
    # Engine
    engine_id = database.Column(database.Integer, database.ForeignKey("engines.id"), index=True, nullable=True)
    max_power_output_kw_actual = database.Column(database.Double, index=True, nullable=True)
    max_power_output_rpm_actual = database.Column(database.Integer, nullable=True)
    max_torque_nm_actual = database.Column(database.Double, index=True, nullable=True)
    max_torque_rpm_actual = database.Column(database.Integer, nullable=True)
    # This refers to the specific car part
    forced_induction_id = database.Column(database.Integer, database.ForeignKey("forced_induction.id"), nullable=True)

    # Drivetrain
    # This refers to the actual transmission car part and may backfill the following two values
    transmission_id = database.Column(database.Integer, database.ForeignKey("transmissions.id"), nullable=True)
    transmission_type_actual_id = database.Column(database.Integer, database.ForeignKey("transmissions_types.id"),
                                                  nullable=True)
    no_of_gears_actual = database.Column(database.Integer, index=True, nullable=True)
    engine_layout_id = database.Column(database.Integer, database.ForeignKey("engine_layouts.id"), index=True,
                                       nullable=False)
    drivetrain_id = database.Column(database.Integer, database.ForeignKey("drivetrains.id"), index=True, nullable=False)

    # Platform
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


class Assist(database.Model):

    __tablename__ = "assists"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name_full = database.Column(database.Unicode, index=True, nullable=False)
    name_short = database.Column(database.Unicode, index=True, nullable=False)

    assists = database.relationship('Car', secondary="car_assist")


class BodyStyle(database.Model):

    __tablename__ = "body_styles"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False)
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
    name_custom = database.Column(database.Unicode, index=True, nullable=True)
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

    cars = database.relationship('Car', backref='drivetrain', lazy='dynamic')


class EngineLayout(database.Model):

    __tablename__ = "engine_layouts"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False)

    cars = database.relationship('Car', backref='transmission_type', lazy='dynamic')


class TransmissionType(database.Model):

    __tablename__ = "transmission_types"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name_full = database.Column(database.Unicode, index=True, nullable=False)
    name_short = database.Column(database.Unicode, index=True, nullable=False)

    cars = database.relationship('Car', backref='drivetrain', lazy='dynamic')


# Many-to-many relationships
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
