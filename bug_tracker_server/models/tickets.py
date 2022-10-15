from ..database.db import db
import datetime

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.String(80), primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(80), nullable=False)
    tag = db.Column(db.ARRAY(db.String(80)), nullable=False)
    priority = db.Column(db.String(15), nullable=False)
    # team = db.Column(db.String(80), db.ForeignKey('teams.name'))
    assigned_user = db.Column(db.String(80), db.ForeignKey('user.username'))
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now().strftime("%d/%m/%Y %H:%m:%S"))
    created_by = db.Column(db.String(80), db.ForeignKey('user.username'))
    closed_on = db.Column(db.DateTime, nullable=True)
    closed_by = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=True)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now().strftime("%d/%m/%Y %H:%m:%S"))
    updated_by = db.Column(db.String(80), db.ForeignKey('user.username'), nullable=False)
    project = db.Column(db.String(80), db.ForeignKey('projects.id'), nullable=True)

    def __init__(self, id, title, description, status, tag, priority, assigned_user, created_by, updated_by, updated_on, closed_on, closed_by, project):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.tag = tag
        self.priority = priority
        self.assigned_user = assigned_user
        self.project = project
        self.created_by = created_by
        self.closed_on = closed_on
        self.closed_by = closed_by
        self.updated_on = updated_on
        self.updated_by = updated_by
