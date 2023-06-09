from games.need_for_speed.iii_hot_pursuit.models.records import EventRecordNFS3
from general import database
from general.models.misc import Location


class TrackNFS3(Location):

    __tablename__ = "tracks_nfs3"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('locations.id'), primary_key=True)

    # General
    best_lap_time_event_record_id = database.Column(database.Integer, nullable=True)
    best_track_time_event_record_id = database.Column(database.Integer, nullable=True)

    # Relationships
    records = database.relationship('EventRecordNFS3', backref='track', lazy='dynamic')

    def get_event_records(self):
        return EventRecordNFS3.query.filter(EventRecordNFS3.track_id == self.id,
                                            EventRecordNFS3.is_deleted == False)\
            .order_by(EventRecordNFS3.id.desc()).all()
