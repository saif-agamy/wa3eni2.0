from flask import Blueprint, render_template, redirect, url_for
from app.models import User, Post, Lost
from flask_login import login_required, current_user

admin_b = Blueprint(
    'admin',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/admin/static/'
)

@login_required
@admin_b.route('/admin/')
def admin():
    if current_user.is_admin:
        users = User.query.all()
        users_num = User.query.count()
        posts = Post.query.all()
        posts_num = Post.query.count()
        losts =Lost.query.all()
        lost_num =Lost.query.count()
        return render_template('admin.html', 
            total_users=users_num, 
            users=users,
            total_posts=posts_num,
            posts=posts,
            total_losts=lost_num,
            losts=losts,
            )
    else :
        return redirect(url_for('home.home'))