from ..database.db import db

class Bugs(db.Model):
    id = db.Column(db.String(80), primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(80), nullable=False)
    tag = db.Column(db.ARRAY(db.String(80)), nullable=False)
    priority = db.Column(db.String(15), nullable=False)
    team = db.Column(db.String(80), db.ForeignKey('teams.name'))
    assigned_user = db.Column(db.String(80), db.ForeignKey('user.username'))
    date = db.Column(db.DateTime(timezone=True), nullable=False, default=db.func.now())

    def __init__(self, id, title, description, status, tag, priority, assigned_user, team, date):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.tag = tag
        self.priority = priority
        self.assigned_user = assigned_user
        self.team = team
        self.date = date
