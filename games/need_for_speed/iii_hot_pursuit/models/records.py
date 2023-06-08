from datetime import datetime

from general import database


class EventRecordNFS3(database.Model):

    __tablename__ = "event_records_nfs3"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)
    datetime_added = database.Column(database.DateTime, default=datetime.utcnow, index=True, nullable=False)
    datetime_edited = database.Column(database.DateTime, default=datetime.utcnow, index=True, nullable=False)
    is_deleted = database.Column(database.Boolean, default=False, index=True, nullable=False)

    # General
    instance_id = database.Column(database.Integer, database.ForeignKey('instances_nfs3.id'), nullable=False)
    event_id = database.Column(database.Integer, database.ForeignKey('events_nfs3.id'), nullable=False)
    track_id = database.Column(database.Integer, database.ForeignKey('tracks_nfs3.id'), nullable=False)
    no_of_event_record = database.Column(database.Integer, nullable=False)
    note = database.Column(database.Unicode, nullable=True)

    # Results
    position = database.Column(database.Integer, nullable=True)
    result = database.Column(database.Unicode, nullable=True)
    time_best_lap_milliseconds = database.Column(database.BigInteger, index=True, nullable=True)
    time_best_lap_human_readable = database.Column(database.Unicode, nullable=True)
    time_track_milliseconds = database.Column(database.BigInteger, index=True, nullable=True)
    time_track_human_readable = database.Column(database.Unicode, nullable=True)
    is_lap_record = database.Column(database.Boolean, default=False, index=True, nullable=False)
    is_track_record = database.Column(database.Boolean, default=False, index=True, nullable=False)
    maximum_speed = database.Column(database.Double, nullable=True)

    # Conditions
    is_backwards = database.Column(database.Boolean, default=False,  nullable=False)
    is_mirrored = database.Column(database.Boolean, default=False,  nullable=False)
    is_at_night = database.Column(database.Boolean, default=False,  nullable=False)
    is_weather_on = database.Column(database.Boolean, default=False, nullable=False)
