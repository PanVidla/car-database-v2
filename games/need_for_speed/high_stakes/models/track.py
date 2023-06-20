from general import database
from general.models.misc import Location


class TrackNFS4(Location):

    __tablename__ = "tracks_nfs4"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('locations.id'), primary_key=True)

    # General
    best_lap_time_event_record_id = database.Column(database.Integer, nullable=True)
    best_track_time_event_record_id = database.Column(database.Integer, nullable=True)

    # Relationships
    records = database.relationship('EventRecordNFS4', backref='track', lazy='dynamic')
