from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, DecimalField, IntegerField, SubmitField
from wtforms.validators import Optional, DataRequired, NumberRange

from general.models.misc import Company
from general.models.part import FuelType, CombustionEngineType, Aspiration, ElectricEngineType


# Engine
class EngineForm(FlaskForm):

    # General
    manufacturer_id = SelectField("Manufacturer", coerce=int)
    name_official = StringField("Official name", validators=[Optional()])
    name_display = StringField("Display name", validators=[DataRequired()])

    # Technical
    fuel_type_id = SelectField("Fuel type", coerce=int)
    max_power_output_kw = DecimalField("Maximum power", validators=[Optional(), NumberRange(min=0.0)])
    max_power_output_rpm = IntegerField("Maximum power RPM", validators=[Optional(), NumberRange(min=0)])
    max_torque_nm = DecimalField("Maximum torque", validators=[Optional(), NumberRange(min=0.0)])
    max_torque_rpm = IntegerField("Maximum torque RPM", validators=[Optional(), NumberRange(min=0)])

    # Initialization
    def __init__(self, *args, **kwargs):
        super(EngineForm, self).__init__(*args, **kwargs)

        self.manufacturer_id.choices = [(0, "n/a")]
        self.manufacturer_id.choices += [(manufacturer.id, "{}".format(manufacturer.name_display))
                                         for manufacturer
                                         in Company.query
                                         .filter(Company.is_car_part_manufacturer == True)
                                         .order_by(Company.name_display.asc()).all()]

        self.fuel_type_id.choices = [(fuel_type.id, "{}".format(fuel_type.name))
                                     for fuel_type
                                     in FuelType.query
                                     .order_by(FuelType.name.asc()).all()]


# Combustion engine
class EngineCombustionForm(EngineForm):

    # Technical
    combustion_engine_type_id = SelectField("Engine type", coerce=int)
    displacement = DecimalField("Displacement", validators=[Optional(), NumberRange(min=0.0)])
    aspiration_id = SelectField("Aspiration", coerce=int)
    cylinder_alignment = StringField("Cylinder alignment", validators=[Optional()])
    valves_per_cylinder = StringField("Valves per cylinder", validators=[Optional()])

    # Initialization
    def __init__(self, *args, **kwargs):
        super(EngineCombustionForm, self).__init__(*args, **kwargs)

        self.combustion_engine_type_id.choices = [(0, "n/a")]
        self.combustion_engine_type_id.choices += [(combustion_engine_type.id, "{}".format(combustion_engine_type.name))
                                                   for combustion_engine_type
                                                   in CombustionEngineType.query
                                                   .order_by(CombustionEngineType.name.asc()).all()]

        self.aspiration_id.choices = [(0, "n/a")]
        self.aspiration_id.choices += [(aspiration.id, "{}".format(aspiration.name))
                                                   for aspiration
                                                   in Aspiration.query
                                                   .order_by(Aspiration.name.asc()).all()]


# Electric engine
class EngineElectricForm(EngineForm):

    # Technical
    electric_engine_type_id = SelectField("Engine type", coerce=int)
    battery_voltage = IntegerField("Battery voltage", validators=[Optional(), NumberRange(min=0)])
    battery_technology = StringField("Battery technology", validators=[Optional()])

    # Initialization
    def __init__(self, *args, **kwargs):
        super(EngineElectricForm, self).__init__(*args, **kwargs)

        self.electric_engine_type_id.choices = [(0, "n/a")]
        self.electric_engine_type_id.choices += [(electric_engine_type.id, "{}".format(electric_engine_type.name))
                                                 for electric_engine_type
                                                 in ElectricEngineType.query
                                                 .order_by(ElectricEngineType.name.asc()).all()]


class EngineCombustionAddForm(EngineCombustionForm):

    submit = SubmitField("Add combustion engine")


class EngineCombustionEditForm(EngineCombustionForm):

    submit = SubmitField("Edit combustion engine")


class EngineElectricAddForm(EngineElectricForm):

    submit = SubmitField("Add electric engine")


class EngineElectricEditForm(EngineElectricForm):

    submit = SubmitField("Edit electric engine")


# Engine type
class EngineTypeForm(FlaskForm):

    # General
    name = StringField("Name", validators=[DataRequired()])


class EngineTypeAddForm(EngineTypeForm):

    submit = SubmitField("Add engine type")


class EngineTypeEditForm(EngineTypeForm):

    submit = SubmitField("Edit engine type")


# Forced induction
class ForcedInductionForm(FlaskForm):

    # General
    manufacturer_id = SelectField("Manufacturer", coerce=int)
    name_official = StringField("Official name", validators=[Optional()])
    name_display = StringField("Display name", validators=[DataRequired()])

    # Technical
    boost_pressure_bar = DecimalField("Boost pressure", validators=[Optional()])
    force_induction_type_id = SelectField("Type", coerce=int)

    # Initialization
    def __init__(self, *args, **kwargs):
        super(ForcedInductionForm, self).__init__(*args, **kwargs)

        self.manufacturer_id.choices = [(0, "n/a")]
        self.manufacturer_id.choices += [(manufacturer.id, "{}".format(manufacturer.name_display))
                                         for manufacturer
                                         in Company.query
                                         .filter(Company.is_car_part_manufacturer == True)
                                         .order_by(Company.name_display.asc()).all()]

        self.force_induction_type_id.choices = [(forced_induction_type.id, "{}".format(forced_induction_type.name))
                                                for forced_induction_type
                                                in Aspiration.query
                                                .filter(Aspiration.name != "naturally aspirated")
                                                .order_by(Aspiration.id.asc()).all()]


class ForcedInductionAddForm(ForcedInductionForm):

    submit = SubmitField("Add forced induction")


class ForcedInductionEditForm(ForcedInductionForm):

    submit = SubmitField("Edit forced induction")
