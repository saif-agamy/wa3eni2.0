from flask import Blueprint, render_template, redirect, url_for
from app.forms import UserForm, LoginForm
from app.models import User
from app.extensions import db
from flask_login import login_user, logout_user

auth_b = Blueprint(
    'auth',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/auth/static'
)

@auth_b.route('/auth/sign/', methods=['GET','POST'])
def sign():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            role=form.role.data,
            from_school=form.from_school.data,
            grade=form.grade.data,
            icon = 'student.png'
        )

        
        if form.role.data == 'ولي أمر':
            user.icon = 'parent.png'
        else :
            user.icon = 'student.png'

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('sign.html', form=form)

@auth_b.route('/auth/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(form.password.data):
            login_user(user,True)

            return redirect(url_for('home.home'))

    return render_template('login.html', form=form)

@auth_b.route('/auth/logout/')
def logout():
    logout_user()
    return redirect(url_for('home.home'))

@auth_b.route('/auth/profile/<int:id>/')
def profile(id):
    user = User.query.get_or_404(id)
    return render_template('profile.html', user=user)