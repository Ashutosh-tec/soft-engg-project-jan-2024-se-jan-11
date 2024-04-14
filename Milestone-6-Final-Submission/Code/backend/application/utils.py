
from application.models import User
from application.models import db
from application.workers import celery
from application.tasks import send_email
from celery import chain
import pandas
import os
import secrets,string    
from random_username.generate import generate_username   

class invalidRoleException(Exception):
    pass

class emptyFileException(Exception):
    pass

def str_to_int_roles(role):
    res = None
    if role.lower() == "student":
        res = 1
    elif role.lower() == "support agent":
        res = 2
    elif role.lower() == "admin":
        res = 3
    elif role.lower() == "manager":
        res = 4
    else:
        raise invalidRoleException
    return res

@celery.task
def add_users_import(csv_file_path, eid):
    """
    Adds users as a batch job wherein a CSV file is passed from the frontend and then operated upon by the backend.
    csv_file_path is the path to the csv file which has the CSV file of details. Please change it accordingly.
    """
    df = None
    b = None
    html = '<html>'
    subject='Error in importing your data'
    try:
        df = pandas.read_csv(csv_file_path)
    except:
        html += '<p> Your file must have atleast one row of data apart from the columns </p> </html>'
        send_email.s((html, eid, subject)).apply_async()
        return 'File Not Found'
    try:
        b = len(df)
        #print(b)
        if b == 0:
            raise emptyFileException
    except:
        html += '<p> Your file must have atleast one row of data apart from the columns </p> </html>'
        send_email.s((html, eid, subject)).apply_async()
        return 'Invalid Data'
    flag = 0
    for i in range(b):
            row = df.iloc[i]
            email_id = None
            try:
                email_id = row["email_id"]
            except:
                html += "<p> Please have an 'email_id' column in your csv file </p> </html>"
                send_email.s((html, eid, subject)).apply_async()
                flag = -1
                break
            try:
                role = row["roles"]
                role = str_to_int_roles(role)
            except:
                flag = 1
                continue
            secure_str = ''.join((secrets.choice(string.ascii_letters) for i in range(8)))
            user_name=generate_username(1)[0]
            user = User(user_name=user_name,email_id=email_id,password=secure_str,role_id=role)
            db.session.add(user)
            db.session.commit()

    if flag == 1:
            html += "<p> Either you don't have a 'roles' column in your csv or some roles were not amongst 'student', 'support agent', 'admin', 'manager'. Those not having an appropriate role haven't been added to the database. Rest have been added. </p> </html>"
            send_email.s((html, eid, subject)).apply_async()
            return 'Roles Improperly specified'
    elif flag == -1:
         return 'email_id column not found'
    else:
        subject = "Your import job has been successfully processed"
        html += "<p> All users have been added successfully to the database. </p> </html>"
        send_email.s((html, eid, subject)).apply_async()
        return "Success"