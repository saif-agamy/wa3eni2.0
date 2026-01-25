from flask import Blueprint, render_template

home_b = Blueprint(
    'home',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/home/static'
)

@home_b.route('/')
def home():
    return render_template('home.html')