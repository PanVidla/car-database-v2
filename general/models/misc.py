from datetime import datetime

from general import database
from general.models.info import Text, Image


# Represents any company (e.g. BMW, Electronic Arts, Playground Studios...)
class Company(database.Model):

    __tablename__ = "companies"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    # Full name, e.g. Volkswagen AG
    name_full = database.Column(database.Unicode, nullable=False)
    # Display name, e.g. Volkswagen
    name_display = database.Column(database.Unicode, index=True, nullable=False)
    # Short name, e.g. VW
    name_short = database.Column(database.Unicode, nullable=True)
    description = database.Column(database.Unicode, nullable=True)

    is_game_developer = database.Column(database.Boolean, default=False, index=True, nullable=False)
    is_game_publisher = database.Column(database.Boolean, default=False, index=True, nullable=False)
    is_car_manufacturer = database.Column(database.Boolean, default=False, index=True, nullable=False)
    is_car_part_manufacturer = database.Column(database.Boolean, default=False, index=True, nullable=False)

    owner_id = database.Column(database.Integer, database.ForeignKey("companies.id"), index=True, nullable=True)
    country_id = database.Column(database.Integer, database.ForeignKey("countries.id"), index=True, nullable=True)
    date_established = database.Column(database.Date, index=True, nullable=True)
    date_ceased_to_exist = database.Column(database.Date, nullable=True)

    # Statistics
    no_of_games_developed = database.Column(database.Integer, default=0, nullable=True)
    no_of_cars_produced = database.Column(database.Integer, default=0, nullable=True)
    no_of_parts_produced = database.Column(database.Integer, default=0, nullable=True)

    # Relationships
    cars = database.relationship('Car', secondary="car_manufacturer")
    engines = database.relationship('Engine', backref='manufacturer', lazy='dynamic')
    forced_induction = database.relationship('ForcedInduction', backref='manufacturer', lazy='dynamic')
    games = database.relationship('Game', backref='developer', lazy='dynamic')
    owner = database.relationship('Company', remote_side=[id], backref='owned_companies')
    transmissions = database.relationship('Transmission',  backref='manufacturer', lazy='dynamic')
    texts = database.relationship('CompanyText', backref='company', lazy='dynamic')
    images = database.relationship('CompanyImage', backref='company', lazy='dynamic')


# Represents a car competition (e.g. F1, GT3, NASCAR, WRC...)
class Competition(database.Model):

    __tablename__ = "competitions"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name_full = database.Column(database.Unicode, index=True, nullable=False)
    name_display = database.Column(database.Unicode, index=True, nullable=False)
    name_short = database.Column(database.Unicode, index=True, nullable=False)
    date_started = database.Column(database.Date, nullable=True)
    date_ended = database.Column(database.Date, nullable=True)
    is_virtual = database.Column(database.Boolean, default=False, index=True, nullable=False)

    # Relationships
    cars = database.relationship('Car', secondary="car_competition")
    texts = database.relationship('CompetitionText', backref='competition', lazy='dynamic')
    images = database.relationship('CompetitionImage', backref='competition', lazy='dynamic')


# Represents a country (e.g. Italy, Germany, United States of America...)
class Country(database.Model):

    __tablename__ = "countries"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    # Full name, e.g. Federal Republic of Germany
    name_full = database.Column(database.Unicode, nullable=False)
    # Display name, e.g. Germany
    name_display = database.Column(database.Unicode, index=True, nullable=False)
    # Short name, e.g. GER
    name_short = database.Column(database.Unicode, nullable=False)

    # Statistics
    no_of_companies_game = database.Column(database.Integer, default=0, nullable=True)
    no_of_companies_car = database.Column(database.Integer, default=0, nullable=True)
    no_of_games = database.Column(database.Integer, default=0, nullable=True)
    no_of_cars = database.Column(database.Integer, default=0, nullable=True)

    # Relationships
    companies = database.relationship('Company', backref='country', lazy='dynamic')
    cars = database.relationship('Car', backref='country', lazy='dynamic')
    texts = database.relationship('CountryText', backref='country', lazy='dynamic')
    images = database.relationship('CountryImage', backref='country', lazy='dynamic')
    locations = database.relationship('Location', backref='country', lazy='dynamic')

    def get_name_short(self):

        if self.name_short == "":
            return "n/a"

        else:
            return self.name_short


class Location(database.Model):

    __tablename__ = "locations"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    name = database.Column(database.Unicode, index=True, nullable=False)
    country_id = database.Column(database.Integer, database.ForeignKey('countries.id'))
    is_fictional = database.Column(database.Boolean, default=True, index=True, nullable=False)

    # Relationships
    texts = database.relationship('LocationText', backref='location', lazy='dynamic')
    images = database.relationship('LocationImage', backref='location', lazy='dynamic')


# Info
class CompanyText(Text):

    __tablename__ = "texts_companies"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('texts.id'), primary_key=True)

    # General
    company_id = database.Column(database.Integer, database.ForeignKey('companies.id'), primary_key=True)


class CompanyImage(Image):

    __tablename__ = "images_companies"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('images.id'), primary_key=True)

    # General
    company_id = database.Column(database.Integer, database.ForeignKey('companies.id'), primary_key=True)


class CompetitionText(Text):

    __tablename__ = "texts_competitions"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('texts.id'), primary_key=True)

    # General
    competition_id = database.Column(database.Integer, database.ForeignKey('competitions.id'), primary_key=True)


class CompetitionImage(Image):

    __tablename__ = "images_competitions"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('images.id'), primary_key=True)

    # General
    competition_id = database.Column(database.Integer, database.ForeignKey('competitions.id'), primary_key=True)


class CountryText(Text):

    __tablename__ = "texts_countries"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('texts.id'), primary_key=True)

    # General
    country_id = database.Column(database.Integer, database.ForeignKey('countries.id'), primary_key=True)


class CountryImage(Image):

    __tablename__ = "images_countries"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('images.id'), primary_key=True)

    # General
    country_id = database.Column(database.Integer, database.ForeignKey('countries.id'), primary_key=True)


class LocationText(Text):

    __tablename__ = "texts_locations"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('texts.id'), primary_key=True)

    # General
    location_id = database.Column(database.Integer, database.ForeignKey('locations.id'), primary_key=True)


class LocationImage(Image):

    __tablename__ = "images_locations"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('images.id'), primary_key=True)

    # General
    is_plan = database.Column(database.Boolean, default=False, index=True, nullable=False)
    location_id = database.Column(database.Integer, database.ForeignKey('locations.id'), primary_key=True)
