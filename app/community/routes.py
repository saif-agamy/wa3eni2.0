from flask import Blueprint, render_template, redirect, url_for,request
from app.extensions import db
from app.forms import PostForm
from app.models import Post,Lost,User
from datetime import datetime
from flask import jsonify
from flask_login import current_user, login_required

community_b = Blueprint(
    "community",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/community/static"
)

@login_required
@community_b.route("/community/")
def blog():
    posts = Post.query.all()
    users_posts = {}
    for post in posts:
        users_posts[User.query.get(post.author_id)] = post

    return render_template('blog.html', users_posts=users_posts)

@login_required
@community_b.route("/community/post/<int:id>/")
def post(id):
    post = Post.query.get_or_404(id)
    user = User.query.get(post.author_id)
    return render_template('post.html', post=post, user=user)

@login_required
@community_b.route("/community/share/<int:id>/", methods=['GET','POST'])
def share(id):
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

@login_required
@community_b.route("/community/post/<int:id>/like/", methods=['GET','POST'])
def Like(id):
    post = Post.query.get_or_404(id)
    
@login_required
@community_b.route("/community/post/<int:id>/comment/", methods=['GET','POST'])
def comment(id):
    pass

@login_required
@community_b.route('/community/lost/')
def lost():
    losts = Lost.query.filter_by(status='lost').all()
    founds = Lost.query.filter_by(status='found').all()

    return render_template('lost.html', losts=losts, founds=founds)

@login_required
@community_b.route('/community/lost/add/<int:id>/', methods=['GET','POST'])
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

@login_required
@community_b.route('/community/delete/<int:id>/', methods=['GET','POST'])
def delete(id):
    user = current_user
    post = Post.query.get_or_404(id)

    if user.id == post.author_id or current_user.is_admin:
        db.session.delete(post)
        db.session.commit()

        return redirect(url_for('community.blog'))
    
    else :
        return redirect(url_for('home.home'))

@login_required
@community_b.route('/community/lost/delete//<int:id>/', methods=['GET','POST'])
def delete_item(id):
    if current_user.is_admin:
        lost = Lost.query.get(id)

        db.session.delete(lost)
        db.session.commit()

        return redirect(url_for('admin.admin'))
    
    else :
        return redirect(url_for('home.home'))