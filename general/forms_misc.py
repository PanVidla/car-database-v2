from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Optional


class CountryForm(FlaskForm):

    # General
    name_full = StringField("Full name", validators=[DataRequired()])
    name_display = StringField("Display name", validators=[DataRequired()])
    name_short = StringField("Short name", validators=[Optional()])


class CountryAddForm(CountryForm):

    submit = SubmitField("Add country")


class CountryEditForm(CountryForm):

    submit = SubmitField("Edit country")
