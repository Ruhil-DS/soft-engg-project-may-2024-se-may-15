import datetime
import uuid

from ...backend.database import Assignment, AssignmentType, Course, Lesson, Module, Note, Option, Question, \
    QuestionType, Role, Submission, User, db


def test_new_user(new_user):
    """
    When a new User is created, check if the email and password are defined correctly
    """
    assert new_user.username == 'test_user1'
    assert new_user.email == 'test_user1@gmail.com'
    assert new_user.password == 'TEstingisgood'


def test_user_roles(init_database):
    """
    When a new User is created with roles, check if the roles are added correctly
    """
    unique_id = str(uuid.uuid4())
    default_role = Role(name='admin')
    db.session.add(default_role)
    default_role = db.session.query(Role).filter_by(name='admin').first()
    user = User(username='test_user_role', email='tester@gmail.com', password='FlaskIsAwesome', fs_uniquifier=unique_id,
                roles=[default_role])
    db.session.add(user)
    db.session.commit()
    user = db.session.query(User).filter_by(username='test_user_role').first()
    assert len(user.roles) == 1
    assert user.roles[0].name == 'admin'


def test_course_module_relationship(init_database):
    """
    When a Module is added to a Course, check if the module is added correctly
    """
    unique_id = str(uuid.uuid4())
    # default_role = Role(name='instructor')
    # db.session.add(default_role)
    default_role = db.session.query(Role).filter_by(name='instructor').first()
    default_user = User(username='test_user_module', email='tester_instr@gmail.com', password='FlaskIsAwesome',
                        fs_uniquifier=unique_id,
                        roles=[default_role])
    db.session.add(default_user)
    db.session.commit()
    default_user = db.session.query(User).filter_by(username='test_user_module').first()
    course1 = Course(course_name='Introduction to Flask in', course_description='Learning the basics of Flask in')
    db.session.add(course1)
    course1 = db.session.query(Course).filter_by(course_name='Introduction to Flask in').first()
    module1 = Module(module_name='Flask Basics in', module_description='Module 1 All about app.py! in',
                     course_id=course1.course_id)

    db.session.add(module1)
    module1 = db.session.query(Module).filter_by(module_name='Flask Basics in').first()
    lesson1 = Lesson(lesson_name='Flask Setup in', lesson_description='Installing the basics',
                     module_id=module1.module_id, video_url='https://www.youtube.com/watch?v=2qgxAHW1w78',
                     slide_url='https://www.slides.com/patkennedy79/flask-basics')
    db.session.add(lesson1)
    lesson1 = db.session.query(Lesson).filter_by(lesson_name='Flask Setup in').first()
    note1 = Note(user_id=default_user.id, lesson_id=lesson1.lesson_id, note='This is a test note in')
    db.session.add(note1)
    assignment1 = Assignment(module_id=module1.module_id, assignment_type=AssignmentType.PA,
                             due_date=datetime.datetime.now())
    db.session.add(assignment1)
    assignment1 = db.session.query(Assignment).filter_by(module_id=module1.module_id).first()
    question1 = Question(assignment_id=assignment1.assignment_id, question_type=QuestionType.MCQ,
                         question='What is Flask? in')
    db.session.add(question1)
    question1 = db.session.query(Question).filter_by(question='What is Flask? in').first()
    option1 = Option(question_id=question1.question_id, option='A web micro-framework :0', is_correct=True)
    db.session.add(option1)
    option1 = db.session.query(Option).filter_by(option='A web micro-framework :0').first()
    option2 = Option(question_id=question1.question_id, option='A container fot H2SO4 >:)')
    db.session.add(option2)
    option3 = Option(question_id=question1.question_id, option='I ran out of ideas. Leave me alone. pls')
    db.session.add(option3)
    submission1 = Submission(user_id=default_user.id, assignment_id=assignment1.assignment_id,
                             submission=f"{{'question_id': {question1.question_id}, 'option_id': {option1.option_id}}}",
                             submission_date=datetime.datetime.now(), grade='100')
    db.session.add(submission1)
    db.session.commit()

    assert len(course1.modules) == 1
    assert course1.modules[0].module_name == 'Flask Basics in'
    assert lesson1.lesson_description == 'Installing the basics'
    assert submission1.assignment_id == assignment1.assignment_id


# def test_lesson_module_relationship(init_database):
#     """
#     When a Lesson is added to a Module, check if the lesson is added correctly
#     """
#     module = Module.query.first()
#     lesson = Lesson(name='Models and Relationships', module=module)
#     db.session.add(lesson)
#     db.session.commit()
#
#     assert lesson.module.name == 'Flask Basics'
#     assert len(module.lessons) == 1
#     assert module.lessons[0].name == 'Models and Relationships'
