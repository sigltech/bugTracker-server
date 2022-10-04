from flask import Blueprint, request, jsonify, make_response, current_app as app
from ..models.bug import Bugs
from ..database.db import db
from functools import wraps
import uuid
import jwt
import datetime

main_routes = Blueprint("main", __name__)

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
            current_user = Bugs.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)
    return decorator  

@main_routes.route("/bugs", methods=["GET", "POST"])
def index():
    if request.method == "GET":

        def bugs_serializer(bug):
            return {
                "id": bug.id,
                "title": bug.title,
                "description": bug.description,
                "status": bug.status,
                "tag": bug.tag,
                "priority": bug.priority,
                "team": bug.team,
                "assigned_user": bug.assigned_user,
                "date": bug.date
            }
        all_bugs = Bugs.query.all()
        return jsonify([*map(bugs_serializer, all_bugs)]),200
    else:
        content = request.json
        print(content)
        bug = Bugs(
            id = f'{uuid.uuid1()}',
            title = content["title"],
            description = content["description"],
            status = content["status"],
            tag = content["tag"],
            priority = content["priority"],
            team = content["team"],
            assigned_user = content["assigned_user"],
            date = datetime.datetime.utcnow()
        )
        db.session.add(bug)
        db.session.commit()
        return jsonify({"message": "New bug added successfully."}), 201

@main_routes.route("/bugs/<id>", methods=["GET","PUT", "DELETE"])
def change_todo(id):
    if request.method == "PUT":
        content = request.json
        bug = Bugs.query.filter_by(id=id).first()
        # bug.description = content["description"]
        bug.completed = content["completed"]
        db.session.commit()
        return jsonify({"message": "Bug updated successfully."}), 200
    elif request.method == "GET":
        bug = Bugs.query.filter_by(id=id).first()
        return jsonify({"id": bug.id, "title": bug.title, "description": bug.description,"status": bug.status, "tag": bug.tag ,"priority": bug.priority, "assigned_user": bug.assigned_user, "team": bug.team, "date": bug.date}), 200
    else:
        bug = Bugs.query.filter_by(id=id).first()
        db.session.delete(bug)
        db.session.commit()
        return jsonify({"message": "Bug deleted successfully."}), 200
