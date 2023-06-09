from games.need_for_speed.iii_hot_pursuit.models.records import EventRecordNFS3
from general import database
from general.models.instance import RacingInstance


class InstanceNFS3(RacingInstance):

    __tablename__ = "instances_nfs3"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('instances_racing.id'), primary_key=True)

    # Game-specific
    # Stats
    nfs3_class_id = database.Column(database.Integer, database.ForeignKey('classes_nfs3.id'))

    acceleration = database.Column(database.Integer, index=True, nullable=False)
    top_speed = database.Column(database.Integer, index=True, nullable=False)
    handling = database.Column(database.Integer, index=True, nullable=False)
    braking = database.Column(database.Integer, index=True, nullable=False)
    average = database.Column(database.Double, index=True, nullable=False)

    # Statistics
    no_of_lap_records = database.Column(database.Integer, default=0, index=True, nullable=False)
    no_of_track_records = database.Column(database.Integer, default=0, index=True, nullable=False)
    no_of_ranked_events = database.Column(database.Integer, default=0, index=True, nullable=False)

    # Relationships
    tune = database.relationship('TuneNFS3', backref='instance', lazy='dynamic')
    event_records = database.relationship('EventRecordNFS3', backref='instance', lazy='dynamic')

    def get_average_position(self):
        return self.average_position if self.average_position is not None else "n/a"

    def get_class(self):
        return self.car_class.name if self.nfs3_class_id is not None else "n/a"

    def get_event_records(self):

        event_records = EventRecordNFS3.query.filter(EventRecordNFS3.instance_id == self.id,
                                                     EventRecordNFS3.is_deleted == False)\
            .order_by(EventRecordNFS3.no_of_event_record.desc()).all()

        return event_records

    def get_event_records_ranked(self):

        event_records = EventRecordNFS3.query.filter(EventRecordNFS3.instance_id == self.id,
                                                     EventRecordNFS3.event.is_ranked == True,
                                                     EventRecordNFS3.is_deleted == False)\
            .order_by(EventRecordNFS3.no_of_event_record.desc()).all()

        return event_records

    def get_tune(self):
        return TuneNFS3.query.filter(TuneNFS3.instance_id == self.id).first()

    def set_average(self):
        self.average = (self.acceleration + self.top_speed + self.handling + self.braking) / 4


# Represents the groups of cars divided by performance
class ClassNFS3(database.Model):

    __tablename__ = "classes_nfs3"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False, unique=True)
    color_hex = database.Column(database.Unicode, nullable=True)

    # Relationships
    instances = database.relationship('InstanceNFS3', backref='car_class', lazy='dynamic')

    def get_instances(self):
        return InstanceNFS3.query.filter(InstanceNFS3.nfs3_class_id == self.id,
                                         InstanceNFS3.is_deleted == False)\
            .order_by(InstanceNFS3.id.desc()).all()


# Represents the current tuning of the car
class TuneNFS3(database.Model):

    __tablename__ = "tunes_nfs3"

    # General
    instance_id = database.Column(database.Integer, database.ForeignKey('instances_nfs3.id'), primary_key=True, nullable=False)

    # Stats
    engine = database.Column(database.Integer, default=0, nullable=False)
    brake_balance = database.Column(database.Integer, default=0, nullable=False)
    steering_speed = database.Column(database.Integer, default=0, nullable=False)
    gearbox_ratio = database.Column(database.Integer, default=0, nullable=False)
    aerodynamics = database.Column(database.Integer, default=0, nullable=False)
    suspension = database.Column(database.Integer, default=0, nullable=False)
    tyres = database.Column(database.Integer, default=0, nullable=False)
