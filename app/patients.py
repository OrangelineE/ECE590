from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from .models.patient import Patient  # Assuming you have a Patient model

from flask import Blueprint
bp = Blueprint('patients', __name__)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Name', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if Patient.email_exists(email.data):
            raise ValidationError('Already a patient with this email.')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        patient = Patient.authenticate(form.email.data, form.password.data)
        if patient is None:
            flash('Invalid email or password')
            return redirect(url_for('patients.login'))
        login_user(patient)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.dashboard')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if Patient.register(
            email=form.email.data,
            password=form.password.data,
            name=form.name.data,
            age=form.age.data
        ):
            flash('Congratulations, you are now a registered patient!')
            return redirect(url_for('patients.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))
