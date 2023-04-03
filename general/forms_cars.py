from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, SelectMultipleField, BooleanField, DecimalField
from wtforms.validators import DataRequired, Optional

from general.models.car import CarClass, BodyStyle, EngineLayout, Drivetrain, Assist
from general.models.misc import Company, Country, Competition
from general.models.part import Engine, ForcedInduction, Transmission, TransmissionType, Suspension, FuelType


# Car
class Car1Form(FlaskForm):

    # General
    year = IntegerField("Year", validators=[DataRequired()])
    primary_manufacturer = SelectField("Primary manufacturer", coerce=int)
    secondary_manufacturers = SelectMultipleField("Secondary manufacturers", validators=[Optional()], coerce=int)
    model = StringField("Model", validators=[DataRequired()])
    name_display = StringField("Display name", validators=[DataRequired()])
    name_short = StringField("Short name", validators=[Optional()])
    country_id = SelectField("Country", coerce=int)
    is_prototype = BooleanField("Prototype")
    is_fictional = BooleanField("Fictional")
    competitions_select = SelectMultipleField("Competitions", validators=[Optional()], coerce=int)
    car_class_id = SelectField("Car class", coerce=int)
    body_style_id = SelectField("Body style", coerce=int)

    # Initialization
    def __init__(self, *args, **kwargs):
        super(Car1Form, self).__init__(*args, **kwargs)

        self.primary_manufacturer.choices = [(manufacturer.id, "{}".format(manufacturer.name_display))
                                             for manufacturer
                                             in Company.query
                                             .filter(Company.is_car_manufacturer == True)
                                             .order_by(Company.name_display.asc()).all()]

        self.secondary_manufacturers.choices = [(manufacturer.id, "{}".format(manufacturer.name_display))
                                                for manufacturer
                                                in Company.query
                                                .filter(Company.is_car_manufacturer == True)
                                                .order_by(Company.name_display.asc()).all()]

        self.country_id.choices = [(0, "None")]
        self.country_id.choices += [(country.id, "{}".format(country.name_display))
                                    for country
                                    in Country.query
                                    .order_by(Country.name_display.asc()).all()]

        self.competitions_select.choices = [(competition.id, "{}".format(competition.name_display))
                                            for competition
                                            in Competition.query
                                     .order_by(Competition.name_display.asc()).all()]

        self.car_class_id.choices = [(car_class.id, "{}".format(car_class.name_custom))
                                     for car_class
                                     in CarClass.query
                                     .order_by(CarClass.name_custom.asc()).all()]

        self.body_style_id.choices = [(body_style.id, "{}".format(body_style.name))
                                      for body_style
                                      in BodyStyle.query
                                      .order_by(BodyStyle.name.asc()).all()]


class CarAdd1Form(Car1Form):

    submit = SubmitField("Create car")


class CarEdit1Form(Car1Form):

    submit = SubmitField("Edit general info")


class Car21Form(FlaskForm):

    # Technical
    # Engine
    engines = SelectMultipleField("Engine(s)", validators=[Optional()], coerce=int)

    submit_existing_engine = SubmitField("Select engine(s)")

    # Initialization
    def __init__(self, *args, **kwargs):
        super(Car21Form, self).__init__(*args, **kwargs)

        self.engines.choices = [(engine.id, "{} ({})".format(engine.name_display, engine.fuel_type.name))
                                for engine
                                in Engine.query
                                .order_by(Engine.fuel_type_id.asc(), Engine.name_display.asc()).all()]


class Car22Form(FlaskForm):

    submit_skip_engine = SubmitField("Skip")


class Car3Form(FlaskForm):

    # Technical
    # Engine
    additional_forced_induction_id = SelectField("Forced induction", coerce=int)
    submit = SubmitField("Set forced induction")

    # Initialization
    def __init__(self, *args, **kwargs):
        super(Car3Form, self).__init__(*args, **kwargs)

        self.additional_forced_induction_id.choices = [(0, "None")]
        self.additional_forced_induction_id.choices += [(forced_induction.id, "{}".format(forced_induction.name_display))
                                                       for forced_induction
                                                       in ForcedInduction.query
                                                       .order_by(ForcedInduction.name_display.asc()).all()]


class Car4Form(FlaskForm):

    # Engine
    fuel_type_actual_id = SelectField("System fuel type", coerce=int)
    max_power_output_kw_actual = DecimalField("Maximum power", validators=[Optional()])
    max_power_output_rpm_actual = IntegerField("Maximum power RPM", validators=[Optional()])
    max_torque_nm_actual = DecimalField("Maximum torque", validators=[Optional()])
    max_torque_rpm_actual = IntegerField("Maximum torque RPM", validators=[Optional()])

    submit = SubmitField("Confirm values")

    # Initialization
    def __init__(self, *args, **kwargs):
        super(Car4Form, self).__init__(*args, **kwargs)

        self.fuel_type_actual_id.choices = [
            (fuel_type.id, "{}".format(fuel_type.name))
            for fuel_type
            in FuelType.query
            .order_by(FuelType.id.asc()).all()]


class Car5Form(FlaskForm):

    # Transmission
    transmission_id = SelectField("Transmission", coerce=int)
    transmission_type_actual_id = SelectField("Transmission type", coerce=int)
    no_of_gears_actual = IntegerField("Gears", validators=[Optional()])
    engine_layout_id = SelectField("Engine layout", coerce=int)
    drivetrain_id = SelectField("Drivetrain", coerce=int)

    submit = SubmitField("Set transmission & drivetrain")

    # Initialization
    def __init__(self, *args, **kwargs):
        super(Car5Form, self).__init__(*args, **kwargs)

        self.transmission_id.choices = [(0, "None")]
        self.transmission_id.choices += [
            (transmission.id, "{}".format(transmission.name_display))
            for transmission
            in Transmission.query
            .order_by(Transmission.name_display.asc()).all()]

        self.transmission_type_actual_id.choices = [
            (transmission_type.id, "{}".format(transmission_type.name))
            for transmission_type
            in TransmissionType.query
            .order_by(TransmissionType.name.asc()).all()]

        self.engine_layout_id.choices = [
            (engine_layout.id, "{}".format(engine_layout.name))
            for engine_layout
            in EngineLayout.query
            .order_by(EngineLayout.name.asc()).all()]

        self.drivetrain_id.choices = [
            (drivetrain.id, "{}".format(drivetrain.name_full))
            for drivetrain
            in Drivetrain.query
            .order_by(Drivetrain.name_full.asc()).all()]


class Car6Form(FlaskForm):

    # Platform
    suspension_front_id = SelectField("Front suspension", coerce=int)
    suspension_rear_id = SelectField("Rear suspension", coerce=int)
    curb_weight_kg = DecimalField("Curb weight", validators=[Optional()])
    weight_distribution = DecimalField("Front weight", validators=[Optional()])
    tires_front = StringField("Front tires", validators=[Optional()])
    tires_rear = StringField("Rear tires", validators=[Optional()])

    submit = SubmitField("Set platform")

    # Initialization
    def __init__(self, *args, **kwargs):
        super(Car6Form, self).__init__(*args, **kwargs)

        self.suspension_front_id.choices = [(0, "None")]
        self.suspension_front_id.choices += [
            (suspension.id, "{}".format(suspension.name_full))
            for suspension
            in Suspension.query
            .order_by(Suspension.name_full.asc()).all()]

        self.suspension_rear_id.choices = [(0, "None")]
        self.suspension_rear_id.choices += [
            (suspension.id, "{}".format(suspension.name_full))
            for suspension
            in Suspension.query
            .order_by(Suspension.name_full.asc()).all()]


class Car7Form(FlaskForm):

    # Performance
    acceleration_0_to_100_kmh_sec = DecimalField("0 to 100 km/h", validators=[Optional()])
    maximum_speed_kmh = DecimalField("Maximum speed", validators=[Optional()])

    submit = SubmitField("Set performance data")


class Car8Form(FlaskForm):

    # Assists
    assists_select = SelectMultipleField("Assists", coerce=int)

    submit = SubmitField("Set assists")

    # Initialization
    def __init__(self, *args, **kwargs):
        super(Car8Form, self).__init__(*args, **kwargs)

        self.assists_select.choices = [(assist.id, "{} ({})".format(assist.name_full, assist.name_short))
                                       for assist
                                       in Assist.query
                                .order_by(Assist.name_full.asc()).all()]


# Aspiration
class AspirationForm(FlaskForm):

    # General
    name = StringField("Name", validators=[DataRequired()])


class AspirationAddForm(AspirationForm):

    submit = SubmitField("Add aspiration")


class AspirationEditForm(AspirationForm):

    submit = SubmitField("Edit aspiration")


# Assists
class AssistForm(FlaskForm):

    # General
    name_full = StringField("Full name", validators=[DataRequired()])
    name_short = StringField("Short name", validators=[DataRequired()])


class AssistAddForm(AssistForm):

    submit = SubmitField("Add assist")


class AssistEditForm(AssistForm):

    submit = SubmitField("Edit assist")


# Body styles
class BodyStyleForm(FlaskForm):

    # General
    name = StringField("Name", validators=[DataRequired()])
    no_of_doors = IntegerField("No. of doors", validators=[DataRequired()])


class BodyStyleAddForm(BodyStyleForm):

    submit = SubmitField("Add body style")


class BodyStyleEditForm(BodyStyleForm):

    submit = SubmitField("Edit body style")


# Car class
class CarClassForm(FlaskForm):

    # General
    name_custom = StringField("Name", validators=[DataRequired()])
    name_short = StringField("Name", validators=[Optional()])
    name_euro = StringField("Euro", validators=[Optional()])
    name_us = StringField("US", validators=[Optional()])
    name_alternative = StringField("Alternative", validators=[Optional()])


class CarClassAddForm(CarClassForm):

    submit = SubmitField("Add car class")


class CarClassEditForm(CarClassForm):

    submit = SubmitField("Edit car class")


# Drivetrain
class DrivetrainForm(FlaskForm):

    # General
    name_full = StringField("Name", validators=[DataRequired()])
    name_short = StringField("Name", validators=[DataRequired()])


class DrivetrainAddForm(DrivetrainForm):

    submit = SubmitField("Add drivetrain")


class DrivetrainEditForm(DrivetrainForm):

    submit = SubmitField("Edit drivetrain")


# Engine layout
class EngineLayoutForm(FlaskForm):

    # General
    name = StringField("Name", validators=[DataRequired()])


class EngineLayoutAddForm(EngineLayoutForm):

    submit = SubmitField("Add engine layout")


class EngineLayoutEditForm(EngineLayoutForm):

    submit = SubmitField("Edit engine layout")


# Fuel type
class FuelForm(FlaskForm):

    # General
    name = StringField("Name", validators=[DataRequired()])


class FuelAddForm(FuelForm):

    submit = SubmitField("Add fuel type")


class FuelEditForm(FuelForm):

    submit = SubmitField("Edit fuel type")
