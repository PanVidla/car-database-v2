from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from general import cardb, database
from general.models.car import BodyStyle, CarClass, Drivetrain, EngineLayout
from general.models.game import GameGenre, Platform, GameState
from general.models.misc import Country, Company
from general.models.part import Aspiration, FuelType, TransmissionType


# Debug menu
@cardb.route("/debug", methods=['GET'])
@login_required
def debug_menu():

    return render_template("debug_menu.html",
                           title="Debug menu",
                           heading="Debug menu")


# Debug menu
@cardb.route("/debug/add-basic-objects", methods=['GET'])
@login_required
def add_basic_objects():

    flash("Adding basic objects.", "info")

    # Countries
    country_1 = Country(name_full="🏴 Debug Country 1",
                        name_display="🏴 Debug 1",
                        name_short="DC1")
    country_2 = Country(name_full="🎌 Debug Country 2",
                        name_display="🎌 Debug 2",
                        name_short="DC2")

    try:
        database.session.add(country_1)
        database.session.add(country_2)
        database.session.commit()
    except RuntimeError:
        flash("There was a problem saving debug countries to the database.")

    # Companies
    game_company = Company(name_full="Debug Game Company",
                           name_display="Debug Game Company",
                           name_short="DGC",
                           description="A debug company serving as a mock object in place of a developer",
                           is_game_developer=True,
                           country_id=country_1.id)

    car_company = Company(name_full="Debug Car Company",
                          name_display="Debug Car Company",
                          name_short="DCC",
                          description="A debug company serving as a mock object in place of a car manufacturer",
                          is_car_manufacturer=True,
                          is_car_part_manufacturer=True,
                          country_id=country_2.id)

    try:
        database.session.add(game_company)
        database.session.add(car_company)
        database.session.commit()
    except RuntimeError:
        flash("There was a problem saving debug companies to the database.")

    # Games-related objects
    genre_arcade = GameGenre(name="arcade",
                             realism=1)
    genre_arcade_simcade = GameGenre(name="arcade-simcade",
                                     realism=2)
    genre_simcade = GameGenre(name="simcade",
                              realism=3)
    genre_simcade_simulation = GameGenre(name="simcade-simulation",
                                         realism=4)
    genre_simulation = GameGenre(name="simulation",
                                 realism=5)
    platform_pc = Platform(name_full="PC (Windows)",
                           name_display="PC (Windows)",
                           name_short="PC (Win)")
    state_not_started = GameState(order=1,
                                  name="not started")
    state_in_progress = GameState(order=2,
                                  name="in-progress")
    state_complete = GameState(order=3,
                               name="complete")
    state_100 = GameState(order=4,
                          name="100%")
    state_paused = GameState(order=5,
                             name="paused")
    state_aborted = GameState(order=6,
                              name="aborted")

    try:
        database.session.add(genre_arcade)
        database.session.add(genre_arcade_simcade)
        database.session.add(genre_simcade)
        database.session.add(genre_simcade_simulation)
        database.session.add(genre_simulation)
        database.session.add(platform_pc)
        database.session.add(state_not_started)
        database.session.add(state_in_progress)
        database.session.add(state_complete)
        database.session.add(state_100)
        database.session.add(state_paused)
        database.session.add(state_aborted)
        database.session.commit()
    except RuntimeError:
        flash("There was a problem saving debug game-related objects to the database.")

    # Car-related objects
    aspiration = Aspiration(name="naturally aspirated")
    body_style = BodyStyle(name="sedan",
                           no_of_doors=4)
    car_class = CarClass(name_custom="A-class")
    drivetrain_fwd = Drivetrain(name_full="front wheel drive",
                                name_short="FWD")
    drivetrain_rwd = Drivetrain(name_full="rear wheel drive",
                                name_short="RWD")
    drivetrain_awd = Drivetrain(name_full="front wheel drive",
                                name_short="AWD")
    engine_layout_front = EngineLayout(name="front-engined")
    engine_layout_mid = EngineLayout(name="mid-engined")
    engine_layout_rear = EngineLayout(name="rear-engined")
    fuel_type_petrol = FuelType(name="petrol")

    # Parts
    transmission_type = TransmissionType(name="manual")

    try:
        database.session.add(aspiration)
        database.session.add(body_style)
        database.session.add(car_class)
        database.session.add(drivetrain_fwd)
        database.session.add(drivetrain_rwd)
        database.session.add(drivetrain_awd)
        database.session.add(engine_layout_front)
        database.session.add(engine_layout_mid)
        database.session.add(engine_layout_rear)
        database.session.add(fuel_type_petrol)
        database.session.add(transmission_type)
        database.session.commit()
    except RuntimeError:
        flash("There was a problem saving debug car-related objects to the database.")

    flash("Adding of basic objects complete.", "success")

    return redirect(url_for("debug_menu"))
