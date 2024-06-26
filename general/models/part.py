from flask import flash, redirect, url_for

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
    engines = database.relationship('EngineCombustion', backref='aspiration', lazy='dynamic')
    forced_inductions = database.relationship('ForcedInduction', backref='type', lazy='dynamic')


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

    def get_fuel(self):
        return self.fuel_type.name

    def get_images(self):

        images = EngineImage.query.filter(EngineImage.engine_id == self.id)
        images = images.order_by(EngineImage.order.asc()).all()

        return images

    def get_manufacturer_name_display(self):
        return self.manufacturer.name_display if self.manufacturer_id is not None else "n/a"

    def get_max_power_output_kw(self):
        return "{:.0f}".format(self.max_power_output_kw) if self.max_power_output_kw is not None else "n/a"

    def get_max_power_output_hp(self):
        return self.max_power_output_kw * 1.34 if self.max_power_output_kw is not None else "n/a"

    def get_max_power_output_rpm(self):
        return self.max_power_output_rpm if self.max_power_output_rpm is not None else "n/a"

    def get_max_power_output_string_kw(self):

        string = ""

        if self.max_power_output_kw is not None:
            string += "{:.0f} kW".format(self.max_power_output_kw)

            if self.max_power_output_rpm is not None:
                string += " @ {} RPM".format(self.max_power_output_rpm)

        else:
            string = "n/a"

        return string

    def get_max_torque_string_nm(self):

        string = ""

        if self.max_torque_nm is not None:
            string += "{:.0f} N⋅m".format(self.max_torque_nm)

            if self.max_torque_rpm is not None:
                string += " @ {} RPM".format(self.max_torque_rpm)

        else:
            string = "n/a"

        return string

    def get_max_torque_nm(self):
        return "{:.0f}".format(self.max_torque_nm) if self.max_torque_nm is not None else "n/a"

    def get_max_torque_rpm(self):
        return self.max_torque_rpm if self.max_torque_rpm is not None else "n/a"

    def get_name_official(self):
        return self.name_official if self.name_official != "" else "n/a"


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

    def edit_combustion_engine_from_form(self, form):

        form.populate_obj(self)

        # No manufacturer is selected
        if form.manufacturer_id.data == 0:
            self.manufacturer_id = None

        # No type of combustion engine is selected
        if form.combustion_engine_type_id.data == 0:
            self.combustion_engine_type_id = None

        # No type of aspiration is selected
        if form.aspiration_id.data == 0:
            self.aspiration_id = None

    def get_aspiration(self):
        return self.aspiration.name if self.aspiration_id is not None else "n/a"

    def get_cylinder_alignment(self):
        return self.cylinder_alignment if self.cylinder_alignment is not (None or "") else "n/a"

    def get_displacement(self):
        return "{} L".format(self.displacement) if self.displacement is not None else "n/a"

    def get_engine_type(self):
        return self.engine_type.name if self.engine_type is not None else "n/a"

    def get_valves_per_cylinder(self):
        return self.valves_per_cylinder if self.valves_per_cylinder is not (None or "") else "n/a"


def create_combustion_engine_from_form(form):

    new_engine = EngineCombustion()
    form.populate_obj(new_engine)

    # No manufacturer is selected
    if form.manufacturer_id.data == 0:
        new_engine.manufacturer_id = None

    # No type of combustion engine is selected
    if form.combustion_engine_type_id.data == 0:
        new_engine.combustion_engine_type_id = None

    # No type of aspiration is selected
    if form.aspiration_id.data == 0:
        new_engine.aspiration_id = None

    return new_engine


def create_copy_from_combustion_engine(original_combustion_engine_id):

    original_engine = EngineCombustion.query.get(original_combustion_engine_id)
    copy_engine = EngineCombustion()

    # General engine information
    copy_engine.manufacturer_id = original_engine.manufacturer_id
    copy_engine.name_official = original_engine.name_official
    copy_engine.name_display = "{} (copy)".format(original_engine.name_display)

    # Technical engine information
    copy_engine.fuel_type_id = original_engine.fuel_type_id

    # Performance engine information
    copy_engine.max_power_output_kw = original_engine.max_power_output_kw
    copy_engine.max_power_output_rpm = original_engine.max_power_output_rpm
    copy_engine.max_torque_nm = original_engine.max_torque_nm
    copy_engine.max_torque_rpm = original_engine.max_torque_rpm

    # Assign combustion engine specific information
    copy_engine.combustion_engine_type_id = original_engine.combustion_engine_type_id
    copy_engine.displacement = original_engine.displacement
    copy_engine.aspiration_id = original_engine.aspiration_id
    copy_engine.valves_per_cylinder = original_engine.valves_per_cylinder
    copy_engine.cylinder_alignment = original_engine.cylinder_alignment

    try:
        database.session.add(copy_engine)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem creating a new engine.", "danger")
        return redirect(url_for("overviews_engines"))

    # Copy text
    for text in original_engine.texts:

        new_text = EngineText(order=text.order,
                              content=text.content,
                              text_type=text.text_type,
                              engine_id=copy_engine.id)

        try:
            database.session.add(new_text)
            database.session.commit()

        except RuntimeError:
            flash("There was a problem copying one of the texts from the original engine.", "danger")
            return redirect(url_for("detail_engine", id=copy_engine.id))

    # Copy images
    for image in original_engine.images:

        new_image = EngineImage(order=image.order,
                                path=image.path,
                                description=image.description,
                                engine_id=copy_engine.id)

        try:
            database.session.add(new_image)
            database.session.commit()

        except RuntimeError:
            flash("There was a problem copying one of the images from the original engine.", "danger")
            return redirect(url_for("detail_engine", id=copy_engine.id))


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

    def edit_electric_engine_from_form(self, form):

        form.populate_obj(self)

        # No manufacturer is selected
        if form.manufacturer_id.data == 0:
            self.manufacturer_id = None

        # No type of electric engine is selected
        if form.electric_engine_type_id.data == 0:
            self.electric_engine_type_id = None

    def get_battery_technology(self):
        return self.battery_technology if self.battery_technology is not (None or "") else "n/a"

    def get_battery_voltage(self):
        return "{:.0f} V".format(self.battery_voltage) if self.battery_technology is not (None or "") else "n/a"

    def get_engine_type(self):
        return self.engine_type.name if self.engine_type is not None else "n/a"


def create_electric_engine_from_form(form):

    new_engine = EngineElectric()
    form.populate_obj(new_engine)

    # No manufacturer is selected
    if form.manufacturer_id.data == 0:
        new_engine.manufacturer_id = None

    # No type of electric engine is selected
    if form.electric_engine_type_id.data == 0:
        new_engine.electric_engine_type_id = None

    return new_engine


def create_copy_from_electric_engine(original_electric_engine_id):

    original_engine = EngineElectric.query.get(original_electric_engine_id)
    copy_engine = EngineElectric()

    # General engine information
    copy_engine.manufacturer_id = original_engine.manufacturer_id
    copy_engine.name_official = original_engine.name_official
    copy_engine.name_display = "{} (copy)".format(original_engine.name_display)

    # Technical engine information
    copy_engine.fuel_type_id = original_engine.fuel_type_id

    # Performance engine information
    copy_engine.max_power_output_kw = original_engine.max_power_output_kw
    copy_engine.max_power_output_rpm = original_engine.max_power_output_rpm
    copy_engine.max_torque_nm = original_engine.max_torque_nm
    copy_engine.max_torque_rpm = original_engine.max_torque_rpm

    # Assign combustion engine specific information
    copy_engine.electric_engine_type_id = original_engine.electric_engine_type_id
    copy_engine.battery_voltage = original_engine.battery_voltage
    copy_engine.battery_technology = original_engine.battery_technology

    try:
        database.session.add(copy_engine)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem creating a new engine.", "danger")
        return redirect(url_for("overview_engines"))

    # Copy text
    for text in original_engine.texts:

        new_text = EngineText(order=text.order,
                              content=text.content,
                              text_type=text.text_type,
                              engine_id=copy_engine.id)

        try:
            database.session.add(new_text)
            database.session.commit()

        except RuntimeError:
            flash("There was a problem copying one of the texts from the original engine.", "danger")
            return redirect(url_for("detail_engine", id=copy_engine.id))

    # Copy images
    for image in original_engine.images:

        new_image = EngineImage(order=image.order,
                                path=image.path,
                                description=image.description,
                                engine_id=copy_engine.id)

        try:
            database.session.add(new_image)
            database.session.commit()

        except RuntimeError:
            flash("There was a problem copying one of the images from the original engine.", "danger")
            return redirect(url_for("detail_engine", id=copy_engine.id))


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

    def edit_forced_induction_from_form(self, form):

        form.populate_obj(self)

        # No manufacturer is selected
        if form.manufacturer_id.data == 0:
            self.manufacturer_id = None

    def get_manufacturer_name_display(self):
        return self.manufacturer.name_display if self.manufacturer_id is not None else "n/a"

    def get_name_official(self):
        return self.name_official if self.name_official is not None else "n/a"

    def get_boost_pressure_bar(self):
        return "{:.0f}".format(self.boost_pressure_bar) if self.boost_pressure_bar is not None else "n/a"

    def get_boost_pressure_string_bar(self):

        string = ""

        if self.boost_pressure_bar is not None:
            string += "{:.0f} bar".format(self.boost_pressure_bar)

        else:
            string = "n/a"

        return string

    def get_images(self):

        images = ForcedInductionImage.query.filter(ForcedInductionImage.forced_induction_id == self.id)
        images = images.order_by(ForcedInductionImage.order.asc()).all()

        return images


def create_forced_induction_from_form(form):

    new_forced_induction = ForcedInduction()
    form.populate_obj(new_forced_induction)

    # No manufacturer is selected
    if form.manufacturer_id.data == 0:
        new_forced_induction.manufacturer_id = None

    return new_forced_induction


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
    cars_front = database.relationship('Car', foreign_keys="Car.suspension_front_id", backref='front_suspension', lazy='dynamic')
    cars_rear = database.relationship('Car', foreign_keys="Car.suspension_rear_id", backref='rear_suspension', lazy='dynamic')
    instances_front = database.relationship('Instance', foreign_keys="Instance.suspension_front_id", backref='front_suspension', lazy='dynamic')
    instances_rear = database.relationship('Instance', foreign_keys="Instance.suspension_rear_id", backref='rear_suspension', lazy='dynamic')
    texts = database.relationship('SuspensionText', backref='suspension', lazy='dynamic')
    images = database.relationship('SuspensionImage', backref='suspension', lazy='dynamic')

    def get_images(self):

        images = SuspensionImage.query.filter(SuspensionImage.suspension_id == self.id)
        images = images.order_by(SuspensionImage.order.asc()).all()

        return images


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

    def edit_transmission_from_form(self, form):

        form.populate_obj(self)

        # No manufacturer is selected
        if form.manufacturer_id.data == 0:
            self.manufacturer_id = None

    def get_images(self):

        images = TransmissionImage.query.filter(TransmissionImage.transmission_id == self.id)
        images = images.order_by(TransmissionImage.order.asc()).all()

        return images

    def get_manufacturer_name_display(self):
        return self.manufacturer.name_display if self.manufacturer_id is not None else "n/a"


def create_transmission_from_form(form):

    new_transmission = Transmission()
    form.populate_obj(new_transmission)

    # No manufacturer is selected
    if form.manufacturer_id.data == 0:
        new_transmission.manufacturer_id = None

    return new_transmission


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
