from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired


# Text
class TextForm(FlaskForm):

    # General
    content = TextAreaField("Content", validators=[DataRequired()])
    text_type = SelectField("Text type", coerce=int)
    submit_add_text = SubmitField("Add text")

    # Initialization
    def __init__(self, *args, **kwargs):
        super(TextForm, self).__init__(*args, **kwargs)

        self.text_type.choices = [(0, "Normal text"),
                                  (1, "Heading 1"),
                                  (2, "Heading 2"),
                                  (3, "Heading 3")]
