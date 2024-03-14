from flask import render_template, url_for, redirect, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from . import create_app, db
from .form import RegisterForm, LoginForm, AddTaskForm, DeleteTaskForm
from .models import Task, User

app = create_app()


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks_page():
    print('tasks_page: Current user:', current_user)
    return render_template('tasks2.html')
    print(type(tasks))
    delete_task_form = DeleteTaskForm()
    add_task_form = AddTaskForm()
    print("add_task_form:", add_task_form.task_name.data)

    if request.method == "POST":
        print("POST request received!")
        form_name = request.form.get('form_name', '')
        print(f'Form name: {form_name}')
        if form_name == 'delete_task_form' and delete_task_form.validate_on_submit():
            deleted_task = request.form.get('deleted_task')
            d_task_object = Task.query.filter_by(id=int(deleted_task)).first()
            if d_task_object:
                db.session.delete(d_task_object)
                db.session.commit()
                flash('Task deleted successfully!', 'success')

        if form_name == 'add_task_form' and add_task_form.validate_on_submit():
            new_task = Task(task_name=add_task_form.task_name.data,
                            task_description=add_task_form.task_description.data,
                            owner=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('New task added!', 'success')

        return redirect(url_for('tasks_page'))

    if request.method == "GET":
        return render_template('tasks.html', tasks=tasks, delete_task_form=delete_task_form,
                               add_task_form=add_task_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are now logged in as: {user_to_create.username}', category='success')
        return redirect(url_for('tasks_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():

        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('tasks_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))


@app.route('/getAllTasks', methods=['GET'])
@login_required
def get_all_tasks():
    print('get_all_tasks: Current user :', current_user)
    tasks = Task.query.filter_by(owner=current_user.id).all()  # Ensure this is a list, even if empty
    tasks_list = [task.to_dict() for task in tasks]
    print('get_all_tasks: tasks_list:', tasks_list)
    return jsonify(tasks_list)


@app.route('/delete_task/<task_id>', methods=['POST', 'DELETE'])
@login_required
def delete_task(task_id):
    print('delete_task: Current user:', current_user)
    task = Task.query.filter_by(id=task_id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        return True
    return False
