from flask_restful import Resource, Api, reqparse, marshal, fields
from flask_security import auth_required, roles_accepted, current_user
from database import db, Course, Module, Lesson, Note, Chatbot as ChatbotDB
from gen_ai.chatbot import Chatbot as ChatbotLLM

api = Api(prefix='/api/v1')


course_fields = {
    "course_id": fields.String,
    "course_name": fields.String,
    "course_description": fields.String
}

class Courses(Resource):
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


module_fields = {
    "module_id": fields.Integer,
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


class ContentField(fields.Raw):
    def format(self, id):
        lesson = Lesson.query.get(id)
        return {
                'content': lesson.lesson_description,
                'video_url': lesson.video_url,
                'slide_url': lesson.slide_url
            }

lesson_fields = {
    'lesson_id': fields.Integer,
    'lesson_name': fields.String,
    'content': ContentField(attribute='lesson_id')
}

class Lessons(Resource):
    @auth_required('token')
    def get(self, course_id, module_id, lesson_id=None):
        course = Course.query.filter_by(course_id=course_id).first()
        module = Module.query.filter_by(course_id=course_id, module_id=module_id).first()
        if not course or not module:
            return {"message": "Course or Module not found"}, 404
        
        if module.course_id != course.course_id:
            return {"message": "Module not found"}, 404
        
        # Fetch all lessons
        if lesson_id is None:
            lessons = Lesson.query.filter_by(module_id=module_id).all()
            if len(lessons) == 0:
                return {"message": "No Lessons Found"}, 404
            return {
                    "course_id": course_id,
                    "module_id": module_id,
                    "lessons": marshal(lessons, lesson_fields)
                }, 200
        
        # Fetch a particular lesson
        else:
            lesson = Lesson.query.filter_by(module_id=module_id, lesson_id=lesson_id).first()
            if not lesson:
                return {"message": "Lesson not found"}, 404
            return marshal(lesson, lesson_fields), 200


note_fields = {
    'note_id': fields.Integer,
    'user_id': fields.Integer,
    'lesson_id': fields.Integer,
    'note': fields.String
}

class Notes(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('note', type=str, required=True, help='Note is required')
        super(Notes, self).__init__()

    @auth_required('token')
    def get(self, lesson_id):
        note = Note.query.filter_by(user_id=current_user.id, lesson_id=lesson_id).first()
        if note is None:
            return {"message": "No Note Found"}, 404
        return marshal(note, note_fields), 200
    
    @auth_required('token')
    def post(self, lesson_id):
        args = self.parser.parse_args()
        note = Note.query.filter_by(user_id=current_user.id, lesson_id=lesson_id).first()
        if note is not None:
            note.note = args['note']
            db.session.commit()
        else:
            note = Note(user_id=current_user.id, lesson_id=lesson_id, note=args['note'])
            db.session.add(note)
            db.session.commit()
        return {"message": "Note posted"}, 201


class ChatbotResource(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('course_id', type=str, required=True, help='Course ID is required')
        self.post_parser.add_argument('query', type=str, required=True, help='Query is required')
        
        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument('course_id', type=str, required=True, help='Course ID is required')
        self.put_parser.add_argument('new_knowledge', type=str, required=True, help='Knowledge is required')
        
        super(ChatbotResource, self).__init__()
    
    # Chatbot Query Endpoint
    @auth_required('token')
    def post(self):
        args = self.post_parser.parse_args()
        
        course = Course.query.filter_by(course_id=args['course_id']).first()
        knowledge_string = ""
        for knowledge in ChatbotDB.query.filter_by(course_id=args['course_id']).all():
            knowledge_string += f"- {knowledge.knowledge}\n"
        
        chatbot = ChatbotLLM(course, knowledge_string)
        response = chatbot.query(args['query'])
        
        return {"query": args['query'], "response": response}, 200
    
    # Chatbot Train Endpoint
    @auth_required('token')
    @roles_accepted('instructor')
    def put(self):
        args = self.put_parser.parse_args()
        chatbot_knowledge = ChatbotDB(course_id=args['course_id'], knowledge=args['new_knowledge'])
        db.session.add(chatbot_knowledge)
        db.session.commit()
        
        course = Course.query.filter_by(course_id=args['course_id']).first()
        knowledge_string = ""
        for knowledge in ChatbotDB.query.filter_by(course_id=args['course_id']).all():
            knowledge_string += f"- {knowledge.knowledge}\n"
        chatbot = ChatbotLLM(course, knowledge_string)
        chatbot.update_knowledge(knowledge_string)
        
        return {"message": "Chatbot knowledge base updated successfully"}, 201


class VideoSummarizer(Resource):
    @auth_required('token')
    def get(self, course_id, module_id, lesson_id):
        # summarizer = Summarizer(args['url'])
        # summary = summarizer.summarize()
        return {
            "summary": "summary",
            "key_points": [
                "key_point_1",
                "key_point_2",
                "key_point_3"
            ]
        }, 200


class SlideSummarizer(Resource):
    @auth_required('token')
    def get(self, course_id, module_id, lesson_id):
        # summarizer = Summarizer(args['url'])
        # summary = summarizer.summarize()
        return {
            "summary": "summary",
            "key_points": [
                "key_point_1",
                "key_point_2",
                "key_point_3"
            ]
        }, 200


api.add_resource(Courses, '/courses', '/courses/<string:course_id>')
api.add_resource(Modules, '/courses/<string:course_id>/modules')
api.add_resource(Lessons, '/courses/<string:course_id>/modules/<int:module_id>/lessons', '/courses/<string:course_id>/modules/<int:module_id>/lessons/<int:lesson_id>')
api.add_resource(Notes, '/notes/<int:lesson_id>')
api.add_resource(ChatbotResource, '/chatbot/query', '/chatbot/train')
api.add_resource(VideoSummarizer, '/courses/<string:course_id>/modules/<int:module_id>/lessons/<int:lesson_id>/generate-summary/video')
api.add_resource(SlideSummarizer, '/courses/<string:course_id>/modules/<int:module_id>/lessons/<int:lesson_id>/generate-summary/slide')