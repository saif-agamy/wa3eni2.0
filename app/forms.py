from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

class PostForm(FlaskForm):
    title = StringField('title', 
    render_kw={
        "class": "form-control border-0 fs-4 fw-bold mb-2", 
        "placeholder": "Post Title..."
    },
    validators=[DataRequired('required field'), Length(5, 200, 'title should be 5 to 200 letter')]
    ) 
    
    # Change this to TextAreaField
    content = TextAreaField('Content',
     render_kw={
        "class": "form-control border-0 mb-3", 
        "placeholder": "What's on your mind?",
        "rows": "5",      # This sets the initial height
        "style": "resize: none;" # Optional: prevents user from stretching the box manually
    }, 
    validators=[DataRequired('required field'), Length(5, 5000, 'content should be more than 5 letters')]
    )
    
    flag = SelectField('post type', 
    render_kw={
        "class": "form-select border-0 bg-light py-2"
    },
    choices=[('question', 'QA'),('research', 'Research'),('news','News'),('warning','Warning')],validators=[DataRequired('required field')]
    )

class UserForm(FlaskForm):
    username = StringField('Username',
    render_kw={
        'class' : 'form-control form-control-lg',
        'type' : 'text',
        'placeholder' : 'أسمك هنا'
    },
    validators=[DataRequired('required field'), Length(3,80,'email must be 3 to 80 letter')]
    )

    email = EmailField('Email',
    render_kw={
        'class' : 'form-control form-control-lg',
        'type' : 'email',
        'placeholder' : 'البريد الألكتروني'
    },
    validators=[DataRequired('required field'), Length(5,200,'email must be 5 to 200 letter')]
    )

    password = PasswordField('Password',
    render_kw={
        'class' : 'form-control form-control-lg',
        'type' : 'password',
        'placeholder' : 'رمز المرور'
    },
    validators=[DataRequired('required field'), Length(5,128,'email must be 5 to 128 letter')]
    )

    confirm_password = PasswordField('Confirm Password',
    render_kw={
        'class' : 'form-control form-control-lg',
        'type' : 'password',
        'placeholder' : 'تأكيد رمز المرور'
    },
    validators=[DataRequired('required field'), Length(5,128,'email must be 5 to 128 letter'), EqualTo('password', "this password don't match the other password")]
    )

    role = SelectField('role', 
        choices=[('المدير','المدير'),('أخصائي','أخصائي'),('معلم','معلم'),('طالب عسكرية','طالب عسكرية'),('مقرر لجنة','مقرر لجنة'),('أمين','أمين'),('أمين مساعد','أمين مساعد'),("قائد عسكري","قائد عسكري"),("مدرب","مدرب"),("ولي أمر","ولي امر"),("طالب","طالب")],
        validators=[DataRequired('required field')]
        )
    
    grade = SelectField('grade', 
        choices=[('الأول الثانوي','الأول الثانوي'),('الثاني الثانوي','الثاني الثانوي'),('الثالث الثانوي','الثالث الثانوي'),('أعدادي','اعدادي'),('أبتدائي','أبتدائي'),('طالب جامعي','طالب جامعي'),('خريج','خريج')],
        validators=[DataRequired('required field')]
        )
    
    from_school = BooleanField('from school', validators=[DataRequired('required field')])

class LoginForm(FlaskForm):
    email = EmailField('Email',
    render_kw={
        'class' : 'form-control form-control-lg',
        'type' : 'email',
        'placeholder' : 'البريد الألكتروني'
    },
    validators=[DataRequired('required field'), Length(5,200,'email must be 5 to 200 letter')]
    )

    password = PasswordField('Password',
    render_kw={
        'class' : 'form-control form-control-lg',
        'type' : 'password',
        'placeholder' : 'رمز المرور'
    },
    validators=[DataRequired('required field'), Length(5,128,'email must be 5 to 128 letter')]
    )

class ExamForm(FlaskForm):
    day = SelectField('يوم المسابقة في رمضان', choices=[('d1','اليوم الأول'),('d2','اليوم الثاني'),('d3','اليوم الثالث'),('d4','اليوم الرابع'),('d5','اليوم الخامس'),('d6','اليوم السادس'),('d7','اليوم السابع'),('d8','اليوم الثامن'),('d9','اليوم التاسع'),('d10','اليوم العاشر'),('d11','اليوم الحادي عشر'),('d12','اليوم الثاني عشر'),('d13','اليوم الثالث عشر'),('d14','اليوم الرابع عشر'),('d15','اليوم الخامس عشر'),('d16','اليوم السادس عشر'),('d17','اليوم السابع عشر'),('d18','اليوم الثامن عشر'),('d19','اليوم التاسع عشر'),('d120','اليوم العشرون'),('d21','اليوم الحادي و العشرون'),('d22','اليوم الثاني و العشرون'),('d23','اليوم الثالث و العشرون'),('d24','اليوم الرابع و العشرون'),('d25','اليوم الخامس و العشرون'),('d26','اليوم السادس و العشرون'),('d27','اليوم السابع و العشرون'),('d28','اليوم الثامن و العشرون'),('d29','اليوم التاسع و العشرون'),('d30','اليوم الثلاثون')], validators=[DataRequired()])
    category = SelectField('تصنيف السؤال', choices=[('Q','القرأن كريم'),('R','رسول الله (ص)'),('F','الفتوحات و مغازي'),('Sh','الصحابة'),('S','الصلاة')], validators=[DataRequired()])

class QuestionForm(FlaskForm):
    question = TextAreaField('السؤال', validators=[DataRequired(), Length(max=256)])
    answer1 = StringField('الأجابة الأولى', validators=[DataRequired(), Length(max=128)])
    answer2 = StringField('الأجابة الثانية', validators=[DataRequired(), Length(max=128)])
    answer3 = StringField('الأجابة الثالثة', validators=[DataRequired(), Length(max=128)])
    answer4 = StringField('الأجابة الرابعة', validators=[DataRequired(), Length(max=128)])
    correct = StringField('الأجابة الصحيحة', validators=[DataRequired(), Length(max=128)])