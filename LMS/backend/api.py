from flask_restful import Resource, Api, reqparse, marshal, fields
from flask_security import auth_required, roles_accepted, current_user
from database import db

api = Api(prefix='/api/v1')