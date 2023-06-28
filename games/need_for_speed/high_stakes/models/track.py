from games.need_for_speed.high_stakes.models.record import EventRecordNFS4
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

    def get_best_lap_time_human_readable(self):
        return EventRecordNFS4.query.get(self.best_lap_time_event_record_id).time_best_lap_human_readable if self.best_lap_time_event_record_id is not None else "n/a"

    def get_best_lap_time_instance_string(self):
        return EventRecordNFS4.query.get(self.best_lap_time_event_record_id).instance.name_nickname if self.best_lap_time_event_record_id is not None else "n/a"

    def get_best_lap_time_milliseconds(self):
        return EventRecordNFS4.query.get(self.best_lap_time_event_record_id).time_best_lap_milliseconds if self.best_lap_time_event_record_id is not None else "n/a"

    def get_best_track_time_human_readable(self):
        return EventRecordNFS4.query.get(self.best_track_time_event_record_id).time_track_human_readable if self.best_track_time_event_record_id is not None else "n/a"

    def get_best_track_time_instance_string(self):
        return EventRecordNFS4.query.get(self.best_track_time_event_record_id).instance.name_nickname if self.best_track_time_event_record_id is not None else "n/a"

    def get_best_track_time_milliseconds(self):
        return EventRecordNFS4.query.get(self.best_track_time_event_record_id).time_track_milliseconds if self.best_track_time_event_record_id is not None else "n/a"

    def get_event_records(self):
        return EventRecordNFS4.query.filter(EventRecordNFS4.track_id == self.id,
                                            EventRecordNFS4.is_deleted == False)\
            .order_by(EventRecordNFS4.datetime_added.desc()).all()

    def update_best_lap_time_event_record(self):

        remaining_event_records = EventRecordNFS4.query.filter(EventRecordNFS4.track_id == self.id,
                                                               EventRecordNFS4.time_best_lap_milliseconds != None,
                                                               EventRecordNFS4.is_deleted == False)\
            .order_by(EventRecordNFS4.time_best_lap_milliseconds.asc()).all()

        self.best_lap_time_event_record_id = remaining_event_records[0].id

    def update_best_track_time_event_record(self):

        remaining_event_records = EventRecordNFS4.query.filter(EventRecordNFS4.track_id == self.id,
                                                               EventRecordNFS4.time_track_milliseconds != None,
                                                               EventRecordNFS4.is_deleted == False) \
            .order_by(EventRecordNFS4.time_track_milliseconds.asc()).all()

        self.best_track_time_event_record_id = remaining_event_records[0].id