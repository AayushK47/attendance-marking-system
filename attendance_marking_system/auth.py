from attendance_marking_system import login_manager
from flask_login import UserMixin
import bcrypt

from attendance_marking_system import app
from attendance_marking_system import cursor

class User(UserMixin):
    def __init__(self, email):
        self.id = email

@login_manager.user_loader
def user_loader(email):
    cursor.execute("SELECT * FROM tbl_faculty WHERE email='{}'".format(email))
    result = cursor.fetchall()
    if  len(result) == 0:
        return None
    else:
        user = User(result[0][2])
        user.name = result[0][0]
        user.designation = result[0][1]
        return user