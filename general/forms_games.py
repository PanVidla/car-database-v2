from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SubmitField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, Optional, NumberRange

from general.models.game import GameSeries, GameGenre, Platform
from general.models.misc import Company


# Game
class GameGeneralForm(FlaskForm):

    # General
    name_full = StringField("Full name", validators=[DataRequired()])
    name_display = StringField("Display name", validators=[DataRequired()])
    name_short = StringField("Short name", validators=[DataRequired()])

    developer_id = SelectField("Developed by", coerce=int)
    game_series_id = SelectField("Part of series", coerce=int)
    order_in_series = IntegerField("No. in series", validators=[Optional(), NumberRange(min=1)])
    date_released = DateField("Date of release", validators=[Optional()])
    genre_id = SelectField("Genre", coerce=int)

    # Initialization
    def __init__(self, *args, **kwargs):
        super(GameGeneralForm, self).__init__(*args, **kwargs)

        self.developer_id.choices = [(company.id, "{}".format(company.name_display))
                                      for company
                                      in Company.query
                                     .filter(Company.is_game_developer == True)
                                     .order_by(Company.name_display.asc()).all()]

        self.game_series_id.choices = [(-1, "None")]
        self.game_series_id.choices += [(series.id, "{}".format(series.name))
                                        for series
                                        in GameSeries.query.order_by(GameSeries.name.asc()).all()]

        self.genre_id.choices = [(genre.id, "{}".format(genre.name))
                                 for genre
                                 in GameGenre.query.order_by(GameGenre.name.asc()).all()]


class GameGeneralAddForm(GameGeneralForm):
    submit = SubmitField("Add game")


class GameGeneralEditForm(GameGeneralForm):
    submit = SubmitField("Edit game")


class GamePlatformsForm(FlaskForm):

    # General
    platforms = SelectMultipleField("Platforms", validators=[DataRequired()], coerce=int)

    # Initialization
    def __init__(self, *args, **kwargs):
        super(GamePlatformsForm, self).__init__(*args, **kwargs)

        self.platforms.choices = [(platform.id, "{}".format(platform.name_display))
                                   for platform
                                   in Platform.query
                                   .order_by(Platform.name_display.asc()).all()]


class GamePlatformsAddForm(GamePlatformsForm):
    submit = SubmitField("Add platforms")


class GamePlatformsEditForm(GamePlatformsForm):
    submit = SubmitField("Add platforms")


# Game series
class GameSeriesForm(FlaskForm):

    # General
    name = StringField("Name", validators=[DataRequired()])


class GameSeriesAddForm(GameSeriesForm):

    submit = SubmitField("Add game series")


class GameSeriesEditForm(GameSeriesForm):

    submit = SubmitField("Edit game series")


# Genre
class GameGenreForm(FlaskForm):

    name = StringField("Name", validators=[DataRequired()])
    realism = IntegerField("Realism", validators=[DataRequired(), NumberRange(min=1, max=5)])


class GameGenreAddForm(GameGenreForm):

    submit = SubmitField("Add genre")


class GameGenreEditForm(GameGenreForm):
    submit = SubmitField("Edit genre")


# Platform
class PlatformForm(FlaskForm):

    # General
    name_full = StringField("Full name", validators=[DataRequired()])
    name_display = StringField("Display name", validators=[DataRequired()])
    name_short = StringField("Short name", validators=[DataRequired()])


class PlatformAddForm(PlatformForm):

    submit = SubmitField("Add platform")


class PlatformEditForm(PlatformForm):

    submit = SubmitField("Edit platform")
