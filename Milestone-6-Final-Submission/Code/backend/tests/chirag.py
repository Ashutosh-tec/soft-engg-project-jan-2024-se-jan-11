# Ticket, User, ImportResourceUser Celery Task
# GET: Check Status Code and Key-Value Pairs
# POST/PATCH: Check Status Code, GET Request and Check Key-Value Pairs
# DELETE: Delete Request, Get Status Code, GET Request and raise Error/not 200 status code
import requests
from flask import json
#import db models here
import sys
import os

SCRIPT_DIRP = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIRP))

from application.models import User,Ticket
BASE="http://127.0.0.1:5000"
url_ticket=BASE+"/api/ticket"
url_user=BASE+"/api/user"

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
    
def test_ticket_student_get():
    header={"secret_authtoken":token_login_student()}
    request=requests.get(url_ticket,headers=header)
    ticket=Ticket.query.filter_by(creator_id=1).all()
    response=request.json()
    response=response['data']
    assert request.status_code==200
    for i in ticket:
        for j in response: 
            if(j["ticket_id"]==i.ticket_id):
                assert j["creator_id"]==i.creator_id
                assert j["title"]==i.title
                assert j["description"]==i.description
                assert j["number_of_upvotes"]==i.number_of_upvotes
                assert j["is_read"]==i.is_read
                assert j["is_open"]==i.is_open
                assert j["is_FAQ"]==i.is_FAQ
                assert j["is_offensive"]==i.is_offensive
                assert j["rating"]==i.rating

def test_ticket_admin_get():
    header={"secret_authtoken":token_login_admin()}
    request=requests.get(url_ticket,headers=header)
    assert request.status_code==403
    
def test_ticket_support_agent_get():
    header={"secret_authtoken":token_login_support_agent()}
    request=requests.get(url_ticket,headers=header)
    assert request.status_code==403
    
def test_ticket_student_post():
    header={"secret_authtoken":token_login_student(),"Content-Type":"application/json"}
    data={
        "title":"test1234",
        "description":"hi",
        "number_of_upvotes":13,
        "is_read":0,
        "is_open":1,
        "is_offensive":0,
        "is_FAQ":0
        }
    data=json.dumps(data)
    response=requests.post(url_ticket,data=data,headers=header)
    assert response.status_code==200
    response_get=requests.get(url_ticket,headers=header)
    response_get=response_get.json()
    response_get=response_get['data']
    for i in response_get:
        if(i["title"]=="test1234"):
            assert i["description"]=="hi"
            assert i["number_of_upvotes"]==13
            assert i["is_read"]==0
            assert i["is_open"]==1
            assert i["is_offensive"]==0
            assert i["is_FAQ"]==0
   
def test_ticket_admin_post():
    header={"secret_authtoken":token_login_admin(),"Content-Type":"application/json"}
    data={
        "title":"test1234",
        "description":"hi",
        "number_of_upvotes":13,
        "is_read":0,
        "is_open":1,
        "is_offensive":0,
        "is_FAQ":0
        }
    data=json.dumps(data)
    response=requests.post(url_ticket,data=data,headers=header)
    assert response.status_code==403
    
def test_ticket_support_agent_post():
    header={"secret_authtoken":token_login_support_agent(),"Content-Type":"application/json"}
    data={
        "title":"test1234",
        "description":"hi",
        "number_of_upvotes":13,
        "is_read":0,
        "is_open":1,
        "is_offensive":0,
        "is_FAQ":0
        }
    data=json.dumps(data)
    response=requests.post(url_ticket,data=data,headers=header)
    assert response.status_code==403
    
def test_ticket_title_student_patch():
    header={"secret_authtoken":token_login_student(),"Content-Type":"application/json"}
    payload={
        "ticket_id":3,
        "title":"test",
    }
    payload=json.dumps(payload)
    response=requests.patch(url_ticket,data=payload,headers=header)
    assert response.status_code==200
    response_get=requests.get(url_ticket,headers=header)
    response_get=response_get.json()
    response_get=response_get['data']
    for i in response_get:
        if(i["ticket_id"]==3):
            assert i["title"]=="test"
    
def test_ticket_admin_patch():
    header={"secret_authtoken":token_login_admin(),"Content-Type":"application/json"}
    payload={
        "ticket_id":3,
        "title":"test",
    }
    payload=json.dumps(payload)
    response=requests.patch(url_ticket,data=payload,headers=header)
    assert response.status_code==403
    
def test_ticket_support_agent_patch():
    header={"secret_authtoken":token_login_support_agent(),"Content-Type":"application/json"}
    payload={
        "ticket_id":3,
        "title":"test",
    }
    payload=json.dumps(payload)
    response=requests.patch(url_ticket,data=payload,headers=header)
    assert response.status_code==403
    
def test_ticket_student_delete():
    url=url_ticket+"/3"
    header={"secret_authtoken":token_login_student(),"Content-Type":"application/json"}
    response=requests.delete(url,headers=header)
    assert response.status_code==200
    ticket=Ticket.query.filter_by(ticket_id=3).first()
    assert ticket==None
    
def test_ticket_admin_delete():
    url=url_ticket+"/3"
    header={"secret_authtoken":token_login_admin(),"Content-Type":"application/json"}
    response=requests.delete(url,headers=header)
    assert response.status_code==400
    
def test_ticket_support_agent_delete():
    url=url_ticket+"/3"
    header={"secret_authtoken":token_login_support_agent(),"Content-Type":"application/json"}
    response=requests.delete(url,headers=header)
    assert response.status_code==400

def test_user_student_get():
    header={"secret_authtoken":token_login_student()}
    response=requests.get(url_user,headers=header)
    assert response.status_code==403

def test_user_support_agent_get():
    header={"secret_authtoken":token_login_support_agent()}
    response=requests.get(url_user,headers=header)
    assert response.status_code==403
    
def test_user_admin_get():
    header={"secret_authtoken":token_login_admin()}
    response=requests.get(url_user,headers=header)
    assert response.status_code==200
    user=User.query.all()
    response=response.json()
    response=response['data']
    for i in user:
        for j in response:
            if(i.user_id==j['user_id']):
                assert i.user_name==j['user_name']
                assert i.email_id==j['email_id']
                assert i.role_id==j['role_id']
                
def test_user_student_post():
    header={"secret_authtoken":token_login_student(),"Content-Type":"application/json"}
    data={
        "email_id":"test@test",
        "role_id":1
    }
    data=json.dumps(data)
    response=requests.post(url_user,data=data,headers=header)
    assert response.status_code==403
    
def test_user_support_agent_post():
    header={"secret_authtoken":token_login_support_agent(),"Content-Type":"application/json"}
    data={
        "email_id":"test@test",
        "role_id":1
    }
    data=json.dumps(data)
    response=requests.post(url_user,data=data,headers=header)
    assert response.status_code==403
    
def test_user_admin_post():
    header={"secret_authtoken":token_login_admin(),"Content-Type":"application/json"}
    data={
        "email_id":"test@test",
        "role_id":1
    }
    data=json.dumps(data)
    response=requests.post(url_user,data=data,headers=header)
    assert response.status_code==200
    response_get=requests.get(url_user,headers=header)
    response_get=response_get.json()
    response_get=response_get['data']
    for i in response_get:
        if(i["email_id"]=="test@test"):
            assert i["role_id"]==1
    
def test_user_student_patch():
    header={"secret_authtoken":token_login_student(),"Content-Type":"application/json"}
    data={"user_name":"test","user_id":8}
    data=json.dumps(data)
    response=requests.patch(url_user,data=data,headers=header)
    assert response.status_code==200

def test_user_support_agent_patch():
    header={"secret_authtoken":token_login_support_agent(),"Content-Type":"application/json"}
    data={"user_name":"test","user_id":8}
    data=json.dumps(data)
    response=requests.patch(url_user,data=data,headers=header)
    assert response.status_code==200
    
def test_user_admin_patch():
    header={"secret_authtoken":token_login_admin(),"Content-Type":"application/json"}
    data={"user_name":"test","user_id":8,"email_id":"test12@test"}
    data=json.dumps(data)
    response=requests.patch(url_user,data=data,headers=header)
    assert response.status_code==200
    response_get=requests.get(url_user,headers=header)
    response_get=response_get.json()
    response_get=response_get['data']
    for i in response_get:
        if(i["user_id"]==8):
            assert i["user_name"]=="test"
            assert i["email_id"]=="test12@test"

def test_user_student_delete():
    url=url_user+"/8"
    header={"secret_authtoken":token_login_student(),"Content-Type":"application/json"}
    response=requests.delete(url,headers=header)
    assert response.status_code==403
    
def test_user_support_agent_delete():
    url=url_user+"/8"
    header={"secret_authtoken":token_login_support_agent(),"Content-Type":"application/json"}
    response=requests.delete(url,headers=header)
    assert response.status_code==403

def test_user_admin_delete():
    url=url_user+"/8"
    header={"secret_authtoken":token_login_admin(),"Content-Type":"application/json"}
    response=requests.delete(url,headers=header)
    assert response.status_code==200
    user=User.query.filter_by(user_id=8).first()
    assert user==None
        
# def test_import_resources_admin():
#     url=BASE+"/api/importUsers"
    