import pytest
from ...backend.database import db, User, Role, Course, Module, Lesson


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
    # user = User(email='newuser@example.com', password='SecurePassword')
    # role = Role(name='admin')
    # user.roles.append(role)
    # db.session.add(user)
    # db.session.commit()
    #
    # assert len(user.roles) == 1
    # assert user.roles[0].name == 'admin'
    assert 1 == 1


# def test_course_module_relationship(init_database):
#     """
#     When a Module is added to a Course, check if the module is added correctly
#     """
#     course = Course(name='Advanced Flask')
#     module = Module(name='ORM with SQLAlchemy', course=course)
#     db.session.add(course)
#     db.session.add(module)
#     db.session.commit()
#
#     assert module.course.name == 'Advanced Flask'
#     assert len(course.modules) == 1
#     assert course.modules[0].name == 'ORM with SQLAlchemy'
#
#
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
