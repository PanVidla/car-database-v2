# Overviews
from flask import render_template, flash, redirect, url_for

from general import cardb, database
from general.forms_games import PlatformAddForm, PlatformEditForm, GameSeriesAddForm, GameSeriesEditForm
from general.models.game import Game, Platform, GameSeries


@cardb.route("/games/", methods=['GET'])
@cardb.route("/games/all", methods=['GET'])
def overview_games():

    games = Game.query.order_by(Game.name_display.asc()).all()

    return render_template("games_overview.html",
                           title="All games",
                           heading="All games",
                           games=games,
                           viewing="games")


@cardb.route("/games/game-series", methods=['GET'])
def overview_game_series():

    game_series = GameSeries.query.order_by(GameSeries.name.asc()).all()

    return render_template("games_overview_game_series.html",
                           title="All game series",
                           heading="All game series",
                           game_series=game_series,
                           viewing="game_series")


@cardb.route("/games/platforms", methods=['GET'])
def overview_platforms():

    platforms = Platform.query.order_by(Platform.name_display.asc()).all()

    return render_template("games_overview_platforms.html",
                           title="Platforms",
                           heading="Platforms",
                           platforms=platforms,
                           viewing="platforms")


# Add game series
@cardb.route("/games/game-series/add-game-series", methods=['GET', 'POST'])
def add_game_series():

    form = GameSeriesAddForm()

    if form.validate_on_submit():

        new_game_series = GameSeries()
        form.populate_obj(new_game_series)

        try:
            database.session.add(new_game_series)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding a new game series to the database.", "danger")
            return redirect(url_for("add_game_series"))

        flash("{} has been successfully added to the database.".format(new_game_series.name), "success")
        return redirect(url_for("overview_game_series"))

    return render_template("games_form_game_series.html",
                           title="Add game series",
                           heading="Add game series",
                           form=form,
                           viewing="game_series")


# Add platform
@cardb.route("/games/platforms/add-platform", methods=['GET', 'POST'])
def add_platform():

    form = PlatformAddForm()

    if form.validate_on_submit():

        new_platform = Platform()
        form.populate_obj(new_platform)

        try:
            database.session.add(new_platform)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding a new platform to the database.", "danger")
            return redirect(url_for("add_platform"))

        flash("{} ({}, {}) has been successfully added to the database.".format(new_platform.name_display,
                                                                                new_platform.name_full,
                                                                                new_platform.name_short),
              "success")
        return redirect(url_for("overview_platforms"))

    return render_template("games_form_platforms.html",
                           title="Add platform",
                           heading="Add platform",
                           form=form,
                           viewing="platforms")


# Edit game series
@cardb.route("/games/game-series/edit-game-series/<id>", methods=['GET', 'POST'])
def edit_game_series(id):

    game_series = GameSeries.query.get(id)
    form = GameSeriesEditForm(obj=game_series)

    if form.validate_on_submit():

        form.populate_obj(game_series)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing {}.".format(game_series.name), "danger")
            return redirect(url_for("edit_game_series", id=game_series.id))

        flash("{} has been successfully edited.".format(game_series.name, "success"))
        return redirect(url_for("detail_game_series", id=game_series.id))

    return render_template("games_form_game_series.html",
                           title="Edit game series",
                           heading="Edit game series",
                           form=form,
                           viewing="game_series")


# Edit platform
@cardb.route("/games/platforms/edit-platform/<id>", methods=['GET', 'POST'])
def edit_platform(id):

    platform = Platform.query.get(id)
    form = PlatformEditForm(obj=platform)

    if form.validate_on_submit():

        form.populate_obj(platform)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing {}.".format(platform.name_display), "danger")
            return redirect(url_for("edit_platform", id=platform.id))

        flash("{} ({}, {}) has been successfully edited.".format(platform.name_display,
                                                                 platform.name_full,
                                                                 platform.name_short), "success")
        return redirect(url_for("detail_platform", id=platform.id))

    return render_template("games_form_platforms.html",
                           title="Edit platform",
                           heading="Edit platform",
                           form=form,
                           viewing="platforms")


# Delete game series
@cardb.route("/games/game-series/delete-game-series/<id>", methods=['GET', 'POST'])
def delete_game_series(id):

    game_series = GameSeries.query.get(id)

    try:
        database.session.delete(game_series)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting {}.".format(game_series.name), "danger")
        return redirect(url_for("detail_game_series", id=game_series.id))

    flash("{} has been successfully deleted.".format(game_series.name), "success")
    return redirect(url_for("overview_game_series"))


# Delete platform
@cardb.route("/games/platforms/delete-platform/<id>", methods=['GET', 'POST'])
def delete_platform(id):

    platform = Platform.query.get(id)

    try:
        database.session.delete(platform)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting {}.".format(platform.name_display), "danger")
        return redirect(url_for("detail_platform", id=platform.id))

    flash("{} ({}, {}) has been successfully deleted.".format(platform.name_display,
                                                              platform.name_full,
                                                              platform.name_short), "success")
    return redirect(url_for("overview_platforms"))


# Game series detail
@cardb.route("/games/game-series/detail/<id>", methods=['GET', 'POST'])
def detail_game_series(id):

    game_series = GameSeries.query.get(id)

    return render_template("games_detail_game_series.html",
                           title="{}".format(game_series.name),
                           heading="{}".format(game_series.name),
                           game_series=game_series,
                           viewing="game_series")


# Platform detail
@cardb.route("/games/platforms/detail/<id>", methods=['GET', 'POST'])
def detail_platform(id):

    platform = Platform.query.get(id)

    return render_template("games_detail_platform.html",
                           title="{}".format(platform.name_display),
                           heading="{}".format(platform.name_full),
                           platform=platform,
                           viewing="platforms")
