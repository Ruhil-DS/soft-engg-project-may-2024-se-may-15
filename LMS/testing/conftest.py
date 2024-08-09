import datetime
import uuid

import pytest

from ..backend.config import TestingConfig
from ..backend.database import Assignment, AssignmentType, Course, Lesson, Module, Note, Option, Question, QuestionType, \
    Role, Submission, User, db
from ..backend.main import app as flask_app


@pytest.fixture(scope='module')
def app():
    """
    Set up the Flask application for testing.
    """
    flask_app.config.from_object(TestingConfig)
    flask_app.testing = True

    yield flask_app

    with flask_app.app_context():
        db.drop_all()


@pytest.fixture(scope='module')
def test_client(app):
    """
    Set up the test client for making requests to the app.
    """
    with app.test_client() as testing_client:
        yield testing_client


@pytest.fixture(scope='module')
def init_database(app):
    """
    Set up the initial state of the database for testing.
    """
    with app.app_context():
        unique_id = str(uuid.uuid4())
        default_role = Role(name='student_test')
        db.session.add(default_role)
        default_role = db.session.query(Role).filter_by(name='student').first()
        default_user = User(username='test_user_default', email='patkennedy79@gmail.com', password='FlaskIsAwesome',
                            fs_uniquifier=unique_id, roles=[default_role])
        db.session.add(default_user)
        default_user = db.session.query(User).filter_by(username='test_user_default').first()
        # roles_table = RolesUsers(user_id=default_user.id, role_id=default_role.id) Doesn't work can't be bothered to fix. Please don't ask for this.
        unique_id = str(uuid.uuid4())
        second_user = User(username='test_user_2', email='patrick@yahoo.com', password='FlaskIsTheBest987',
                           fs_uniquifier=unique_id)
        # db.session.add(roles_table)
        db.session.add(second_user)
        db.session.commit()

        course1 = Course(course_name='Introduction to Flask', course_description='Learning the basics of Flask')
        db.session.add(course1)
        course1 = db.session.query(Course).filter_by(course_name='Introduction to Flask').first()
        module1 = Module(module_name='Flask Basics', module_description='Module 1 All about app.py!',
                         course_id=course1.course_id)
        db.session.add(module1)
        module1 = db.session.query(Module).filter_by(module_name='Flask Basics').first()
        lesson1 = Lesson(lesson_name='Flask Setup', lesson_description='Installing the basics',
                         module_id=module1.module_id, video_url='https://www.youtube.com/watch?v=2qgxAHW1w78',
                         slide_url='https://www.slides.com/patkennedy79/flask-basics')
        db.session.add(lesson1)
        lesson1 = db.session.query(Lesson).filter_by(lesson_name='Flask Setup').first()
        note1 = Note(user_id=default_user.id, lesson_id=lesson1.lesson_id, note='This is a test note')
        db.session.add(note1)
        assignment1 = Assignment(module_id=module1.module_id, assignment_type=AssignmentType.PA,
                                 due_date=datetime.datetime.now())
        db.session.add(assignment1)
        assignment1 = db.session.query(Assignment).filter_by(module_id=module1.module_id).first()
        question1 = Question(assignment_id=assignment1.assignment_id, question_type=QuestionType.MCQ,
                             question='What is Flask?')
        db.session.add(question1)
        question1 = db.session.query(Question).filter_by(question='What is Flask?').first()
        option1 = Option(question_id=question1.question_id, option='A web micro-framework', is_correct=True)
        db.session.add(option1)
        option1 = db.session.query(Option).filter_by(option='A web micro-framework').first()
        option2 = Option(question_id=question1.question_id, option='A container fot H2SO4')
        db.session.add(option2)
        option3 = Option(question_id=question1.question_id, option='I ran out of ideas. Leave me alone.')
        db.session.add(option3)
        submission1 = Submission(user_id=default_user.id, assignment_id=assignment1.assignment_id,
                                 submission=f"{{'question_id': {question1.question_id}, 'option_id': {option1.option_id}}}",
                                 submission_date=datetime.datetime.now(), grade='100')
        db.session.add(submission1)
        db.session.commit()

        yield


@pytest.fixture(scope='function')
def log_in_default_user(test_client):
    """
    Fixture to log in the default user for testing.
    """
    test_client.post('/api/v1/login',
                     json={'email': 'patkennedy79@gmail.com', 'password': 'FlaskIsAwesome'})

    yield

    test_client.get('/logout')


@pytest.fixture(scope='function')
def log_in_second_user(test_client):
    """
    Fixture to log in the second user for testing.
    """
    test_client.post('/api/v1/login',
                     json={'email': 'patrick@yahoo.com', 'password': 'FlaskIsTheBest987'})

    yield

    test_client.get('/logout')


@pytest.fixture(scope='module')
def new_user():
    """
    Create a new User for testing.
    """
    unique_id = str(uuid.uuid4())
    user = User(username='test_user1', email='test_user1@gmail.com', password='TEstingisgood', fs_uniquifier=unique_id)
    yield user
