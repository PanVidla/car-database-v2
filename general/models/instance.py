from datetime import datetime

from flask import flash
from sqlalchemy.orm import backref

from general import database
from general.models.car import Assist
from general.models.info import Text, Image
from general.models.part import Engine, EngineCombustion, EngineElectric


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
    game_id = database.Column(database.Integer, database.ForeignKey("games.id"), index=True, nullable=False)

    # Visuals
    color_name = database.Column(database.Unicode, index=True, nullable=True)
    color_hex = database.Column(database.Unicode, index=False, nullable=True)
    theme = database.Column(database.Unicode, index=True, nullable=True)

    # Technical
    # Engine
    engines = database.relationship('Engine', secondary="instance_engine", lazy='dynamic')
    fuel_type_actual_id = database.Column(database.Integer, database.ForeignKey("fuel_types.id"), index=True,
                                          nullable=True)
    max_power_output_kw_actual = database.Column(database.Double, index=True, nullable=True)
    max_power_output_rpm_actual = database.Column(database.Integer, nullable=True)
    max_torque_nm_actual = database.Column(database.Double, index=True, nullable=True)
    max_torque_rpm_actual = database.Column(database.Integer, nullable=True)
    # This refers to the specific car part
    additional_forced_induction_id = database.Column(database.Integer, database.ForeignKey("forced_induction.id"),
                                                     nullable=True)
    aspiration_actual_id = database.Column(database.Integer, database.ForeignKey("aspirations.id"), nullable=True)

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
    assists = database.relationship('Assist', secondary="instance_assist")

    # Statistics
    no_of_sessions = database.Column(database.Integer, default=0, index=True, nullable=False)
    no_of_events_total = database.Column(database.Integer, default=0, index=True, nullable=False)

    # Relationships
    texts = database.relationship('InstanceText', backref='instance', lazy='dynamic')
    images = database.relationship('InstanceImage', backref='instance', lazy='dynamic')

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

    def get_color(self):

        if self.color_name != "":
            color = "{}".format(self.color_name)

            if self.color_hex != "":
                color += " ({})".format(self.color_hex)

            return color

        else:
            return "n/a"

    def get_curb_weight_kg(self):
        return "{} kg".format(self.curb_weight_kg) if self.curb_weight_kg is not None else "n/a"

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

    def get_is_complete(self):
        return "✓" if self.is_complete else "x"

    def get_is_for_collection(self):
        return "✓" if self.is_for_collection else "x"

    def get_specialization(self):
        return self.specialization.name_full if self.specialization_id is not None else "n/a"

    def get_instance_type(self):
        return self.type.name_full if self.instance_type_id is not None else "n/a"

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

    def get_theme(self):
        return self.theme if self.theme != "" else "n/a"

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

    def set_assists(self, assists_ids):

        # Delete the old instance-assist associations
        instance_assist_old = InstanceAssist.query.filter(InstanceAssist.instance_id == self.id).all()

        for instance_assist_association in instance_assist_old:

            try:
                database.session.delete(instance_assist_association)

            except RuntimeError:
                flash("There was a problem deleting an old association between {} and {}.".format(self.name_full,
                                                                                                  instance_assist_association.assist.name_short),
                      "danger")

            database.session.commit()

        # Create new instance-asssist associations
        for assist_id in assists_ids:

            try:
                instance_assist_association = InstanceAssist(instance_id=self.id, assist_id=assist_id)
                database.session.add(instance_assist_association)

            except RuntimeError:
                assist = Assist.query.get(assist_id)
                flash("There was a problem adding a new association between {} and {}.".format(self.name_full,
                                                                                               assist.short),
                      "danger")

        database.session.commit()

        self.datetime_edited = datetime.utcnow()

    def set_engines(self, engine_ids):

        # Delete the old instance-engine associations
        instance_engine_old = InstanceEngine.query.filter(InstanceEngine.instance_id == self.id).all()

        for instance_engine_association in instance_engine_old:

            try:
                database.session.delete(instance_engine_association)

            except RuntimeError:
                flash("There was a problem deleting an old association between {} and {}.".format(self.name_full,
                                                                                                  instance_engine_association.engine.name_display),
                      "danger")

            database.session.commit()

        # Create new instance-engine associations
        for engine_id in engine_ids:

            try:
                instance_engine_association = InstanceEngine(instance_id=self.id, engine_id=engine_id)
                database.session.add(instance_engine_association)

            except RuntimeError:
                engine = Engine.query.get(engine_id)
                flash("There was a problem adding a new association between {} and {}.".format(self.name_full,
                                                                                               engine.name_display),
                      "danger")

        database.session.commit()

        self.datetime_edited = datetime.utcnow()

    def set_forced_induction(self, forced_induction_id):

        if forced_induction_id == 0:
            self.additional_forced_induction_id = None

        else:
            self.additional_forced_induction_id = forced_induction_id

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

    def set_type_and_specialization(self, form):

        if form.instance_type_id.data == 0:
            self.instance_type_id = None

        if form.specialization_id.data == 0:
            self.specialization_id = None

        self.datetime_edited = datetime.utcnow()


class RacingInstance(Instance):

    __tablename__ = "instances_racing"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('instances.id'), primary_key=True)

    # Statistics
    no_of_events_won = database.Column(database.Integer, default=0, index=True, nullable=False)
    no_of_events_won_percent = database.Column(database.Double, index=True, nullable=True)
    no_of_events_podium = database.Column(database.Integer, default=0, index=True, nullable=False)
    no_of_events_podium_percent = database.Column(database.Double, index=True, nullable=True)
    no_of_events_lost = database.Column(database.Integer, default=0, index=True, nullable=False)
    no_of_events_lost_percent = database.Column(database.Double, index=True, nullable=True)
    no_of_events_dnf = database.Column(database.Integer, default=0, index=True, nullable=False)
    no_of_events_dnf_percent = database.Column(database.Double, index=True, nullable=True)
    average_position = database.Column(database.Double, index=True, nullable=True)


# Info
class InstanceText(Text):

    __tablename__ = "texts_instances"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('texts.id'), primary_key=True)

    # General
    instance_id = database.Column(database.Integer, database.ForeignKey('instances.id'), primary_key=True)


class InstanceImage(Image):

    __tablename__ = "images_instances"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('images.id'), primary_key=True)

    # General
    is_thumbnail = database.Column(database.Boolean, default=False, index=True, nullable=False)
    instance_id = database.Column(database.Integer, database.ForeignKey('instances.id'), primary_key=True)


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


# Represents what the car specializes within its discipline (e.g. straight-line speed, road drifting, dirt rally...)
class InstanceSpecialization(database.Model):

    __tablename__ = "instance_specializations"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name_full = database.Column(database.Unicode, index=True, nullable=False)
    name_short = database.Column(database.Unicode, index=True, nullable=False)

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


class InstanceEngine(database.Model):

    __tablename__ = "instance_engine"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)
    instance_id = database.Column(database.Integer, database.ForeignKey("instances.id"))
    engine_id = database.Column(database.Integer, database.ForeignKey("engines.id"))
    instance = database.relationship('Instance', backref=backref("instance_engine", cascade="all, delete-orphan"))
    engine = database.relationship('Engine', backref=backref("instance_engine", cascade="all, delete-orphan"))
