from general import database
from general.models.instance import RacingInstance


class InstanceNFS4(RacingInstance):

    __tablename__ = "instances_nfs4"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('instances_racing.id'), primary_key=True)

    # Game-specific
    # Stats
    nfs4_class_id = database.Column(database.Integer, database.ForeignKey('classes_nfs4.id'))
    is_pursuit_vehicle = database.Column(database.Boolean, index=True, default=False, nullable=False)
    is_unlocked_in_career = database.Column(database.Boolean, index=True, default=False, nullable=False)
    is_unlocked_in_arcade = database.Column(database.Boolean, index=True, default=False, nullable=False)

    acceleration = database.Column(database.Integer, index=True, nullable=True)
    top_speed = database.Column(database.Integer, index=True, nullable=True)
    handling = database.Column(database.Integer, index=True, nullable=True)
    braking = database.Column(database.Integer, index=True, nullable=True)
    overall = database.Column(database.Integer, index=True, nullable=True)

    upgrade_level = database.Column(database.Integer, default=0, nullable=True)

    buying_price = database.Column(database.Integer, nullable=True)

    # Statistics
    no_of_lap_records = database.Column(database.Integer, default=0, index=True, nullable=False)
    no_of_track_records = database.Column(database.Integer, default=0, index=True, nullable=False)
    no_of_ranked_events = database.Column(database.Integer, default=0, index=True, nullable=False)

    # Relationships
    tune = database.relationship('TuneNFS4', backref='instance', lazy='dynamic')
    event_records = database.relationship('EventRecordNFS4', backref='instance', lazy='dynamic')

    def get_class(self):
        return self.car_class.name if self.nfs4_class_id is not None else "n/a"


# Represents the groups of cars divided by performance
class ClassNFS4(database.Model):

    __tablename__ = "classes_nfs4"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False, unique=True)
    color_hex = database.Column(database.Unicode, nullable=True)

    # Relationships
    instances = database.relationship('InstanceNFS4', backref='car_class', lazy='dynamic')

    def get_color(self):
        return self.color_hex if self.color_hex != "" else "n/a"

    def get_instances(self):
        return InstanceNFS4.query.filter(InstanceNFS4.nfs4_class_id == self.id,
                                         InstanceNFS4.is_deleted == False)\
            .order_by(InstanceNFS4.id.desc()).all()


# Represents the current tuning of the car
class TuneNFS4(database.Model):

    __tablename__ = "tunes_nfs4"

    # General
    instance_id = database.Column(database.Integer, database.ForeignKey('instances_nfs4.id'), primary_key=True, nullable=False)

    # Stats
    engine = database.Column(database.Integer, default=0, nullable=False)
    brake_balance = database.Column(database.Integer, default=0, nullable=False)
    steering_speed = database.Column(database.Integer, default=0, nullable=False)
    gearbox_ratio = database.Column(database.Integer, default=0, nullable=False)
    aerodynamics = database.Column(database.Integer, default=0, nullable=False)
    suspension = database.Column(database.Integer, default=0, nullable=False)
    tyres = database.Column(database.Integer, default=0, nullable=False)
