from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

from general.models.game import Game


class SelectGameForm(FlaskForm):

    game_name_full = SelectField("Game", coerce=str)

    submit = SubmitField("Select game")

    # Initialization
    def __init__(self, *args, **kwargs):
        super(SelectGameForm, self).__init__(*args, **kwargs)

        self.game_name_full.choices = [(game.name_full, "{}".format(game.name_full))
                                       for game
                                       in Game.query
                                       .order_by(Game.name_display.asc()).all()]
