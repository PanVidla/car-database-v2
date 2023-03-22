from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional

from general.models.misc import Company, Country


class CompanyForm(FlaskForm):

    # General
    name_full = StringField("Full name", validators=[DataRequired()])
    name_display = StringField("Display name", validators=[DataRequired()])
    name_short = StringField("Short name", validators=[Optional()])
    description = StringField("Description", validators=[Optional()])
    is_game_developer = BooleanField("Developer")
    is_car_manufacturer = BooleanField("Car manufacturer")
    is_car_part_manufacturer = BooleanField("Part manufacturer")

    # Relationships
    owner_id = SelectField("Owned by", coerce=int)
    country_id = SelectField("Country", coerce=int)

    # Dates
    date_established = DateField("Established", validators=[Optional()], format='%d-%m-%Y')
    date_ceased_to_exist = DateField("Ceased to exist", validators=[Optional()], format='%d-%m-%Y')

    # Initialization
    def __init__(self, *args, **kwargs):

        super(CompanyForm, self).__init__(*args, **kwargs)

        self.owner_id.choices = [(-1, "None")]
        self.owner_id.choices += [(company.id, "{}".format(company.name_display))
                                  for company
                                  in Company.query.order_by(Company.name_display.asc()).all()]

        self.country_id.choices = [(-1, "None")]
        self.country_id.choices += [(country.id, "{}".format(country.name_display))
                                    for country
                                    in Country.query.order_by(Country.name_display.asc()).all()]


class CompanyAddForm(CompanyForm):

    submit = SubmitField("Add company")


class CompanyEditForm(CompanyForm):

    submit = SubmitField("Edit company")
