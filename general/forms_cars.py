from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Optional


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


# Car class
class CarClassForm(FlaskForm):

    # General
    name_custom = StringField("Name", validators=[DataRequired()])
    name_short = StringField("Name", validators=[Optional()])
    name_euro = StringField("Euro", validators=[Optional()])
    name_us = StringField("US", validators=[Optional()])
    name_alternative = StringField("Alternative", validators=[Optional()])


class CarClassAddForm(CarClassForm):

    submit = SubmitField("Add car class")


class CarClassEditForm(CarClassForm):

    submit = SubmitField("Edit car class")


# Drivetrain
class DrivetrainForm(FlaskForm):

    # General
    name_full = StringField("Name", validators=[DataRequired()])
    name_short = StringField("Name", validators=[DataRequired()])


class DrivetrainAddForm(DrivetrainForm):

    submit = SubmitField("Add drivetrain")


class DrivetrainEditForm(DrivetrainForm):

    submit = SubmitField("Edit drivetrain")
