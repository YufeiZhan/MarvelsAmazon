from flask import render_template, redirect, url_for, flash, request, jsonify
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from ..models.user import User

from flask import Blueprint
bp = Blueprint('users', __name__)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

@bp.route('/account')
@login_required # Requires a user to be logged in to access this page otherwise redirect to defined login page automatically
def account():
    user_info = User.get(current_user.id)
    return render_template('account.html', title='Account Detail', user_info=user_info, role=User.getRole(current_user.id))

@bp.route('/topup/<id>')
def topup(id):
    if User.topup(id):
        flash('Congratulations. You have increased your account balance by $100.')
    return redirect(url_for('users.account'))


@bp.route('/withdraws/<id>/<amount>', methods=['GET', 'POST'])
def withdraws(id, amount):
    withdrawAmount = float(amount)
    if withdrawAmount < 0:
        flash(f'Cannot withdraw an amount of {amount} smaller than 0!')
        return redirect(url_for('users.account'))
    else:
        if User.get_balance(id) < withdrawAmount:
            flash(f'Insufficient balance. Cannot withdraw the specified amount of ${withdrawAmount}!')
            return redirect(url_for('users.account'))
        elif User.withdraw(id, withdrawAmount):
            flash(f'You successfully withdrew an amount of {withdrawAmount}. Your new balance is {User.get_balance(id)}')
            return redirect(url_for('users.account'))

@bp.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    if current_user.is_authenticated:
        form = UpdateForm()
        if form.validate_on_submit():
            if User.update_user_info(id, form.email.data, form.password.data, form.firstname.data, form.lastname.data):
                flash('Congratulations. You have updated your user information.')
                return redirect(url_for('users.account'))
        return render_template('update.html', title='Account Info Update', form=form, role=User.getRole(current_user.id))
    # Restrict user/request from accessing this page w/o login
    else:
        flash('Restricted access ONLY. Please sign in or register first.')
        return redirect(url_for('users.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')

class UpdateForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/updateRole/<int:role>')
@login_required # Requires a user to be logged in to access this page otherwise redirect to defined login page automatically
def updateRole(role):
    User.update_user_role(current_user.id, role)
    return jsonify({'message': 'Role updated successfully'})  # Example response


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))