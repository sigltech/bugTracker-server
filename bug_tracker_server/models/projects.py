from ..database.db import db
import datetime

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    completed_on = db.Column(db.DateTime, nullable=True)
    completed_by = db.Column(db.String(80), nullable=True)
    projected_completion_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, id, name, description, completed_on, completed_by, projected_completion_date):
        self.id = id
        self.name = name
        self.description = description
        self.completed_on = completed_on
        self.completed_by = completed_by
        self.projected_completion_date = projected_completion_date
