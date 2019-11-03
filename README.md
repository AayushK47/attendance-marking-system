# Attendance Marking System

## About
Attendance Marking System is a simple web based application that takes image of a class as input, detects and identifies all the students present in the image and saves their attendance in the database.

## Project Structure
```bash
├── attendance_marking_system
│   ├── models
│   │   ├── haarcascade_frontalface_default.xml
│   │   ├── model.h5
│   ├── static
│   │   ├── main.css
│   ├── templates
│   │   ├── attendance.html
│   │   ├── index.html
│   │   ├── layout.html
│   │   ├── register.html
│   ├── __init__.py
│   ├── auth.py
│   ├── forms.py
│   ├── detect.py
│   ├── routes.py
├── ML
├── predict.py
├── requirements.txt
├── run.py
├── .gitignore
├── README.md
```
## Dependencies

The packages required to run this software are:-
- flask
- flask_wtf
- flask_login
- mysql-connector-python
- numpy
- tensorflow v1.15.0
- opencv-python
- bcrypt

You can install all the required dependencies simply by executing the following command :-

```
pip install -r requirements.txt
```

## How to run

Once all the required dependancies are installed, simply execute the following command to start the server :-

- **For Windows**
```
python run.py
```

- **For Mac and Linux**
```
python3 run.py
```