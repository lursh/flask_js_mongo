from flask import Blueprint,Flask, flash, request, redirect, url_for, render_template
from db import db
import bcrypt
import os
import urllib.request
import json
from json import JSONEncoder




app = Flask(__name__,static_folder="./static",static_url_path='/static')
app.secret_key="1999007021"


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = 'static/uploads/'



def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





@app.route('/')
def home_page():
   return render_template("mainhome.html")





@app.route("/addstudent", methods=['post'])
def register():
   records= db.students
   file = request.files['photo']
   filename = file.filename
   path=os.path.join(UPLOAD_FOLDER, filename)
   if 'photo' not in request.files:
      message='No file part'
      return message
   if file.filename == '':
      message='No image selected for uploading'
      return message
   if file and allowed_file(file.filename):			
      file.save(path)
      print('upload_image filename: ' + filename)
   if not allowed_file(file.filename):
      message="Allowed image types are -> png, jpg, jpeg, gif"
      return file.filename+":"+message 		
		
   photourl= path
   email = request.form.get("email")
   uname=request.form.get("name")
   dob=request.form.get("dob")
   email=request.form.get("email")
   phone=request.form.get("phone")
   home_address=request.form.get("home_address")
   gua_name= request.form.get("gua_name")
   date_join= request.form.get("date_join")
   gua_phone= request.form.get("gua_phone")
   institute_name= request.form.get("institute_name")
   #institute_id= db.institutes.find({"name":institute_name})._id
   room_no= request.form.get("room_no")
   password1 = request.form.get("password1")
   password2 = request.form.get("password2")
   email_found = records.find_one({"email": email})
   if email_found:
      message = 'This email already exists in database'
      return message
   if password1 != password2:
      message = 'Passwords should match!'
      return message
   else:
      hashed = bcrypt.hashpw(str(password2).encode('utf-8'), bcrypt.gensalt())
      user_input = {'name': uname, 'email': email, 'password': hashed,"dob":dob,"email":email,"phone":phone,"home_address":home_address,"gua_name":gua_name,"date_join":date_join,"gua_phone":gua_phone,"institute_name":institute_name,"room_no":room_no,"pic_url":photourl}
      records.insert_one(user_input)
      message = 'Sucessfully Added!'
      return message






@app.route('/admin',methods=['get'])
def admin_home_display():
   return render_template("admin.html")



@app.route('/students',methods=['get'])
def list_student():
   records=db.students
   return render_template('list_students.html',records=records)

app.run(host='0.0.0.0', port=1111, debug=True)
