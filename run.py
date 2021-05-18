from flask import Blueprint,Flask, flash, request, redirect, url_for, render_template
from db import db
import bcrypt
import os
import urllib.request
import json
from json import JSONEncoder
from mod_admin import mod_admin



app = Flask(__name__,static_folder="./static",static_url_path='/static',template_folder="./templates")

app.register_blueprint(mod_admin)

app.secret_key="1999007021"

@app.route('/')
def home_page():
   return render_template("mainhome.html")


app.run(host='0.0.0.0', port=1111, debug=True)
