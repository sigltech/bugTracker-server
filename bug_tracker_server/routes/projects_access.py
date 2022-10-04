from flask import Blueprint, request, jsonify, make_response, current_app as app
from ..models.projects_access import ProjectAccess
from ..database.db import db
from functools import wraps
import uuid
import jwt
import datetime

projects_access_routes = Blueprint("projects_access", __name__)

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = ProjectAccess.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)
    return decorator

@projects_access_routes.route("/projects_access", methods=["GET", "POST"])
def index():
    if request.method == "GET":

        def projects_access_serializer(project_access):
            return {
                "id": project_access.id,
                "project": project_access.project,
                "user": project_access.user,
                "date": project_access.date
            }
        all_projects_access = ProjectAccess.query.all()
        return jsonify([*map(projects_access_serializer, all_projects_access)]),200
    else:
        content = request.json
        print(content)
        project_access = ProjectAccess(
            id = f'{uuid.uuid1()}',
            project = content["project"],
            user = content["user"],
            # date = datetime.datetime.utcnow()
        )
        db.session.add(project_access)
        db.session.commit()
        return jsonify({"message": "project_access created successfully"}),200

