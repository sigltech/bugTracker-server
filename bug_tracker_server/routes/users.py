from flask import Blueprint, request, jsonify, make_response, current_app as app
from flask_cors import cross_origin
from ..database.db import db
from ..models import users
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
import uuid
import jwt
import datetime

user_routes = Blueprint("users", __name__)

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
            current_user = users.User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)
    return decorator    

@user_routes.route("/users", methods=["GET"])
def get_all_users():
    try:
        def user_serializer(users):
            # serialiser for user object. returns the user information listed as a json object
                return {
                    "id": users.id,
                    "username": users.username,
                    "email": users.email,
                    "firstname": users.firstname
                }

        all_users = users.User.query.all()
        return jsonify([*map(user_serializer, users.User.query.all())]),200
    except:
        return jsonify({"message": "There was an error getting the users."}), 500


@user_routes.route("/register", methods=["POST"])
def create():
    if request.method == "POST":
        try:
            content = request.json
            # print(content)
            print(content["username"])
            print(content["email"])
            print(content["password"])
            print(content["name"])
            
            hashed_password = generate_password_hash(content["password"], method='sha256')
            hashed_password_confirmation = generate_password_hash(content["passwordConfirmation"], method='sha256')
            user = users.User(
                id = f'{uuid.uuid1()}',
                username = content["username"],
                password = hashed_password,
                passwordConfirmation = hashed_password_confirmation,
                firstname = content["name"],
                email = content["email"],
                user_type = content["userType"]
            )

            db.session.add(user)
            db.session.commit()
            return 'user added'
        except:
            if(request.json["password"] != request.json["passwordConfirmation"]):
                return jsonify({"message": "Passwords do not match."}), 500
            elif(users.User.query.filter_by(username=request.json["username"]).first()):
                return jsonify({"message": "Username already exists."}), 409
            return jsonify({"message": "There was an error creating the user"}), 500

@user_routes.route('/login', methods=['POST']) 
def login_user():

    # Check that login request was sent with basic auth
    auth = request.authorization

    if not auth or not auth.username or not auth.password: 
        return make_response('could not verify basic auth', 401, {'Authentication': 'login required"'})   
    
    user = users.User.query.filter_by(username=auth.username).first()  
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id': user.id, 'exp' : datetime.datetime.now() + datetime.timedelta(minutes=45)}, app.config['SECRET_KEY'], "HS256"), {"user_id": user.id, "username": user.username, "user_type": user.user_type}
        return jsonify({'token': token}), 200
    else:
        return jsonify('could not verify'), 401


