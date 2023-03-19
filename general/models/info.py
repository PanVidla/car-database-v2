from general import database


class Text(database.Model):

    __tablename__ = "texts"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    order = database.Column(database.Integer, index=True, nullable=False)
    content = database.Column(database.Unicode, nullable=False)
    text_type = database.Column(database.Integer, default=0, index=True, nullable=False)


class Image(database.Model):

    __tablename__ = "images"

    # Metadata
    id = database.Column(database.Integer, primary_key=True)

    # General
    order = database.Column(database.Integer, index=True, nullable=False)
    path = database.Column(database.Unicode, nullable=False)
    description = database.Column(database.Unicode, nullable=True)
