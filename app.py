from flask import Flask,render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///sms.db"
app.config['SQLALCHEMY_BINDS']= {
    'tms':"sqlite:///tms.db",
    'cms':"sqlite:///cms.db"
    }
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Sms(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    student=db.Column(db.String(200),nullable=False)
    father=db.Column(db.String(500),nullable=False)
    mother=db.Column(db.String(500),nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.student}"
     
class Tms(db.Model):
    __bind_key__ = 'tms'
    sno=db.Column(db.Integer,primary_key=True)
    teacher=db.Column(db.String(200),nullable=False)
    subject=db.Column(db.String(500),nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.teacher}"

class Cms(db.Model):
    __bind_key__ = 'cms'
    sno=db.Column(db.Integer,primary_key=True)
    course=db.Column(db.String(200),nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.course}"


@app.route('/student', methods=['GET','POST'])
def student():
    if request.method=='POST':
        student = request.form['student']
        father = request.form['father']
        mother= request.form['mother']
        sms = Sms(student= student, father= father, mother=mother)
        db.session.add(sms)
        db.session.commit()
    allSms=Sms.query.all()
    print(allSms)
    return render_template('student.html', allSms=allSms)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/teacher', methods=['GET','POST'])
def teacher():
    if request.method=='POST':
        teacher = request.form['teacher']
        subject = request.form['subject']
        tms = Tms(teacher= teacher,subject=subject)
        db.session.add(tms)
        db.session.commit()
    allTms=Tms.query.all()
    print(allTms)
    return render_template('teacher.html', allTms=allTms)

@app.route('/course',methods=['GET','POST'])
def course():
    if request.method=='POST':
        course = request.form['course']
        cms = Cms(course= course)
        db.session.add(cms)
        db.session.commit()
    allCms=Cms.query.all()
    print(allCms)
    return render_template('course.html',allCms=allCms)

@app.route('/show')
def show():
    allSms=Sms.query.all()
    print(allSms)
    return 'show'
    
@app.route('/delete/<int:sno>')
def delete(sno):
    sms= Sms.query.filter_by(sno=sno).first()
    db.session.delete(sms)
    db.session.commit()
    return redirect('/student')

@app.route('/remove/<int:sno>')
def remove(sno):
    tms= Tms.query.filter_by(sno=sno).first()
    db.session.delete(tms)
    db.session.commit()
    return redirect('/teacher')

@app.route('/cut/<int:sno>')
def cut(sno):
    cms= Cms.query.filter_by(sno=sno).first()
    db.session.delete(cms)
    db.session.commit()
    return redirect('/course')

if __name__== "__main__":
    app.run(debug=True )