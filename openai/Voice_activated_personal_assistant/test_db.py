from flask import Flask

from app.extensions import db
from app.models import Task

app = Flask(__name__)
dir = r"C:\Users\yfess\PycharmProjects\dat_255_gruppe_projekt\app\task.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dir
db.init_app(app)

with app.app_context():
    try:
        test_task = Task(task_name='testi', task_description='tasti description', owner=5)
        db.session.add(test_task)
        db.session.commit()
    except:
        db.session.rollback()
        print('An item with this ID already exists.')
