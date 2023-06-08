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
    is_ranked = database.Column(database.Integer, default=True, index=True, nullable=False)

    # Relationships
    records = database.relationship('EventRecordNFS3', backref='event', lazy='dynamic')
