from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


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