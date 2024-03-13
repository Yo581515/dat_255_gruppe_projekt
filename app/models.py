from .extensions import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    tasks = db.relationship('Task', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def __repr__(self):
        return f'User {self.username}'


class Task(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    task_name = db.Column(db.String(length=30), nullable=False, unique=False)
    task_description = db.Column(db.String(length=1024), nullable=False, unique=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Task {self.task_name}'

    def to_dict(self):
        """Convert the Task object into a serializable dictionary."""
        return {
            "id": self.id,
            "name": self.task_name,
            "description": self.task_description,
            # add other fields as necessary
        }
