# System modules.
from datetime import datetime

# Personal modules.
from config import db, ma


class Master(db.Model):
    __tablename__ = "master"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))


class MasterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Master
        load_instance = True


class Detail(db.Model):
    __tablename__ = "detail"
    user_id = db.Column(db.Integer, primary_key=True)
    postalcode = db.Column(db.String(32))
    cityname = db.Column(db.String(32))
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class DetailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Detail
        load_instance = True
