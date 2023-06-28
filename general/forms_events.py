from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional, Length, NumberRange


class EventTypeForm(FlaskForm):

    # General
    name = StringField("Name", validators=[DataRequired()])
    color_hex = StringField("Color", validators=[Optional(), Length(min=7, max=7)])
    order_in_list = IntegerField("Order", validators=[Optional(), NumberRange(min=1)])

    submit = SubmitField("Set event type data")


# Form intended for adding rules in a modal in the event type detail view
class RuleForm(FlaskForm):

    # Conditions
    operand_1 = SelectField("If", coerce=int)
    operator = SelectField("", coerce=int)
    operand_2 = StringField("", validators=[DataRequired()])

    # Initialization
    def __init__(self, *args, **kwargs):
        super(RuleForm, self).__init__(*args, **kwargs)

        self.operand_1.choices = [(0, "position"),
                                  (1, "time"),
                                  (2, "car type")]

        self.operator.choices = [(0, "equals"),
                                 (1, ">="),
                                 (2, ">"),
                                 (3, "<"),
                                 (4, "<="),
                                 (5, "between (including)"),
                                 (6, "between (excluding")]


class RuleAddForm(RuleForm):

    # General
    order = IntegerField("Order", validators=[Optional(), NumberRange(min=1)])

    # Result
    result = StringField("Result", validators=[DataRequired()])
    color_hex = StringField("Color", validators=[Optional(), Length(min=7, max=7)])

    submit_add_rule = SubmitField("Add")


# Form intended for adding of additional conditions to a rule
class RuleConditionAddForm(RuleForm):

    # Logical connector
    connector = SelectField("", coerce=int)

    submit_add_condition = SubmitField("Add condition")

    # Initialization
    def __init__(self, *args, **kwargs):
        super(RuleConditionAddForm, self).__init__(*args, **kwargs)

        # For now, only the "and" operator is allowed to decrease the complexity
        self.connector.choices = [(0, "and")]
        # self.connector.choices = [(0, "and"),
        #                           (1, "or")]
