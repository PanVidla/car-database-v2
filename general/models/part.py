from general import database


# Represents a type of aspiration (e.g. naturally-aspirated, turbo-charged, nitrous...)
class Aspiration(database.Model):

    __tablename__ = "aspirations"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False)

    cars = database.relationship('Car', backref='aspiration', lazy='dynamic')


class Engine(database.Model):

    __tablename__ = "engines"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    manufacturer_id = database.Column(database.Integer, database.ForeignKey("companies.id"), index=True, nullable=True)
    name_official = database.Column(database.Unicode, index=True, nullable=True)
    name_display = database.Column(database.Unicode, index=True, nullable=False)

    # Technical
    # Type of engine (spark-ignition 4-stroke)
    type = database.Column(database.Unicode, nullable=True)
    fuel_type_id = database.Column(database.Integer, database.ForeignKey("fuel_types.id"), index=True, nullable=False)
    # This represents the type of aspiration (e.g. naturally aspirated, turbocharged, nitrous...)
    aspiration_id = database.Column(database.Integer, database.ForeignKey("aspirations.id"), nullable=True)
    valves_per_cylinder = database.Column(database.Integer, nullable=True)
    cylinder_alignment = database.Column(database.Unicode, nullable=True)

    # Performance
    max_power_output_kw = database.Column(database.Double, index=True, nullable=True)
    max_power_output_rpm = database.Column(database.Integer, nullable=True)
    max_torque_nm = database.Column(database.Double, index=True, nullable=True)
    max_torque_rpm = database.Column(database.Integer, nullable=True)

    cars = database.relationship('Car', backref='engine', lazy='dynamic')


class ForcedInduction(database.Model):

    __tablename__ = "forced_induction"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    manufacturer_id = database.Column(database.Integer, database.ForeignKey("companies.id"), index=True, nullable=True)
    name_official = database.Column(database.Unicode, index=True, nullable=True)
    name_display = database.Column(database.Unicode, index=True, nullable=False)


class Transmission(database.Model):

    __tablename__ = "transmissions"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    manufacturer_id = database.Column(database.Integer, database.ForeignKey("companies.id"), index=True, nullable=True)
    name_official = database.Column(database.Unicode, index=True, nullable=True)
    name_display = database.Column(database.Unicode, index=True, nullable=False)
    no_of_gears = database.Column(database.Unicode, index=True, nullable=False)
    type_id = database.Column(database.Integer, database.ForeignKey("transmission_types.id"), index=True, nullable=False)


class FuelType(database.Model):

    __tablename__ = "fuel_types"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False)

    cars = database.relationship('Car', backref='fuel_type', lazy='dynamic')


class TransmissionType(database.Model):

    __tablename__ = "transmission_types"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False)

    # Relationships
    transmissions = database.relationship('Transmission', backref='type', lazy='dynamic')
    cars = database.relationship('Car', backref='transmission_type', lazy='dynamic')
