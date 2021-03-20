from application import db
from application.model.time_interval import prepare_time_to_db


class WorkingTime(db.Model):
    __tablename__ = 'working_time'

    id: int = db.Column(db.Integer, primary_key=True)
    courier_id: int = db.Column(db.Integer, db.ForeignKey('couriers.courier_id'))
    from_hours: int = db.Column(db.Integer)
    to_hours: int = db.Column(db.Integer)

    def __init__(self, hours: str):
        self.from_hours, self.to_hours = prepare_time_to_db(hours)
