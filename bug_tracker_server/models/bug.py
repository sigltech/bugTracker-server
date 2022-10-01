from ..database.db import db

class Bugs(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    completed = db.Column(db.Boolean, nullable=False)
    tag = db.Column(db.String(500), nullable=False)
    importance = db.Column(db.String(5), nullable=False)
    team = db.Column(db.String(80), db.ForeignKey('teams.name'),nullable=False)
    username = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)

    def __init__(self, id, description, completed, tag, importance, username, team):
        self.id = id
        self.description = description
        self.completed = completed
        self.tag = tag
        self.importance = importance
        self.username = username
        self.team = team
