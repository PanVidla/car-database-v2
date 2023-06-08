from flask import render_template

from games.need_for_speed.iii_hot_pursuit import blueprint
from games.need_for_speed.iii_hot_pursuit.models.instance import InstanceNFS3


@blueprint.route("/instances/overview", methods=['GET'])
@blueprint.route("/instances/overview/all", methods=['GET'])
def overview_instances():

    instances = InstanceNFS3.query. \
        filter(InstanceNFS3.is_deleted != True) \
        .order_by(InstanceNFS3.nfs3_class_id.asc()).all()

    return render_template("nfs3_instances_overview.html",
                           title="Need for Speed III",
                           heading="All Need for Speed III instances",
                           instances=instances,
                           viewing="instances")
