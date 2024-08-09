from flask import Flask, jsonify, request
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, roles_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import marshal, fields
from flask_cors import CORS
from .config import DevelopmentConfig, TestingConfig
from .database import db, User, Role
from .api import api


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
api.init_app(app)
cors = CORS(app, origins=['http://localhost:5173'])
db.init_app(app)
datastore = SQLAlchemyUserDatastore(db, User, Role)
app.security = Security(app, datastore, register_blueprint=False)
app.app_context().push()

# Create instance of db with student and instructor roles and a default instructor
with app.app_context():
    db.create_all()

    datastore.find_or_create_role(name='instructor')
    datastore.find_or_create_role(name='student')
    db.session.commit()

    if not datastore.find_user(email='instructor1@seekpp.com'):
        datastore.create_user(username='Instructor1',
                              email='instructor1@seekpp.com',
                              password=generate_password_hash('instructor1'),
                              roles=['instructor'])

    db.session.commit()


# API endpoint for Log in
@app.post('/api/v1/login')
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    if not email:
        return jsonify({"message": "Email is required"}), 400
    if not password:
        return jsonify({"message": "Password is required"}), 400

    user = datastore.find_user(email=email)

    if not user:
        return jsonify({"message": "User not found"}), 404

    if check_password_hash(user.password, password):
        return jsonify({
            "message": "user logged in",
            "email": user.email,
            "username": user.username,
            "role": user.roles[0].name,
            "token": user.get_auth_token(),
            "id": user.id
        }), 200
    else:
        return jsonify({"message": "Invalid password"}), 401


# API endpoint for Register
@app.post('/api/v1/register')
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    role = data['role']
    if not username:
        return jsonify({"message": "Username is required"}), 400
    if not email:
        return jsonify({"message": "Email is required"}), 400
    if not password:
        return jsonify({"message": "Password is required"}), 400
    if not role:
        return jsonify({"message": "Role is required"}), 400

    if role != 'student' and role != 'instructor':
        return jsonify({"message": "Invalid role"}), 400

    if datastore.find_user(email=email) or datastore.find_user(username=username):
        return jsonify({"message": "User already exists"}), 409

    user = datastore.create_user(username=username,
                                 email=email,
                                 password=generate_password_hash(password),
                                 roles=[role])
    user.active = True
    db.session.commit()

    return jsonify({"message": "User Registered Successfully!"}), 200


if __name__ == '__main__':
    app.run(debug=True)
