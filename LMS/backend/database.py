from flask_sqlalchemy import SQLAlchemy
import enum
from sqlalchemy import Enum
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

# Association table between Users and Roles
class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'), primary_key=True)

# Model for Users
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))

# Model for Roles (Student or Instructor)
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

# Model for Course
class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.String(8), primary_key=True)
    course_name = db.Column(db.String(100), unique=True, nullable=False)
    course_description = db.Column(db.String(), nullable=False)
    modules = db.relationship('Module', backref='course', lazy=True)

# Model for Module (Week)
class Module(db.Model):
    __tablename__ = 'module'
    module_id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String(100), unique=True, nullable=False)
    module_description = db.Column(db.Text, nullable=False)
    course_id = db.Column(db.String(8), db.ForeignKey('course.course_id'), nullable=False)
    lessons = db.relationship('Lesson', backref='module', lazy=True)
    assignments = db.relationship('Assignment', backref='module', lazy=True)

# Model for Lesson (Video and Slides)
class Lesson(db.Model):
    __tablename__ = 'lesson'
    lesson_id = db.Column(db.Integer, primary_key=True)
    lesson_name = db.Column(db.String(100), unique=True, nullable=False)
    lesson_description = db.Column(db.Text, nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.module_id'), nullable=False)
    video_url = db.Column(db.String(), nullable=False)
    slide_url = db.Column(db.String(), nullable=False)

# Model for Notes (made by student)
class Note(db.Model):
    __tablename__ = 'note'
    note_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('module.module_id'), nullable=False)
    note = db.Column(db.Text, nullable=False)

# Enumerator for Assessment Types
class AssessmentType(enum.Enum):
    PRACTICE = 'practice'       # Practice
    GRADED = 'graded'           # Graded

# Enumerator for Assignment Types
class AssignmentType(enum.Enum):
    THEORY = 'theory'             # Theory Assignment with MCQs
    PROGRAMMING = 'programming'   # Programming Assignment

# Model for Assignments
class Assignment(db.Model):
    __tablename__ = 'assignment'
    assignment_id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.String(8), db.ForeignKey('module.module_id'), nullable=False)
    assessment_type = db.Column(db.Enum(AssessmentType), nullable=False)
    assignment_type = db.Column(db.Enum(AssignmentType), nullable=False)
    due_date = db.Column(db.DateTime(), nullable=False)
    questions = db.relationship('Question', backref='assignment', lazy=True)

# Enumerator for Question Types - Open to Extension
class QuestionType(enum.Enum):
    MCQ = 'mcq'
    PROGRAMMING = 'programming'

# Model for Questions
class Question(db.Model):
    __tablename__ = 'question'
    question_id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.assignment_id'), nullable=False)
    question_type = db.Column(db.Enum(QuestionType), nullable=False)
    question = db.Column(db.Text, nullable=False)
    options = db.relationship('Option', backref='question', lazy=True)          # for MCQ
    test_cases = db.relationship('TestCase', backref='question', lazy=True)     # for Programming

# Model for Options for MCQs
class Option(db.Model):
    __tablename__ = 'option'
    option_id = db.Column(db.Integer, primary_key=True)
    option_num = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)
    option = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)

# Enumerator for Test Case Types
class TestCaseType(enum.Enum):
    PUBLIC = 'public'
    PRIVATE = 'private'

# Model for Test Cases for Programming Questions
class TestCase(db.Model):
    __tablename__ = 'test_case'
    test_case_id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.question_id'), nullable=False)
    test_case_type = db.Column(db.Enum(TestCaseType), nullable=False)
    input_data = db.Column(db.Text, nullable=False)
    expected_output = db.Column(db.Text, nullable=False)

# Model for Submissions
class Submission(db.Model):
    submission_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.assignment_id'), nullable=False)
    submission_date = db.Column(db.DateTime(), nullable=False)
    submission = db.Column(db.Text, nullable=False)
    grade = db.Column(db.String(), nullable=False)
    
# Model for Chatbot Knowledge Base
class Chatbot(db.Model):
    __tablename__ = 'chatbot'
    knowledge_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(8), db.ForeignKey('course.course_id'), nullable=False)
    knowledge = db.Column(db.Text, nullable=False)