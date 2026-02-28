from flask import Blueprint, render_template, redirect, url_for
from app.models import User, Post, Lost, Exam, Question, db, Exam_Enrollments
from flask_login import login_required, current_user
from app.forms import ExamForm, QuestionForm
from functools import wraps

admin_b = Blueprint(
    'admin',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/admin/static/'
)

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_admin :
            return func(*args, **kwargs)
        else :
            return redirect(url_for('home.home'))
        
    return wrapper


@admin_b.route('/admin/')
@login_required
@admin_required
def admin():
    users = User.query.all()
    users_num = User.query.count()
    posts = Post.query.all()
    posts_num = Post.query.count()
    losts =Lost.query.all()
    lost_num =Lost.query.count()
    exams = Exam.query.all()
    exams_num = Exam.query.count()
    questions = Question.query.all()
    questions_num = Question.query.count()

    exams_participations = db.session.query(
        User.username, 
        Exam_Enrollments.exam_id,  # MUST include this!
        Exam_Enrollments.score, 
        Exam_Enrollments.time
    ).join(
        Exam_Enrollments, User.id == Exam_Enrollments.user_id
    ).limit(10).order_by(
        Exam_Enrollments.score.desc(),
        Exam_Enrollments.time.asc(),
    ).all()

    return render_template('admin.html', 
        total_users=users_num, 
        users=users,
        total_posts=posts_num,
        posts=posts,
        total_losts=lost_num,
        losts=losts,
        exams=exams,
        exams_num=exams_num,
        questions=questions,
        questions_num=questions_num,
        exams_participations=exams_participations,
        )
    
@admin_b.route('/admin/auth/user/<int:id>/set_admin/')
@login_required
@admin_required
def set_admin(id):
    if not current_user.id == id :
        user = User.query.get_or_404(id)
        user.set_admin()
        db.session.commit()

    return redirect(url_for('admin.admin'))

@admin_b.route('/admin/auth/user/<int:id>/verify/')
@login_required
@admin_required
def verify(id):
    user = User.query.get_or_404(id)
    user.verify()
    db.session.commit()

    return redirect(url_for('admin.admin'))

#editing users! 
@admin_b.route('/admin/auth/user/<int:id>/changepassword/')
@login_required
@admin_required
def change_password(id):
    pass
    
@admin_b.route('/admin/community/ramadan/add', methods=['GET','POST'])
@login_required
@admin_required
def add_exam():
    Exam_Form = ExamForm()

    if Exam_Form.validate_on_submit():
        Exams_same_day = Exam.query.filter_by(day=Exam_Form.day.data).first()
        if Exams_same_day is None :
            new_exam = Exam(
                day=Exam_Form.day.data,
                category=Exam_Form.category.data
            )

            db.session.add(new_exam)
            db.session.commit()

            return redirect(url_for('admin.admin'))

    return render_template('add_exam.html', exam_form=Exam_Form)
    
    
@admin_b.route('/admin/community/ramadan/<int:id>/addquestion', methods=['GET','POST'])
@login_required
@admin_required
def add_question(id):
    Question_Form = QuestionForm()

    if Question_Form.validate_on_submit():
        exam = Exam.query.get_or_404(id)
        if len(exam.questions) < 3:
            new_question = Question(
                exam_id=id,
                question=Question_Form.question.data,
                answer1=Question_Form.answer1.data,
                answer2=Question_Form.answer2.data,
                answer3=Question_Form.answer3.data,
                answer4=Question_Form.answer4.data,
                correct=Question_Form.correct.data
            )

            db.session.add(new_question)
            db.session.commit()

        return redirect(url_for('admin.admin'))

    return render_template('add_question.html', question_form=Question_Form)
    
@admin_b.route('/admin/community/ramadan/<int:id>/delete', methods=['GET','POST'])
@login_required
@admin_required
def delete_exam(id):
    the_exam = Exam.query.get(id)
    if the_exam :
        db.session.delete(the_exam)
        db.session.commit()

    return redirect(url_for('admin.admin'))


@admin_b.route('/admin/community/ramadan/<int:id>/active', methods=['GET','POST'])
@login_required
@admin_required
def active_exam(id):
    the_exam = Exam.query.get(id)

    if the_exam:
        # 1. If the selected exam is ALREADY active, just deactivate it.
        if the_exam.active:
            the_exam.active = False
        else:
            # 2. If we are activating a new exam, deactivate the old one FIRST (if it exists).
            activated_exam = Exam.query.filter_by(active=True).first()
            if activated_exam:
                activated_exam.active = False
            
            # 3. Now activate the target exam.
            the_exam.active = True

        db.session.commit()

        return redirect(url_for('admin.admin'))
    else :
        return redirect(url_for('admin.admin'))