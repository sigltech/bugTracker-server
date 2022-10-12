from flask import Blueprint, request, jsonify, make_response, current_app as app
from ..models.projects import Project
from ..database.db import db
from functools import wraps
import uuid
import jwt
import datetime

projects_routes = Blueprint("projects", __name__)

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
            current_user = Project.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)
    return decorator 

@projects_routes.route("/projects", methods=["GET", "POST"])
def index():
    if request.method == "GET":

        def projects_serializer(project):
            return {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "team": project.team,
                "date": project.date
            }
        all_projects = Project.query.all()
        return jsonify([*map(projects_serializer, all_projects)]),200
    else:
        content = request.json
        print(content)
        project = Project(
            id = f'{uuid.uuid1()}',
            name = content["name"],
            description = content["description"],
            team = content["team"],
            date = datetime.datetime.utcnow(),
            users = content["users"],
            projected_completion_date = content["projected_completion_date"],
            completed_on = content["completed_on"],
            completed_by = content["completed_by"]
        )
        db.session.add(project)
        db.session.commit()
        return jsonify({"message": "project created successfully"}),200

@projects_routes.route("/projects/<id>", methods=["GET", "PUT", "DELETE"])
def project(id):
    if request.method == "GET":
        project = Project.query.filter_by(id=id).first()
        if project:
            return jsonify({
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "team": project.team,
                "date": project.date
            }),200
        else:
            return jsonify({"message": "project not found"}),404
    elif request.method == "PUT":
        project = Project.query.filter_by(id=id).first()
        if project:
            content = request.json
            project.name = content["name"]
            project.description = content["description"]
            project.team = content["team"]
            db.session.commit()
            return jsonify({"message": "project updated successfully"}),200
        else:
            return jsonify({"message": "project not found"}),404
    else:
        project = Project.query.filter_by(id=id).first()
        if project:
            db.session.delete(project)
            db.session.commit()
            return jsonify({"message": "project deleted successfully"}),200
        else:
            return jsonify({"message": "project not found"}),404

