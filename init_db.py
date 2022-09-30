from bug_tracker_server import db
from bug_tracker_server.models import users

# Clear it all out

db.drop_all()

# Set it back up

db.create_all()
