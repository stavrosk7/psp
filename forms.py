from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired

class EmployeeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    salary_per_hour = FloatField('Salary per Hour', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TaskForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    predecessor_tasks = StringField('Predecessor Tasks')  # New field
    submit = SubmitField('Submit')
