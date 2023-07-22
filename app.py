from io import BytesIO
import json
import string
from zipfile import ZipFile
import zipfile
from flask import Flask, after_this_request, jsonify, make_response, redirect, render_template, send_file, url_for,request, current_app
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc
from SVM import SVM
from ResumeParser import ResumeParser
import win32api
from flask_migrate import Migrate
import speech_recognition as sr
import moviepy.editor as mp
import aspose.words as aw
import pickle
from sqlalchemy import select,update,delete
from math import ceil
from flask import session
from flask_mail import Mail,Message
from glob import glob

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

app = Flask(__name__)
app.config['UPLOAD_DIRECTORY'] = 'uploads/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume.sqlite3'
app.config['SECRET_KEY'] = 'resume'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ALLOWED_EXTENSIONS'] = ['.pdf','.docx','.mp4','.doc']
app.config['ALLOWED_EXTENSIONS_CERTIFICATE'] = [".pdf",".jpeg",".jpg",".png"]
app.config['SESSION_COOKIE_DURATION'] = 10 #3600  # 1 hour

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True  
app.config['MAIL_USERNAME'] = 'jobsearchsystem666@gmail.com' 
app.config['MAIL_PASSWORD'] = 'lzhloitkawgdvrkj' #app password 
mail = Mail(app)

# app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024 #video purpose


db = SQLAlchemy(app)
migrate = Migrate(app,db)

model = SVM()
rp = ResumeParser()

class resume(db.Model):
    _id = db.Column("ID",db.Integer, primary_key = True)
    Filename = db.Column(db.String(100))
    Field = db.Column(db.String(50))
    Att_Active = db.Column(db.Integer)
    Att_Agreeableness = db.Column(db.Integer)
    Att_Cautiousness = db.Column(db.Integer)
    Att_Compliant = db.Column(db.Integer)
    Att_Confidence = db.Column(db.Integer)
    Att_Conscientiousness = db.Column(db.Integer)
    Att_Dominant = db.Column(db.Integer)
    Att_Emotionality = db.Column(db.Integer)
    Att_Extroversion = db.Column(db.Integer)
    Att_Hard_Working = db.Column(db.Integer)
    Att_Honest = db.Column(db.Integer)
    Att_Influecing = db.Column(db.Integer)
    Att_Innovative = db.Column(db.Integer)
    Att_Knowledge_sharing = db.Column(db.Integer)
    Att_Leadership = db.Column(db.Integer)
    Att_Neuroticism = db.Column(db.Integer)
    Att_Openness = db.Column(db.Integer)
    Att_Punctual = db.Column(db.Integer)
    Att_Responsible = db.Column(db.Integer)
    Att_Steady = db.Column(db.Integer)
    Att_Teamwork = db.Column(db.Integer)
    data = db.Column(db.BLOB)
    Email = db.Column(db.String(50))
    Phone = db.Column(db.String(50))
    Skills = db.Column(db.String(100))
    Education = db.Column(db.String(100))
    Education_Level = db.Column(db.String(50))
    CGPA = db.Column(db.String(10))
    Name = db.Column(db.String(50))
    Speech = db.Column(db.BLOB)
    Has_Certificate = db.Column(db.String(10))
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return str(self._id)+str(self.Filename)+str(self.Field)+str(self.Att_Agreeableness)

    def __init__(self,*args):
        if len(args) == 31:
            self.Filename = args[0]
            self.Field = args[1]
            self.Att_Active = args[2]
            self.Att_Agreeableness = args[3]
            self.Att_Cautiousness = args[4]
            self.Att_Compliant = args[5]
            self.Att_Confidence = args[6]
            self.Att_Conscientiousness = args[7]
            self.Att_Dominant = args[8]
            self.Att_Emotionality = args[9]
            self.Att_Extroversion = args[10]
            self.Att_Hard_Working = args[11]
            self.Att_Honest = args[12]
            self.Att_Influecing = args[13]
            self.Att_Innovative = args[14]
            self.Att_Knowledge_sharing = args[15]
            self.Att_Leadership = args[16]
            self.Att_Neuroticism = args[17]
            self.Att_Openness = args[18] 
            self.Att_Punctual = args[19]
            self.Att_Responsible = args[20]
            self.Att_Steady = args[21]
            self.Att_Teamwork = args[22]
            self.data = args[23]
            self.Phone = args[24]
            self.Email = args[25]
            self.Skills = args[26]
            self.Education = args[27]
            self.Education_Level = args[28]
            self.CGPA = args[29]
            self.Name = args[30]
        elif len(args) == 8:   
            self.Field = args[0]
            self.Phone = args[1]
            self.Email = args[2]
            self.Skills = args[3]
            self.Education = args[4]
            self.Education_Level = args[5]
            self.CGPA = args[6]
            self.Name = args[7]
        elif len(args) == 27:
            self.Att_Active = args[0]
            self.Att_Agreeableness = args[1]
            self.Att_Cautiousness = args[2]
            self.Att_Compliant = args[3]
            self.Att_Confidence = args[4]
            self.Att_Conscientiousness = args[5]
            self.Att_Dominant = args[6]
            self.Att_Emotionality = args[7]
            self.Att_Extroversion = args[8]
            self.Att_Hard_Working = args[9]
            self.Att_Honest = args[10]
            self.Att_Influecing = args[11]
            self.Att_Innovative = args[12]
            self.Att_Knowledge_sharing = args[13]
            self.Att_Leadership = args[14]
            self.Att_Neuroticism = args[15]
            self.Att_Openness = args[16] 
            self.Att_Punctual = args[17]
            self.Att_Responsible = args[18]
            self.Att_Steady = args[19]
            self.Att_Teamwork = args[20]
            self.Field = args[21]
            self.Email = args[22]
            self.Skills = args[23]
            self.Education = args[24]
            self.Education_Level = args[25]
            self.CGPA = args[26]
        elif len(args) == 21:   
            self.Att_Active = args[0]
            self.Att_Agreeableness = args[1]
            self.Att_Cautiousness = args[2]
            self.Att_Compliant = args[3]
            self.Att_Confidence = args[4]
            self.Att_Conscientiousness = args[5]
            self.Att_Dominant = args[6]
            self.Att_Emotionality = args[7]
            self.Att_Extroversion = args[8]
            self.Att_Hard_Working = args[9]
            self.Att_Honest = args[10]
            self.Att_Influecing = args[11]
            self.Att_Innovative = args[12]
            self.Att_Knowledge_sharing = args[13]
            self.Att_Leadership = args[14]
            self.Att_Neuroticism = args[15]
            self.Att_Openness = args[16] 
            self.Att_Punctual = args[17]
            self.Att_Responsible = args[18]
            self.Att_Steady = args[19]
            self.Att_Teamwork = args[20]
        elif len(args) == 2:
            self.Phone = args[0]
            self.Name = args[1]
        elif len(args) == 32:
            self.Filename = args[0]
            self.Field = args[1]
            self.Att_Active = args[2]
            self.Att_Agreeableness = args[3]
            self.Att_Cautiousness = args[4]
            self.Att_Compliant = args[5]
            self.Att_Confidence = args[6]
            self.Att_Conscientiousness = args[7]
            self.Att_Dominant = args[8]
            self.Att_Emotionality = args[9]
            self.Att_Extroversion = args[10]
            self.Att_Hard_Working = args[11]
            self.Att_Honest = args[12]
            self.Att_Influecing = args[13]
            self.Att_Innovative = args[14]
            self.Att_Knowledge_sharing = args[15]
            self.Att_Leadership = args[16]
            self.Att_Neuroticism = args[17]
            self.Att_Openness = args[18] 
            self.Att_Punctual = args[19]
            self.Att_Responsible = args[20]
            self.Att_Steady = args[21]
            self.Att_Teamwork = args[22]
            self.data = args[23]
            self.Phone = args[24]
            self.Email = args[25]
            self.Skills = args[26]
            self.Education = args[27]
            self.Education_Level = args[28]
            self.CGPA = args[29]
            self.Name = args[30]
            self.Speech = args[31]


class File(db.Model):
    ID = db.Column("ID",db.Integer, primary_key = True)
    Name = db.Column(db.String(100))
    Data = db.Column(db.BLOB)
    Text = db.Column(db.BLOB)
    Candidate_ID = db.Column(db.Integer)

    def __repr__(self):
        return str(self.ID)+str(self.Name)+str(self.Data)+str(self.Candidate_ID)
    
    def __init__(self,*args):
        if len(args) == 3:
            self.Name = args[0]
            self.Data = args[1]
            self.Candidate_ID = args[2]
        elif len(args) == 4:
            self.Name = args[0]
            self.Data = args[1]
            self.Text = args[2]
            self.Candidate_ID = args[3]

class Certificate(db.Model):
    ID = db.Column("ID",db.Integer, primary_key = True)
    Name = db.Column(db.String(100))
    Data = db.Column(db.BLOB)
    Candidate_ID = db.Column(db.Integer)

    def __repr__(self):
        return str(self.ID)+str(self.Name)+str(self.Data)+str(self.Candidate_ID)
    
    def __init__(self,*args):
        if len(args) == 3:
            self.Name = args[0]
            self.Data = args[1]
            self.Candidate_ID = args[2]


@app.before_request
def before_request():
    global model, rp 

@app.route("/login")
def login():
    if 'user_role' in session and session['user_role'] == 'admin' and session['login_status'] == 'success':
        return redirect(url_for("home",session = session))
    elif 'user_role' in session and session['user_role'] == 'student':
        return redirect(url_for("intro_student",session = session))
    
    return render_template("Login.html")

@app.route("/login", methods=['POST'])
def login_response():
    passcode = request.form.get('passcode') 
    password = request.form.get('password') 
    if passcode == 'MMU' and password == "1234":
        session['login_status'] = 'success'
        session['user_role'] = 'admin'
        return redirect(url_for("home",session = session))
    else:
        session['login_status'] = 'fail'
        return render_template("Login.html",session = session)



@app.route("/")
def intro_student():
    # session.clear()
    if 'user_role' not in session:
        # Set the session variable when the user first enters the route
        session['user_role'] = 'student'
    
    if request.args.get('message')  == "As13#s12": 
        if request.args.get('candidate_id') is not None:
            return render_template("ErrorMessage.html",message=request.args.get('message'),candidate_id = request.args.get('candidate_id'))

    return render_template("Intro.html",session = session)

@app.route("/2")
def intro_admin():
    # # global model, rp 
    # session.clear()
    if 'user_role' not in session:
        # Set the session variable when the user first enters the route
        return render_template("Login.html")
    else:
        return render_template("Intro.html",session = session)



def paging(page_no,data):
    per_page=10
    # records = resume.query.count()
    record_per_page = data.paginate(page=page_no, per_page=per_page,error_out=False)
    return record_per_page

@app.route('/home')
def home():  
    # Retrieve the value of a session variable
    session_value = session.get('user_role')
    if session_value == 'student':
        if request.args.get('message')  == "As13#s12":
            if request.args.get('candidate_id') is not None:
                return redirect(url_for("intro_student",session = session,message = request.args.get('message'),candidate_id = request.args.get('candidate_id') ))

        return redirect(url_for("intro_student",session = session))
    
    
    #Filter Action
    cgpa = None
    name = None
    field = None
    personality = None
    if request.args.get('cgpa') is not None:
        cgpa = request.args.get('cgpa')
    if request.args.get('name') is not None:
        name = request.args.get('name')  
    if request.args.get('field') is not None:
        field = request.args.get('field')
    if request.args.get('personality') is not None:
        personality = request.args.get('personality')
    if cgpa is not None or name is not None or field is not None or personality is not None:
        result = filter_function(name,cgpa,field,personality)
    else:
        result = resume.query.order_by(resume._id.desc())
    
    record_per_page = paging(request.args.get('page', 1, type=int),result)

    # if request.args.get('flash_message') is not None:
    #     return render_template("Home.html",session = session,values = record_per_page,flash_message=request.args.get('flash_message'), personality = personality, field = field, name = name, cgpa=cgpa)
    # return render_template("Home.html",session = session,values = record_per_page, flash_message="False", personality = personality, field = field, name = name, cgpa=cgpa)
    if request.args.get('message')  == "As13#s12":
        if request.args.get('candidate_id') is not None:
            return render_template("Popup2.html",message=request.args.get('message'),candidate_id=request.args.get('candidate_id'),session = session,values = record_per_page, personality = personality, field = field, name = name, cgpa=cgpa)

    return render_template("Home.html",session = session,values = record_per_page, personality = personality, field = field, name = name, cgpa=cgpa)

def filter_function(name,cgpa,field,personality):
    filtered = resume.query.all()
    counter = -1
    # if file is not None:
    #     if len(file) > 0 :
    #         if (file[-1].isspace()): 
    #             fileProccessed = '%'+(file.lower()[:-1])+'%'
    #         else:        
    #             fileProccessed = '%'+(file.lower())+'%'
    #         filter_file = resume.query.filter( resume.Filename.like(fileProccessed)).all()
    #         filtered = list(set(filtered).intersection(filter_file))
    #         counter += 1

    if name is not None:
        if len(name) > 0 :
            if (name[-1].isspace()): 
                nameProccessed = '%'+(name.lower()[:-1])+'%'
            else:        
                nameProccessed = '%'+(name.lower())+'%'
            filter_name = resume.query.filter( resume.Name.like(nameProccessed)).all()
            filtered = list(set(filtered).intersection(filter_name))
            counter += 1

    if field is not None:
        if len(field) > 0 :
            if (field[-1].isspace()): 
                fieldProccessed = '%'+(field.title()[:-1])+'%'
            else:        
                fieldProccessed = '%'+(field.title())+'%'

            filter_field = resume.query.filter( resume.Field.like(fieldProccessed) ).all()
            filtered = list(set(filtered).intersection(filter_field))
            counter += 1

    if  personality is not None:
        if len(personality) > 0:
            if (personality[-1].isspace()): 
                personalityProccessed = (personality.lower()[:-1]).split(",") 
            else:        
                personalityProccessed = (personality.lower()).split(",")

            for x in personalityProccessed:
                counter += 1
                executed = 0
                if x in "active":
                    filter_personality = resume.query.filter( resume.Att_Active == 1 ).all()
                    executed += 1
                elif x in "agreeableness":
                    filter_personality = resume.query.filter( resume.Att_Agreeableness == 1 ).all()
                    executed += 1
                elif x in "cautiousness":
                    filter_personality = resume.query.filter( resume.Att_Cautiousness == 1 ).all()
                    executed += 1                
                elif x in "compliant":
                    filter_personality = resume.query.filter( resume.Att_Compliant == 1 ).all()
                    executed += 1                
                elif x in "confidence":
                    filter_personality = resume.query.filter( resume.Att_Confidence == 1 ).all()
                    executed += 1                
                elif x in "conscientiousness":
                    filter_personality = resume.query.filter( resume.Att_Conscientiousness == 1 ).all()
                    executed += 1
                
                elif x == "dominant":
                    filter_personality = resume.query.filter( resume.Att_Dominant == 1 ).all()
                    executed += 1
                elif x in "emotionality":
                    filter_personality = resume.query.filter( resume.Att_Emotionality == 1 ).all()
                    executed += 1
                elif x in "extroversion":
                    filter_personality = resume.query.filter( resume.Att_Extroversion == 1 ).all()
                    executed += 1
                elif x in "hard working":
                    filter_personality = resume.query.filter( resume.Att_Hard_Working == 1 ).all()
                    executed += 1
                elif x in "honest":
                    filter_personality = resume.query.filter( resume.Att_Honest == 1 ).all()
                    executed += 1
                elif x in "influencing":
                    filter_personality = resume.query.filter( resume.Att_Influecing == 1 ).all()
                    executed += 1
                elif x in "innovative":
                    filter_personality = resume.query.filter( resume.Att_Innovative == 1 ).all()
                    executed += 1
                elif x in "knowledge-sharing":
                    filter_personality = resume.query.filter( resume.Att_Knowledge_sharing == 1 ).all()
                    executed += 1
                elif x in "leadership":
                    filter_personality = resume.query.filter( resume.Att_Leadership == 1 ).all()
                    executed += 1
                elif x in "neuroticism":
                    filter_personality = resume.query.filter( resume.Att_Neuroticism == 1 ).all()
                    executed += 1
                elif x in "openness":
                    filter_personality = resume.query.filter( resume.Att_Openness == 1 ).all()
                    executed += 1
                elif x in "punctual":
                    filter_personality = resume.query.filter( resume.Att_Punctual == 1 ).all()
                    executed += 1
                elif x in "responsible":
                    filter_personality = resume.query.filter( resume.Att_Responsible == 1 ).all()
                    executed += 1
                elif x in "steady":
                    filter_personality = resume.query.filter( resume.Att_Steady == 1 ).all()
                    executed += 1
                elif x in "teamwork":
                    filter_personality = resume.query.filter( resume.Att_Teamwork == 1 ).all()
                    executed += 1
                
                if executed > 0:
                    filtered = list(set(filtered).intersection(filter_personality))

    if counter == -1:
        result = resume.query.order_by(resume._id.desc()).all()
    else:
        result = filtered
        
    # if cgpa == ('asc'):
    #     result = sorted(result, key=lambda resume: resume.CGPA)
    # elif cgpa == ('desc'):
    #     result = sorted(result, key=lambda resume: resume.CGPA, reverse=True)

    # convert the list to a set of IDs
    id_set = set([data._id for data in result])
    # create a new query based on the IDs
    if cgpa == ('asc'):
        query = db.session.query(resume).filter(resume._id.in_(id_set)).order_by(resume.CGPA.asc())
    elif cgpa == ('desc'):
        query = db.session.query(resume).filter(resume._id.in_(id_set)).order_by(resume.CGPA.desc())
    else:
        query = db.session.query(resume).filter(resume._id.in_(id_set)).order_by(resume._id.desc())

    return query

#delete record if user want to modify the uploaded document
@app.route("/delete")
def delete():
    if request.args.get('candidate_id') is not None:
        x = int(request.args.get('candidate_id'))
        user_exist = resume.query.filter_by(_id = x).first()
        if user_exist :
            resume_delete = resume.query.filter_by(_id= int(x)).first()

            file_delete = File.query.filter_by(Candidate_ID = int(x))
            file_delete_list = file_delete.all()

            cert_delete = Certificate.query.filter_by(Candidate_ID = int(x))
            cert_delete_list = cert_delete.all()

            for file_to_be_delete in file_delete_list:
                pathOfFile = os.path.join(app.config['UPLOAD_DIRECTORY'],file_to_be_delete.Name)

                if os.path.exists(os.path.join(app.config['UPLOAD_DIRECTORY']+'converted_mp3/converted_{}.wav'.format(file_to_be_delete.Name))):
                    os.remove(os.path.join(app.config['UPLOAD_DIRECTORY']+'converted_mp3/converted_{}.wav'.format(file_to_be_delete.Name)))
                if os.path.exists(os.path.join(app.config['UPLOAD_DIRECTORY']+'speech_recognized/speech_{}.txt'.format(file_to_be_delete.Name))):
                    os.remove(os.path.join(app.config['UPLOAD_DIRECTORY']+'speech_recognized/speech_{}.txt'.format(file_to_be_delete.Name)))
                if os.path.exists(pathOfFile):
                    try:
                        os.remove(pathOfFile)
                    except:
                        None 
           
            for x in file_delete_list:
                db.session.delete(x)
            for x in cert_delete_list:
                db.session.delete(x)

            db.session.delete(resume_delete)
            db.session.commit()

            return redirect(url_for("upload"))
    return redirect(url_for("home"))



@app.route("/", methods=['POST'])
@app.route("/home", methods=['POST'])
@app.route("/popup", methods=['POST'])
def home3():
    # Retrieve the value of a session variable
    session_value = session.get('user_role')
    if session_value == 'student':
        return redirect(url_for("intro_student",session = session))
    
    #Perform Deleted Action
    checkedBox = request.form.getlist('checkBox')
    if checkedBox is not None:
        for x in checkedBox:
            resume_delete = resume.query.filter_by(_id= int(x)).first()

            file_delete = File.query.filter_by(Candidate_ID = int(x))
            file_delete_list = file_delete.all()

            cert_delete = Certificate.query.filter_by(Candidate_ID = int(x))
            cert_delete_list = cert_delete.all()

            for file_to_be_delete in file_delete_list:
                pathOfFile = os.path.join(app.config['UPLOAD_DIRECTORY'],file_to_be_delete.Name)

                if os.path.exists(os.path.join(app.config['UPLOAD_DIRECTORY']+'converted_mp3/converted_{}.wav'.format(file_to_be_delete.Name))):
                    os.remove(os.path.join(app.config['UPLOAD_DIRECTORY']+'converted_mp3/converted_{}.wav'.format(file_to_be_delete.Name)))
                if os.path.exists(os.path.join(app.config['UPLOAD_DIRECTORY']+'speech_recognized/speech_{}.txt'.format(file_to_be_delete.Name))):
                    os.remove(os.path.join(app.config['UPLOAD_DIRECTORY']+'speech_recognized/speech_{}.txt'.format(file_to_be_delete.Name)))
                if os.path.exists(pathOfFile):
                    try:
                        os.remove(pathOfFile)
                    except:
                        None 
           
            for x in file_delete_list:
                db.session.delete(x)
            for x in cert_delete_list:
                db.session.delete(x)

            db.session.delete(resume_delete)
            db.session.commit()


    #Filter Action
    cgpa = request.form.get('cgpa')
    # print(cgpa)
    name = request.form.get("name")
    field  = request.form.get("field")
    personality  = request.form.get("personality")


    result = filter_function(name,cgpa,field,personality)
    result = paging(request.args.get('page', 1, type=int),result)

    return render_template("Home.html",values = result, personality = personality, field = field, name = name, cgpa=cgpa)

#attitude modal box
@app.route("/popup")
def popup():
    # Retrieve the value of a session variable
    session_value = session.get('user_role')
    if session_value == 'student':
        return redirect(url_for("intro_student",session = session))
    
    y = 1
    filtered = resume.query.all()

    if request.args.get('candidateID') is not None:
        y = (request.args.get('candidateID'))


    user_exist = resume.query.filter_by(_id = y).first()
    if user_exist :
        if request.args.get('cgpa') is not None:
                cgpa = request.args.get("cgpa")
        else:
            cgpa = None

        if request.args.get('name') is not None:
            name = request.args.get("name")
        else:
            name = None
        if request.args.get('field') is not None:
            field = request.args.get("field")
        else:
            field = None
        if request.args.get('personality') is not None:
            personality = request.args.get("personality")
        else:
            personality = None


        # page = request.args.get('page', 1, type=int)

        result = filter_function(name,cgpa,field,personality)
        result = paging(request.args.get('page', 1, type=int),result)

        return render_template("PopUp.html", values = result, personality = personality,cgpa=cgpa ,field = field,name = name ,detail = resume.query.filter_by(_id = y).first())
    else:
        return render_template("PopUp.html",values = filtered, no_word_found="candidate not found",detail = 'Error')
    
#certificate modal box
@app.route("/popup2")
def popup2():
    # Retrieve the value of a session variable
    session_value = session.get('user_role')
    if session_value == 'student':
        return redirect(url_for("intro_student",session = session))
    
    y = 1
    filtered = resume.query.all()

    if request.args.get('candidateID') is not None:
        y = (request.args.get('candidateID'))

    user_exist = resume.query.filter_by(_id = y).first()
    if user_exist :
        if request.args.get('cgpa') is not None:
                cgpa = request.args.get("cgpa")
        else:
            cgpa = None

        if request.args.get('name') is not None:
            name = request.args.get("name")
        else:
            name = None
        if request.args.get('field') is not None:
            field = request.args.get("field")
        else:
            field = None
        if request.args.get('personality') is not None:
            personality = request.args.get("personality")
        else:
            personality = None


        # page = request.args.get('page', 1, type=int)

        result = filter_function(name,cgpa,field,personality)
        result = paging(request.args.get('page', 1, type=int),result)

        return render_template("PopUp2.html", values = result, personality = personality,cgpa=cgpa ,field = field,name = name ,detail = Certificate.query.filter_by(Candidate_ID = y))
    else:
        return render_template("PopUp2.html",values = filtered, no_word_found="certificate not found",detail = 'Error')

@app.route("/download/<candidateID>", methods=['POST','GET'])
def download(candidateID):
    # Retrieve the value of a session variable
    session_value = session.get('user_role')
    if session_value == 'student':
        return redirect(url_for("intro_student",session = session))
    
    uploads = File.query.filter_by(Candidate_ID = candidateID).all()

    # Create a BytesIO object to store the zipped data.
    zip_data = BytesIO()

    # Create a ZipFile object and add the blobs to it using writestr() method.
    with zipfile.ZipFile(zip_data, mode='w') as z:
        for upload in uploads:
            if '.mp4' in upload.Name:
                video=  BytesIO(upload.Data)
                z.writestr(upload.Name,video.getvalue()) #video
                naming = (upload.Name).replace(".mp4",".txt")
                speech=  BytesIO(upload.Text)
                z.writestr("speech_"+naming, speech.getvalue()) #video

            else:
                z.writestr(upload.Name, upload.Data)

    zip_data.seek(0)

    return send_file(
        zip_data,
        as_attachment=True,
        download_name='archive.zip'
    )        
    if '.mp4' in upload.Filename:

        stream = BytesIO()
        with ZipFile(stream, 'w') as zf:
            video=  BytesIO(upload.data)
            zf.writestr(upload.Filename,video.getvalue()) #video
            # zf.write(upload.data.encode('UTF-8'), upload.Filename)
            # zf.write(os.path.join(app.config['UPLOAD_DIRECTORY']+upload.Filename), upload.Filename)

            naming = (upload.Filename).replace(".mp4",".txt")
            speech=  BytesIO(upload.Speech)
            zf.writestr("speech_"+naming, speech.getvalue()) #video
            # zf.write(os.path.join(app.config['UPLOAD_DIRECTORY']+'speech_recognized/speech_{}.txt'.format(upload.Filename)), 'speech_{}.txt'.format(naming))#speech

            # zf.write(send_file(BytesIO(upload.Speech), download_name="speech_recognized", as_attachment=True))

        stream.seek(0)

        return send_file(
            stream,
            as_attachment=True,
            download_name='archive.zip'
        )
    else:
        return send_file(BytesIO(upload.data), download_name=upload.Filename, as_attachment=True)


@app.route("/upload",methods=['POST','GET'])
def upload():
    if request.method == "POST":
        files = request.files.getlist('file')
        predicted_result= []
        # initialize the result list after LOGIC performed
        result_after_logic = []

        personal_information = ["-","-","-","-","-","-"]

        name_entered = request.form['inputName']
        phone_entered = request.form['inputPhone']

        found_candidate = resume.query.filter_by(Name = name_entered,Phone=phone_entered).first()

        if found_candidate:         
            return render_template("ErrorMessage.html", no_word_found="Duplicate candidate",detail = name_entered)
   
            return redirect(url_for("upload",flash_message = "Duplicate"))
        else:
            res = resume(phone_entered,name_entered)
            db.session.add(res)
            db.session.commit()

            # return render_template("test.html",message= len(files))
            non_empty_files = [file for file in files if file.filename != '']

            for file in non_empty_files:                     
                extension = os.path.splitext(file.filename)[1]

                if file:
                    if extension not in app.config['ALLOWED_EXTENSIONS']: #already handled in javascript
                        pass
                    else:
                        # return render_template("test.html",message= file.filename)

                        # print(file.read())
                        no_word_found = False #for validation purpose #if false meaning the text extracted contains text else if true, no text were found from the file

                        file.save(os.path.join(
                        app.config['UPLOAD_DIRECTORY'],
                        file.filename
                        ))
                        # rme = open(app.config['UPLOAD_DIRECTORY']+file.filename,"r")
                        # print(file.read())

                        # Convert the video into text
                        if extension == ".mp4":

                            try:
                                clip = mp.VideoFileClip(os.path.join(app.config['UPLOAD_DIRECTORY']+file.filename))
                                clip.audio.write_audiofile(r"uploads/converted_mp3/converted_{}.wav".format(file.filename))
                            
                                r = sr.Recognizer()
                                audio = sr.AudioFile("uploads/converted_mp3/converted_{}.wav".format(file.filename))
                                with audio as source:
                                    r.adjust_for_ambient_noise(source, duration=0.5)
                                    audio_file = r.record(source)
                                result = r.recognize_google(audio_file)
                                with open(r"uploads/speech_recognized/speech_{}.txt".format(file.filename),mode='w') as speech_file:
                                    speech_file.write(result)
                                clip.close()
                                text = rp.extract_text_from_file(os.path.join(app.config['UPLOAD_DIRECTORY']+'speech_recognized/speech_{}.txt'.format(file.filename)))
                                ValidationText = text.translate({ord(c): None for c in string.whitespace})
                                if len(ValidationText) <=20:
                                    error_filename = file.filename
                                    no_word_found = True
                            except: 
                                error_filename = file.filename
                                no_word_found=True
                        
                        #convert doc to docx format
                        elif extension == ".doc":
                            try:
                                doc_path = os.path.join(app.config['UPLOAD_DIRECTORY']+file.filename)
                                doc = aw.Document(doc_path)
                                doc_filename = doc_path.split("\\")[-1]
                                doc_filename = doc_filename.split('.doc')[0]
                                docx_path = doc_filename+'.docx'
                                doc.save(docx_path)

                                text = rp.extract_text_from_file(docx_path)
                                ValidationText = text.translate({ord(c): None for c in string.whitespace})
                                if len(ValidationText) <=20:
                                    error_filename = file.filename
                                    no_word_found = True
                                if os.path.exists(docx_path):
                                    os.remove(docx_path)
                            except:
                                error_filename = file.filename
                                no_word_found=True

                        else:
                            try:
                                text = rp.extract_text_from_file(os.path.join(app.config['UPLOAD_DIRECTORY']+file.filename))
                                ValidationText = text.translate({ord(c): None for c in string.whitespace})
                                if len(ValidationText) <=20:
                                    error_filename = file.filename
                                    no_word_found = True
                            except:
                                error_filename = file.filename
                                no_word_found=True

                        if no_word_found:
                            # pathOfFile = os.path.join(app.config['UPLOAD_DIRECTORY'],file.filename)
                            # if os.path.exists(os.path.join(app.config['UPLOAD_DIRECTORY']+'converted_mp3/converted_{}.wav'.format(file.filename))):
                            #     os.remove(os.path.join(app.config['UPLOAD_DIRECTORY']+'converted_mp3/converted_{}.wav'.format(file.filename)))
                            # if os.path.exists(os.path.join(app.config['UPLOAD_DIRECTORY']+'speech_recognized/speech_{}.txt'.format(file.filename))):
                            #     os.remove(os.path.join(app.config['UPLOAD_DIRECTORY']+'speech_recognized/speech_{}.txt'.format(file.filename)))
                            # if os.path.exists(pathOfFile):
                            #     try:
                            #         os.remove(pathOfFile)
                            #     except:
                            #         None 
                            id_result=db.session.query(resume._id).filter_by(Name=name_entered,Phone = phone_entered).first()
                            id_result = id_result[0] if id_result else None
                            
                            file_delete = File.query.filter_by(Candidate_ID = id_result)
                            file_delete_list = file_delete.all()

                            for x in file_delete_list:
                                db.session.delete(x)


                            resume.query.filter(resume.Name == name_entered,resume.Phone==phone_entered).delete()
                            db.session.commit()
                            for file in non_empty_files:
                                pathOfFile = os.path.join(app.config['UPLOAD_DIRECTORY'],file.filename)
                                if os.path.exists(os.path.join(app.config['UPLOAD_DIRECTORY']+'converted_mp3/converted_{}.wav'.format(file.filename))):
                                    os.remove(os.path.join(app.config['UPLOAD_DIRECTORY']+'converted_mp3/converted_{}.wav'.format(file.filename)))
                                if os.path.exists(os.path.join(app.config['UPLOAD_DIRECTORY']+'speech_recognized/speech_{}.txt'.format(file.filename))):
                                    os.remove(os.path.join(app.config['UPLOAD_DIRECTORY']+'speech_recognized/speech_{}.txt'.format(file.filename)))
                                if os.path.exists(pathOfFile):
                                    try:
                                        os.remove(pathOfFile)
                                    except:
                                        None 

                            # result = paging(request.args.get('page', 1, type=int),resume.query)

                            # return render_template("PopUp.html",values =result, no_word_found="no word found",detail = error_filename)
                            return render_template("ErrorMessage.html", no_word_found="no word found",detail = error_filename)

                        else:    
                            Cleaned_text = model.clean_text(text)
                            tokenized = model.tokenization(Cleaned_text)
                            stemmed = model.stemming(tokenized)
                            result = list(set(model.prediction(stemmed)))

                            field = rp.extract_field(text) #get field
                            if personal_information[0] == "-":
                                personal_information[0] = field


                            # phone_number = rp.extract_phone_number(text)
                            # if phone_number is None:
                            #     phone_number = '-'

                            emails = rp.extract_emails(text)
                            emails = [i for i in emails if '@gmail.com' or '@yahoo.com' or '@hotmail.com' or 'edu.my' or '.my' in i]
                            if personal_information[1] == "-":
                                if len(emails) > 0:
                                    personal_information[1] = emails


                            skills = list(rp.extract_skills(text))
                            if len(skills) > 0:
                                skills = ",".join(skills)
                                if personal_information[2] == "-":
                                    personal_information[2] = skills

                            education_information = rp.extract_education(text)
                            if personal_information[3] == "-":
                                if education_information != "-":
                                    personal_information[3] = education_information

                            educationle = list(rp.extract_educationlevel(text))                            
                            if len(educationle) > 0:
                                if personal_information[4] == "-":
                                    personal_information[4] = educationle[0]

                            cgpa = rp.findCGPA(text)
                            if cgpa != "-":
                                if personal_information[5] == "-":
                                    personal_information[5] = cgpa
                            # name = rp.findName(text,extension)


                            personality = ['active','agreeableness','cautiousness','compliant','confidence','conscientiousness','dominant','emotionality','extroversion','hard working','honest','influecing','innovative','knowledge-sharing','leadership','neuroticism','openness','punctual','responsible','steady','teamwork']
                            final = []
                            for p in personality:
                                if p in result:
                                    final.append(1)
                                else:
                                    final.append(0)
                            predicted_result.append(final)


                            # res = resume(field,phone_entered,emails[0],skills,education_information,educationle[0],cgpa,name_entered)
                            # id_result = select(resume).where(resume.Name == name_entered).first()
                            id_result=db.session.query(resume._id).filter_by(Name=name_entered,Phone = phone_entered).first()
                            id_result = id_result[0] if id_result else None


                            if extension == ".mp4":
                                file.seek(0)
                                # Open the text file for reading
                                with open("uploads/speech_recognized/speech_{}.txt".format(file.filename), 'rb') as speech_file:
                                    file_contents = speech_file.read()
                                
                                file_upload = File(file.filename,file.read(),file_contents,id_result)
                                db.session.add(file_upload)
                                db.session.commit()
                                speech_file.close()
                            else:
                                file.seek(0)
                                # return render_template("test.html",message= id_result)

                                file_upload = File(file.filename,file.read(),id_result)
                                db.session.add(file_upload)
                                db.session.commit()
                    # return redirect(url_for("confirmation",filename = file.filename))
                else:
                    return render_template("Upload.html",flash_message="True")
                
            if len(predicted_result) >0:
                if len(predicted_result) == 1:
                    result_after_logic = predicted_result[0]
                else:
                    # Get the number of columns
                    num_cols = len(predicted_result[0])

                    # Loop over each column
                    for col in range(num_cols):
                        # Initialize the flag to False for OR logic
                        or_result = 0
                        for row in range(len(predicted_result)):
                            # If the value in the row is 1, set the flag to True
                            if predicted_result[row][col] == 1:
                                or_result = 1
                                break
                        # Append the flag value to the result list
                        result_after_logic.append(or_result)


                    # # iterate through each sublist in the list of list
                    # for sublist in predicted_result:
                    #     # initialize a variable to hold the result of the AND operation
                    #     and_result = 1
                        
                    #     # iterate through each element in the sublist
                    #     for element in sublist:
                    #         # perform the AND operation
                    #         and_result &= element
                            
                    #     # append the AND result to the result list
                    #     result_after_logic.append(and_result)

                # return render_template("test.html",message= result_after_logic)

                # update_query = update(resume).where(resume.Name == name_entered).values(Att_Active=result_after_logic[0],Att_Agreeableness=result_after_logic[1],Att_Cautiousness=result_after_logic[2],Att_Compliant=result_after_logic[3],Att_Confidence=result_after_logic[4],Att_Conscientiousness=result_after_logic[5],Att_Dominant=result_after_logic[6],Att_Emotionality=result_after_logic[7],Att_Extroversion=result_after_logic[8],Att_Hard_Working=result_after_logic[9],Att_Honest=result_after_logic[10],Att_Influecing=result_after_logic[11],Att_Innovative=result_after_logic[12],Att_Knowledge_sharing=result_after_logic[13],Att_Leadership=result_after_logic[14],Att_Neuroticism=result_after_logic[15],Att_Openness=result_after_logic[16],Att_Punctual=result_after_logic[17],Att_Responsible=result_after_logic[18],Att_Steady=result_after_logic[19],Att_Teamwork=result_after_logic[20],Field = personal_information[0],Email = personal_information[1],Skills = personal_information[2],Education = personal_information[3],Education_Level = personal_information[4],CGPA = personal_information[5])
                # db.session.execute(update_query)

                candidate = resume.query.filter_by(Name = name_entered,Phone=phone_entered).first()
                candidate.Att_Active=result_after_logic[0]
                candidate.Att_Agreeableness=result_after_logic[1]
                candidate.Att_Cautiousness=result_after_logic[2]

                candidate.Att_Compliant=result_after_logic[3]
                candidate.Att_Confidence=result_after_logic[4]
                candidate.Att_Conscientiousness=result_after_logic[5]

                candidate.Att_Dominant=result_after_logic[6]
                candidate.Att_Emotionality=result_after_logic[7]
                candidate.Att_Extroversion=result_after_logic[8]
                candidate.Att_Hard_Working=result_after_logic[9]
                candidate.Att_Honest=result_after_logic[10]
                candidate.Att_Influecing=result_after_logic[11]
                candidate.Att_Innovative=result_after_logic[12]
                candidate.Att_Knowledge_sharing=result_after_logic[13]
                candidate.Att_Leadership=result_after_logic[14]
                candidate.Att_Neuroticism=result_after_logic[15]
                candidate.Att_Openness=result_after_logic[16]
                candidate.Att_Punctual=result_after_logic[17]
                candidate.Att_Responsible=result_after_logic[18]
                candidate.Att_Steady=result_after_logic[19]
                candidate.Att_Teamwork=result_after_logic[20]
                candidate.Field = personal_information[0]
                candidate.Email = personal_information[1][0]
                candidate.Skills = personal_information[2]
                candidate.Education = personal_information[3]
                candidate.Education_Level = personal_information[4]
                candidate.CGPA = personal_information[5]
                db.session.commit()
                #send mail to inform admin got new candidate uploaded his/her document
                msg = Message('New Candidate Document Upload Notification', sender='jobsearchsystem666@gmail.com', recipients=['1181103488@student.mmu.edu.my'])
                msg.body = f"Good day to you. A new candidate has successfully uploaded thier document into the system. This email serves as a notification to bring your attention to this important update. \n\nCandidate Name: {name_entered} \n\n Phone Number: {phone_entered}"
                mail.send(msg)
                
                return redirect(url_for("certificate_upload",candidateID = candidate._id))
            else:
                resume.query.filter(resume.Name == name_entered,resume.Phone==phone_entered).delete()
                db.session.commit()
                return render_template("Upload.html",flash_message="True")

    else:
        return render_template("Upload.html",flash_message="False")


@app.route("/test")
def test():
    # resume_delete = resume.query.filter_by(Name = '546')
    # resume_delete_list = resume_delete.all()

    # for x in resume_delete_list:
    #     db.session.delete(x)

    # file_delete = File.query.filter_by(Candidate_ID = 45)
    # file_delete_list = file_delete.all()

    # for x in file_delete_list:
    #     db.session.delete(x)

    # cert_delete = Certificate.query.filter_by(Candidate_ID = None)
    # certificate_delete_list = cert_delete.all()

    # for x in certificate_delete_list:
    #     db.session.delete(x)

    # delete_query = resume.delete().where(Name = '546')
    # db.session.execute(delete_query)

    # db.session.commit()
    
    # Assuming you have a resume object
    resumes = resume.query.filter(resume.Name == '546').all()

    # Delete the resume object
    for x in resumes:
        db.session.delete(x)
    db.session.commit()
    return render_template("test.html", message = resume.query.all())

@app.route("/certificate_upload")
def certificate_upload():
    if request.args.get('candidateID') is not None:
        user_exist = resume.query.filter_by(_id = request.args.get('candidateID')).first()
        if user_exist :
            return render_template("Certificate.html",candidateID = request.args.get('candidateID'))
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

@app.route('/download_certificate/<filename>')
def download_certificate(filename):
    # Retrieve the value of a session variable
    session_value = session.get('user_role')
    if session_value == 'student':
        return redirect(url_for("intro_student",session = session))
    
    cert = db.session.query(Certificate).filter_by(Name=filename).first()
    return send_file(BytesIO(cert.Data), download_name=cert.Name, as_attachment=True)


@app.route("/certificate_upload",methods=['POST'])
def certificate_upload2():
    if request.form.get('candidate_id') is not None:
        user_exist = resume.query.filter_by(_id = request.form.get('candidate_id')).first()
        if user_exist :
            files = request.files.getlist('file')
            # return render_template("test.html", message = request.form.get('candidate_id'))
            non_empty_files = [file for file in files if file.filename != '']

            if non_empty_files:
                uploaded = False

                for file in non_empty_files:
                    if file:
                        filename = file.filename
                        extension = os.path.splitext(filename)[1]

                        if extension not in app.config['ALLOWED_EXTENSIONS_CERTIFICATE']: #already handled in javascript
                            pass
                        else:
                            uploaded = True
                            certificate = Certificate(file.filename, file.read(), request.form.get('candidate_id'))
                            db.session.add(certificate)
                            db.session.commit()
                    else:                    
                        return render_template("Upload.html",flash_message="No certificate selected")

                if uploaded:
                    candidate = resume.query.filter_by(_id = request.form.get('candidate_id')).first()
                    candidate.Has_Certificate = "Yes"
                    db.session.commit()
                else:
                    return render_template("Upload.html",flash_message="No certificate selected")

                return redirect(url_for("home",message='As13#s12',candidate_id = request.form.get('candidate_id')))
            else:
                return render_template("Upload.html",flash_message="No certificate selected")
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

# @app.route("/questionnaire",methods=['POST'])
# def answers():
#     if request.method == 'POST':
#         answers = {}
#         # for question in questions:
#         #     answers[question['id']] = int(request.form[question['id']])
#         # return render_template('result.html', answers=answers)


if __name__ == "__main__":
    # db.create_all() -refer to youtube to create
    app.run(debug=True)