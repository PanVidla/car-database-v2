from general import database
from general.models.instance import Instance


class InstanceCT(Instance):

    __tablename__ = "instances_ct"

    # Metadata
    id = database.Column(database.Integer, database.ForeignKey('instances.id'), primary_key=True)
