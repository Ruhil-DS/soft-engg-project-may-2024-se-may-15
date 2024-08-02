from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'), primary_key=True)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.String(8), primary_key=True)
    course_name = db.Column(db.String(100), unique=True, nullable=False)
    course_description = db.Column(db.String(), nullable=False)
    modules = db.relationship('Module', backref='course', lazy=True)

class Module(db.Model):
    __tablename__ = 'module'
    module_id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String(100), unique=True, nullable=False)
    module_description = db.Column(db.String(), nullable=False)
    course_id = db.Column(db.String(8), db.ForeignKey('course.course_id'), nullable=False)
    lessons = db.relationship('Lesson', backref='module', lazy=True)
    # pas = db.relationship('PA', backref='module', lazy=True)
    # gas = db.relationship('GA', backref='module', lazy=True)
    # prpas = db.relationship('PrPA', backref='module', lazy=True)
    # grpas = db.relationship('GrPA', backref='module', lazy=True)

class Lesson(db.Model):
    __tablename__ = 'lesson'
    lesson_id = db.Column(db.Integer, primary_key=True)
    lesson_name = db.Column(db.String(100), unique=True, nullable=False)
    lesson_description = db.Column(db.String(), nullable=False)
    module_id = db.Column(db.String(8), db.ForeignKey('module.module_id'), nullable=False)
    video_url = db.Column(db.String(), nullable=False)
    slide_url = db.Column(db.String(), nullable=False)