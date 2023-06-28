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

    def get_color_hex(self):
        return self.color_hex if self.color_hex != "" else "n/a"


# Represents a type of event that binds rules to itself, so that rules don't need to be re-defined for every single
# event in every game.
class EventType(database.Model):

    __tablename__ = "event_types"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False, unique=True)
    color_hex = database.Column(database.Unicode, nullable=True)
    order_in_list = database.Column(database.Integer, index=True, nullable=True, unique=True)

    # Relationships
    rules = database.relationship('Rule', backref='event_type', lazy='dynamic')
    events = database.relationship('Event', backref='event_type', lazy='dynamic')

    def edit_event_type_from_form(self, form):

        # Check if an event type of the same name already exists
        event_type_with_the_same_name = EventType.query.filter(EventType.name == form.name.data).first()
        if (event_type_with_the_same_name is not None) and (event_type_with_the_same_name != self):
            result = 1

            return result

        # Check if an event type with the same order in list already exists
        event_type_with_the_same_order_in_list = EventType.query.filter(EventType.order_in_list == form.order_in_list.data).first()
        if (event_type_with_the_same_order_in_list is not None) and (event_type_with_the_same_name != self):
            result = 2

            return result

        # If the data from the form pass all the checks above, change the values in the EventType object and return 0
        result = 0
        form.populate_obj(self)

        return result

    def get_color_hex(self):
        return self.color_hex if self.color_hex != "" else "n/a"

    def get_events(self):

        events = Event.query\
            .filter(Event.event_type_id == self.id)\
            .order_by(Event.game_id.desc(),
                      Event.name.asc())\
            .all()

        return events

    def get_no_of_rules(self):
        return len(Rule.query.filter(Rule.event_type_id == self.id).all())

    def get_order_in_list(self):
        return self.order_in_list if self.order_in_list is not None else "n/a"

    def get_rules(self):

        rules = Rule.query.filter(Rule.event_type_id == self.id).order_by(Rule.order.asc()).all()
        return rules


def create_event_type_from_form(form):

    # Return a list where the first element is an error code and the second element is the event type object
    result = []

    # Check if an event type of the same name already exists
    event_type_with_the_same_name = EventType.query.filter(EventType.name == form.name.data).first()
    if event_type_with_the_same_name is not None:

        result.append(1)
        result.append(event_type_with_the_same_name)

        return result

    # Check if an event type with the same order in list already exists
    event_type_with_the_same_order_in_list = EventType.query.filter(EventType.order_in_list == form.order_in_list.data).first()
    if event_type_with_the_same_order_in_list is not None:

        result.append(2)
        result.append(event_type_with_the_same_order_in_list)

        return result

    # If the data from the form pass all the checks above, create the new EventType object and return it
    new_event_type = EventType()
    form.populate_obj(new_event_type)

    result.append(0)
    result.append(new_event_type)

    return result


# Represents a rule for the determination of event result
class Rule(database.Model):

    __tablename__ = "rules"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)
    event_type_id = database.Column(database.Integer, database.ForeignKey('event_types.id'), index=True)

    # General
    order = database.Column(database.Integer, index=True, nullable=False)
    # This color is applied to the result
    color_hex = database.Column(database.Unicode, nullable=True)

    # Logic
    logical_elements = database.Column(JSON, nullable=False)

    # Represents a result that will be applied to an event record if the rule(s) is deemed true.
    result = database.Column(database.Unicode, index=True, nullable=False)

    def get_color_hex(self):
        return self.color_hex if self.color_hex != "" else "n/a"

    def get_condition_string(self, number_of_condition):

        # Operand 1
        if self.logical_elements[number_of_condition]["operand_1"] == 0:
            operand_1 = "position"
        elif self.logical_elements[number_of_condition]["operand_1"] == 1:
            operand_1 = "time"
        elif self.logical_elements[number_of_condition]["operand_1"] == 2:
            operand_1 = "car type"
        else:
            operand_1 = "n/a"

        # Operator
        if self.logical_elements[number_of_condition]["operator"] == 0:
            operator = "equal to"
        elif self.logical_elements[number_of_condition]["operator"] == 1:
            operator = "equal or greater than"
        elif self.logical_elements[number_of_condition]["operator"] == 2:
            operator = "greater than"
        elif self.logical_elements[number_of_condition]["operator"] == 3:
            operator = "lesser than"
        elif self.logical_elements[number_of_condition]["operator"] == 4:
            operator = "equal or lesser than"
        elif self.logical_elements[number_of_condition]["operator"] == 5:
            operator = "between (including)"
        elif self.logical_elements[number_of_condition]["operator"] == 6:
            operator = "between (excluding)"
        else:
            operator = "n/a"

        # Operand 2
        if (self.logical_elements[number_of_condition]["operator"] == 5) or (self.logical_elements[number_of_condition]["operator"] == 6):
            numbers_without_comma = self.logical_elements[number_of_condition]["operand_2"].split(", ")
            operand_2 = "{} and {}".format(numbers_without_comma[0], numbers_without_comma[1])
        else:
            operand_2 = self.logical_elements[number_of_condition]["operand_2"]

        string = "if {} is {} {}".format(operand_1, operator, operand_2)
        return string


def create_rule_from_form(form, event_type_id):

    # Return a list where the first element is ab error code and the second element is the rule
    result = []

    # Check if a rule with the same order already exists
    rule_with_the_same_order = Rule.query\
        .filter(Rule.event_type_id == event_type_id,
                Rule.order == form.order.data)\
        .first()
    if rule_with_the_same_order is not None:

        result.append(1)
        result.append(rule_with_the_same_order)

        return result

    # Check if the first operand is set to "car type" and the operator to "equals"
    if form.operand_1.data == 2:
        if form.operator.data != 0:

            result.append(2)
            result.append(None)

    # If the data from the form pass the checks above, create the new Rule object and return it
    new_rule = Rule(event_type_id=event_type_id)
    form.populate_obj(new_rule)
    logical_elements_json = {1: {"operand_1": form.operand_1.data,
                                 "operator": form.operator.data,
                                 "operand_2": form.operand_2.data}}
    new_rule.logical_elements = logical_elements_json

    result.append(0)
    result.append(new_rule)

    return result
