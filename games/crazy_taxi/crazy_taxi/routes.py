from games.crazy_taxi.crazy_taxi import blueprint


@blueprint.route("/instances/overview", methods=['GET'])
@blueprint.route("/instances/overview/all", methods=['GET'])
def overview_instances():

    pass


@blueprint.route("/instances/add-instance", methods=['GET', 'POST'])
def add_instance():

    return "Yes!"
