from flask import Blueprint, request, jsonify, make_response, current_app as app
from ..models.teams import Teams
from ..database.db import db
from functools import wraps
import uuid
import jwt
import datetime

teams_routes = Blueprint("teams", __name__)

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
            current_user = Teams.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)
    return decorator  

@teams_routes.route("/teams", methods=["GET", "POST"])
def teams():
    if request.method == "GET":

        def teams_serializer(team):
            return {
                "id": team.id,
                "name": team.name,
                "description": team.description,
                "members": team.members,
                "owner": team.owner,
                "bugs": team.bugs
            }
        all_teams = Teams.query.all()
        return jsonify([*map(teams_serializer, all_teams)]),200
    else:
        content = request.json
        team = Teams(
            id = f'{uuid.uuid1()}',
            name = content["name"],
            description = content["description"],
            members = content["members"],
            owner=content["owner"],
            bugs = content["bugs"]
        )
        db.session.add(team)
        db.session.commit()
        return jsonify({"message": "New team added successfully."}), 201
