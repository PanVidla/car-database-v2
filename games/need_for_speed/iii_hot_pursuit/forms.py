from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField, StringField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Optional, Length, InputRequired

from games.need_for_speed.iii_hot_pursuit.models.instance import ClassNFS3
from general.models.misc import Country


class InstanceNFS3Form(FlaskForm):

    # Game-specific
    nfs3_class_id = SelectField("Class", coerce=int)
    acceleration = IntegerField("Acceleration", validators=[DataRequired(), NumberRange(min=0, max=20)])
    top_speed = IntegerField("Top speed", validators=[DataRequired(), NumberRange(min=0, max=20)])
    handling = IntegerField("Handling", validators=[DataRequired(), NumberRange(min=0, max=20)])
    braking = IntegerField("Braking", validators=[DataRequired(), NumberRange(min=0, max=20)])

    submit = SubmitField("Set game-specific information")

    # Initialization
    def __init__(self, *args, **kwargs):
        super(InstanceNFS3Form, self).__init__(*args, **kwargs)

        self.nfs3_class_id.choices = [(car_class.id, "{}".format(car_class.name))
                                          for car_class
                                          in ClassNFS3.query
                                          .order_by(ClassNFS3.name.asc()).all()]


class ClassNFS3Form(FlaskForm):

    # General
    name = StringField("Name", validators=[DataRequired()])
    color_hex = StringField("Color", validators=[Optional(), Length(min=7, max=7)])

    submit = SubmitField("Set class information")


class TuneNFS3Form(FlaskForm):

    # General
    engine = IntegerField("Engine", validators=[InputRequired(), NumberRange(min=-100, max=100)])
    brake_balance = IntegerField("Brake balance", validators=[InputRequired(), NumberRange(min=-100, max=100)])
    steering_speed = IntegerField("Steering speed", validators=[InputRequired(), NumberRange(min=-100, max=100)])
    gearbox_ratio = IntegerField("Gearbox ratio", validators=[InputRequired(), NumberRange(min=-100, max=100)])
    aerodynamics = IntegerField("Aerodynamics", validators=[InputRequired(), NumberRange(min=-100, max=100)])
    suspension = IntegerField("Suspension", validators=[InputRequired(), NumberRange(min=-100, max=100)])
    tyres = IntegerField("Tyres", validators=[InputRequired(), NumberRange(min=-100, max=100)])

    submit_edit_tune = SubmitField("Set tuning values")


class EventNFS3Form(FlaskForm):

    # General
    name = StringField("Name", validators=[InputRequired()])
    color_hex = StringField("Color", validators=[Optional()])

    no_of_participants = IntegerField("No. of participants", validators=[InputRequired(), NumberRange(min=1, max=8)])
    no_of_laps = IntegerField("No. of laps", validators=[InputRequired(), NumberRange(min=2, max=8)])
    is_ranked = BooleanField("Ranked")

    submit = SubmitField("Set event values")


class TrackNFS3Form(FlaskForm):

    # General
    name = StringField("Name", validators=[InputRequired()])
    country_id = SelectField("Country", coerce=int)

    submit = SubmitField("Set track values")

    # Initialization
    def __init__(self, *args, **kwargs):
        super(TrackNFS3Form, self).__init__(*args, **kwargs)

        self.country_id.choices = [(country.id, "{}".format(country.name_display))
                                   for country
                                   in Country.query.order_by(Country.name_display.asc()).all()]
