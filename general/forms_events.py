from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, NumberRange


class EventTypeForm(FlaskForm):

    # General
    name = StringField("Name", validators=[DataRequired()])
    color_hex = StringField("Color", validators=[Optional(), Length(min=7, max=7)])
    order_in_list = IntegerField("Order", validators=[Optional(), NumberRange(min=1)])

    submit = SubmitField("Set event type data")
