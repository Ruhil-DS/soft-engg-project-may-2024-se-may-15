from flask_restful import Resource, Api, reqparse, marshal, fields
from flask_security import auth_required, roles_required, current_user
from database import db, Course, Module, Lesson, Note, Chatbot as ChatbotDB, Assignment, \
    AssessmentType, AssignmentType, Question, QuestionType, Option, TestCase, TestCaseType, \
    Submission, User
from gen_ai.chatbot import Chatbot as ChatbotLLM
from gen_ai.video_summarizer import get_video_summary
from gen_ai.slide_summarizer import get_slide_summary
from gen_ai.translator import get_translation
from gen_ai.text_to_code_converter import get_converted_code
from gen_ai.assignment_generator import generate_theory_questions, generate_programming_questions, \
    generate_test_cases
from datetime import datetime, timezone, timedelta
from flask import jsonify

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
    def get(self, course_id, module_id=None):
        if module_id is None:
            modules = Module.query.filter_by(course_id=course_id).all()
            if len(modules) == 0:
                return {"message": "No Modules Found"}, 404
            return {
                "course_id": course_id,
                "modules": marshal(modules, module_fields)
            }, 200
        else:
            module = Module.query.filter_by(course_id=course_id, module_id=module_id).first()
            if not module:
                return {"message": "Module not found"}, 404
            return {
                "course_id": course_id,
                "module": marshal(module, module_fields)
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
    @roles_required('instructor')
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
        course = Course.query.filter_by(course_id=course_id).first()
        lesson = Lesson.query.filter_by(module_id=module_id, lesson_id=lesson_id).first()

        return get_video_summary(course, lesson), 200


class SlideSummarizer(Resource):
    @auth_required('token')
    def get(self, course_id, module_id, lesson_id):
        course = Course.query.filter_by(course_id=course_id).first()
        lesson = Lesson.query.filter_by(module_id=module_id, lesson_id=lesson_id).first()

        return get_slide_summary(course, lesson), 200


class Translator(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('source_text', type=str, required=True, help='Source Text is required')
        self.parser.add_argument('target_language', type=str, required=True, help='Target Language is required')
        super(Translator, self).__init__()

    @auth_required('token')
    def post(self):
        args = self.parser.parse_args()

        return get_translation(args['source_text'], args['target_language']), 200


class SpeechToCode(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('audio_transcript', type=str, required=True, help='Audio Transcript is required')
        self.parser.add_argument('coding_language', type=str, required=True, help='Coding Language is required')
        self.parser.add_argument('question', type=str, required=True, help='Question is required')
        super(SpeechToCode, self).__init__()

    @auth_required('token')
    def post(self):
        args = self.parser.parse_args()
        return get_converted_code(args['audio_transcript'], args['coding_language'], args['question']), 200


options_fields = {
    "option_num": fields.Integer,
    "option": fields.String,
    "is_correct": fields.Boolean
}

theory_question_fields = {
    "question_id": fields.Integer,
    "question": fields.String,
}
theory_question_fields['options'] = fields.List(fields.Nested(options_fields))


class PA(Resource):
    @auth_required('token')
    def get(self, module_id):
        assignment = Assignment.query.filter_by(module_id=module_id,
                                                assessment_type=AssessmentType.PRACTICE,
                                                assignment_type=AssignmentType.THEORY).first()

        if assignment is None:
            return {"message": "No practice assignment found"}, 404

        return {
            "module_id": module_id,
            "assignment_type": "theory",
            "assessment_type": "practice",
            "due_date": str(assignment.due_date),
            "questions": marshal(assignment.questions, theory_question_fields)
        }, 200

    @auth_required('token')
    def post(self, module_id):
        module = Module.query.filter_by(module_id=module_id).first()
        if not module:
            return {"message": "Module not found"}, 404
        
        course = Course.query.filter_by(course_id=module.course_id).first()
        
        pa = Assignment.query.filter_by(module_id=module_id,
                                        assessment_type=AssessmentType.PRACTICE,
                                        assignment_type=AssignmentType.THEORY).first()
        
        if not pa:
            pa = Assignment(module_id=module_id,
                            assignment_type=AssignmentType.THEORY,
                            assessment_type=AssessmentType.PRACTICE,
                            due_date=datetime.today() + timedelta(days=7))
        
        while True:
            try:
                questions = generate_theory_questions(course, module)
                break
            except Exception as e:
                pass
        
        for question in questions.__root__:
            new_question = Question(question_type=QuestionType.MCQ,
                                    question=question.question)
            
            for option in question.options:
                new_question.options.append(Option(option_num=option.option_num,
                                                   option=option.option,
                                                   is_correct=option.is_correct))
            
            pa.questions.append(new_question)
        
        db.session.add(pa)
        db.session.commit()

        return {"message": "Practice assignment created successfully"}, 201


class GA(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('module_id', type=int, required=True, help='Module ID is required')
        self.parser.add_argument('assignment_type', type=str, required=True, help='Assignment Type is required')
        self.parser.add_argument('assessment_type', type=str, required=True, help='Assessment Type is required')
        self.parser.add_argument('due_date', type=str, required=True, help='Due Date is required')
        self.parser.add_argument('questions', type=list, required=True, location='json', help='Questions is required')
        super(GA, self).__init__()

    @auth_required('token')
    def get(self, module_id):
        assignment = Assignment.query.filter_by(module_id=module_id,
                                                assessment_type=AssessmentType.GRADED,
                                                assignment_type=AssignmentType.THEORY).first()

        if assignment is None:
            return {"message": "No graded assignment found"}, 404

        return {
            "module_id": module_id,
            "assignment_type": "theory",
            "assessment_type": "graded",
            "due_date": str(assignment.due_date),
            "questions": marshal(assignment.questions, theory_question_fields)
        }, 200

    @auth_required('token')
    @roles_required('instructor')
    def post(self, module_id):
        args = self.parser.parse_args()

        module = Module.query.filter_by(module_id=module_id).first()
        if not module:
            return {"message": "Module not found"}, 404

        ga = Assignment(module_id=module_id,
                        assignment_type=AssignmentType.THEORY,
                        assessment_type=AssessmentType.GRADED,
                        due_date=datetime.strptime(args['due_date'], '%Y-%m-%dT%H:%M:%SZ'))

        for question in args['questions']:
            new_question = Question(question_type=QuestionType.MCQ,
                                    question=question['question'])

            for option in question['options']:
                new_question.options.append(
                    Option(option_num=option['option_num'],
                           option=option['option'],
                           is_correct=option['is_correct']))

            ga.questions.append(new_question)

        db.session.add(ga)
        db.session.commit()

        return {"message": "Graded assignment created successfully"}, 201


test_case_fields = {
    "test_input": fields.String(attribute='input_data'),
    "expected_output": fields.String(attribute='expected_output')
}


class TestCasesFields(fields.Raw):
    def format(self, id):
        public_test_cases = TestCase.query.filter_by(question_id=id,
                                                     test_case_type=TestCaseType.PUBLIC).all()
        private_test_cases = TestCase.query.filter_by(question_id=id,
                                                      test_case_type=TestCaseType.PRIVATE).all()

        return {
            "public": marshal(public_test_cases, test_case_fields),
            "private": marshal(private_test_cases, test_case_fields)
        }


programming_question_fields = {
    "question_id": fields.Integer,
    "question": fields.String,
}
programming_question_fields['test_cases'] = TestCasesFields(attribute='question_id')


class PrPA(Resource):
    @auth_required('token')
    def get(self, module_id):
        assignment = Assignment.query.filter_by(module_id=module_id,
                                                assessment_type=AssessmentType.PRACTICE,
                                                assignment_type=AssignmentType.PROGRAMMING).first()

        if assignment is None:
            return {"message": "No practice programming assignment found"}, 404

        return {
            "module_id": module_id,
            "assignment_type": "programming",
            "assessment_type": "practice",
            "due_date": str(assignment.due_date),
            "questions": marshal(assignment.questions, programming_question_fields)
        }, 200

    @auth_required('token')
    def post(self, module_id):
        module = Module.query.filter_by(module_id=module_id).first()
        if not module:
            return {"message": "Module not found"}, 404

        course = Course.query.filter_by(course_id=module.course_id).first()
        
        prpa = Assignment.query.filter_by(module_id=module_id,
                                          assessment_type=AssessmentType.PRACTICE,
                                          assignment_type=AssignmentType.PROGRAMMING).first()
        
        if not prpa:
            prpa = Assignment(module_id=module_id,
                              assignment_type=AssignmentType.PROGRAMMING,
                              assessment_type=AssessmentType.PRACTICE,
                              due_date=datetime.today() + timedelta(days=7))
        
        while True:
            try:
                questions = generate_programming_questions(course, module)
                break
            except Exception as e:
                pass
            
        
        for question in questions.__root__:
            new_question = Question(question_type=QuestionType.PROGRAMMING,
                                    question=question)

            while True:
                try:
                    test_cases = generate_test_cases(module, question).__root__
                    break
                except Exception as e:
                    pass
            
            for test_case in test_cases[:len(test_cases) // 2]:
                new_question.test_cases.append(
                    TestCase(test_case_type=TestCaseType.PUBLIC,
                             input_data=test_case.test_input,
                             expected_output=test_case.expected_output))
                
            for test_case in test_cases[len(test_cases) // 2:]:
                new_question.test_cases.append(
                    TestCase(test_case_type=TestCaseType.PRIVATE,
                             input_data=test_case.test_input,
                             expected_output=test_case.expected_output))

            prpa.questions.append(new_question)

        db.session.add(prpa)
        db.session.commit()
        
        return {"message": "Practice programming assignment created successfully"}, 201


class GrPA(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('module_id', type=int, required=True, help='Module ID is required')
        self.parser.add_argument('assignment_type', type=str, required=True, help='Assignment Type is required')
        self.parser.add_argument('assessment_type', type=str, required=True, help='Assessment Type is required')
        self.parser.add_argument('due_date', type=str, required=True, help='Due Date is required')
        self.parser.add_argument('questions', type=list, required=True, location='json', help='Questions is required')
        super(GrPA, self).__init__()

    @auth_required('token')
    def get(self, module_id):
        assignment = Assignment.query.filter_by(module_id=module_id,
                                                assessment_type=AssessmentType.GRADED,
                                                assignment_type=AssignmentType.PROGRAMMING).first()

        if assignment is None:
            return {"message": "No graded programming assignment found"}, 404

        return {
            "module_id": module_id,
            "assignment_type": "programming",
            "assessment_type": "graded",
            "due_date": str(assignment.due_date),
            "questions": marshal(assignment.questions, programming_question_fields)
        }, 200

    @auth_required('token')
    @roles_required('instructor')
    def post(self, module_id):
        args = self.parser.parse_args()

        module = Module.query.filter_by(module_id=module_id).first()
        if not module:
            return {"message": "Module not found"}, 404

        grpa = Assignment(module_id=module_id,
                          assignment_type=AssignmentType.PROGRAMMING,
                          assessment_type=AssessmentType.GRADED,
                          due_date=datetime.strptime(args['due_date'], '%Y-%m-%dT%H:%M:%SZ'))

        for question in args['questions']:
            new_question = Question(question_type=QuestionType.PROGRAMMING,
                                    question=question['question'])

            for test_case in question['test_cases']['public']:
                new_question.test_cases.append(
                    TestCase(test_case_type=TestCaseType.PUBLIC,
                             input_data=test_case['test_input'],
                             expected_output=test_case['expected_output']))

            for test_case in question['test_cases']['private']:
                new_question.test_cases.append(
                    TestCase(test_case_type=TestCaseType.PRIVATE,
                             input_data=test_case['test_input'],
                             expected_output=test_case['expected_output']))

            grpa.questions.append(new_question)

        db.session.add(grpa)
        db.session.commit()

        return {"message": "Graded programming assignment created successfully"}, 201


class PASubmission(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

        # Arguments for the submission
        self.parser.add_argument('submission', type=str, required=True, help='Submission content is required')
        self.parser.add_argument('module_id', type=int, required=True, help='Module ID is required')

        super(PASubmission, self).__init__()

    @auth_required('token')
    @roles_required('student')
    def post(self, module_id):
        args = self.parser.parse_args()
        submission_content = args['submission']
        submission_date = args.get('submission_date', datetime.now(timezone.utc))

        assignment = Assignment.query.filter_by(module_id=module_id,
                                                assessment_type=AssessmentType.PRACTICE,
                                                assignment_type=AssignmentType.THEORY).first()
        
        if not assignment:
            return {'message': 'Assignment not found'}, 404

        # Get the current user (requires jwt_required to be enabled)
        user = User.query.get(user_id=current_user.id)

        # Check if the content is not empty
        if not submission_content:
            return {'message': 'Empty Submission'}, 404

        submission = Submission(
            user_id=user.id,
            assignment_id=assignment.id,
            submission=submission_content,
            submission_date=submission_date,
            grade='not graded'
        )

        db.session.add(submission)
        db.session.commit()

        return {"message": "Practice Assignment Solution submitted successfully"}, 201


class GASubmission(Resource):

    def __init__(self):

        self.parser = reqparse.RequestParser()

        # Arguments for the submission
        self.parser.add_argument('submission', type=str, required=True, help='Submission content is required')
        self.parser.add_argument('module_id', type=int, required=True, help='Module ID is required')

        super(GASubmission, self).__init__()

    @auth_required('token')
    @roles_required('student')
    def post(self, module_id):
        args = self.parser.parse_args()
        submission_content = args['submission']
        submission_date = args.get('submission_date', datetime.now(timezone.utc))

        assignment = Assignment.query.filter_by(module_id=module_id,
                                                assessment_type=AssessmentType.GRADED,
                                                assignment_type=AssignmentType.THEORY).first()
        
        if not assignment:
            return {'message': 'Assignment not found'}, 404

        # Get the current user (requires jwt_required to be enabled)
        user = User.query.get(user_id=current_user.id)

        # Check if the content is not empty
        if not submission_content:
            return {'message': 'Empty Submission'}, 404

        submission = Submission(
            user_id=user.id,
            assignment_id=assignment.id,
            submission=submission_content,
            submission_date=submission_date,
            grade='not graded'
        )

        db.session.add(submission)
        db.session.commit()

        return {"message": "Graded Assignment Solution submitted successfully"}, 201


class PrPASubmission(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

        # Arguments for the submission
        self.parser.add_argument('submission', type=str, required=True, help='Submission content is required')
        self.parser.add_argument('module_id', type=int, required=True, help='Module ID is required')

        super(PrPASubmission, self).__init__()

    @auth_required('token')
    @roles_required('student')
    def post(self, module_id):
        args = self.parser.parse_args()
        submission_content = args['submission']
        submission_date = args.get('submission_date', datetime.now(timezone.utc))
        
        assignment = Assignment.query.filter_by(module_id=module_id,
                                                assessment_type=AssessmentType.PRACTICE,
                                                assignment_type=AssignmentType.PROGRAMMING).first()

        if not assignment:
            return {'message': 'Assignment not found'}, 404

        user = User.query.get(user_id=current_user.id)

        # Check if the content is not empty
        if not submission_content:
            return {'message': 'Empty Submission'}, 404

        submission = Submission(
            user_id=user.id,
            assignment_id=assignment.id,
            submission=submission_content,
            submission_date=submission_date,
            grade='not graded'
        )

        db.session.add(submission)
        db.session.commit()

        return {"message": "Practice Programming Assignment Solution submitted successfully"}, 201


class GrPASubmission(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

        # Arguments for the submission
        self.parser.add_argument('submission', type=str, required=True, help='Submission content is required')
        self.parser.add_argument('module_id', type=int, required=True, help='Module ID is required')

        super(GrPASubmission, self).__init__()
        # sample parser argument
        # self.parser.add_argument('question_id', type=int, required=True, help='Question ID is required')

    @auth_required('token')
    @roles_required('student')
    def post(self, module_id):
        args = self.parser.parse_args()
        submission_content = args['submission']
        submission_date = args.get('submission_date', datetime.now(timezone.utc))
        
        assignment = Assignment.query.filter_by(module_id=module_id,
                                                assessment_type=AssessmentType.GRADED,
                                                assignment_type=AssignmentType.PROGRAMMING).first()

        if not assignment:
            return {'message': 'Assignment not found'}, 404

        user = User.query.get(user_id=current_user.id)

        # Check if the content is not empty
        if not submission_content:
            return {'message': 'Empty Submission'}, 404

        submission = Submission(
            user_id=user.id,
            assignment_id=assignment.id,
            submission=submission_content,
            submission_date=submission_date,
            grade='not graded'
        )

        db.session.add(submission)
        db.session.commit()

        return {"message": "Graded Programming Assignment Solution submitted successfully"}, 201


class TestCaseGenerator(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('question', type=str, required=True, help='Question is required')
        self.parser.add_argument('num_public_test_cases', type=int, required=True, help='Number of public test cases is required')
        self.parser.add_argument('num_private_test_cases', type=int, required=True, help='Number of private test cases is required')
        
        super(TestCaseGenerator, self).__init__()
    
    # @auth_required('token')
    # @roles_required('instructor')
    def post(self, module_id):
        args = self.parser.parse_args()
        
        module = Module.query.filter_by(module_id=module_id).first()
        if not module:
            return {"message": "Module not found"}, 404

        course = Course.query.filter_by(course_id=module.course_id).first()
        
        num_test_cases = args['num_public_test_cases'] + args['num_private_test_cases']
        
        while True:
            try:
                test_cases = generate_test_cases(module, args['question'], num_test_cases).__root__
                break
            except Exception as e:
                pass
        
        return {
            "question": args['question'],
            "public": [
                {
                    "test_input": test_case.test_input,
                    "expected_output": test_case.expected_output
                }
                for test_case in test_cases[:args['num_public_test_cases']]
            ],
            "private": [
                {
                    "test_input": test_case.test_input,
                    "expected_output": test_case.expected_output
                }
                for test_case in test_cases[args['num_public_test_cases']:]
            ]
        }, 201


api.add_resource(
    Courses,
    '/courses',
    '/courses/<string:course_id>'
)

api.add_resource(
    Modules,
    '/courses/<string:course_id>/modules',
    '/courses/<string:course_id>/modules/<int:module_id>'
)

api.add_resource(
    Lessons,
    '/courses/<string:course_id>/modules/<int:module_id>/lessons',
    '/courses/<string:course_id>/modules/<int:module_id>/lessons/<int:lesson_id>'
)

api.add_resource(
    Notes,
    '/notes/<int:lesson_id>'
)

api.add_resource(
    ChatbotResource,
    '/chatbot/query',
    '/chatbot/train'
)

api.add_resource(
    VideoSummarizer,
    '/courses/<string:course_id>/modules/<int:module_id>/lessons/<int:lesson_id>/generate-summary/video'
)

api.add_resource(
    SlideSummarizer,
    '/courses/<string:course_id>/modules/<int:module_id>/lessons/<int:lesson_id>/generate-summary/slide'
)

api.add_resource(
    Translator,
    '/translate'
)

api.add_resource(
    SpeechToCode,
    '/transcript-to-code'
)

api.add_resource(
    PA,
    '/assignment/practice/theory/<int:module_id>',
    '/assignment/practice/theory/<int:module_id>/generate'
)

api.add_resource(
    GA,
    '/assignment/graded/theory/<int:module_id>'
)

api.add_resource(
    PrPA,
    '/assignment/practice/programming/<int:module_id>',
    '/assignment/practice/programming/<int:module_id>/generate'
)

api.add_resource(
    GrPA,
    '/assignment/graded/programming/<int:module_id>'
)

api.add_resource(
    PASubmission,
    '/assignment/practice/theory/<int:module_id>/submit'
)

api.add_resource(
    GASubmission,
    '/assignment/graded/theory/<int:module_id>/submit'
)

api.add_resource(
    PrPASubmission,
    '/assignment/practice/programming/<int:module_id>/submit'
)

api.add_resource(
    GrPASubmission,
    '/assignment/graded/programming/<int:module_id>/submit'
)

api.add_resource(
    TestCaseGenerator,
    '/assignment/graded/programming/<int:module_id>/generate-test-cases'
)