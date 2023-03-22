from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional


class PlatformForm(FlaskForm):

    # General
    name_full = StringField("Full name", validators=[DataRequired()])
    name_display = StringField("Display name", validators=[DataRequired()])
    name_short = StringField("Short name", validators=[Optional()])


class PlatformAddForm(PlatformForm):

    submit = SubmitField("Add platform")


class PlatformEditForm(PlatformForm):

    submit = SubmitField("Edit platform")
