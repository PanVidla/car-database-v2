from flask import render_template, flash, redirect, url_for
from flask_login import login_required
from sqlalchemy import or_

from general import cardb, database
from general.forms_companies import CompanyAddForm, CompanyEditForm
from general.forms_info import TextForm, ImageForm
from general.models.car import Car
from general.models.misc import Company, create_company_from_form, CompanyText, CompanyImage
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
@login_required
def add_company():

    form = CompanyAddForm()

    if form.validate_on_submit():

        # Check if a company with the same full or display name already exists in the database
        existing_company = Company.query.filter(or_(Company.name_full == form.name_full.data,
                                                    Company.name_display == form.name_display.data)).first()

        if existing_company is not None:
            flash("There is already a company called {} ({}, {}) in the database.".format(existing_company.name_display,
                                                                                          existing_company.name_full,
                                                                                          existing_company.name_short),
                  "warning")
            return redirect(url_for("overview_companies"))

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
@login_required
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
@login_required
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


# Delete company text
@cardb.route("/misc/companies/text/delete-text/<id>", methods=['GET', 'POST'])
@login_required
def delete_company_text(id):

    text = CompanyText.query.get(id)

    try:
        database.session.delete(text)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the text.", "danger")
        return redirect(url_for("detail_company", id=text.company_id))

    flash("The text has been successfully deleted.", "success")
    return redirect(url_for("detail_company", id=text.company_id))


# Delete company image
@cardb.route("/misc/companies/image/delete-image/<id>", methods=['GET', 'POST'])
@login_required
def delete_company_image(id):

    image = CompanyImage.query.get(id)

    try:
        database.session.delete(image)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the image.", "danger")
        return redirect(url_for("detail_company", id=image.company_id))

    flash("The image has been successfully deleted.", "success")

    # Re-align the order of images so that there is an image with order no. 1
    company = Company.query.get(image.company_id)
    remaining_images = company.get_images()

    counter = 1

    try:
        for image in remaining_images:

            image.order = counter
            counter += 1

            database.session.commit()

    except RuntimeError:
        flash("There was a problem with resetting the order of the remaining images.", "danger")
        return redirect(url_for("detail_company", id=image.company_id))

    flash("The remaining images had their order successfully reset.", "success")
    return redirect(url_for("detail_company", id=image.company_id))


# Company detail
@cardb.route("/companies/detail/<id>", methods=['GET', 'POST'])
@login_required
def detail_company(id):

    company = Company.query.get(id)
    cars = Car.query \
        .filter(Car.is_deleted != True) \
        .filter(Car.manufacturers.any(id=company.id)) \
        .order_by(Car.manufacturers_display.asc(), Car.year.asc(), Car.model.asc()) \
        .all()
    texts = CompanyText.query \
        .filter(CompanyText.company_id == company.id) \
        .order_by(CompanyText.order.asc()) \
        .all()
    add_text_form = TextForm()
    add_image_form = ImageForm()

    # Add text
    if add_text_form.submit_add_text.data and add_text_form.validate():

        whole_text = add_text_form.content.data

        for paragraph in whole_text.splitlines():

            if paragraph == "":
                continue

            else:

                new_text = CompanyText()
                new_text.content = paragraph
                new_text.text_type = add_text_form.text_type.data
                new_text.order = len(company.texts.all()) + 1
                new_text.company_id = company.id

                try:
                    database.session.add(new_text)
                    database.session.commit()
                except RuntimeError:
                    flash("There was a problem adding text to {}.".format(company.name_display), "danger")
                    return redirect(url_for("detail_company", id=company.id))

        flash("The text has been successfully added to {}.".format(company.name_display), "success")
        return redirect(url_for("detail_company", id=company.id))

    # Add image
    if add_image_form.submit_add_image.data and add_image_form.validate():

        new_image = CompanyImage()
        add_image_form.populate_obj(new_image)
        new_image.order = len(company.images.all()) + 1
        new_image.company_id = company.id

        try:
            database.session.add(new_image)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding an image to {}.".format(company.name_display), "danger")
            return redirect(url_for("detail_company", id=company.id))

        flash("The image has been successfully added to {}.".format(company.name_display), "success")
        return redirect(url_for("detail_company", id=company.id))

    return render_template("companies_detail.html",
                           title="{}".format(company.name_display),
                           heading="{}".format(company.name_full),
                           company=company,
                           texts=texts,
                           cars=cars,
                           add_text_form=add_text_form,
                           add_image_form=add_image_form)
