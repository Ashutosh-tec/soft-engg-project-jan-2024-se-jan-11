# # # Celery Tasks, FAQApi
# # # GET: Check Status Code and Key-Value Pairs
# # # POST/PATCH: Check Status Code, GET Request and Check Key-Value Pairs
# # # DELETE: Delete Request, Get Status Code, GET Request and raise Error/not 200 status code
import pytest
from application.tasks import send_email, response_notification, unanswered_ticket_notification
from application.tasks import celery
from celery import chain


#Send Email test case when html, subject and email id is correct
def test_send_email_all_parameters_okay():
    html = '<html> <p> Hi! </p> </html>'
    eid = 'calyx.keadon@dollstore.org'
    subject = 'This is a subject'
    email = (html,eid,subject)
    assert send_email.s(email).apply_async().get() == 200

# Email variable should be a tuple of the form (html, email_address, subject)
def test_send_email_improper_tuple_supplied():
    html = '<html> <p> Hi! </p> </html>'
    subject = 'This is a subject'
    email = (html, subject)
    with pytest.raises(ValueError):
        send_email.s(email).apply_async().get()

#Improper Email Address
def test_incorrect_email_address():
    html = '<html> <p> Hi! </p> </html>'
    subject = 'This is a subject'
    eid = 'abc'
    email = (html,eid,subject)
    assert send_email.s(email).apply_async().get() == 400

#All Fields properly defined for Response Notification, whatever error you get will be from 
def test_response_notfication_all_okay():
    ticket_obj = {'title': 'Problems with my ID Card', 'ticket_id': 1, 'creator_id': 1, 'creator_email': 'redding.abba@dollstore.org'}
    response_obj = {'responder_id': 2, 'response': 'test response', 'response_id': 17, 'responder_uname': 'chirag'}
    send_notification = chain(response_notification.s(ticket_obj = ticket_obj, response_obj=response_obj), send_email.s()).apply_async()
    assert send_notification.get() == 200

#One Or more keys missing from expected input
def test_response_notification_inadequate_data_passed():
    ticket_obj = {'title': 'Problems with my ID Card', 'ticket_id': 1, 'creator_id': 1,}
    response_obj = {'responder_id': 2, 'response': 'test response', 'response_id': 17, 'responder_uname': 'chirag'}
    send_notification = chain(response_notification.s(ticket_obj = ticket_obj, response_obj=response_obj), send_email.s()).apply_async()
    with pytest.raises(KeyError):
        send_notification.get()

import requests
from flask import json
BASE="http://127.0.0.1:5000"

def token_login_student():
    url=BASE+"/login"
    data={"email":"redding.abba@dollstore.org","password":"arya"}
    response=requests.post(url,data=data)
    return response.json()["token"]

def token_login_support_agent():
    url=BASE+"/login"
    data={"email":"chirag@chirag.com","password":"chirag"}
    response=requests.post(url,data=data)
    return response.json()["token"]

def token_login_admin():
    url=BASE+"/login"
    data={"email":"varun@varun.com","password":"varun"}
    response=requests.post(url,data=data)
    return response.json()["token"]

def test_response_check():
    response=requests.get(BASE)
    assert response.status_code==200

# FAQ ENDPOINT TESTING #
url_faq=BASE+"/api/faq"
from application.models import FAQ

# GET REQUEST FOR STUDENT #
def test_faq_authorized_get():
    header={"secret_authtoken":token_login_student()}
    request=requests.get(url_faq,headers=header)
    faqs=FAQ.query.all()
    response=request.json()
    responses=response['data']
    assert request.status_code==200
    assert len(list(faqs)) == len(responses)
    for d in responses:
        for q in faqs:
            if q.ticket_id == d['ticket_id']:
                assert d['ticket_id'] ==  q.ticket_id
                assert d['category'] == q.category
                assert d['is_approved'] == q.is_approved

def test_faq_inauthenticated_get():
    request=requests.get(url_faq)
    response=request.json()
    assert request.status_code==200
    assert response['status']=='unsuccessful, missing the authtoken'

## POST REQUEST ##
def test_faq_unauthorized_role_post():
    data = json.dumps({ "category": "operational","is_approved": False, "ticket_id": 2})
    header={"secret_authtoken":token_login_student(), "Content-Type":"application/json"}
    request=requests.post(url_faq,data=data, headers=header)
    assert request.status_code==403
    assert request.json()['message']=="Unauthorized"

def test_faq_inauthenticated_post():
    data = json.dumps({ "category": "operational","is_approved": False, "ticket_id": 2})
    header={"Content-Type":"application/json"}
    request=requests.post(url_faq,data=data)
    assert request.status_code==200
    assert request.json()['status']=='unsuccessful, missing the authtoken'

def test_faq_authorized_role_post_no_ticket_id():
    data = json.dumps({ "category": "operational","is_approved": False})
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.post(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="ticket_id is required and should be integer"

def test_faq_authorized_role_post_no_category():
    data = json.dumps({"is_approved": False, "ticket_id": 2})
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.post(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="category is required and should be string"

def test_faq_authorized_role_post_no_is_approved():
    data = json.dumps({ "category": "operational", "ticket_id": 2})
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.post(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="is_approved is required and should be boolean"

def test_faq_authorized_role_post_nonexistant_ticket_id():
    input_dict = { "category": "operational","is_approved": False, "ticket_id": 10000}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.post(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="ticket_id does not exist"
    assert FAQ.query.filter_by(ticket_id=input_dict["ticket_id"]).first() is None

def test_faq_authorized_role_post_nonexistant_category():
    input_dict = { "category": "abc","is_approved": False, "ticket_id": 2}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.post(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="category does not exist"
    assert FAQ.query.filter_by(ticket_id=input_dict["ticket_id"]).first() is None

def test_faq_authorized_role_post_invalid_isapproved():
    input_dict = { "category": "operational","is_approved": "abs", "ticket_id": 2}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.post(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="is_approved must be boolean"
    assert FAQ.query.filter_by(ticket_id=input_dict["ticket_id"]).first() is None

def test_faq_authorized_role_post_ticket_already_in_db():
    data = json.dumps({ "category": "operational","is_approved": False, "ticket_id": 1})
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.post(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="ticket already in FAQ"

def test_faq_authorized_role_post_valid_data():
    input_dict = { "category": "operational","is_approved": False, "ticket_id": 2}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.post(url_faq,data=data, headers=header)
    assert request.status_code==200
    assert request.json()['message']=="FAQ item added successfully"
    faq = FAQ.query.filter_by(ticket_id=2).first()
    assert input_dict["category"] == faq.category
    assert input_dict["is_approved"] == faq.is_approved

## DELETE REQUEST ##
delete_url = url_faq+'/2'

def test_faq_authorized_role_delete_valid():
    header={"secret_authtoken":token_login_admin()}
    request=requests.delete(delete_url, headers=header)
    assert request.status_code==200
    assert request.json()['message']=="FAQ item deleted successfully"
    assert FAQ.query.filter_by(ticket_id=2).first() is None

def test_faq_unauthorized_role_delete():
    header={"secret_authtoken":token_login_student()}
    request=requests.delete(delete_url, headers=header)
    assert request.status_code==403
    assert request.json()['message']=="Unauthorized"

def test_faq_inauthenticated_delete():
    request=requests.delete(delete_url)
    assert request.status_code==200
    assert request.json()['status']=='unsuccessful, missing the authtoken'

def test_faq_authorized_role_delete_nonexistant_ticket():
    header={"secret_authtoken":token_login_admin()}
    request=requests.delete(url_faq+'/1000', headers=header)
    assert request.status_code==400
    assert request.json()['message']=="ticket_id does not exist"

def test_faq_authroized_role_delete_ticket_not_in_faq():
    header={"secret_authtoken":token_login_admin()}
    request=requests.delete(url_faq+'/2', headers=header)
    assert request.status_code==400
    assert request.json()['message']=="ticket_id is not in FAQ"

## PATCH ## 

def test_faq_inauthenticated_patch():
    request=requests.patch(delete_url)
    assert request.status_code==200
    assert request.json()['status']=='unsuccessful, missing the authtoken'

def test_faq_unauthorized_role_patch():
    data = json.dumps({ "category": "operational","is_approved": False, "ticket_id": 2})
    header={"secret_authtoken":token_login_student(), "Content-Type":"application/json"}
    request=requests.patch(url_faq,data=data, headers=header)
    assert request.status_code==403
    assert request.json()['message']=="Unauthorized"

def test_faq_authorized_role_patch_no_ticket_id():
    data = json.dumps({ "category": "operational","is_approved": False})
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.patch(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="ticket_id is required and should be integer"

def test_faq_authorized_role_patch_no_category():
    input_dict = {"is_approved": False, "ticket_id": 1}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.patch(url_faq,data=data, headers=header)
    assert request.status_code==200
    assert request.json()['message']=="FAQ item updated successfully"
    assert input_dict["is_approved"]==FAQ.query.filter_by(ticket_id=1).first().is_approved

def test_faq_authorized_role_patch_no_is_approved():
    input_dict = { "category": "operational", "ticket_id": 1}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.patch(url_faq,data=data, headers=header)
    assert request.status_code==200
    assert request.json()['message']=="FAQ item updated successfully"
    assert input_dict["category"] == FAQ.query.filter_by(ticket_id=1).first().category

def test_faq_authorized_role_patch_nonexistant_ticket_id():
    data = json.dumps({ "category": "operational","is_approved": False, "ticket_id": 10000})
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.patch(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="ticket_id does not exist"
    assert not FAQ.query.filter_by(ticket_id=10000).first() 

def test_faq_authorized_role_patch_nonexistant_category():
    input_dict={ "category": "abc","is_approved": False, "ticket_id": 1}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.patch(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="category does not exist"
    assert input_dict["category"] != FAQ.query.filter_by(ticket_id=1).first().category


def test_faq_authorized_role_patch_invalid_isapproved():
    input_dict = { "category": "operational","is_approved": "abs", "ticket_id": 1}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.patch(url_faq,data=data, headers=header)
    assert request.status_code==400
    assert request.json()['message']=="is_approved must be boolean"
    assert input_dict["is_approved"] != FAQ.query.filter_by(ticket_id=1).first().is_approved


def test_faq_authorized_role_patch_valid_data():
    input_dict = { "category": "random","is_approved": False, "ticket_id": 1}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.patch(url_faq,data=data, headers=header)
    assert request.status_code==200
    assert request.json()['message']=="FAQ item updated successfully"
    faq = FAQ.query.filter_by(ticket_id=1).first()
    assert input_dict["category"] == faq.category
    assert input_dict["is_approved"] == faq.is_approved


from application import create_app, db
from application.config import CeleryTesting
from application.tasks import unanswered_ticket_notification, poor_resolution_time
from application.models import User, Ticket, Response

@pytest.fixture
def app():
    def _app(config_class):
        app, api, celery = create_app(config_class)
        if config_class is CeleryTesting:
            db.drop_all()
            # from application import models
            db.create_all()
            new_student = User(user_name='student', password='password', email_id='student@student.com', role_id=1)
            new_agent = User(user_name='agent', password='password2', email_id='agent@agent.com', role_id=2)
            new_manager = User(user_name='manager', password='password3', email_id='ascher.daymon@dollstore.org', role_id=4)
            new_student2 = User(user_name='student2', password='password4', email_id='student2@student.com', role_id=1)
            db.session.add(new_student)
            db.session.add(new_agent)
            db.session.add(new_manager)
            db.session.add(new_student2)
            db.session.commit()
        return app
    
    yield _app
    db.session.remove()
    if str(db.engine.url) == CeleryTesting.SQLALCHEMY_DATABASE_URI:
        db.drop_all()

from datetime import datetime, timedelta
def test_unanswered_tickets_notification_email_sent_three_day_old_ticket_no_support_response(app):
    three_days_ago = datetime.now() - timedelta(hours=72)
    app = app(CeleryTesting)
    new_ticket = Ticket(title='test', description = 'test desc', creation_date = three_days_ago, creator_id=1, number_of_upvotes=0, is_read=False, is_open=True, is_offensive=False, is_FAQ=False)
    db.session.add(new_ticket)
    db.session.commit()
    assert unanswered_ticket_notification() == 'Notification Sent'


def test_unanswered_tickets_notification_email_not_sent_ticket_is_not_open(app):
    three_days_ago = datetime.now() - timedelta(hours=72)
    app = app(CeleryTesting)
    new_ticket = Ticket(title='test', description = 'test desc', creation_date = three_days_ago, creator_id=1, number_of_upvotes=0, is_read=False, is_open=False, is_offensive=False, is_FAQ=False)
    db.session.add(new_ticket)
    db.session.commit()
    assert unanswered_ticket_notification() == 'No Unresolved Tickets'

def test_unanswered_tickets_notification_email_not_sent_as_ticket_open_but_response_from_agent(app):
    three_days_ago = datetime.now() - timedelta(hours=72)
    app = app(CeleryTesting)
    new_ticket = Ticket(title='test', description = 'test desc', creation_date = three_days_ago, creator_id=1, number_of_upvotes=0, is_read=False, is_open=True, is_offensive=False, is_FAQ=False)
    new_response = Response(ticket_id=1, response='test', responder_id=2, response_timestamp=datetime.now())
    db.session.add(new_ticket)
    db.session.add(new_response)
    db.session.commit()
    assert unanswered_ticket_notification() == 'All Tickets Answered'

def test_unanswered_tickets_notification_email_sent_as_ticket_open_and_response_by_another_student_but_not_agent(app):
    three_days_ago = datetime.now() - timedelta(hours=72)
    app = app(CeleryTesting)
    new_ticket = Ticket(title='test', description = 'test desc', creation_date = three_days_ago, creator_id=1, number_of_upvotes=0, is_read=False, is_open=True, is_offensive=False, is_FAQ=False)
    new_response = Response(ticket_id=1, response='test', responder_id=4, response_timestamp=datetime.now())
    db.session.add(new_ticket)
    db.session.add(new_response)
    db.session.commit()
    assert unanswered_ticket_notification() == 'Notification Sent'

def test_poor_resolution_time_email_sent_due_to_poor_performance(app):
    three_days_ago = datetime.now() - timedelta(hours=72)
    app = app(CeleryTesting)
    new_ticket = Ticket(title='test', description = 'test desc', creation_date = three_days_ago, creator_id=1, number_of_upvotes=0, is_read=False, is_open=False, is_offensive=False, is_FAQ=False)
    new_response = Response(ticket_id=1, response='test', responder_id=2, response_timestamp=datetime.now())
    db.session.add(new_ticket)
    db.session.add(new_response)
    db.session.commit()
    assert poor_resolution_time() == 'Email sent with details of agents with poor resolution time'

def test_poor_resolution_time_email_not_sent_due_to_good_performance(app):
    one_day_ago = datetime.now() - timedelta(hours=24)
    app = app(CeleryTesting)
    new_ticket = Ticket(title='test', description = 'test desc', creation_date = one_day_ago, creator_id=1, number_of_upvotes=0, is_read=False, is_open=False, is_offensive=False, is_FAQ=False)
    new_response = Response(ticket_id=1, response='test', responder_id=2, response_timestamp=datetime.now())
    db.session.add(new_ticket)
    db.session.add(new_response)
    db.session.commit()
    assert poor_resolution_time() == 'All Agents have have a resolution time less than 48 hours in the past 30 days'

def test_poor_resolution_time_email_not_sent_if_average_resolution_time_is_48(app):
    now = datetime.now()
    fourty_eight_hours_ago = now - timedelta(hours=48)
    app = app(CeleryTesting)
    new_ticket = Ticket(title='test', description = 'test desc', creation_date = fourty_eight_hours_ago, creator_id=1, number_of_upvotes=0, is_read=False, is_open=False, is_offensive=False, is_FAQ=False)
    new_response = Response(ticket_id=1, response='test', responder_id=2, response_timestamp=now)
    db.session.add(new_ticket)
    db.session.add(new_response)
    db.session.commit()
    assert poor_resolution_time() == 'All Agents have have a resolution time less than 48 hours in the past 30 days'

def test_poor_resolution_time_email_not_sent_if_average_resolution_time_is_greater_than_48_but_thats_for_tickets_older_than_a_month(app):
    now = datetime.now()
    thirty_one_days_ago = now - timedelta(days=31)
    app = app(CeleryTesting)
    new_ticket = Ticket(title='test', description = 'test desc', creation_date = thirty_one_days_ago, creator_id=1, number_of_upvotes=0, is_read=False, is_open=False, is_offensive=False, is_FAQ=False)
    new_response = Response(ticket_id=1, response='test', responder_id=2, response_timestamp=now)
    db.session.add(new_ticket)
    db.session.add(new_response)
    db.session.commit()
    assert poor_resolution_time() == 'All Agents have have a resolution time less than 48 hours in the past 30 days'