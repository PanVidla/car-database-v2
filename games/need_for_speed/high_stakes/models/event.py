from general import database
from general.models.event import Event


# Represents a type of race in NFS4 - further split into Career and Arcade event
class EventNFS4(Event):

    __tablename__ = "events_nfs4"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('events.id'), primary_key=True)

    # Game-specific
    no_of_participants = database.Column(database.Integer, index=True, nullable=False)
    no_of_laps = database.Column(database.Integer, index=True, nullable=False)
    skill_level = database.Column(database.Unicode, index=True, nullable=True)
    car_restriction = database.Column(database.Unicode, index=True, nullable=True)

    is_ranked = database.Column(database.Boolean, index=True)

    # Relationships
    records = database.relationship('EventRecordNFS4', backref='event', lazy='dynamic')

    def get_car_restriction(self):
        return self.car_restriction if self.car_restriction != "" else "n/a"

    def get_skill_level(self):
        return self.skill_level if self.skill_level != "" else "n/a"


# Represents an arcade event in NFS4 - single race, hot pursuit, time trial...
# The specific conditions for the event are a part of the event record, not the event itself
class ArcadeEventNFS4(EventNFS4):

    __tablename__ = "events_nfs4_arcade"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('events_nfs4.id'), primary_key=True)

    # General
    order_in_overview = database.Column(database.Integer, index=True, unique=True, nullable=False)
    arcade_series_id = database.Column(database.Integer, database.ForeignKey('series_nfs4_arcade.id'), nullable=False)
    order_in_series = database.Column(database.Integer, index=True, unique=True, nullable=False)


# Represents an arcade event in NFS4 - single race, hot pursuit, time trial...
class CareerEventNFS4(EventNFS4):

    __tablename__ = "events_nfs4_career"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('events_nfs4.id'), primary_key=True)

    # General
    career_series_id = database.Column(database.Integer, database.ForeignKey('series_nfs4_career.id'), nullable=False)
    order_in_series = database.Column(database.Integer, index=True, nullable=False)
    track_id = database.Column(database.Integer, database.ForeignKey('tracks_nfs4.id'), nullable=False)

    # Conditions
    is_backwards = database.Column(database.Boolean, default=False, nullable=False)
    is_mirrored = database.Column(database.Boolean, default=False, nullable=False)
    is_at_night = database.Column(database.Boolean, default=False, nullable=False)
    is_weather_on = database.Column(database.Boolean, default=False, nullable=False)


class SeriesNFS4(database.Model):

    __tablename__ = "series_nfs4"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False)
    no_of_participants = database.Column(database.Integer, index=True, nullable=False)
    skill_level = database.Column(database.Unicode, index=True, nullable=True)
    car_restriction = database.Column(database.Unicode, index=True, nullable=True)

    order_in_list = database.Column(database.Integer, index=True, nullable=False)


class ArcadeSeriesNFS4(SeriesNFS4):

    __tablename__ = "series_nfs4_arcade"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('series_nfs4.id'), primary_key=True)


class CareerSeriesNFS4(SeriesNFS4):

    __tablename__ = "series_nfs4_career"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('series_nfs4.id'), primary_key=True)

    # General
    tour_id = database.Column(database.Integer, database.ForeignKey('tours_nfs4.id'), nullable=False)
    order_in_tour = database.Column(database.Integer, index=True, nullable=False)


class TourNFS4(database.Model):

    __tablename__ = "tours_nfs4"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False)
    order_in_overview = database.Column(database.Integer, index=True, nullable=False)
