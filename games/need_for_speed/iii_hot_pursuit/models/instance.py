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
        return "{:.2f}".format(self.average_position) if self.average_position is not None else "n/a"

    def get_class(self):
        return self.car_class.name if self.nfs3_class_id is not None else "n/a"

    def get_event_records(self):

        event_records = EventRecordNFS3.query.filter(EventRecordNFS3.instance_id == self.id,
                                                     EventRecordNFS3.is_deleted == False)\
            .order_by(EventRecordNFS3.no_of_event_record.desc()).all()

        return event_records

    def get_event_records_ranked(self):

        ranked_event_records = []

        event_records = EventRecordNFS3.query.filter(EventRecordNFS3.instance_id == self.id,
                                                     EventRecordNFS3.is_deleted == False)\
            .order_by(EventRecordNFS3.no_of_event_record.desc()).all()

        for event_record in event_records:
            if event_record.event.is_ranked is True:
                ranked_event_records.append(event_record)

        return ranked_event_records

    def get_tune(self):
        return TuneNFS3.query.filter(TuneNFS3.instance_id == self.id).first()

    def set_average(self):
        self.average = (self.acceleration + self.top_speed + self.handling + self.braking) / 4

    def set_no_events_total(self):
        self.no_of_events_total = len(self.get_event_records())

    def set_no_events_ranked(self):
        self.no_of_ranked_events = len(self.get_event_records_ranked())

    def set_no_of_events_won(self):

        ranked_event_records = self.get_event_records_ranked()
        no_of_wins = 0

        for event_record in ranked_event_records:
            if event_record.result == "win":
                no_of_wins += 1

        self.no_of_events_won = no_of_wins

    def set_no_of_events_won_percentage(self):
        if self.no_of_ranked_events != 0:
            self.no_of_events_won_percent = self.no_of_events_won / self.no_of_ranked_events
        else:
            self.no_of_events_won_percent = 0

    def set_no_of_events_podium(self):

        ranked_event_records = self.get_event_records_ranked()
        no_of_podiums = 0

        for event_record in ranked_event_records:
            if event_record.result == "podium":
                no_of_podiums += 1

        self.no_of_events_podium = no_of_podiums

    def set_no_of_events_podium_percentage(self):
        if self.no_of_ranked_events != 0:
            self.no_of_events_podium_percent = self.no_of_events_podium / self.no_of_ranked_events
        else:
            self.no_of_events_podium_percent = 0

    def set_no_of_events_lost(self):

        ranked_event_records = self.get_event_records_ranked()
        no_of_losses = 0

        for event_record in ranked_event_records:
            if event_record.result == "loss":
                no_of_losses += 1

        self.no_of_events_lost = no_of_losses

    def set_no_of_events_lost_percentage(self):
        if self.no_of_ranked_events != 0:
            self.no_of_events_lost_percent = self.no_of_events_lost / self.no_of_ranked_events
        else:
            self.no_of_events_lost_percent = 0

    def set_no_of_events_dnf(self):

        ranked_event_records = self.get_event_records_ranked()
        no_of_dnfs = 0

        for event_record in ranked_event_records:
            if event_record.result == "DNF":
                no_of_dnfs += 1

        self.no_of_events_dnf = no_of_dnfs

    def set_no_of_events_dnf_percentage(self):
        if self.no_of_ranked_events != 0:
            self.no_of_events_dnf_percent = self.no_of_events_dnf / self.no_of_ranked_events
        else:
            self.no_of_events_dnf_percent = 0

    def set_no_of_lap_records(self):

        event_records = self.get_event_records()
        no_of_lap_records = 0

        for event_record in event_records:
            if event_record.is_lap_record is True:
                no_of_lap_records +=1

        self.no_of_lap_records = no_of_lap_records

    def set_no_of_track_records(self):

        event_records = self.get_event_records()
        no_of_track_records = 0

        for event_record in event_records:
            if event_record.is_track_record is True:
                no_of_track_records += 1

        self.no_of_track_records = no_of_track_records

    def set_average_position(self):

        ranked_event_records = self.get_event_records_ranked()
        sum_of_positions = 0

        if self.no_of_ranked_events !=0:

            for event_record in ranked_event_records:

                if event_record.result == "DNF":
                    sum_of_positions += event_record.event.no_of_participants + 1

                else:
                    sum_of_positions += event_record.position

            self.average_position = sum_of_positions / self.no_of_ranked_events

        else:
            self.average_position = 0

    def update_statistics(self):

        self.set_no_events_total()
        self.set_no_events_ranked()

        self.set_no_of_events_won()
        self.set_no_of_events_won_percentage()
        self.set_no_of_events_podium()
        self.set_no_of_events_podium_percentage()
        self.set_no_of_events_lost()
        self.set_no_of_events_lost_percentage()
        self.set_no_of_events_dnf()
        self.set_no_of_events_dnf_percentage()
        self.set_average_position()

        self.set_no_of_lap_records()
        self.set_no_of_track_records()


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
