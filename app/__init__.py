from flask import Flask
from os import path
from app.extensions import db
from app.models import Post, User, Exam, Question
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy import text
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '7673267953625642985783265'

    BASE_DIR = path.abspath(path.dirname(__file__))

    from app.home.routes import home_b
    from app.school.routes import school_b
    from app.community.routes import community_b
    from app.auth.routes import auth_b
    from app.chat_bot.routes import chat_bot_b
    from app.admin.routes import admin_b
    
    app.register_blueprint(home_b)
    app.register_blueprint(school_b)
    app.register_blueprint(community_b)
    app.register_blueprint(auth_b)
    app.register_blueprint(chat_bot_b)
    app.register_blueprint(admin_b)

    #SQL server handling
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(BASE_DIR,'db','site.db')}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    #edit the sql 
    with app.app_context():
        # db.create_all()

        # This SQL command forces the database to drop the stuck table
        try:
            db.session.execute(text("DROP TABLE _alembic_tmp_exam"))
            db.session.commit()
            print("✅ Success! Temporary table dropped.")
        except Exception as e:
            print(f"⚠️ Error (maybe it's already gone?): {e}")

    #setup migrations
    migrate = Migrate(app,db)
    migrate.init_app(app,db)

    #initialize user auth sys
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
     

    return app

@login_manager.user_loader
def load_user(user_id):
    # This function tells Flask-Login how to find a user by their ID
    # user_id is passed as a string, so we convert it to int for SQLAlchemy
    return User.query.get(int(user_id))