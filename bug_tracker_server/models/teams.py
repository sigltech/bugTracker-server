# from ..database.db import db

# class Team(db.Model):
#     __tablename__ = 'teams'
#     id = db.Column(db.String(80), primary_key=True)
#     name = db.Column(db.String(80), unique=True, nullable=False)
#     description = db.Column(db.String(120), nullable=False)
#     members = db.Column(db.String(500), nullable=True)
#     owner = db.Column(db.String(80), nullable=True)
#     bugs = db.Column(db.String(500), nullable=True)


#     def __init__(self, id, name, description, members, owner, bugs):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.members = members
#         self.owner = owner
#         self.bugs = bugs
