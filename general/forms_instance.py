from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired, Optional

from general.models.car import Car, Drivetrain, EngineLayout
from general.models.game import Game
from general.models.instance import InstanceType, InstanceSpecialization


class SelectGameForm(FlaskForm):

    game_name_full = SelectField("Game", coerce=int)
    car_id = SelectField("Car", coerce=int)

    submit = SubmitField("Select game")

    # Initialization
    def __init__(self, *args, **kwargs):
        super(SelectGameForm, self).__init__(*args, **kwargs)

        self.game_name_full.choices = [(game.id, "{}".format(game.name_full))
                                       for game
                                       in Game.query
                                       .filter(Game.is_deleted != True)
                                       .order_by(Game.name_display.asc()).all()]

        self.car_id.choices = [(car.id, "{}".format(car.name_display))
                               for car
                               in Car.query
                               .filter(Car.is_deleted != True)
                               .order_by(Car.name_display.asc()).all()]


class InstanceGeneralForm(FlaskForm):

    # General
    name_full = StringField("Full name", validators=[DataRequired()])
    name_nickname = StringField("Nickname", validators=[DataRequired()])
    instance_type_id = SelectField("Instance type", coerce=int)
    specialization_id = SelectField("Specialization", coerce=int)
    drivetrain_id = SelectField("Drivetrain", coerce=int)
    engine_layout_id = SelectField("Engine layout", coerce=int)
    is_complete = BooleanField("Complete")
    is_for_collection = BooleanField("Collection")

    # Visuals
    color_name = StringField("Color name", validators=[Optional()])
    color_hex = StringField("Color hex value", validators=[Optional()])
    theme = StringField("Theme", validators=[Optional()])

    submit = SubmitField("Set general information")

    # Initialization
    def __init__(self, *args, **kwargs):
        super(InstanceGeneralForm, self).__init__(*args, **kwargs)

        self.instance_type_id.choices = [(0, "n/a")]
        self.instance_type_id.choices += [(instance_type.id, "{}".format(instance_type.name_full))
                                          for instance_type
                                          in InstanceType.query
                                          .order_by(InstanceType.name_full.asc()).all()]

        self.specialization_id.choices = [(0, "n/a")]
        self.specialization_id.choices += [(specialization.id, "{}".format(specialization.name_full))
                                           for specialization
                                           in InstanceSpecialization.query
                                           .order_by(InstanceSpecialization.name_full.asc()).all()]

        self.drivetrain_id.choices = [(drivetrain.id, "{}".format(drivetrain.name_full))
                                      for drivetrain
                                      in Drivetrain.query
                                      .order_by(Drivetrain.id.asc()).all()]

        self.engine_layout_id.choices = [(engine_layout.id, "{}".format(engine_layout.name))
                                         for engine_layout
                                         in EngineLayout.query
                                         .order_by(EngineLayout.name.asc()).all()]


class InstanceTypeForm(FlaskForm):

    # General
    name_full = StringField("Name", validators=[DataRequired()])
    name_short = StringField("Shortcut", validators=[DataRequired()])
    color_hex = StringField("Color", validators=[Optional()])


class InstanceTypeAddForm(InstanceTypeForm):

    submit = SubmitField("Add instance type")


class InstanceTypeEditForm(InstanceTypeForm):

    submit = SubmitField("Edit instance type")


class SpecializationForm(FlaskForm):

    # General
    name_full = StringField("Name", validators=[DataRequired()])
    name_short = StringField("Shortcut", validators=[DataRequired()])
    color_hex = StringField("Color", validators=[Optional()])


class SpecializationAddForm(SpecializationForm):

    submit = SubmitField("Add specialization")


class SpecializationEditForm(SpecializationForm):

    submit = SubmitField("Edit specialization")
