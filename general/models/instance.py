from datetime import datetime

from sqlalchemy.orm import backref

from general import database


# Represents a video game instance of a car
class Instance(database.Model):

    __tablename__ = "instances"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)
    datetime_added = database.Column(database.DateTime, default=datetime.utcnow, index=True, nullable=False)
    datetime_edited = database.Column(database.DateTime, default=datetime.utcnow, index=True, nullable=False)
    datetime_played = database.Column(database.DateTime, index=True, nullable=True)
    is_deleted = database.Column(database.Boolean, default=False, index=True, nullable=False)

    # General
    name_full = database.Column(database.Unicode, index=True, nullable=False)
    name_nickname = database.Column(database.Unicode, index=True, nullable=False, unique=True)
    instance_type_id = database.Column(database.Integer, database.ForeignKey("instance_types.id"), index=True,
                                       nullable=True)
    specialization_id = database.Column(database.Integer, database.ForeignKey("instance_specializations.id"),
                                        index=True, nullable=True)
    is_complete = database.Column(database.Boolean, default=False, index=True, nullable=False)
    is_for_collection = database.Column(database.Boolean, default=False, index=True, nullable=False)
    car_id = database.Column(database.Integer, database.ForeignKey("cars.id"), index=True, nullable=False)

    # Visuals
    color_name = database.Column(database.Unicode, index=True, nullable=True)
    color_hex = database.Column(database.Unicode, index=True, nullable=True)
    theme = database.Column(database.Unicode, index=True, nullable=True)

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
    assists = database.relationship('Assist', secondary="instance_assist")

    # Statistics
    no_of_sessions = database.Column(database.Integer, default=0, index=True, nullable=False)


# Represents a type of driving a car can be dedicated to (e.g. road racing, drifting, rally...)
class InstanceType(database.Model):

    __tablename__ = "instance_types"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name_full = database.Column(database.Unicode, index=True, nullable=False, unique=True)
    name_short = database.Column(database.Unicode, index=True, nullable=False, unique=True)

    # Relationships
    instances = database.relationship('Instance', backref='type', lazy='dynamic')
    specializations = database.relationship('InstanceSpecialization', backref='type', lazy='dynamic')


# Represents what the car specializes within its discipline (e.g. straight-line speed, road drifting, dirt rally...)
class InstanceSpecialization(database.Model):

    __tablename__ = "instance_specializations"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name_full = database.Column(database.Unicode, index=True, nullable=False)
    name_short = database.Column(database.Unicode, index=True, nullable=False)
    instance_type_id = database.Column(database.Integer, database.ForeignKey("instance_types.id"), index=True,
                                       nullable=False)

    # Relationships
    instances = database.relationship('Instance', backref='specialization', lazy='dynamic')


# Many-to-many relationships
class InstanceAssist(database.Model):

    __tablename__ = "instance_assist"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)
    instance_id = database.Column(database.Integer, database.ForeignKey("instances.id"))
    assist_id = database.Column(database.Integer, database.ForeignKey("assists.id"))
    instance = database.relationship('Instance', backref=backref("instance_assist", cascade="all, delete-orphan"))
    assist = database.relationship('Assist', backref=backref("instance_assist", cascade="all, delete-orphan"))
