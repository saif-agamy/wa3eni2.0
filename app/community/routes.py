from flask import Blueprint, render_template, redirect, url_for,request
from app.extensions import db
from app.forms import PostForm, ExamForm, QuestionForm
from app.models import Post,Lost,User, Exam,Question, Exam_Enrollments, Question_Enrollments
from datetime import datetime
from flask import jsonify
from flask_login import current_user, login_required
from sqlalchemy import func

community_b = Blueprint(
    "community",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/community/static"
)

@community_b.route("/community/")
@login_required
def blog():
    posts = Post.query.all()
    users_posts = {}
    for post in posts:
        users_posts[User.query.get(post.author_id)] = post

    return render_template('blog.html', users_posts=users_posts)

@community_b.route("/community/post/<int:id>/")
@login_required
def post(id):
    post = Post.query.get_or_404(id)
    user = User.query.get(post.author_id)
    return render_template('post.html', post=post, user=user)


@community_b.route("/community/share/<int:id>/", methods=['GET','POST'])
@login_required
def share(id):
    if current_user.verified :
        form = PostForm()
        if form.validate_on_submit():
            post = Post(
                author_id=id,
                title=form.title.data,
                content=form.content.data,
                flag=form.flag.data,
            )

            db.session.add(post)
            db.session.commit()

            return redirect(url_for('community.blog'))

        return render_template('create_post.html', form=form)
    else :
        return redirect(url_for('community.blog'))


@community_b.route("/community/post/<int:id>/like/", methods=['GET','POST'])
@login_required
def Like(id):
    pass
    

@community_b.route("/community/post/<int:id>/comment/", methods=['GET','POST'])
@login_required
def comment(id):
    pass


@community_b.route('/community/lost/')
@login_required
def lost():
    losts = Lost.query.filter_by(status='lost').all()
    founds = Lost.query.filter_by(status='found').all()

    return render_template('lost.html', losts=losts, founds=founds)


@community_b.route('/community/lost/add/<int:id>/', methods=['GET','POST'])
@login_required
def add(id):
    if request.method == 'POST':
        # Assuming you are using Flask
        date_str = request.form.get('date') # This is the string "2026-01-25"

        # Convert string to Python date object
        date_object = datetime.strptime(date_str, '%Y-%m-%d').date()

        item = Lost(
            author_id=id,
            name=request.form.get('name'),
            type=request.form.get('type'),
            date=date_object,
            place=request.form.get('place'),
            discription=request.form.get('description'),
            status=request.form.get('reportType')
        )

        db.session.add(item)
        db.session.commit()
        return redirect(url_for('community.lost'))

    return render_template('add_item.html')


@community_b.route('/community/delete/<int:id>/', methods=['GET','POST'])
@login_required
def delete(id):
    user = current_user
    post = Post.query.get_or_404(id)

    if user.id == post.author_id or current_user.is_admin:
        db.session.delete(post)
        db.session.commit()

        if current_user.is_admin :
            return redirect(url_for('admin.admin'))
        
        return redirect(url_for('community.blog'))
    
    else :
        return redirect(url_for('home.home'))


@community_b.route('/community/lost/delete//<int:id>/', methods=['GET','POST'])
@login_required
def delete_item(id):
    if current_user.is_admin:
        lost = Lost.query.get(id)

        db.session.delete(lost)
        db.session.commit()

        return redirect(url_for('admin.admin'))
    
    else :
        return redirect(url_for('home.home'))


@community_b.route('/community/ramadan/')
@login_required
def ramadan_comp():
    solved = request.args.get('solved')
    no_exam = request.args.get('no_exam')

    return render_template('ramadan_comp.html', solved=solved, no_exam=no_exam)


@community_b.route('/community/ramadan/exam', methods=['GET','POST'])
@login_required
def exam():
    the_exam = Exam.query.filter_by(active=True).first()
    
    # 1. If no active exam, bounce them back home
    if not the_exam:
        return redirect(url_for('community.ramadan_comp', no_exam=True))

    # 2. Check if the user has ANY record for this exam (even a blank one)
    exam_link = Exam_Enrollments.query.filter_by(user_id=current_user.id, exam_id=the_exam.id).first()

    # ==========================================
    # HANDLE GET (Opening the exam page)
    # ==========================================
    if request.method == 'GET':
        if exam_link:
            # They already loaded this page once before! Lock them out.
            return redirect(url_for('community.ramadan_comp', solved=True))
        
        # This is their first time opening the page.
        # Create a "blank" record immediately to lock them in.
        new_link = Exam_Enrollments(
            user_id=current_user.id,
            exam_id=the_exam.id,
            time=0,    # Default before they submit
            score=0    # Default before they submit
        )
        db.session.add(new_link)
        db.session.commit()
        
        return render_template('exam.html', questions=the_exam.questions)

    # ==========================================
    # HANDLE POST (Submitting the exam)
    # ==========================================
    if request.method == 'POST':
        if not exam_link:
            # Safety check: they somehow posted without loading the page first
            return redirect(url_for('home.home'))

        questions = the_exam.questions
        score = 0

        # Grade the questions
        for question in questions:
            user_choic = request.form.get(f'question_{question.id}')
            
            if user_choic:
                user_value = getattr(question, user_choic)
                
                if user_value == question.correct:
                    score += 1
                    solved_status = 'yes'
                else:
                    solved_status = 'no'
                    
                Q_link = Question_Enrollments(
                    user_id=current_user.id,
                    question_id=question.id,
                    solved=solved_status
                )
                db.session.add(Q_link)

        # 3. UPDATE the existing blank record we created during the GET request
        exam_link.score = score
        exam_link.time = request.form.get('time_spent')
        db.session.commit()
        
        # Redirect after successful submission
        return redirect(url_for('community.ramadan_comp', solved=True))


@community_b.route('/community/ramadan/add', methods=['GET','POST'])
@login_required
def add_exam():
    if current_user.is_admin :
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
    else :
        return redirect(url_for('admin.admin'))


@community_b.route('/community/ramadan/<int:id>/addquestion', methods=['GET','POST'])
@login_required
def add_question(id):
    if current_user.is_admin :
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
    else :
        return redirect(url_for('admin.admin'))
    


@community_b.route('/community/ramadan/<int:id>/delete', methods=['GET','POST'])
@login_required
def delete_exam(id):
    if current_user.is_admin :
        the_exam = Exam.query.get(id)
        if the_exam :
            db.session.delete(the_exam)
            db.session.commit()

        return redirect(url_for('admin.admin'))
    else :
            return redirect(url_for('admin.admin'))


@community_b.route('/community/ramadan/<int:id>/active', methods=['GET','POST'])
@login_required
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
    
@community_b.route('/community/ramadan/leaderboard')
@login_required
def leader_board():

    # We query the User's name, the sum of their scores, and the sum of their times.
    top_students = db.session.query(
        User.username,
        func.sum(Exam_Enrollments.score).label('total_score'),
        func.sum(Exam_Enrollments.time).label('total_time')
    ).join(
        Exam_Enrollments, User.id == Exam_Enrollments.user_id
    ).group_by(
        User.id
    ).order_by(
        func.sum(Exam_Enrollments.score).desc(), 
        func.sum(Exam_Enrollments.time).asc()
    ).limit(10).all()

    return render_template('leader_board.html', students=top_students)