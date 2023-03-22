from flask import render_template

from general import cardb
from general.forms_companies import CompanyAddForm
from general.models.misc import Company
from general.strings import *


# Overviews
@cardb.route("/companies/", methods=['GET'])
@cardb.route("/companies/all", methods=['GET'])
def overview_companies():

    companies = Company.query.order_by(Company.name_display.asc()).all()

    return render_template("companies_overview.html",
                           title=title_companies,
                           heading=overview_heading_companies,
                           companies=companies)


@cardb.route("/companies/developers", methods=['GET'])
def overview_companies_developers():

    companies = Company.query.filter(Company.is_game_developer is True).order_by(Company.name_display.asc()).all()

    return render_template("companies_overview.html",
                           title=title_companies_developers,
                           heading=overview_heading_companies_developers,
                           companies=companies)


@cardb.route("/companies/car-manufacturers", methods=['GET'])
def overview_companies_car_manufacturers():

    companies = Company.query.filter(Company.is_car_manufacturer is True).order_by(Company.name_display.asc()).all()

    return render_template("companies_overview.html",
                           title=title_companies_car_manufacturers,
                           heading=overview_heading_companies_car_manufacturers,
                           companies=companies)


@cardb.route("/companies/part-manufacturers", methods=['GET'])
def overview_companies_car_part_manufacturers():

    companies = Company.query.filter(Company.is_car_part_manufacturer is True).order_by(Company.name_display.asc()).all()

    return render_template("companies_overview.html",
                           title=title_companies_car_part_manufacturers,
                           heading=overview_heading_companies_car_part_manufacturers,
                           companies=companies)


# Add company
@cardb.route("/companies/add-company", methods=['GET', 'POST'])
def add_company():

    form = CompanyAddForm()

    return render_template("companies_form.html",
                           title="Add company",
                           heading="Add company",
                           form=form)
