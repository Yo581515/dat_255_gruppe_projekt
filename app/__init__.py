import os
from flask import Flask
from sqlalchemy.exc import IntegrityError
from .extensions import db, bcrypt, login_manager
from .models import Task, User
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    # CORS(app, supports_credentials=True)
    CORS(app)

    # Database configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'task.db')
    app.config['SECRET_KEY'] = '00ec9f02962c52e7e0a2ad71'
    # app.config['CORS_HEADERS'] = 'Content-Type'

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login_page'
    login_manager.login_message_category = 'info'

    with app.app_context():
        db.create_all()
        add_example_tasks()
        add_example_users()

        print('All tasks in the database:')
        print_all_tasks()

        print()

        print("All users in the database:")
        print_all_users()

        # Your database initialization code

    from . import routes  # Import routes after initializing db to avoid circular imports

    return app


def add_example_tasks():
    try:
        task1 = Task(id=1, task_name='study dat255', task_description='study DAT255 description')
        db.session.add(task1)
        db.session.commit()

        task2 = Task(id=2, task_name='study dat502', task_description='study ADA502 description')
        db.session.add(task2)
        db.session.commit()

    except IntegrityError:
        db.session.rollback()
        print('An item with this ID already exists.')


def add_example_users():
    try:
        user1 = User(id=1, username='user', email_address='user@email.com',
                     password_hash='123456')
        db.session.add(user1)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()  # Roll back the session in case of error for users
        print('A user with this ID already exists.')


def print_all_tasks():
    try:
        print(Task.query.filter(Task.id < 3).all())
    except IntegrityError:
        db.session.rollback()
        print('cant find the task with this id less than 3')


def print_all_users():
    try:
        print(User.query.filter(User.id < 3).all())
    except IntegrityError:
        db.session.rollback()
        print('cant find the task with this id less than 3')
