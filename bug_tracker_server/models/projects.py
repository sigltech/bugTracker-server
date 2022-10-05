from ..database.db import db
import datetime

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    team = db.Column(db.String(80), db.ForeignKey('teams.name'))
    ceated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __init__(self, id, name, description, team, ceated_on):
        self.id = id
        self.name = name
        self.description = description
        self.team = team
        self.ceated_on = ceated_on
