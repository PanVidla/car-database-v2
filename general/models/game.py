from datetime import datetime

from flask import flash, redirect, url_for
from sqlalchemy.orm import backref

from general import database, cardb
from general.models.info import Text, Image


# Represents a video game (e.g. Need for Speed III: Hot Pursuit, Forza Horizon 4...)
class Game(database.Model):

    __tablename__ = "games"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)
    datetime_added = database.Column(database.DateTime, default=datetime.utcnow, index=True, nullable=False)
    datetime_edited = database.Column(database.DateTime, default=datetime.utcnow, index=True, nullable=False)
    datetime_played = database.Column(database.DateTime, index=True, nullable=True)
    is_deleted = database.Column(database.Boolean, default=False, index=True, nullable=False)

    # General
    # Full name, e.g. Need for Speed III: Hot Pursuit
    name_full = database.Column(database.Unicode, index=True, nullable=False)
    # Display name, e.g. Need for Speed III
    name_display = database.Column(database.Unicode, nullable=False)
    # Short name, e.g. NFS3
    name_short = database.Column(database.Unicode, nullable=False)
    game_series_id = database.Column(database.Integer, database.ForeignKey("game_series.id"), index=True, nullable=True)
    order_in_series = database.Column(database.Integer, nullable=True)
    platforms = database.relationship('Platform', secondary="game_platform")
    developer_id = database.Column(database.Integer, database.ForeignKey("companies.id"), index=True, nullable=False)
    date_released = database.Column(database.Date, index=True, nullable=True)
    genre_id = database.Column(database.Integer, database.ForeignKey("game_genres.id"), index=True, nullable=False)

    # Technical
    game_state_id = database.Column(database.Integer, database.ForeignKey("game_states.id"), nullable=True)
    activities = database.relationship('GameActivity', backref='game', lazy='dynamic')

    # Statistics
    no_of_instances = database.Column(database.Integer, default=0, nullable=False)
    no_of_times_played = database.Column(database.Integer, default=0, nullable=False)

    # Relationships
    games = database.relationship('Event', backref='game', lazy='dynamic')
    instances = database.relationship('Instance', backref='game', lazy='dynamic')
    texts = database.relationship('GameText', backref='game', lazy='dynamic')
    images = database.relationship('GameImage', backref='game', lazy='dynamic')

    def edit_game_from_form(self, form):

        # If the game is not in a series
        if form.game_series_id.data == -1:
            self.game_series_id = None
            self.order_in_series = None

        else:
            # If the game in the same series with the same order exists
            existing_game = Game.query.filter(
                Game.game_series_id == form.game_series_id.data,
                Game.order_in_series == form.order_in_series.data,
                Game.is_deleted == False).first()
            if existing_game is not None:
                flash("{} already has the same order in the same series!".format(existing_game.name_display), "warning")
                return -1

        # If the game is in a series, but order in series is not filled out
        if (form.game_series_id.data != -1) and (form.order_in_series.data is None):
            flash("If the game is a part of a series, the order in the series needs to be filled out!", "warning")
            return -1

        form.populate_obj(self)
        self.datetime_edited = datetime.utcnow()

        return 0

    def get_datetime_added(self):
        return "{}".format(
            self.datetime_added.strftime("%d.%m.%Y %H:%M:%S")) if self.datetime_added is not None else "n/a"

    def get_datetime_edited(self):
        return "{}".format(
            self.datetime_edited.strftime("%d.%m.%Y %H:%M:%S")) if self.datetime_edited is not None else "n/a"

    def get_datetime_played(self):
        return "{}".format(
            self.datetime_played.strftime("%d.%m.%Y %H:%M:%S")) if self.datetime_played is not None else "n/a"

    def get_description(self):

        description_string = ""

        if self.genre.name == ("arcade" or "arcade-simcade"):
            description_string += "An"

        else:
            description_string += "A"

        description_string += " {} game from {} developed by {} for {}".format(self.genre.name,
                                                                               self.get_year_released(),
                                                                               self.developer.name_display,
                                                                               self.get_platforms())

        return description_string

    def get_images(self):

        images = GameImage.query.filter(GameImage.game_id == self.id, GameImage.is_logo == False)
        images = images.order_by(GameImage.order.asc()).all()

        return images

    def get_last_played_date(self):
        return "{}".format(
            self.datetime_played.strftime("%d.%m.%Y")) if self.datetime_played is not None else "n/a"

    def get_logos(self):

        logos = GameImage.query.filter(GameImage.game_id == self.id, GameImage.is_logo == True)
        logos = logos.order_by(GameImage.order.asc()).all()

        return logos

    def get_date_released(self):
        return "{}".format(
            self.date_released.strftime("%d.%m.%Y")) if self.date_released is not None else "n/a"

    def get_platforms(self):

        game_platform_associations = GamePlatform.query.filter(GamePlatform.game_id == self.id).all()

        if game_platform_associations == []:
            return "n/a"

        platform_string = ""
        first = True

        for game_platform_association in game_platform_associations:
            if first is not True:
                platform_string += " / "

            platform_string += game_platform_association.platform.name_short

            first = False

        return platform_string

    def get_state(self):
        return self.state.name if self.state is not None else "n/a"

    def get_series(self):
        return self.series.name if self.series is not None else "n/a"

    def get_year_released(self):
        return self.date_released.year if self.date_released is not None else "n/a"

    def set_platforms(self, platform_ids):

        # Delete the old game-platform associations
        game_platform_old = GamePlatform.query.filter(GamePlatform.game_id == self.id).all()

        for game_platform_association in game_platform_old:

            try:
                database.session.delete(game_platform_association)

            except RuntimeError:
                flash("There was a problem deleting an old association between {} and {}.".format(self.name_display, game_platform_association.platform.name_display), "danger")

            database.session.commit()

        # Create new game-platform associations
        for platform_id in platform_ids:

            try:
                game_platform_association = GamePlatform(game_id=self.id, platform_id=platform_id)
                database.session.add(game_platform_association)

            except RuntimeError:
                platform = Platform.query.get(platform_id)
                flash("There was a problem adding a new association between {} and {}.".format(self.name_display, platform.name_display), "danger")

            database.session.commit()

        self.datetime_edited = datetime.utcnow()


def create_game_from_form(form):

    # Check if a game from the same year with the same name already exists
    existing_game = Game.query.filter(Game.name_display == form.name_display.data,
                                      Game.date_released == form.date_released.data).first()

    if existing_game is not None:
        flash("There is already a game of this name and released in the same year in the database.", "warning")
        return -1

    new_game = Game()
    form.populate_obj(new_game)

    # Assign a base game state
    initial_game_state = GameState.query.order_by(GameState.order.asc()).first()
    new_game.game_state_id = initial_game_state.id

    # If the game is not in a series
    if form.game_series_id.data == -1:
        new_game.game_series_id = None
        new_game.order_in_series = None

    else:
        # If the game in the same series with the same order exists
        if Game.query.filter(
                Game.game_series_id == form.game_series_id.data,
                Game.order_in_series == form.order_in_series.data).first() is not None:
            flash("There is already a game in the same series with the same order in the series!", "warning")
            return -1

    # If the game is in a series, but order in series is not filled out
    if (form.game_series_id.data != -1) and (form.order_in_series.data is None):
        flash("If the game is a part of a series, the order in the series needs to be filled out!", "warning")
        return -1

    return new_game


def get_games_in_progress():

    games_in_progress = Game.query\
        .filter(Game.game_state_id == 2,
                Game.is_deleted == False)\
        .order_by(Game.name_display.asc())\
        .all()

    return games_in_progress


cardb.jinja_env.globals.update(get_games_in_progress=get_games_in_progress)


# Serves to keep track of what should be played next in the game (e.g. multiplayer (co-op), tournament...)
class GameActivity(database.Model):

    __tablename__ = "game_activities"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False)
    description = database.Column(database.Unicode, nullable=True)
    order = database.Column(database.Integer, nullable=False)
    is_active = database.Column(database.Boolean, default=False, nullable=False)

    # Relationships
    game_id = database.Column(database.Integer, database.ForeignKey("games.id"), nullable=False)


def activity_with_same_order_number_exists(game, order):

    activity = GameActivity.query.filter(GameActivity.game_id == game.id, GameActivity.order == order).first()

    if activity is None:
        return False
    else:
        return True


def create_initial_activity_from_form(form, game):

    new_activity = GameActivity()
    form.populate_obj(new_activity)
    new_activity.game_id = game.id
    new_activity.order = 1
    new_activity.is_active = True

    return new_activity


def create_non_initial_activity_from_form(form, game):

    if activity_with_same_order_number_exists(game, form.order.data):
        return -1

    new_activity = GameActivity()
    form.populate_obj(new_activity)
    new_activity.game_id = game.id
    new_activity.is_active = False

    return new_activity


# Represents a (racing) game genre (e.g. arcade, simcade, simulation...)
class GameGenre(database.Model):

    __tablename__ = "game_genres"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False, unique=True)
    # Should be a value between 0 and 4 (0 - arcade, 2 - simcade, 4 - simulation)
    realism = database.Column(database.Integer, nullable=False, unique=True)

    # Relationships
    games = database.relationship('Game', backref='genre', lazy='dynamic')

    def get_css_name(self):

        if self.name == "arcade":
            return "genre-arcade"

        if self.name == "arcade-simcade":
            return "genre-arcade-simcade"

        if self.name == "simcade":
            return "genre-simcade"

        if self.name == "simcade-simulation":
            return "genre-simcade-simulation"

        if self.name == "simulation":
            return "genre-simulation"


# Represents a series of games (e.g. Need for Speed, Forza, Test Drive...)
class GameSeries(database.Model):

    __tablename__ = "game_series"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False, unique=True)

    # Relationships
    games = database.relationship('Game', backref='series', lazy='dynamic')
    texts = database.relationship('GameSeriesText', backref='game_series', lazy='dynamic')
    images = database.relationship('GameSeriesImage', backref='game_series', lazy='dynamic')

    def get_images(self):

        images = GameSeriesImage.query.filter(GameSeriesImage.game_series_id == self.id, GameSeriesImage.is_logo == False)
        images = images.order_by(GameSeriesImage.order.asc()).all()

        return images

    def get_logos(self):

        logos = GameSeriesImage.query.filter(GameSeriesImage.game_series_id == self.id, GameSeriesImage.is_logo == True)
        logos = logos.order_by(GameSeriesImage.order.asc()).all()

        return logos


# Represents the state of the game (e.g. not started, in-progressed, finished...)
class GameState(database.Model):

    __tablename__ = "game_states"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    order = database.Column(database.Integer, index=True, nullable=False, unique=True)
    name = database.Column(database.Unicode, index=True, nullable=False, unique=True)

    # Relationships
    games = database.relationship('Game', backref='state', lazy='dynamic')

    def get_css_name(self):

        if self.name == "not started":
            return "state-not-started"

        if self.name == "in-progress":
            return "state-in-progress"

        if self.name == "complete":
            return "state-complete"

        if self.name == "100%":
            return "state-100"

        if self.name == "paused":
            return "state-paused"

        if self.name == "aborted":
            return "state-aborted"


# Represents a video game platform (e.g. PC, PlayStation 3, Android...)
class Platform(database.Model):

    __tablename__ = "platforms"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    # Full name, e.g. PlayStation 3
    name_full = database.Column(database.Unicode, index=True, nullable=False, unique=True)
    # Display name, e.g. Playstation 3
    name_display = database.Column(database.Unicode, nullable=False, unique=True)
    # Short name, e.g. PS3
    name_short = database.Column(database.Unicode, nullable=False, unique=True)

    # Relationships
    games = database.relationship('Game', secondary="game_platform")
    texts = database.relationship('PlatformText', backref='platform', lazy='dynamic')
    images = database.relationship('PlatformImage', backref='platform', lazy='dynamic')

    def get_images(self):

        images = PlatformImage.query.filter(PlatformImage.platform_id == self.id, PlatformImage.is_logo == False)
        images = images.order_by(PlatformImage.order.asc()).all()

        return images

    def get_logos(self):

        logos = PlatformImage.query.filter(PlatformImage.platform_id == self.id, PlatformImage.is_logo == True)
        logos = logos.order_by(PlatformImage.order.asc()).all()

        return logos


# Info
class GameText(Text):

    __tablename__ = "texts_games"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('texts.id'), primary_key=True)

    # General
    game_id = database.Column(database.Integer, database.ForeignKey('games.id'), primary_key=True)


class GameImage(Image):

    __tablename__ = "images_games"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('images.id'), primary_key=True)

    # General
    is_logo = database.Column(database.Boolean, default=False, index=True, nullable=False)
    game_id = database.Column(database.Integer, database.ForeignKey('games.id'), primary_key=True)


class GameSeriesText(Text):

    __tablename__ = "texts_game_series"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('texts.id'), primary_key=True)

    # General
    game_series_id = database.Column(database.Integer, database.ForeignKey('game_series.id'), primary_key=True)


class GameSeriesImage(Image):

    __tablename__ = "images_game_series"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('images.id'), primary_key=True)

    # General
    is_logo = database.Column(database.Boolean, default=False, index=True, nullable=False)
    game_series_id = database.Column(database.Integer, database.ForeignKey('game_series.id'), primary_key=True)


class PlatformText(Text):

    __tablename__ = "texts_platforms"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('texts.id'), primary_key=True)

    # General
    platform_id = database.Column(database.Integer, database.ForeignKey('platforms.id'), primary_key=True)


class PlatformImage(Image):

    __tablename__ = "images_platforms"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('images.id'), primary_key=True)

    # General
    is_logo = database.Column(database.Boolean, default=False, index=True, nullable=False)
    platform_id = database.Column(database.Integer, database.ForeignKey('platforms.id'), primary_key=True)


# Many-to-many relationships
class GamePlatform(database.Model):

    __tablename__ = "game_platform"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)
    game_id = database.Column(database.Integer, database.ForeignKey("games.id"))
    platform_id = database.Column(database.Integer, database.ForeignKey("platforms.id"))
    game = database.relationship('Game', backref=backref("game_platform", cascade="all, delete-orphan"))
    platform = database.relationship('Platform', backref=backref("game_platform", cascade="all, delete-orphan"))
