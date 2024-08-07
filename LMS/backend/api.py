from flask_restful import Resource, Api, reqparse, marshal, fields
from flask_security import auth_required, roles_accepted, current_user
from database import db, Course, Module

api = Api(prefix='/api/v1')


course_fields = {
    "course_id": fields.String,
    "course_name": fields.String,
    "course_description": fields.String
}
class Courses(Resource):
    # NOTE: Only to be implemented if POST/PUT/DELETE request for CUD operations
    # def __init__(self):
    #     self.parser = reqparse.RequestParser()
    #     self.parser.add_argument('course_id', type=str, required=True, help='Course ID is required')
    #     self.parser.add_argument('course_name', type=str, required=True, help='Course Name is required')
    #     self.parser.add_argument('course_description', type=str, required=True, help='Course Description is required')
    #     super(Courses, self).__init__()

    @auth_required('token')
    def get(self, course_id=None):
        if course_id is None:
            courses = Course.query.all()
            if len(courses) == 0:
                return {"message": "No Courses Found"}, 404
            return marshal(courses, course_fields), 200
        
        course = Course.query.filter_by(course_id=course_id).first()
        if not course:
            return {"message": "Course not found"}, 404
        return marshal(course, course_fields), 200

api.add_resource(Courses, '/courses', '/courses/<string:course_id>')


module_fields = {
    "module_id": fields.String,
    "module_name": fields.String,
    "module_description": fields.String
}

class Modules(Resource):
    @auth_required('token')
    def get(self, course_id):
        modules = Module.query.filter_by(course_id=course_id).all()
        if len(modules) == 0:
            return {"message": "No Modules Found"}, 404
        return {
                "course_id": course_id,
                "modules": marshal(modules, module_fields)
            }, 200

api.add_resource(Modules, '/courses/<string:course_id>/modules')