from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AssistForm(FlaskForm):

    # General
    name_full = StringField("Full name", validators=[DataRequired()])
    name_short = StringField("Short name", validators=[DataRequired()])


class AssistAddForm(AssistForm):

    submit = SubmitField("Add assist")


class AssistEditForm(AssistForm):

    submit = SubmitField("Edit assist")
