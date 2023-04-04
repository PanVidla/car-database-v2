# Overviews
from datetime import datetime

from flask import render_template, flash, redirect, url_for

from general import cardb, database
from general.forms_games import PlatformAddForm, PlatformEditForm, GameSeriesAddForm, GameSeriesEditForm, \
    GameGenreAddForm, GameGenreEditForm, GameGeneralAddForm, GamePlatformsAddForm, GameStateAddForm, GameStateEditForm, \
    GameActivityInitialAddForm, GameGeneralEditForm, GamePlatformsEditForm, GameActivityNonInitialAddForm, \
    GameStateChangeForm, GameActivityEditForm
from general.forms_info import TextForm
from general.models.game import Game, Platform, GameSeries, GameGenre, create_game_from_form, GameState, GameActivity, \
    create_initial_activity_from_form, GamePlatform, create_non_initial_activity_from_form, GameText, GameSeriesText, \
    PlatformText


@cardb.route("/games/", methods=['GET'])
@cardb.route("/games/all", methods=['GET'])
def overview_games():

    games = Game.query\
        .filter(Game.is_deleted != True)\
        .order_by(Game.name_display.asc()).all()

    return render_template("games_overview.html",
                           title="Games",
                           heading="All games",
                           games=games,
                           viewing="games")


@cardb.route("/games/game-series", methods=['GET'])
def overview_game_series():

    game_series = GameSeries.query.order_by(GameSeries.name.asc()).all()

    return render_template("games_overview_game_series.html",
                           title="Game series",
                           heading="All game series",
                           game_series=game_series,
                           viewing="game_series")


@cardb.route("/games/genres", methods=['GET'])
def overview_genres():

    genres = GameGenre.query.order_by(GameGenre.realism.asc()).all()

    return render_template("games_overview_genres.html",
                           title="Genres",
                           heading="Genres",
                           genres=genres,
                           viewing="genres")


@cardb.route("/games/platforms", methods=['GET'])
def overview_platforms():

    platforms = Platform.query.order_by(Platform.name_display.asc()).all()

    return render_template("games_overview_platforms.html",
                           title="Platforms",
                           heading="All platforms",
                           platforms=platforms,
                           viewing="platforms")


@cardb.route("/games/states", methods=['GET'])
def overview_states():

    states = GameState.query.order_by(GameState.order.asc()).all()

    return render_template("games_overview_states.html",
                           title="Platforms",
                           heading="All platforms",
                           states=states,
                           viewing="states")


# Add game (general information)
@cardb.route("/games/add-game/general", methods=['GET', 'POST'])
def add_game_general():

    form = GameGeneralAddForm()

    if form.validate_on_submit():

        new_game = create_game_from_form(form)

        if new_game == -1:
            return redirect(url_for("overview_games"))

        try:
            database.session.add(new_game)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding a new game to the database.", "danger")
            return redirect(url_for("add_game_general"))

        flash("{} ({}, {}) has been successfully added to the database.".format(new_game.name_display,
                                                                                new_game.name_full,
                                                                                new_game.name_short), "success")
        return redirect(url_for("add_game_platforms", id=new_game.id))

    return render_template("games_form_1_general.html",
                           title="Add game",
                           heading="Add game",
                           form=form,
                           viewing="games")


# Add game (platform information)
@cardb.route("/games/add-game/platforms/<id>", methods=['GET', 'POST'])
def add_game_platforms(id):

    game = Game.query.get(id)
    form = GamePlatformsAddForm()

    if form.validate_on_submit():

        game.set_platforms(form.platforms.data)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding platforms to the game.", "danger")
            return redirect(url_for("add_game_platforms"))

        for platform in game.platforms:
            flash("{} now exists on platform {}.".format(game.name_display, platform.name_display), "success")

        return redirect(url_for("add_game_activity", id=game.id))

    return render_template("games_form_2_platforms.html",
                           title="Add game",
                           heading="Add game",
                           form=form,
                           viewing="games")


# Add game (initial activity)
@cardb.route("/games/add-game/activities/<id>", methods=['GET', 'POST'])
def add_game_activity(id):

    game = Game.query.get(id)
    form = GameActivityInitialAddForm()

    if form.validate_on_submit():

        new_activity = create_initial_activity_from_form(form, game)

        try:
            database.session.add(new_activity)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding the initial activity \"{}\" to the game.".format(new_activity.name), "danger")
            return redirect(url_for("add_game_activity", id=game.id))

        flash("The initial activity \"{}\" has been successfully added to {}.".format(new_activity.name, game.name_display), "success")
        return redirect(url_for("overview_games"))

    return render_template("games_form_3_initial_activity.html",
                           title="Add game",
                           heading="Add game",
                           form=form,
                           viewing="games")


# Add activity (not to be confused with add_game_activity, which only adds the initial activity)
@cardb.route("/games/activities/add-activity/<game_id>", methods=['GET', 'POST'])
def add_activity(game_id):

    game = Game.query.get(game_id)
    form = GameActivityNonInitialAddForm()

    if form.validate_on_submit():

        new_activity = create_non_initial_activity_from_form(form, game)

        if new_activity == -1:
            flash("An activity for this game with the same order number already exists!", "danger")
            return redirect(url_for("add_activity", game_id=game.id))

        try:
            database.session.add(new_activity)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding the activity \"{}\" to the game.".format(new_activity.name), "danger")
            return redirect(url_for("add_activity", game_id=game.id))

        flash("The activity \"{}\" has been successfully added to {}.".format(new_activity.name, game.name_display), "success")
        return redirect(url_for("detail_game", id=game.id))

    return render_template("games_form_3_non_initial_activity.html",
                           title="Add game",
                           heading="Add game",
                           form=form,
                           viewing="games")


# Next activity
@cardb.route("/games/activities/next-activity/<game_id>", methods=['GET', 'POST'])
def next_activity(game_id):

    game = Game.query.get(game_id)
    active_activity = GameActivity.query.filter(GameActivity.game_id == game_id, GameActivity.is_active == True).first()
    next_activity = GameActivity.query.filter(GameActivity.game_id == game_id, GameActivity.order == active_activity.order + 1).first()

    if next_activity is None:
        next_activity = GameActivity.query.filter(GameActivity.game_id == game_id, GameActivity.order == 1).first()

    active_activity.is_active = False
    next_activity.is_active = True

    try:
        database.session.commit()
    except RuntimeError:
        flash("Next activity couldn't be selected.", "danger")

    return redirect(url_for("detail_game", id=game.id))


@cardb.route("/games/activities/previous-activity/<game_id>", methods=['GET', 'POST'])
def previous_activity(game_id):

    game = Game.query.get(game_id)
    active_activity = GameActivity.query.filter(GameActivity.game_id == game_id, GameActivity.is_active == True).first()
    previous_activity = GameActivity.query.filter(GameActivity.game_id == game_id, GameActivity.order == active_activity.order - 1).first()

    if previous_activity is None:
        previous_activity = GameActivity.query.filter(GameActivity.game_id == game_id).order_by(GameActivity.order.desc()).all()
        previous_activity = previous_activity[0]

    active_activity.is_active = False
    previous_activity.is_active = True

    try:
        database.session.commit()
    except RuntimeError:
        flash("Next activity couldn't be selected.", "danger")

    return redirect(url_for("detail_game", id=game.id))


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


# Add genre
@cardb.route("/games/genres/add-genre", methods=['GET', 'POST'])
def add_genre():

    form = GameGenreAddForm()

    if form.validate_on_submit():

        new_genre = GameGenre()
        form.populate_obj(new_genre)

        try:
            database.session.add(new_genre)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding a new genre to the database.", "danger")
            return redirect(url_for("add_genre"))

        flash("{} has been successfully added to the database.".format(new_genre.name), "success")
        return redirect(url_for("overview_genres"))

    return render_template("games_form_genres.html",
                           title="Add genre",
                           heading="Add genre",
                           form=form,
                           viewing="genres")


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


# Add state
@cardb.route("/games/states/add-state", methods=['GET', 'POST'])
def add_state():

    form = GameStateAddForm()

    if form.validate_on_submit():

        new_state = GameState()
        form.populate_obj(new_state)

        try:
            database.session.add(new_state)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding a new game state to the database.", "danger")
            return redirect(url_for("add_state"))

        flash("The state \"{}\" has been successfully added to the database.".format(new_state.name), "success")
        return redirect(url_for("overview_states"))

    return render_template("games_form_states.html",
                           title="Add state",
                           heading="Add game state",
                           form=form,
                           viewing="states")


# Edit game (general information)
@cardb.route("/games/edit-game/<id>/general", methods=['GET', 'POST'])
def edit_game_general(id):

    game = Game.query.get(id)
    form = GameGeneralEditForm(obj=game)

    if form.validate_on_submit():

        edit_status = game.edit_game_from_form(form)

        if edit_status == -1:
            flash("There was a problem editing the game.", "danger")
            return redirect(url_for("detail_game", id=game.id))

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the game.", "danger")
            return redirect(url_for("detail_game", id=game.id))

        flash("{} ({}, {}) has been successfully edited.".format(game.name_display,
                                                                                game.name_full,
                                                                                game.name_short), "success")
        return redirect(url_for("detail_game", id=game.id))

    return render_template("games_form_1_general.html",
                           title="{}".format(game.name_display),
                           heading="{}".format(game.name_full),
                           form=form,
                           viewing="games",
                           editing=True)


# Edit game (platforms)
@cardb.route("/games/edit-game/<id>/platforms", methods=['GET', 'POST'])
def edit_game_platforms(id):

    game = Game.query.get(id)
    platforms = GamePlatform.query.filter(GamePlatform.game_id == game.id).all()
    platform_ids = []

    for platform in platforms:
        platform_ids += str(platform.platform_id)

    form = GamePlatformsEditForm(platforms=platform_ids)

    if form.validate_on_submit():

        game.set_platforms(form.platforms.data)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the game.", "danger")
            return redirect(url_for("detail_game", id=game.id))

        flash("{} ({}, {}) has been successfully edited.".format(game.name_display,
                                                                 game.name_full,
                                                                 game.name_short), "success")
        return redirect(url_for("detail_game", id=game.id))

    return render_template("games_form_2_platforms.html",
                           title="{}".format(game.name_display),
                           heading="{}".format(game.name_full),
                           form=form,
                           viewing="games",
                           editing=True)


# Edit activity
@cardb.route("/games/activities/edit-activity/<id>", methods=['GET', 'POST'])
def edit_activity(id):

    activity = GameActivity.query.get(id)
    form = GameActivityEditForm(obj=activity)

    if form.validate_on_submit():

        form.populate_obj(activity)
        activity.game.datetime_edited = datetime.utcnow()

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing \"{}\".".format(activity.name), "danger")
            return redirect(url_for("edit_activity", id=activity.id))

        flash("Activity \"{}\" has been successfully edited.".format(activity.name, "success"))
        return redirect(url_for("detail_game", id=activity.game_id))

    return render_template("games_form_3_non_initial_activity.html",
                           title="Edit activity",
                           heading="Edit activity",
                           form=form,
                           viewing="games")


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


# Edit genre
@cardb.route("/games/genres/edit-genre/<id>", methods=['GET', 'POST'])
def edit_genre(id):

    genre = GameGenre.query.get(id)
    form = GameGenreEditForm(obj=genre)

    if form.validate_on_submit():

        form.populate_obj(genre)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing {}.".format(genre.name), "danger")
            return redirect(url_for("edit_genre", id=genre.id))

        flash("{} has been successfully edited.".format(genre.name, "success"))
        return redirect(url_for("detail_genre", id=genre.id))

    return render_template("games_form_genres.html",
                           title="Edit genre",
                           heading="Edit genre",
                           form=form,
                           viewing="genres")


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


# Edit state
@cardb.route("/games/state/edit-state/<id>", methods=['GET', 'POST'])
def edit_state(id):

    state = GameState.query.get(id)
    form = GameStateEditForm(obj=state)

    if form.validate_on_submit():

        form.populate_obj(state)

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem editing the state \"{}\".".format(state.name), "danger")
            return redirect(url_for("edit_state", id=state.id))

        flash("The state \"{}\" has been successfully edited.".format(state.name, "success"))
        return redirect(url_for("detail_state", id=state.id))

    return render_template("games_form_states.html",
                           title="Edit state",
                           heading="Edit state",
                           form=form,
                           viewing="states")


# Change state
@cardb.route("/games/state/change-state/<game_id>/<state_id>", methods=['GET', 'POST'])
def change_state(game_id, state_id):

    game = Game.query.get(id)
    game.game_state_id = state_id

    try:
        database.session.commit()
    except RuntimeError:
        flash("There was a problem changing the state for {}.".format(game.name_display), "danger")
        return redirect(url_for("detail_game", id=game.id))

    flash("The state of {} has been successfully changed.".format(game.name), "success")
    return redirect(url_for("detail_game", id=game.id))


# Delete game
@cardb.route("/games/delete-game/<id>", methods=['GET', 'POST'])
def delete_game(id):

    game = Game.query.get(id)
    game.is_deleted = True

    try:
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting {} ({}, {}).".format(game.name_display,
                                                                      game.name_full,
                                                                      game.name_short), "danger")
        return redirect(url_for("detail_game", id=game.id))

    flash("{} ({}, {}) has been successfully deleted.".format(game.name_display,
                                                              game.name_full,
                                                              game.name_short), "success")
    return redirect(url_for("overview_games"))


# Delete activity
@cardb.route("/games/activities/delete-activity/<id>", methods=['GET', 'POST'])
def delete_activity(id):

    activity = GameActivity.query.get(id)
    activity.game.datetime_edited = datetime.utcnow()

    try:
        database.session.delete(activity)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting {}.".format(activity.name), "danger")
        return redirect(url_for("detail_game", id=activity.game_id))

    flash("Activity \"{}\" has been successfully deleted.".format(activity.name), "success")
    return redirect(url_for("detail_game", id=activity.game_id))


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


# Delete genre
@cardb.route("/games/genres/delete-genre/<id>", methods=['GET', 'POST'])
def delete_genre(id):

    genre = GameGenre.query.get(id)

    try:
        database.session.delete(genre)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting {}.".format(genre.name), "danger")
        return redirect(url_for("detail_genre", id=genre.id))

    flash("{} has been successfully deleted.".format(genre.name), "success")
    return redirect(url_for("overview_genres"))


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


# Delete state
@cardb.route("/games/states/delete-state/<id>", methods=['GET', 'POST'])
def delete_state(id):

    state = GameState.query.get(id)

    try:
        database.session.delete(state)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the state \"{}\".".format(state.name), "danger")
        return redirect(url_for("detail_state", id=state.id))

    flash("The state \"{}\" has been successfully deleted.".format(state.name), "success")
    return redirect(url_for("overview_states"))


# Delete game text
@cardb.route("/games/text/delete-text/<id>", methods=['GET', 'POST'])
def delete_game_text(id):

    text = GameText.query.get(id)

    try:
        database.session.delete(text)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the text.", "danger")
        return redirect(url_for("detail_game", id=text.game_id))

    flash("The text has been successfully deleted.", "success")
    return redirect(url_for("detail_game", id=text.game_id))


# Delete game series text
@cardb.route("/games/game-series/text/delete-text/<id>", methods=['GET', 'POST'])
def delete_game_series_text(id):

    text = GameSeriesText.query.get(id)

    try:
        database.session.delete(text)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the text.", "danger")
        return redirect(url_for("detail_game_series", id=text.game_series_id))

    flash("The text has been successfully deleted.", "success")
    return redirect(url_for("detail_game_series", id=text.game_series_id))


# Delete platform text
@cardb.route("/games/platforms/text/delete-text/<id>", methods=['GET', 'POST'])
def delete_platform_text(id):

    text = PlatformText.query.get(id)

    try:
        database.session.delete(text)
        database.session.commit()

    except RuntimeError:
        flash("There was a problem with deleting the text.", "danger")
        return redirect(url_for("detail_platform", id=text.platform_id))

    flash("The text has been successfully deleted.", "success")
    return redirect(url_for("detail_platform", id=text.platform_id))


# Game detail
@cardb.route("/games/detail/<id>", methods=['GET', 'POST'])
def detail_game(id):

    game = Game.query.get(id)
    activities = GameActivity.query.filter(GameActivity.game_id == game.id).order_by(GameActivity.order.asc()).all()
    change_state_form = GameStateChangeForm()
    add_text_form = TextForm()

    # Add text
    if add_text_form.submit_add_text.data and add_text_form.validate():

        new_text = GameText()
        add_text_form.populate_obj(new_text)
        new_text.order = len(game.texts.all()) + 1
        new_text.game_id = game.id

        game.datetime_edited = datetime.utcnow()

        try:
            database.session.add(new_text)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding text to {}.".format(game.name_display), "danger")
            return redirect(url_for("detail_game", id=game.id))

        flash("The text has been successfully added to {}.".format(game.name_display), "success")
        return redirect(url_for("detail_game", id=game.id))

    # Change state
    if change_state_form.submit_change_state.data and change_state_form.validate():

        game.game_state_id = change_state_form.id.data
        game.datetime_edited = datetime.utcnow()

        try:
            database.session.commit()
        except RuntimeError:
            flash("There was a problem changing the state for {}.".format(game.name_display), "danger")
            return redirect(url_for("detail_game", id=game.id))

        flash("The state of {} has been successfully changed to \"{}\".".format(game.name_display, game.state.name), "success")
        return redirect(url_for("detail_game", id=game.id))

    return render_template("games_detail.html",
                           title="{}".format(game.name_display),
                           heading="{}".format(game.name_full),
                           game=game,
                           viewing="games",
                           add_text_form=add_text_form,
                           change_state_form=change_state_form,
                           activities=activities)


# Game series detail
@cardb.route("/games/game-series/detail/<id>", methods=['GET', 'POST'])
def detail_game_series(id):

    game_series = GameSeries.query.get(id)
    add_text_form = TextForm()

    # Add text
    if add_text_form.submit_add_text.data and add_text_form.validate():

        new_text = GameSeriesText()
        add_text_form.populate_obj(new_text)
        new_text.order = len(game_series.texts.all()) + 1
        new_text.game_series_id = game_series.id

        try:
            database.session.add(new_text)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding text to {}.".format(game_series.name), "danger")
            return redirect(url_for("detail_game_series", id=game_series.id))

        flash("The text has been successfully added to {}.".format(game_series.name), "success")
        return redirect(url_for("detail_game_series", id=game_series.id))

    return render_template("games_detail_game_series.html",
                           title="{}".format(game_series.name),
                           heading="{}".format(game_series.name),
                           game_series=game_series,
                           add_text_form=add_text_form,
                           viewing="game_series")


# Genre detail
@cardb.route("/games/genres/detail/<id>", methods=['GET', 'POST'])
def detail_genre(id):

    genre = GameGenre.query.get(id)

    return render_template("games_detail_genre.html",
                           title="{}".format(genre.name),
                           heading="{}".format(genre.name),
                           genre=genre,
                           viewing="genres")


# Platform detail
@cardb.route("/games/platforms/detail/<id>", methods=['GET', 'POST'])
def detail_platform(id):

    platform = Platform.query.get(id)
    add_text_form = TextForm()

    # Add text
    if add_text_form.submit_add_text.data and add_text_form.validate():

        new_text = PlatformText()
        add_text_form.populate_obj(new_text)
        new_text.order = len(platform.texts.all()) + 1
        new_text.platform_id = platform.id

        try:
            database.session.add(new_text)
            database.session.commit()
        except RuntimeError:
            flash("There was a problem adding text to {}.".format(platform.name_display), "danger")
            return redirect(url_for("detail_platform", id=platform.id))

        flash("The text has been successfully added to {}.".format(platform.name_display), "success")
        return redirect(url_for("detail_platform", id=platform.id))

    return render_template("games_detail_platform.html",
                           title="{}".format(platform.name_display),
                           heading="{}".format(platform.name_full),
                           platform=platform,
                           add_text_form=add_text_form,
                           viewing="platforms")


# State detail
@cardb.route("/games/states/detail/<id>", methods=['GET', 'POST'])
def detail_state(id):

    state = GameState.query.get(id)

    return render_template("games_detail_state.html",
                           title="{}".format(state.name),
                           heading="{}".format(state.name),
                           state=state,
                           viewing="states")
