from ..database.db import db
import datetime

class ProjectAccess(db.Model):
    __tablename__ = 'projects_access'
    id = db.Column(db.String(80), primary_key=True)
    project = db.Column(db.String(80), db.ForeignKey('projects.id'))
    user = db.Column(db.String(80), db.ForeignKey('user.username'))
    date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.datetime.now().strftime("%d/%m/%Y %H:%m:%S"))
    access_type = db.Column(db.String(80), nullable=False)

    def __init__(self, id, project, user, date, accessType):
        self.id = id
        self.project = project
        self.user = user
        self.date = date
        self.accessType = accessType
