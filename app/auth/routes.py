from flask import Blueprint, render_template, redirect, url_for
from app.forms import UserForm, LoginForm
from app.models import User
from app.extensions import db
from flask_login import login_user, logout_user, login_required, current_user

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
    error_message=None
    if form.validate_on_submit():
        email_user = User.query.filter_by(email=form.email.data).first()
        username_user = User.query.filter_by(username=form.username.data).first()
        if email_user :
            error_message = 'there is an acount with this email'
        elif username_user :
            error_message = 'there is an account with this username'
        else :
            user = User(
                email=form.email.data,
                username=form.username.data,
                role=form.role.data,
                from_school=form.from_school.data,
                grade=form.grade.data,
            )

            if form.role.data == 'المدير':
                user.icon = 'head-teacher.png'
            elif form.role.data == 'قائد عسكري':
                user.icon = 'army-leader.png'
            elif form.role.data == 'طالب عسكرية':
                user.icon = 'army-student.png'
            elif form.role.data == 'أخصائي':
                user.icon = 'specialist.png'
            elif form.role.data == 'أمين':
                user.icon = 'trustee.png'
            elif form.role.data == 'أمين مساعد':
                user.icon = 'helper-trustee.png'
            elif form.role.data == 'مقرر لجنة':
                user.icon = 'reporteur.png'
            elif form.role.data == 'مدرب':
                user.icon = 'trainer.png'
            elif form.role.data == 'معلم':
                user.icon = 'teacher.png'
            elif form.role.data == 'ولي أمر': 
                user.icon = 'parent.png'
            else :
                user.icon = 'student.png'

            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()

            return redirect(url_for('auth.login'))

    return render_template('sign.html', error_message=error_message, form=form)

@auth_b.route('/auth/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    error_message = None
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(form.password.data):
            login_user(user,True)

            return redirect(url_for('home.home'))
        else :
            error_message = 'Email or Password is wrong try again!'

    return render_template('login.html',error_message=error_message, form=form)


@auth_b.route('/auth/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.home'))

@auth_b.route('/auth/profile/<int:id>/')
@login_required
def profile(id):
    user = User.query.get_or_404(id)
    return render_template('profile.html', user=user)

@auth_b.route('/auth/user/<int:id>/set_admin/')
@login_required
def set_admin(id):
    if current_user.is_admin :
        if not current_user.id == id :
            user = User.query.get_or_404(id)
            user.set_admin()
            db.session.commit()

        return redirect(url_for('admin.admin'))
    
    else : return redirect(url_for('home.home'))

@auth_b.route('/auth/user/<int:id>/verify/')
@login_required
def verify(id):
    if current_user.is_admin :
        user = User.query.get_or_404(id)
        user.verify()
        db.session.commit()

        return redirect(url_for('admin.admin'))
    
    else : return redirect(url_for('home.home'))