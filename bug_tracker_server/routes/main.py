from flask import Blueprint, request, jsonify, make_response, current_app as app
from ..models.tickets import Ticket
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
            current_user = Ticket.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)
    return decorator  

@main_routes.route("/tickets", methods=["GET", "POST"])
def index():
    if request.method == "GET":

        def tickets_serializer(ticket):
            return {
                "id": ticket.id,
                "title": ticket.title,
                "description": ticket.description,
                "status": ticket.status,
                "tag": ticket.tag,
                "priority": ticket.priority,
                "team": ticket.team,
                "assigned_user": ticket.assigned_user,
                "created_on": ticket.created_on,
                "created_by": ticket.created_by,
                "closed_on": ticket.closed_on,
                "closed_by": ticket.closed_by,
                "updated_on": ticket.updated_on,
                "updated_by": ticket.updated_by
            }
        all_tickets = Ticket.query.all()
        return jsonify([*map(tickets_serializer, all_tickets)]),200
    else:
        content = request.json
        print(content)
        ticket = Ticket(
            id = f'{uuid.uuid1()}',
            title = content["title"],
            description = content["description"],
            status = content["status"],
            tag = content["tag"],
            priority = content["priority"],
            team = content["team"],
            assigned_user = content["assigned_user"],
            created_by = content["created_by"],
            updated_by= content["updated_by"],
            created_on = datetime.datetime.now(),
            updated_on = datetime.datetime.now(),
            closed_on = None,
            closed_by = None

        )
        db.session.add(ticket)
        db.session.commit()
        return jsonify({"message": "New ticket added successfully."}), 201

@main_routes.route("/tickets/<id>", methods=["GET","PUT", "DELETE"])
def change_todo(id):
    if request.method == "PUT":
        content = request.json
        ticket = Ticket.query.filter_by(id=id).first()
        db.session.commit()
        return jsonify({"message": "Ticket updated successfully."}), 200
    elif request.method == "GET":
        ticket = Ticket.query.filter_by(id=id).first()
        return jsonify({
            "id": ticket.id, 
            "title": ticket.title, 
            "description": ticket.description,
            "status": ticket.status, 
            "tag": ticket.tag ,
            "priority": ticket.priority, 
            "assigned_user": ticket.assigned_user, 
            "team": ticket.team, 
            "created_by": ticket.created_by,
            "created_on": ticket.created_on,
            "closed_by": ticket.closed_by,
            "closed_on": ticket.closed_on,
            "updated_by": ticket.updated_by,
            "updated_on": ticket.updated_on
            }), 200
    else:
        ticket = Ticket.query.filter_by(id=id).first()
        db.session.delete(ticket)
        db.session.commit()
        return jsonify({"message": "Ticket deleted successfully."}), 200
