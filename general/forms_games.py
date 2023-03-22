from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional

from general.models.misc import Company


class GameForm(FlaskForm):

    # General
    name_full = StringField("Full name", validators=[DataRequired()])
    name_display = StringField("Display name", validators=[DataRequired()])
    name_short = StringField("Short name", validators=[DataRequired()])

    developer_id = SelectField("Developed by", coerce=int)
    game_series_id = SelectField("Part of series", coerce=int)

    # Initialization
    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)

        self.developer_id.choices = [(company.id, "{}".format(company.name_display))
                                      for company
                                      in Company.query
                                     .filter(Company.is_game_developer == True)
                                     .order_by(Company.name_display.asc()).all()]


class GameSeriesForm(FlaskForm):

    # General
    name = StringField("Name", validators=[DataRequired()])


class GameSeriesAddForm(GameSeriesForm):

    submit = SubmitField("Add game series")


class GameSeriesEditForm(GameSeriesForm):
    submit = SubmitField("Edit game series")


class PlatformForm(FlaskForm):

    # General
    name_full = StringField("Full name", validators=[DataRequired()])
    name_display = StringField("Display name", validators=[DataRequired()])
    name_short = StringField("Short name", validators=[DataRequired()])


class PlatformAddForm(PlatformForm):

    submit = SubmitField("Add platform")


class PlatformEditForm(PlatformForm):

    submit = SubmitField("Edit platform")
