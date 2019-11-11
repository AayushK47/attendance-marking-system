import os
import sys
import cv2
import bcrypt
from itertools import combinations
from sklearn.utils import shuffle
from flask import render_template, redirect, url_for, flash, request
from base64 import b64encode
import json
import pickle
from flask_login import login_user, current_user, logout_user
from werkzeug.utils import secure_filename

from attendance_marking_system import app
from attendance_marking_system.detect import detect_faces, extract_faces
from attendance_marking_system.forms import LoginForm, RegisterForm, AttendanceForm, StudentForm
from attendance_marking_system import cursor, conn
from attendance_marking_system.auth import User

@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('attendance'))
    
    login_form = LoginForm()

    if login_form.validate_on_submit():
        cursor.execute(f"SELECT * FROM tbl_faculty WHERE email='{login_form.email.data}'")
        user = cursor.fetchall()
        if len(user) > 0 and bcrypt.checkpw(login_form.password.data.encode(), user[0][-1].encode()):
            user = User(login_form.email.data)
            login_user(user)
            return redirect(url_for('attendance'))
        else:
            flash('Invalid credentials! Check your email and password.','danger')
            return redirect(url_for('index'))


    return render_template('index.html', active="signin", form=login_form, auth=current_user.is_authenticated)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('attendance'))

    register_form = RegisterForm()

    if register_form.validate_on_submit():
        add_user(register_form)
        flash('Registration successful! Login to continue','success')
        return redirect(url_for('index'))

    return render_template('register.html', active="register", form=register_form, auth=current_user.is_authenticated)

def add_user(form):
    hashed_pw = str(bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()), 'utf-8')
    sql = "INSERT INTO tbl_faculty (name, designation, email, password) VALUES (%s, %s, %s, %s);"
    val = (form.name.data, form.designation.data, form.email.data, hashed_pw)
    cursor.execute(sql, val)
    conn.commit()

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if not current_user.is_authenticated:
        flash('You need to be logged in to access that page','danger')
        return redirect(url_for('index'))
    attendance_form = AttendanceForm()

    if request.method == 'POST':
        getFileData(attendance_form)
        present, present_final, image = mark_attendance()
        insert_lecture_data(attendance_form, image)
        image = b64encode(image).decode("utf-8")
        attendance_form.class_name.choices = get_choices()
        query = 'INSERT INTO tbl_attendance (lecture_no, _date, enrollment_no, class) VALUES '
        values = ''
        print(present_final)
        for i in present_final:
            vals = f"('{attendance_form.lecture_number.data}', '{attendance_form.date.data}', '{i[0].decode()}', '{attendance_form.class_name.data}'), "
            values += vals

        values = values[:-2] + ';'
        cursor.execute(query + values)
        conn.commit()
        return render_template('attendance.html', active='attendance', form=attendance_form, auth=current_user.is_authenticated, image=image, tbl=present_final, styles=None)


    attendance_form.class_name.choices = get_choices()
    return render_template('attendance.html', active='attendance', form=attendance_form, auth=current_user.is_authenticated, image=None, tbl=False)

def get_choices():
    data = cursor.execute("SELECT name FROM tbl_class")
    data = cursor.fetchall()
    choices = [('', 'Class')]
    for i in range(len(data)):
        choices.append((data[i][0], data[i][0]))
    return choices

def getFileData(form):
    f = form.image.data
    filename = secure_filename(f.filename)
    f.save(os.path.join( os.getcwd(), 'img-1.jpg'))


def insert_lecture_data(form, image):
    sql = '''INSERT INTO  tbl_lecture (lecture_no, class, teacher, _date) VALUES (%s, %s, %s, %s)'''
    vals = (form.lecture_number.data, form.class_name.data, current_user.id, form.date.data)
    cursor.execute(sql, vals)
    conn.commit()
    print('lecture data inserted')

def mark_attendance():
    present = []
    img1 = cv2.imread(os.path.join(os.getcwd(), 'img-1.jpg'))
    face_dims, faces = extract_faces(cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY), img1)
    count = len(faces)
    print(count)

    cursor = conn.cursor(raw=True)
    cursor.execute('SELECT enrollment_no, student_image FROM tbl_student')
    data = cursor.fetchall()

    index = 0
    for face in faces:
        prl = len(present)
        cv2.imwrite('img-2.jpg', face)

        for enroll, image in data:
            if enroll in present:
                continue
            filename = 'img-3.jpg'
            with open(filename, 'wb') as f:
                f.write(image)
            img = cv2.imread(filename)
            os.system(f'python predict.py img-2.jpg {filename}')
            with open('results.txt', 'r') as f:
                result = f.read()
            print(f'result {result}')
            if int(result) == 1:
                present.append(enroll)
                break
        
        if(len(present) == prl):
            present.append('unknown')
        
        x, y, w, h = face_dims[index]
        cv2.rectangle(img1, (x, y), (x+w, y+h), (0, 0, 255), 5)
        name = 'unknown' if present[-1] == 'unknown' else present[-1].decode()
        cv2.putText(img1, f'{name}', (x+10, y+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        index += 1
    
    cv2.imwrite('img-1.jpg', img1)
    with open('img-1.jpg', 'rb') as f:
        image_raw = f.read()
    
    os.remove('results.txt')

    cursor_raw = conn.cursor(raw=True)
    cursor_raw.execute('SELECT enrollment_no, name FROM tbl_student')
    data = cursor_raw.fetchall()

    present_final = []
    for i in data:
        if i[0] in present:
            present_final.append(i)

    os.remove('img-3.jpg')
    os.remove('img-2.jpg')
    os.remove('img-1.jpg')

    return present, present_final, image_raw

@app.route('/history')
def history():
    params = dict(request.args)
    if len(params) == 0:
        cursor.execute(f"SELECT * FROM tbl_lecture WHERE teacher='{current_user.id}'")
        data = cursor.fetchall()
        return render_template('history.html', active='history', auth=current_user.is_authenticated, history=data)
    else:
        cursor.execute(f"SELECT tbl_attendance.enrollment_no, name FROM tbl_attendance INNER JOIN tbl_student ON tbl_attendance.enrollment_no=tbl_student.enrollment_no WHERE lecture_no='{params['lec']}' AND tbl_attendance.class='{params['class']}' AND _date='{params['date']}'")
        data = cursor.fetchall()
        print(data)
        return render_template('detail.html', active='history', auth=current_user.is_authenticated, params=params, details=data)

@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out successfully!','success')
    return redirect(url_for('index'))