from general import database
from general.models.info import Text, Image


# Represents a type of aspiration (e.g. naturally-aspirated, turbo-charged, nitrous...)
class Aspiration(database.Model):

    __tablename__ = "aspirations"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False)

    # Relationships
    cars = database.relationship('Car', backref='aspiration', lazy='dynamic')
    engines = database.relationship('Engine', backref='aspiration', lazy='dynamic')
    forced_inductions = database.relationship('ForcedInduction', backref='type', lazy='dynamic')
    instances = database.relationship('Instance', backref='aspiration', lazy='dynamic')


class Engine(database.Model):

    __tablename__ = "engines"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    manufacturer_id = database.Column(database.Integer, database.ForeignKey("companies.id"), index=True, nullable=True)
    name_official = database.Column(database.Unicode, index=True, nullable=True)
    name_display = database.Column(database.Unicode, index=True, nullable=False)

    # Technical
    fuel_type_id = database.Column(database.Integer, database.ForeignKey("fuel_types.id"), index=True, nullable=False)

    # Performance
    max_power_output_kw = database.Column(database.Double, index=True, nullable=True)
    max_power_output_rpm = database.Column(database.Integer, nullable=True)
    max_torque_nm = database.Column(database.Double, index=True, nullable=True)
    max_torque_rpm = database.Column(database.Integer, nullable=True)

    # Relationships
    cars = database.relationship('Car', secondary="car_engine", lazy='dynamic')
    instances = database.relationship('Instance', secondary="instance_engine", lazy='dynamic')
    texts = database.relationship('EngineText', backref='engine', lazy='dynamic')
    images = database.relationship('EngineImage', backref='engine', lazy='dynamic')


class EngineCombustion(Engine):

    __tablename__ = "combustion_engines"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('engines.id'), primary_key=True)

    # Technical
    # Type of engine (e.g. spark-ignition 4-stroke)
    combustion_engine_type_id = database.Column(database.Integer, database.ForeignKey("combustion_engine_types.id"),
                                                index=True, nullable=True)
    displacement = database.Column(database.Double, index=True, nullable=True)
    # This represents the type of aspiration (e.g. naturally aspirated, turbocharged, nitrous...)
    aspiration_id = database.Column(database.Integer, database.ForeignKey("aspirations.id"), nullable=True)
    valves_per_cylinder = database.Column(database.Integer, nullable=True)
    cylinder_alignment = database.Column(database.Unicode, nullable=True)


class EngineElectric(Engine):

    __tablename__ = "electric_engines"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('engines.id'), primary_key=True)

    # Technical
    # Type of engine (e.g. permanent magnet synchronous)
    electric_engine_type_id = database.Column(database.Integer, database.ForeignKey("electric_engine_types.id"),
                                              index=True, nullable=True)
    battery_voltage = database.Column(database.Integer, index=True, nullable=True)
    battery_technology = database.Column(database.Unicode, index=True, nullable=True)


class CombustionEngineType(database.Model):

    __tablename__ = "combustion_engine_types"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False, unique=True)

    # Relationships
    engines = database.relationship('EngineCombustion', backref='engine_type', lazy='dynamic')


class ElectricEngineType(database.Model):

    __tablename__ = "electric_engine_types"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False, unique=True)

    # Relationships
    engines = database.relationship('EngineElectric', backref='engine_type', lazy='dynamic')


class ForcedInduction(database.Model):

    __tablename__ = "forced_induction"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    manufacturer_id = database.Column(database.Integer, database.ForeignKey("companies.id"), index=True, nullable=True)
    name_official = database.Column(database.Unicode, index=True, nullable=True)
    name_display = database.Column(database.Unicode, index=True, nullable=False)

    # Technical
    boost_pressure_bar = database.Column(database.Double, nullable=True)
    force_induction_type_id = database.Column(database.Integer, database.ForeignKey("aspirations.id"), index=True,
                                              nullable=False)

    # Relationships
    cars = database.relationship('Car', backref='forced_induction', lazy='dynamic')
    instances = database.relationship('Instance', backref='forced_induction', lazy='dynamic')
    texts = database.relationship('ForcedInductionText', backref='forced_induction', lazy='dynamic')
    images = database.relationship('ForcedInductionImage', backref='forced_induction', lazy='dynamic')


class FuelType(database.Model):

    __tablename__ = "fuel_types"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False)

    # Relationships
    cars = database.relationship('Car', backref='fuel_type', lazy='dynamic')
    engines = database.relationship('Engine', backref='fuel_type', lazy='dynamic')
    instances = database.relationship('Instance', backref='fuel_type', lazy='dynamic')


class Suspension(database.Model):

    __tablename__ = "suspension"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name_full = database.Column(database.Unicode, index=True, nullable=False, unique=True)
    name_short = database.Column(database.Unicode, index=True, nullable=True, unique=True)

    # Relationships
    cars = database.relationship('Car', backref='suspension', lazy='dynamic')
    instances = database.relationship('Instance', backref='suspension', lazy='dynamic')
    texts = database.relationship('SuspensionText', backref='suspension', lazy='dynamic')
    images = database.relationship('SuspensionImage', backref='suspension', lazy='dynamic')


class Transmission(database.Model):

    __tablename__ = "transmissions"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    manufacturer_id = database.Column(database.Integer, database.ForeignKey("companies.id"), index=True, nullable=True)
    name_official = database.Column(database.Unicode, index=True, nullable=True)
    name_display = database.Column(database.Unicode, index=True, nullable=False)
    no_of_gears = database.Column(database.Integer, index=True, nullable=False)
    type_id = database.Column(database.Integer, database.ForeignKey("transmission_types.id"), index=True, nullable=False)

    # Relationships
    cars = database.relationship('Car', backref='transmission', lazy='dynamic')
    instances = database.relationship('Instance', backref='transmission', lazy='dynamic')
    texts = database.relationship('TransmissionText', backref='transmission', lazy='dynamic')
    images = database.relationship('TransmissionImage', backref='transmission', lazy='dynamic')


class TransmissionType(database.Model):

    __tablename__ = "transmission_types"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False, unique=True)

    # Relationships
    transmissions = database.relationship('Transmission', backref='type', lazy='dynamic')
    cars = database.relationship('Car', backref='transmission_type', lazy='dynamic')
    instances = database.relationship('Instance', backref='transmission_type', lazy='dynamic')


# Info
class EngineText(Text):

    __tablename__ = "texts_engines"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('texts.id'), primary_key=True)

    # General
    engine_id = database.Column(database.Integer, database.ForeignKey('engines.id'), primary_key=True)


class EngineImage(Image):

    __tablename__ = "images_engines"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('images.id'), primary_key=True)

    # General
    engine_id = database.Column(database.Integer, database.ForeignKey('engines.id'), primary_key=True)


class ForcedInductionText(Text):

    __tablename__ = "texts_forced_induction"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('texts.id'), primary_key=True)

    # General
    forced_induction_id = database.Column(database.Integer, database.ForeignKey('forced_induction.id'), primary_key=True)


class ForcedInductionImage(Image):

    __tablename__ = "images_forced_induction"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('images.id'), primary_key=True)

    # General
    forced_induction_id = database.Column(database.Integer, database.ForeignKey('forced_induction.id'), primary_key=True)


class SuspensionText(Text):

    __tablename__ = "texts_suspension"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('texts.id'), primary_key=True)

    # General
    suspension_id = database.Column(database.Integer, database.ForeignKey('suspension.id'), primary_key=True)


class SuspensionImage(Image):

    __tablename__ = "images_suspension"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('images.id'), primary_key=True)

    # General
    suspension_id = database.Column(database.Integer, database.ForeignKey('suspension.id'), primary_key=True)


class TransmissionText(Text):

    __tablename__ = "texts_transmissions"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('texts.id'), primary_key=True)

    # General
    transmission_id = database.Column(database.Integer, database.ForeignKey('transmissions.id'), primary_key=True)


class TransmissionImage(Image):

    __tablename__ = "images_transmissions"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('images.id'), primary_key=True)

    # General
    transmission_id = database.Column(database.Integer, database.ForeignKey('transmissions.id'), primary_key=True)
