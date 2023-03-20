from general import database


# Represents a type of race in NFS3 (e.g. standard road race, extended knockout, endurance tournament road race...)
class EventNFS3(database.Model):

    __tablename__ = "events_nfs3"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False)
    no_of_participants = database.Column(database.Integer, index=True, nullable=False)
    no_of_laps = database.Column(database.Integer, index=True, nullable=False)
    is_ranked = database.Column(database.Integer, default=True, index=True, nullable=False)

    # Series
    series_id = database.Column(database.Integer, database.ForeignKey('series_nfs3.id'), nullable=True)
    order_in_series = database.Column(database.Integer, nullable=True)

    # Relationships
    records = database.relationship('EventRecordNFS3', backref='event', lazy='dynamic')


# Represents a series of races that belong together (e.g. tournament, knockout...)
class SeriesNFS3(database.Model):

    __tablename__ = "series_nfs3"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False, unique=True)

    # Relationships
    events = database.relationship('EventNFS3', backref='series', lazy='dynamic')
