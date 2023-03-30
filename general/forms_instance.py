from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired, Optional

from general.models.car import Car
from general.models.game import Game
from general.models.instance import InstanceType, InstanceSpecialization


class SelectGameForm(FlaskForm):

    game_name_full = SelectField("Game", coerce=str)
    car_id = SelectField("Car", coerce=int)

    submit = SubmitField("Select game")

    # Initialization
    def __init__(self, *args, **kwargs):
        super(SelectGameForm, self).__init__(*args, **kwargs)

        self.game_name_full.choices = [(game.name_full, "{}".format(game.name_full))
                                       for game
                                       in Game.query
                                       .order_by(Game.name_display.asc()).all()]

        self.car_id.choices = [(car.id, "{}".format(car.name_display))
                               for car
                               in Car.query
                               .order_by(Car.name_display.asc()).all()]


class InstanceForm(FlaskForm):

    # General
    name_full = StringField("Full name", validators=[DataRequired()])
    name_nickname = StringField("Nickname", validators=[DataRequired()])
    instance_type_id = SelectField("Instance type", coerce=int)
    specialization_id = SelectField("Specialization", coerce=int)
    is_complete = BooleanField("Complete")
    is_for_collection = BooleanField("For collection only")

    # Visuals
    color_name = StringField("Color name", validators=[Optional()])
    color_hex = StringField("Color hex value", validators=[Optional()])
    theme = StringField("Theme", validators=[Optional()])

    # Initialization
    def __init__(self, *args, **kwargs):
        super(InstanceForm, self).__init__(*args, **kwargs)

        self.instance_type_id.choices = [(instance_type.name_full, "{}".format(instance_type.name_full))
                                         for instance_type
                                         in InstanceType.query
                                         .order_by(InstanceType.name_full.asc()).all()]

        self.specialization_id.choices = [(specialization.name_full, "{}".format(specialization.name_full))
                                          for specialization
                                          in InstanceSpecialization.query
                                          .order_by(InstanceSpecialization.name_full.asc()).all()]
