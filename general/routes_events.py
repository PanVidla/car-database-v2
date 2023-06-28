from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from sqlalchemy.orm.attributes import flag_modified

from general import cardb, database
from general.forms_events import EventTypeForm, RuleAddForm, RuleConditionAddForm, RuleEditForm
from general.models.event import EventType, Event, create_event_type_from_form, create_rule_from_form, Rule


# Events overview
@cardb.route("/events", methods=['GET'])
@cardb.route("/events/all", methods=['GET'])
def overview_events():

    events = Event.query.order_by(Event.game_id.desc(), Event.event_type_id.asc(), Event.name.asc()).all()

    return render_template("events_overview.html",
                           title="Events",
                           heading="All events",
                           events=events,
                           viewing="events")


# Event types overview
@cardb.route("/events/types", methods=['GET'])
@cardb.route("/events/types/all", methods=['GET'])
def overview_event_types():

    event_types = EventType.query.order_by(EventType.order_in_list.asc(), EventType.name.asc()).all()

    return render_template("events_overview_types.html",
                           title="Event types",
                           heading="All event types",
                           event_types=event_types,
                           viewing="event_types")


# Add game (general information)
@cardb.route("/events/types/add-event-type", methods=['GET', 'POST'])
@login_required
def add_event_type():

    form = EventTypeForm()

    if form.validate_on_submit():

        attempt_at_creating_new_event_type = create_event_type_from_form(form)
        result = attempt_at_creating_new_event_type[0]
        event_type = attempt_at_creating_new_event_type[1]

        if result == 1:
            flash("An event type with the same name ({}, {}) already exists.".format(event_type.id,
                                                                                     event_type.name),
                  "warning")
            return redirect(url_for("add_event_type"))

        if result == 2:
            flash("An event type with the same order in list ({}, {}) already exists.".format(event_type.id,
                                                                                              event_type.name),
                  "warning")
            return redirect(url_for("add_event_type"))

        if result == 0:
            flash("Creating a new event type named {} ({}, {}).".format(event_type.name,
                                                                        event_type.color_hex,
                                                                        event_type.order_in_list),
                  "info")

        else:
            flash("There was an unknown error when creating a new event type from form.", "danger")
            return redirect(url_for("add_event_type"))

        try:
            database.session.add(event_type)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding the new event type to the database.", "danger")
            return redirect(url_for("add_event_type"))

        flash("The new event type \"{}\" ({}, {}) has been successfully added to the database.".format(event_type.name,
                                                                                                       event_type.color_hex,
                                                                                                       event_type.order_in_list),
              "success")
        return redirect(url_for("detail_event_type", id=event_type.id))

    return render_template("events_form_event_type.html",
                           title="Add event type",
                           heading="Add event type",
                           form=form,
                           viewing="event_types")


# Add rule condition
@cardb.route("/events/types/rules/<id>/add-condition", methods=['GET', 'POST'])
@login_required
def add_rule_condition(id):

    rule = Rule.query.get(id)
    form = RuleConditionAddForm()

    if form.validate_on_submit():

        attempt_at_creating_additional_condition = rule.add_additional_condition_from_form(form)
        result = attempt_at_creating_additional_condition

        if result == 2:
            flash("If the rule is set to \"car type\", then only the \"equals\" operator is allowed.",
                  "warning")
            return redirect(url_for("add_rule_condition", id=rule.id))

        if result == 0:
            flash("Adding a new condition to the rule.", "info")

            flag_modified(rule, "logical_elements")
            database.session.add(rule)

        else:
            flash("There was an unknown error when adding a new condition to the rule from form.", "danger")
            return redirect(url_for("add_rule_condition", id=rule.id))

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding the new condition for the rule to the database.", "danger")
            return redirect(url_for("add_rule_condition", id=rule.id))

        flash("The new condition has been successfully added to the rule in the database.", "success")
        return redirect(url_for("detail_event_type", id=rule.event_type_id))

    return render_template("events_form_rule_add_condition.html",
                           title="Add condition",
                           heading="Add condition to the rule",
                           form=form,
                           viewing="event_types")


# Edit event type
@cardb.route("/events/types/edit-event-type/<id>", methods=['GET', 'POST'])
@login_required
def edit_event_type(id):

    event_type = EventType.query.get(id)
    form = EventTypeForm(obj=event_type)

    if form.validate_on_submit():

        editing_result = event_type.edit_event_type_from_form(form)

        if editing_result == 1:
            flash("An event type with the same name ({}, {}) already exists.".format(event_type.id,
                                                                                     event_type.name),
                  "warning")
            return redirect(url_for("edit_event_type", id=event_type.id))

        if editing_result == 2:
            flash("An event type with the same order in list ({}, {}) already exists.".format(event_type.id,
                                                                                              event_type.name),
                  "warning")
            return redirect(url_for("edit_event_type", id=event_type.id))

        if editing_result == 0:
            flash("Editing the event \"{}\" ({}, {}).".format(event_type.name,
                                                              event_type.color_hex,
                                                              event_type.order_in_list),
                  "info")

        else:
            flash("There was an unknown error when editing the event type from form.", "danger")
            return redirect(url_for("edit_event_type", id=event_type.id))

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem saving the changes made to the event type into the database.", "danger")
            return redirect(url_for("edit_event_type", id=event_type.id))

        flash("The new event type \"{}\" ({}, {}) has been successfully edited.".format(event_type.name,
                                                                                        event_type.color_hex,
                                                                                        event_type.order_in_list),
              "success")
        return redirect(url_for("detail_event_type", id=event_type.id))

    return render_template("events_form_event_type.html",
                           title="{}".format(event_type.name),
                           heading="{}".format(event_type.name),
                           form=form,
                           viewing="event_types",
                           editing=True)


# Edit rule condition
@cardb.route("/events/types/rules/edit-rule/<id>", methods=['GET', 'POST'])
@login_required
def edit_rule(id):

    rule = Rule.query.get(id)
    form = RuleEditForm(obj=rule)

    if form.validate_on_submit():

        attempt_at_editing_form = rule.edit_rule_from_form(form)
        result = attempt_at_editing_form

        if result == 1:
            flash("A rule with the same order already exists.".format(rule.id), "warning")
            return redirect(url_for("edit_rule", id=rule.id))

        if result == 0:
            flash("Editing rule.", "info")

        else:
            flash("There was an unknown error when editing the rule.", "danger")
            return redirect(url_for("edit_rule", id=rule.id))

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem saving changes to the rule in the database.", "danger")
            return redirect(url_for("edit_rule", id=rule.id))

        flash("The changes to the rule have been successfully saved to the database.", "success")
        return redirect(url_for("detail_event_type", id=rule.event_type_id))

    return render_template("events_form_rule_edit.html",
                           title="Edit rule",
                           heading="Edit rule",
                           form=form,
                           viewing="event_types")


# Delete event type
@cardb.route("/events/types/delete-event-type/<id>", methods=['GET', 'POST'])
@login_required
def delete_event_type(id):

    event_type = EventType.query.get(id)

    try:
        database.session.delete(event_type)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the event type \"{}\" ({}, {}) from the database.".format(event_type.name,
                                                                                                           event_type.color_hex,
                                                                                                           event_type.order_in_list),
              "danger")
        return redirect(url_for("detail_event_type", id=event_type.id))

    flash("The event type \"{}\" ({}, {}) has been successfully deleted from the database.".format(event_type.name,
                                                                                                   event_type.color_hex,
                                                                                                   event_type.order_in_list
                                                                                                   ),
          "success")
    return redirect(url_for("overview_event_types"))


# Delete rule
@cardb.route("/events/types/rules/delete-rule/<id>", methods=['GET', 'POST'])
@login_required
def delete_rule(id):

    rule = Rule.query.get(id)

    try:
        database.session.delete(rule)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the rule from the database.", "danger")
        return redirect(url_for("detail_event_type", id=rule.event_type_id))

    flash("The rule has been successfully deleted from the database.", "success")
    return redirect(url_for("detail_event_type", id=rule.event_type_id))


# Event type detail
@cardb.route("/events/types/detail/<id>", methods=['GET', 'POST'])
@login_required
def detail_event_type(id):

    event_type = EventType.query.get(id)

    form_add_rule = RuleAddForm()

    if form_add_rule.submit_add_rule.data and form_add_rule.validate():

        attempt_at_creating_new_rule = create_rule_from_form(form_add_rule, event_type.id)
        result = attempt_at_creating_new_rule[0]
        rule = attempt_at_creating_new_rule[1]

        if result == 1:
            flash("A rule with the same order ({}) already exists.".format(rule.id),
                  "warning")
            return redirect(url_for("detail_event_type", id=event_type.id))

        if result == 2:
            flash("If the rule is set to \"car type\", then only the \"equals\" operator is allowed.",
                  "warning")
            return redirect(url_for("detail_event_type", id=event_type.id))

        if result == 0:
            flash("Creating a rule.", "info")

        else:
            flash("There was an unknown error when creating a new rule from form.", "danger")
            return redirect(url_for("detail_event_type", id=event_type.id))

        try:
            database.session.add(rule)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding the new rule to the database.", "danger")
            return redirect(url_for("detail_event_type", id=event_type.id))

        flash("The new rule has been successfully added to the database.", "success")
        return redirect(url_for("detail_event_type", id=event_type.id))

    return render_template("events_detail_event_type.html",
                           title="{}".format(event_type.name),
                           heading="{}".format(event_type.name),
                           event_type=event_type,
                           form_add_rule=form_add_rule,
                           viewing="event_types")
