from flask import render_template, flash, redirect, url_for

from general import cardb, database
from general.forms_companies import CompanyAddForm, CompanyEditForm
from general.models.misc import Company, create_company_from_form
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

    companies = Company.query.filter(Company.is_game_developer == True).order_by(Company.name_display.asc()).all()

    return render_template("companies_overview.html",
                           title=title_companies_developers,
                           heading=overview_heading_companies_developers,
                           companies=companies)


@cardb.route("/companies/car-manufacturers", methods=['GET'])
def overview_companies_car_manufacturers():

    companies = Company.query.filter(Company.is_car_manufacturer == True).order_by(Company.name_display.asc()).all()

    return render_template("companies_overview.html",
                           title=title_companies_car_manufacturers,
                           heading=overview_heading_companies_car_manufacturers,
                           companies=companies)


@cardb.route("/companies/part-manufacturers", methods=['GET'])
def overview_companies_car_part_manufacturers():

    companies = Company.query.filter(Company.is_car_part_manufacturer == True).order_by(Company.name_display.asc()).all()

    return render_template("companies_overview.html",
                           title=title_companies_car_part_manufacturers,
                           heading=overview_heading_companies_car_part_manufacturers,
                           companies=companies)


# Add company
@cardb.route("/companies/add-company", methods=['GET', 'POST'])
def add_company():

    form = CompanyAddForm()

    if form.validate_on_submit():

        new_company = create_company_from_form(form)

        try:
            database.session.add(new_company)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding a new company to the database.", "danger")
            return redirect(url_for("add_company"))

        flash("{} ({}, {}) has been successfully added to the database.".format(new_company.name_display,
                                                                                new_company.name_full,
                                                                                new_company.get_name_short()),
              "success")
        return redirect(url_for("overview_companies"))

    return render_template("companies_form.html",
                           title="Add company",
                           heading="Add company",
                           form=form)


# Edit company
@cardb.route("/companies/edit-company/<id>", methods=['GET', 'POST'])
def edit_company(id):

    company = Company.query.get(id)
    form = CompanyEditForm(obj=company)

    if form.validate_on_submit():

        company.edit_company_from_form(form)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing {}.".format(company.name_display), "danger")
            return redirect(url_for("edit_company", id=company.id))

        flash("{} ({}, {}) has been successfully edited.".format(company.name_display,
                                                                 company.name_full,
                                                                 company.get_name_short()), "success")
        return redirect(url_for("detail_company", id=company.id))

    return render_template("companies_form.html",
                           title="Edit company",
                           heading="Edit company",
                           form=form)


# Delete company
@cardb.route("/misc/companies/delete-company/<id>", methods=['GET', 'POST'])
def delete_company(id):

    company = Company.query.get(id)

    try:
        database.session.delete(company)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting {}.".format(company.name_display), "danger")
        return redirect(url_for("detail_company", id=company.id))

    flash("{} ({}, {}) has been successfully deleted.".format(company.name_display,
                                                              company.name_full,
                                                              company.get_name_short()), "success")
    return redirect(url_for("overview_companies"))


# Company detail
@cardb.route("/companies/detail/<id>", methods=['GET', 'POST'])
def detail_company(id):

    company = Company.query.get(id)

    return render_template("companies_detail.html",
                           title="{}".format(company.name_display),
                           heading="{}".format(company.name_full),
                           company=company)
