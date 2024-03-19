from flask import Flask

from app.extensions import db
from app.models import Task

app = Flask(__name__)
dir = r"C:\Users\yfess\PycharmProjects\dat_255_gruppe_projekt\app\task.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dir
db.init_app(app)

with app.app_context():
    try:
        test_task = Task(task_name='clean the dishes', task_description="if i don't clean the dishes, i will be in "
                                                                        "trouble.", owner=2)
        db.session.add(test_task)
        db.session.commit()

        test_task2 = Task(task_name='Read Fastai fast', task_description="i should read fastai very fast", owner=2)
        db.session.add(test_task2)
        db.session.commit()

        test_task2 = Task(task_name='lorem ipsum short', task_description="Lorem ipsum dolor sit amet, consectetur "
                                                                          "adipiscing elit, sed do eiusmod tempor "
                                                                          "incididunt ut labore et dolore magna "
                                                                          "aliqua. Ut enim ad minim veniam, "
                                                                          "quis nostrud exercitation ullamco "
                                                                          "laboris nisi ut aliquip ex ea commodo"
                                                                          " consequat. Duis aute irure dolor in "
                                                                          "reprehenderit in voluptate velit esse "
                                                                          "cillum dolore eu fugiat nulla pariatur. "
                                                                          "Excepteur sint occaecat cupidatat non "
                                                                          "proident, sunt in culpa qui officia "
                                                                          "deserunt mollit anim id est laborum.",
                          owner=2)
        db.session.add(test_task2)
        db.session.commit()
    except:
        db.session.rollback()
        print('An item with this ID already exists.')
