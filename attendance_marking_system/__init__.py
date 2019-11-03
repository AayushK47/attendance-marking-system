from flask import Flask, render_template, url_for, redirect, session
from flask_login import LoginManager
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cebafbb0ccf0dcc2f70b3c0607fb46725d949e044c8cdfeadd1f176b9cd90fb3'
app.config['UPLOAD_FOLDER'] = './'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="attendance_marking_system"
)
cursor = conn.cursor()

login_manager = LoginManager(app)

from attendance_marking_system import routes