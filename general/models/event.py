from sqlalchemy import JSON

from general import database


# Represents a specific event in a game (e.g. standard road race, extended knockout, long haul...)
class Event(database.Model):

    __tablename__ = "events"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    game_id = database.Column(database.Integer, database.ForeignKey('games.id'), nullable=False)
    name = database.Column(database.Unicode, index=True, nullable=False)
    color_hex = database.Column(database.Unicode, nullable=True)

    event_type_id = database.Column(database.Integer, database.ForeignKey('event_types.id'), nullable=False, index=True)


# Represents a type of event that binds rules to itself, so that rules don't need to be re-defined for every single
# event in every game.
class EventType(database.Model):

    __tablename__ = "event_types"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False)
    color_hex = database.Column(database.Unicode, nullable=True)

    # Relationships
    rules = database.relationship('Rule', backref='event_type', lazy='dynamic')
    events = database.relationship('Event', backref='event_type', lazy='dynamic')


# Represents a rule for the determination of event result
class Rule(database.Model):

    __tablename__ = "rules"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)
    event_type_id = database.Column(database.Integer, database.ForeignKey('event_types.id'), index=True)

    # General
    order = database.Column(database.Integer, index=True, nullable=False)

    # Logic
    logical_elements = database.Column(JSON, nullable=False)

    # Represents a result that will be applied to an event record if the rule(s) is deemed true.
    result = database.Column(database.Unicode, index=True, nullable=False)
