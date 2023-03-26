from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, BooleanField
from wtforms.validators import DataRequired, Optional


# Competition
class CompetitionForm(FlaskForm):

    # General
    name_full = StringField("Full name", validators=[DataRequired()])
    name_display = StringField("Display name", validators=[DataRequired()])
    name_short = StringField("Short name", validators=[DataRequired()])
    date_started = DateField("Started", validators=[Optional()])
    date_ended = DateField("Ended", validators=[Optional()])
    is_virtual = BooleanField("Is virtual?")


class CompetitionAddForm(CompetitionForm):

    submit = SubmitField("Add competition")


class CompetitionEditForm(CompetitionForm):

    submit = SubmitField("Edit competition")


# Country
class CountryForm(FlaskForm):

    # General
    name_full = StringField("Full name", validators=[DataRequired()])
    name_display = StringField("Display name", validators=[DataRequired()])
    name_short = StringField("Short name", validators=[Optional()])


class CountryAddForm(CountryForm):

    submit = SubmitField("Add country")


class CountryEditForm(CountryForm):

    submit = SubmitField("Edit country")
