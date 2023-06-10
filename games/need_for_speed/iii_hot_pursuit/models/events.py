from games.need_for_speed.iii_hot_pursuit.models.records import EventRecordNFS3
from general import database


# Represents a type of race in NFS3 (e.g. standard road race, extended knockout, endurance tournament road race...)
class EventNFS3(database.Model):

    __tablename__ = "events_nfs3"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False)
    color_hex = database.Column(database.Unicode, nullable=True)

    # Game-specific
    no_of_participants = database.Column(database.Integer, index=True, nullable=False)
    no_of_laps = database.Column(database.Integer, index=True, nullable=False)
    is_ranked = database.Column(database.Boolean, default=True, index=True, nullable=False)

    # Relationships
    records = database.relationship('EventRecordNFS3', backref='event', lazy='dynamic')

    def get_event_records(self):
        return EventRecordNFS3.query.filter(EventRecordNFS3.event_id == self.id,
                                            EventRecordNFS3.is_deleted == False)\
            .order_by(EventRecordNFS3.datetime_added.desc()).all()

    def get_is_ranked(self):
        return "✓" if self.is_ranked == True else "x"
