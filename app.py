from flask import Flask, render_template, request, redirect, url_for, send_file
from models import db, Employee, Task
from forms import EmployeeForm, TaskForm
import os
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from schedule.schedule import assign_tasks
from schedule.gantt import plot_gantt_chart

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# Employees CRUD routes
@app.route('/employees')
def show_employees():
    employees = Employee.query.all()
    return render_template('employees.html', employees=employees)

@app.route('/employee/new', methods=['GET', 'POST'])
def new_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        new_employee = Employee(
            name=form.name.data,
            position=form.position.data,
            salary_per_hour=form.salary_per_hour.data
        )
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('show_employees'))
    return render_template('employee_form.html', form=form)

@app.route('/employee/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=employee)
    if form.validate_on_submit():
        employee.name = form.name.data
        employee.position = form.position.data
        employee.salary_per_hour = form.salary_per_hour.data
        db.session.commit()
        return redirect(url_for('show_employees'))
    return render_template('employee_form.html', form=form)

@app.route('/employee/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('show_employees'))

# Tasks CRUD routes
@app.route('/tasks')
def show_tasks():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/task/new', methods=['GET', 'POST'])
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(
            name=form.name.data,
            position=form.position.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            predecessor_tasks=form.predecessor_tasks.data  # New field
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('show_tasks'))
    return render_template('task_form.html', form=form)

@app.route('/task/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get_or_404(id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.name = form.name.data
        task.position = form.position.data
        task.start_date = form.start_date.data
        task.end_date = form.end_date.data
        task.predecessor_tasks = form.predecessor_tasks.data  # New field
        db.session.commit()
        return redirect(url_for('show_tasks'))
    return render_template('task_form.html', form=form)

@app.route('/task/delete/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('show_tasks'))

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        employees = [(e.id, e.name, e.position, e.salary_per_hour) for e in Employee.query.all()]
        tasks = [(t.id, t.name, t.position, t.start_date.strftime('%Y-%m-%d'), t.end_date.strftime('%Y-%m-%d'), t.predecessor_tasks) for t in Task.query.all()]

        assignments, project_duration, total_cost = assign_tasks(employees, tasks)

        return render_template('schedule.html', assignments=assignments, project_duration=project_duration, total_cost=total_cost)

    return render_template('schedule_form.html')

@app.route('/gantt_chart')
def gantt_chart():
    try:
        employees = [(e.id, e.name, e.position, e.salary_per_hour) for e in Employee.query.all()]
        tasks = [(t.id, t.name, t.position, t.start_date.strftime('%Y-%m-%d'), t.end_date.strftime('%Y-%m-%d'), t.predecessor_tasks) for t in Task.query.all()]
        
        # Log the tasks and employees
        app.logger.info(f'Tasks: {tasks}')
        app.logger.info(f'Employees: {employees}')
        
        assignments, _, _ = assign_tasks(employees, tasks)
        
        # Log the assignments
        app.logger.info(f'Assignments: {assignments}')
        
        fig = plot_gantt_chart(tasks, assignments)
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        output.seek(0)  # Ensure the pointer is at the start of the stream
        return send_file(output, mimetype='image/png')
    except Exception as e:
        app.logger.error(f'Error generating Gantt chart: {e}')
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
    app.logger.setLevel(logging.DEBUG)
