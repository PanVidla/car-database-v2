from datetime import datetime

from sqlalchemy.orm import backref

from general import database
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
    date_published = database.Column(database.Date, index=True, nullable=True)

    # Technical
    game_state_id = database.Column(database.Integer, database.ForeignKey("game_states.id"), nullable=True)
    activities = database.relationship('GameActivity', backref='game', lazy='dynamic')

    # Statistics
    no_of_instances = database.Column(database.Integer, default=0, nullable=False)
    no_of_times_played = database.Column(database.Integer, default=0, nullable=False)

    # Relationships
    texts = database.relationship('GameText', backref='game', lazy='dynamic')
    images = database.relationship('GameImage', backref='game', lazy='dynamic')


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


# Represents the state of the game (e.g. not started, in-progressed, finished...)
class GameState(database.Model):

    __tablename__ = "game_states"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    order = database.Column(database.Integer, index=True, nullable=False, unique=True)
    name = database.Column(database.Integer, index=True, nullable=False, unique=True)

    # Relationships
    games = database.relationship('Game', backref='state', lazy='dynamic')


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
