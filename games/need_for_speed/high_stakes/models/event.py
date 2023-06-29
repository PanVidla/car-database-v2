from general import database
from general.models.event import Event


# Represents a type of race in NFS4 - further split into Career and Arcade event
class EventNFS4(Event):

    __tablename__ = "events_nfs4"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('events.id'), primary_key=True)

    # Game-specific
    no_of_participants = database.Column(database.Integer, index=True, nullable=False)
    no_of_laps = database.Column(database.Integer, index=True, nullable=True)
    skill_level = database.Column(database.Unicode, index=True, nullable=True)
    car_restriction = database.Column(database.Unicode, index=True, nullable=True)

    is_ranked = database.Column(database.Boolean, index=True)

    # Relationships
    records = database.relationship('EventRecordNFS4', backref='event', lazy='dynamic')

    def get_car_restriction(self):
        return self.car_restriction if self.car_restriction != "" else "n/a"

    def get_game_string(self):
        return "Need for Speed: High Stakes"

    def get_is_ranked(self):
        return "✓" if self.is_ranked is True else "x"

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
    order_in_series = database.Column(database.Integer, index=True, nullable=True)


def create_new_arcade_event_from_form(form):

    result = []

    # Check if there is already an arcade event with the same order in overview
    arcade_event_with_the_same_order_in_overview = ArcadeEventNFS4.query\
        .filter(ArcadeEventNFS4.order_in_overview == form.order_in_overview.data)\
        .first()
    if arcade_event_with_the_same_order_in_overview is not None:

        result.append(1)
        result.append(arcade_event_with_the_same_order_in_overview)
        result.append("The arcade event {} already has the same order in overview ({}) as this one.".format(
            arcade_event_with_the_same_order_in_overview.name,
            arcade_event_with_the_same_order_in_overview.order_in_overview))

        return result

    # Check if the arcade_series_id field is filled in and if it is, then check if the order is filled in as well
    if form.arcade_series_id.data != 0 and form.order_in_series.data is None:

        result.append(2)
        result.append(None)
        result.append("If the an arcade series is selected, the order in series needs to be filled in as well.")

        return result

    # If both the arcade_series_id and order_in_series are filled in, then check if there is already an event with
    # the same values.
    if form.arcade_series_id.data != 0 and form.order_in_series.data is not None:
        arcade_event_with_the_same_order_in_series = ArcadeEventNFS4.query\
            .filter(ArcadeEventNFS4.arcade_series_id == form.arcade_series_id.data,
                    ArcadeEventNFS4.order_in_series == form.order_in_series.data)\
            .first()
        if arcade_event_with_the_same_order_in_series is not None:

            result.append(3)
            result.append(arcade_event_with_the_same_order_in_series)
            result.append("There is already an arcade event ({}, {}, {}) in the same series with the same order in series.").format(arcade_event_with_the_same_order_in_series.name,
                                                                                                                                    arcade_event_with_the_same_order_in_series.series.name,
                                                                                                                                    arcade_event_with_the_same_order_in_series.order_in_series)

            return result

    # If the data pass all the checks above, create the arcade event
    new_arcade_event = ArcadeEventNFS4()
    form.populate_obj(new_arcade_event)

    result.append(0),
    result.append(new_arcade_event)
    result.append("Creating a new arcade event.")

    return result


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

    # Relationships
    events = database.relationship('ArcadeEventNFS4', backref='series', lazy='dynamic')


class CareerSeriesNFS4(SeriesNFS4):

    __tablename__ = "series_nfs4_career"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('series_nfs4.id'), primary_key=True)

    # General
    tour_id = database.Column(database.Integer, database.ForeignKey('tours_nfs4.id'), nullable=False)
    order_in_tour = database.Column(database.Integer, index=True, nullable=False)

    # Relationships
    events = database.relationship('CareerEventNFS4', backref='series', lazy='dynamic')


class TourNFS4(database.Model):

    __tablename__ = "tours_nfs4"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False)
    order_in_overview = database.Column(database.Integer, index=True, nullable=False)

    # Relationships
    series = database.relationship('CareerSeriesNFS4', backref='tour', lazy='dynamic')
