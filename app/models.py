from app.extensions import db
from datetime import datetime
from sqlalchemy import JSON
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

exam_category_linker = {
    'Q' : 'قرأن كريم',
    'R':'رسول الله (ص)',
    'F':'الفتوحات و مغازي',
    'Sh':'الصحابة',
    'S':'الصلاة',
}

exam_day_linker = {
    'd1':'اليوم الأول',
    'd2':'اليوم الثاني',
    'd3':'اليوم الثالث',
    'd4':'اليوم الرابع',
    'd5':'اليوم الخامس',
    'd6':'اليوم السادس',
    'd7':'اليوم السابع',
    'd8':'اليوم الثامن',
    'd9':'اليوم التاسع',
    'd10':'اليوم العاشر',
    'd11':'اليوم الحادي عشر',
    'd12':'اليوم الثاني عشر',
    'd13':'اليوم الثالث عشر',
    'd14':'اليوم الرابع عشر',
    'd15':'اليوم الخامس عشر',
    'd16':'اليوم السادس عشر',
    'd17':'اليوم السابع عشر',
    'd18':'اليوم الثامن عشر',
    'd19':'اليوم التاسع عشر',
    'd120':'اليوم العشرون',
    'd21':'اليوم الحادي و العشرون',
    'd22':'اليوم الثاني و العشرون',
    'd23':'اليوم الثالث و العشرون',
    'd24':'اليوم الرابع و العشرون',
    'd25':'اليوم الخامس و العشرون',
    'd26':'اليوم السادس و العشرون',
    'd27':'اليوم السابع و العشرون',
    'd28':'اليوم الثامن و العشرون',
    'd29':'اليوم التاسع و العشرون',
    'd30':'اليوم الثلاثون',
}  

class User(db.Model, UserMixin):
    #fields attributes
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password_hashed = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    from_school = db.Column(db.Boolean(), nullable=False)
    icon = db.Column(db.String(5000),nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    verified = db.Column(db.Boolean(), nullable=False, default=False)
    skill = db.Column(db.String(80), nullable=False, default='None')
    # You must add this manually!
    is_admin = db.Column(db.Boolean, default=False)

    #handling methods
    def set_password(self, password):
        self.password_hashed = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hashed, password)
    
    def verify(self):
        if self.verified :
            self.verified = False
        else :
            self.verified = True 

    def set_admin(self):
        if self.is_admin :
            self.is_admin = False
        else :
            self.is_admin = True

    def ban(self):
        if self.is_active:
            self.is_active = False
        else :
            self.is_active = True

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    flag = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    update_date = db.Column(db.DateTime, default=datetime.utcnow)
    #----------------
    likes = db.Column(JSON, nullable=True, default=list)
    Comments = db.Column(JSON, nullable=True, default=list)

class Lost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    discription = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    place = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(30), nullable=False)

class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(3), nullable=False, unique=True)
    category = db.Column(db.String(128), nullable=False)
    questions = db.relationship('Question', backref='exam', lazy=True)
    active = db.Column(db.Boolean, default=True)

    def get_display_category(self):
        return exam_category_linker[self.category]
    
    def get_display_day(self):
        return exam_day_linker[self.day]

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'))
    question = db.Column(db.String(256), nullable=False)
    answer1 = db.Column(db.String(128), nullable=False)
    answer2 = db.Column(db.String(128), nullable=False)
    answer3 = db.Column(db.String(128), nullable=False)
    answer4 = db.Column(db.String(128), nullable=False)
    correct = db.Column(db.String(128), nullable=False)

class Exam_Enrollments(db.Model):
    #foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), primary_key=True)

    #extra data
    time = db.Column(db.String(128), nullable=False)
    score = db.Column(db.Integer, nullable=False)

class Question_Enrollments(db.Model):
    #foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)

    #extra data
    solved = db.Column(db.String(128), default=False)