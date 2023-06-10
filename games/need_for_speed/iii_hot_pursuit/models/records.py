from datetime import datetime

from flask import flash, redirect, url_for

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
    is_backwards = database.Column(database.Boolean, default=False, nullable=False)
    is_mirrored = database.Column(database.Boolean, default=False, nullable=False)
    is_at_night = database.Column(database.Boolean, default=False, nullable=False)
    is_weather_on = database.Column(database.Boolean, default=False, nullable=False)

    def is_current_lap_record(self):

        current_lap_record_id = self.track.best_lap_time_event_record_id

        if self.id == current_lap_record_id:
            return True

        else:
            return False

    def is_current_track_record(self):

        current_track_record_id = self.track.best_track_time_event_record_id

        if self.id == current_track_record_id:
            return True

        else:
            return False

    def get_datetime_added(self):
        return "{}".format(
            self.datetime_added.strftime("%d.%m.%Y %H:%M:%S")) if self.datetime_added is not None else "n/a"

    def get_datetime_edited(self):
        return "{}".format(
            self.datetime_edited.strftime("%d.%m.%Y %H:%M:%S")) if self.datetime_edited is not None else "n/a"

    def get_is_at_night(self):
        return "✓" if self.is_at_night == True else "x"

    def get_is_backwards(self):
        return "✓" if self.is_backwards == True else "x"

    def get_is_lap_record(self):
        return "✓" if self.is_lap_record else "x"

    def get_is_mirrored(self):
        return "✓" if self.is_mirrored == True else "x"

    def get_is_track_record(self):
        return "✓" if self.is_track_record else "x"

    def get_is_weather_on(self):
        return "✓" if self.is_weather_on == True else "x"

    def get_maximum_speed(self):
        return "{:.1f} km/h".format(self.maximum_speed) if self.maximum_speed is not None else "n/a"

    def get_position(self):
        return self.position if self.position is not None else "n/a"

    def get_result(self):
        return self.result if self.result is not None else "n/a"

    def get_time_best_lap_human_readable(self):
        return self.time_best_lap_human_readable if self.time_best_lap_human_readable != "" else "n/a"

    def get_time_track_human_readable(self):
        return self.time_track_human_readable if self.time_track_human_readable != "" else "n/a"

    def set_calculated_values(self):

        self.set_result()
        self.set_time_best_lap_milliseconds()
        self.set_time_track_milliseconds()
        self.set_is_lap_record()
        self.set_is_track_record()

    def set_is_lap_record(self):

        if self.time_best_lap_milliseconds is None:
            self.is_lap_record = False

        else:

            event_record_track = self.track

            # If there is no best lap time, then this event record is the new lap record
            if event_record_track.best_lap_time_event_record_id is None:

                self.is_lap_record = True
                event_record_track.best_lap_time_event_record_id = self.id

                try:
                    database.session.commit()
                except RuntimeError:
                    flash("There was a problem updating the best lap time event record on {}.".format(event_record_track.name), "danger")
                    return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=self.id))

                flash("The newly added event record is a lap record!", "success")
                return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=self.id))

            # Compare if this event record has a lower time than the current best lap time
            else:
                current_lap_time_event_record = EventRecordNFS3.query.get(event_record_track.best_lap_time_event_record_id)
                current_lap_time_in_milliseconds = current_lap_time_event_record.time_best_lap_milliseconds

                if self.time_best_lap_milliseconds < current_lap_time_in_milliseconds:

                    self.is_lap_record = True

                    event_record_track.best_lap_time_event_record_id = self.id

                    try:
                        database.session.commit()
                    except RuntimeError:
                        flash("There was a problem updating the best lap time event record on {}.".format(
                            event_record_track.name), "danger")
                        return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=self.id))

                    flash("The newly added event record is a lap record!", "success")
                    return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=self.id))

                else:
                    self.is_lap_record = False

    def set_is_track_record(self):

        if self.time_track_milliseconds is None:
            self.is_track_record = False
            return

        else:

            event_record_track = self.track

            # If there is no best track time, then this event record is the new track record
            if event_record_track.best_track_time_event_record_id is None:

                self.is_track_record = True
                event_record_track.best_track_time_event_record_id = self.id

                try:
                    database.session.commit()
                except RuntimeError:
                    flash("There was a problem updating the best track time event record on {}.".format(
                        event_record_track.name), "danger")
                    return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=self.id))

                flash("The newly added event record is a track record!", "success")
                return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=self.id))

            # Compare if this event record has a lower time than the current best track time
            else:
                current_track_time_event_record = EventRecordNFS3.query.get(
                    event_record_track.best_track_time_event_record_id)
                current_track_time_in_milliseconds = current_track_time_event_record.time_track_milliseconds

                if self.time_track_milliseconds < current_track_time_in_milliseconds:

                    self.is_track_record = True

                    event_record_track.best_track_time_event_record_id = self.id

                    try:
                        database.session.commit()
                    except RuntimeError:
                        flash("There was a problem updating the best track time event record on {}.".format(
                            event_record_track.name), "danger")
                        return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=self.id))

                    flash("The newly added event record is a track record!", "success")
                    return redirect(url_for("need_for_speed.iii_hot_pursuit.detail_instance", id=self.id))

                else:
                    self.is_track_record = False

    def set_result(self):

        if \
                (self.event.name == "race (standard)") or \
                (self.event.name == "race (special)") or \
                (self.event.name == "tournament"):

            if self.position is None:
                self.result = "DNF"
                return

            if self.position == 1:
                self.result = "win"
            elif (self.position == 2) or (self.position == 3):
                self.result = "podium"
            elif 4 <= self.position <= 7:
                self.result = "complete"
            elif self.position == 8:
                self.result = "loss"
            else:
                self.result = "DNF"

        if self.event.name == "race (1 v 1)":

            if self.position is None:
                self.result = "DNF"
                return

            if self.position == 1:
                self.result = "win"
            elif self.position == 2:
                self.result = "loss"
            else:
                self.result = "DNF"

        if self.event.name == "hot pursuit":

            if self.position is None:
                self.result = "busted"
                return

            if self.position == 1:
                self.result = "most wanted"
            elif self.position == 2:
                self.result = "complete"
            else:
                self.result = "DNF"

    def set_time_best_lap_milliseconds(self):

        if self.time_best_lap_human_readable == "":
            self.time_best_lap_milliseconds = None

        else:
            self.time_best_lap_milliseconds = parse_human_readable_time_to_milliseconds(self.time_best_lap_human_readable)

    def set_time_track_milliseconds(self):

        if self.time_track_human_readable == "":
            self.time_track_milliseconds = None

        else:
            self.time_track_milliseconds = parse_human_readable_time_to_milliseconds(self.time_track_human_readable)


def parse_human_readable_time_to_milliseconds(human_readable_time):

    string_array_1 = human_readable_time.split(":")
    string_array_2 = string_array_1[1].split(".")

    minutes = int(string_array_1[0])
    seconds = int(string_array_2[0])
    milliseconds = int(string_array_2[1])

    milliseconds_total = milliseconds + seconds * 1000 + minutes * 60000

    return milliseconds_total
