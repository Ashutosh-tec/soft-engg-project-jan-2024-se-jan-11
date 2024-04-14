## TicketAll, GetResolutionTimes, FlaggedPostAPI, ResponseAPI_by_ticket, getResponseAPI_by_ticket, ResponseAPI_by_user, ResponseAPI_by_response_id
# GET: Check Status Code and Key-Value Pairs
# POST/PATCH: Check Status Code, GET Request and Check Key-Value Pairs
# DELETE: Delete Request, Get Status Code, GET Request and raise Error/not 200 status code

import requests
from flask import json
#import db models here
import sys
import os
from datetime import datetime

SCRIPT_DIRP = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIRP))

from application.models import Ticket, Response, Flagged_Post
BASE="http://127.0.0.1:5000"
url_ticket_all=BASE+"/api/ticketAll"
url_getResolutionTimes=BASE+"/api/getResolutionTimes"
url_flaggedPosts = BASE+"/api/flaggedPosts"
url_respResp = BASE+ "/api/respResp"
url_respUser = BASE+"/api/respUser"
url_getRespTicket = BASE+"/api/getResponseAPI_by_ticket"
url_RespTicket = BASE+"/api/respTicket"
url_RespDelete = BASE+"/api/respRespDel/2/8"
url_RespDelete2 = BASE+"/api/respRespDel/2/13"

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

def token_login_manager():
    url = BASE+"/login"
    data = {"email": "boss@boss.com", "password": "boss"}
    response = requests.post(url, data = data)
    return response.json()["token"]

#TICKET ALL GET Request.

def test_ticket_all_get():
    header = {"secret_authtoken":token_login_student()}
    request=requests.get(url_ticket_all,headers=header)
    tickets = list(Ticket.query.filter_by().all())
    response = request.json()
    responses = response["data"]
    assert request.status_code==200
    for d in responses:
        for q in tickets:
            if q.ticket_id == d['ticket_id']:
                assert d['ticket_id'] ==  q.ticket_id
                assert d['title']==q.title
                assert d['description']==q.description
                assert d['creation_date']== str(q.creation_date)
                assert d['creator_id']==q.creator_id
                assert d['number_of_upvotes']==q.number_of_upvotes
                assert d['is_read']==q.is_read
                assert d['is_open']==q.is_open
                assert d['is_offensive']== q.is_offensive
                assert d['is_FAQ']==q.is_FAQ
                assert d['rating']==q.rating
    assert len(tickets) == len(responses)
def test_ticket_all_unauthenticated_get():
    request=requests.get(url_ticket_all)
    response=request.json()
    assert request.status_code==200
    assert response['status']=='unsuccessful, missing the authtoken'

# TICKET ALL PATCH request

def test_ticket_all_patch():
    input_dict = { "number_of_upvotes": 146,"is_read": False, "ticket_id": 2}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.patch(url_ticket_all,data=data, headers=header)
    assert request.status_code==200
    assert request.json()['message']=="success"
    ticket = Ticket.query.filter_by(ticket_id=input_dict["ticket_id"]).first()
    assert input_dict["number_of_upvotes"] == ticket.number_of_upvotes
    assert input_dict["is_read"] == ticket.is_read

def test_ticket_all_patch_ticket_not_found():
    input_dict = { "number_of_upvotes": 10023,"is_read": False, "ticket_id": 1e4}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.patch(url_ticket_all,data=data, headers=header)
    assert request.status_code==404
    assert request.json()['message']=="There is no such ticket by that ID"

def test_ticket_all_patch_no_ticket_id():
    input_dict = { "number_of_upvotes": 10023,"is_read": False}
    data = json.dumps(input_dict)
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.patch(url_ticket_all,data=data, headers=header)
    assert request.status_code==403
    assert request.json()['message']=="Please mention the ticketId field in your form"


def test_ticket_all_unauthenticated_patch():
    request=requests.patch(url_ticket_all)
    response=request.json()
    assert request.status_code==200
    assert response['status']=='unsuccessful, missing the authtoken'

#GETRESOLUTIONTIMES POST REQUEST

def test_getResolutionTimes_post_unauthenticated():
    request=requests.post(url_getResolutionTimes)
    response=request.json()
    assert request.status_code==200
    assert response['status']=='unsuccessful, missing the authtoken'

def test_getResolutionTimes_post_wrong_role():
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    input_dict = { "number_of_upvotes": 10023,"is_read": False, "ticket_id": 1e4}
    data = json.dumps(input_dict)
    request=requests.post(url = url_getResolutionTimes,data = data, headers=header)
    response = request.json()
    assert request.status_code == 404
    assert response["message"] == "You are not authorized to access this feature!"

def test_getResolutionTimes_post_no_ticket_id():
    header={"secret_authtoken":token_login_manager(), "Content-Type":"application/json"}
    input_dict = {}
    data = json.dumps(input_dict)
    request=requests.post(url = url_getResolutionTimes,data = data, headers=header)
    response = request.json()
    assert request.status_code == 403
    assert response["message"] == "Please enter the ticket ID."
    
def test_getResolutionTimes_post_ticket_isopen():
    header={"secret_authtoken":token_login_manager(), "Content-Type":"application/json"}
    input_dict = {"ticket_id": 1}
    data = json.dumps(input_dict)
    request=requests.post(url = url_getResolutionTimes,data = data, headers=header)
    response = request.json()
    assert request.status_code == 404
    assert response["message"] == "This ticket hasn't been responded to yet or is still open!"

def test_getResolutionTimes_post_wrong_ticket_id():
    header={"secret_authtoken":token_login_manager(), "Content-Type":"application/json"}
    input_dict = {"ticket_id": 1000}
    data = json.dumps(input_dict)
    request=requests.post(url = url_getResolutionTimes,data = data, headers=header)
    response = request.json()
    assert request.status_code == 404
    assert response["message"] == "No such ticket exists by the given ticket ID."

def test_getResolutionTimes_post():
    #Only checks if days, seconds, microseconds and ticket IDs match
    header={"secret_authtoken":token_login_manager(), "Content-Type":"application/json"}
    input_dict = {"ticket_id": [1,2]} 
    data = json.dumps(input_dict)
    request=requests.post(url = url_getResolutionTimes,data = data, headers=header)
    response = request.json()
    assert request.status_code == 200
    if isinstance(input_dict["ticket_id"], int):
        responses = Response.query.filter_by(ticket_id = input_dict["ticket_id"]).all()
        responses = list(responses)
        ticket = Ticket.query.filter_by(ticket_id = input_dict["ticket_id"]).first()
        a = {}
        response_times = []
        for thing in responses:
            if isinstance(thing.response_timestamp, datetime):
                #print("Here 1")
                response_times.append(thing.response_timestamp)
            elif isinstance(thing.response_timestamp, str):
                #print("Here 2")
                response_times.append(datetime.strptime(thing.response_timestamp,'%Y-%m-%d %H:%M:%S.%f'))
            response_time = max(response_times)
            a["creation_time"] = None
            if isinstance(ticket.creation_date, str):
                a["creation_time"] = datetime.strptime(ticket.creation_date, '%Y-%m-%d %H:%M:%S.%f')
            elif isinstance(ticket.creation_date, datetime):
                a["creation_time"] = ticket.creation_date
            a["response_time"] = response_time
            a["resolution_time_datetime_format"] = a["response_time"] - a["creation_time"]
            a["days"] = a["resolution_time_datetime_format"].days
            a["seconds"] = a["resolution_time_datetime_format"].seconds
            a["microseconds"] = a["resolution_time_datetime_format"].microseconds
            a["resolution_time_datetime_format"] = str(a["resolution_time_datetime_format"])
            a["creation_time"] = a["creation_time"]
            a["ticket_id"] = input_dict["ticket_id"]
            a["response_time"] = None
            a["resolution_time_datetime_format"] = None
            a["creation_time"] = None
        d = response["data"]
        for keys in a:
            if a[keys] is not None:
                assert a[keys] == d[keys]
    elif isinstance(input_dict["ticket_id"], list):
        data = []        
        for item in input_dict["ticket_id"]:
            d = {}
            ticket = None
            ticket = Ticket.query.filter_by(ticket_id = item).first()
            if ticket is None:
                continue
            if isinstance(ticket.creation_date, str):
                d["creation_time"] = datetime.strptime(ticket.creation_date, '%Y-%m-%d %H:%M:%S.%f')
            elif isinstance(ticket.creation_date, datetime):
                d["creation_time"] = ticket.creation_date
            responses = Response.query.filter_by(ticket_id = item).all()
            if ticket.is_open == False:
                responses = list(responses)
                response_times = []
                for thing in responses:
                    if isinstance(thing.response_timestamp, datetime):
                        response_times.append(thing.response_timestamp)
                    elif isinstance(thing.response_timestamp, str):
                        #print("Here 2")
                        response_times.append(datetime.strptime(thing.response_timestamp,'%Y-%m-%d %H:%M:%S.%f'))
                    
                response_time = max(response_times)
                d["response_time"] = response_time
                d["resolution_time_datetime_format"] = d["response_time"] - d["creation_time"]
                d["days"] = d["resolution_time_datetime_format"].days
                d["seconds"] = d["resolution_time_datetime_format"].seconds
                d["microseconds"] = d["resolution_time_datetime_format"].microseconds
                d["response_time"] = d["response_time"]
                d["resolution_time_datetime_format"] = str(d["resolution_time_datetime_format"])
                d["creation_time"] = d["creation_time"]
                d["ticket_id"] = item
                d["response_time"] = None
                d["resolution_time_datetime_format"] = None
                d["creation_time"] = None
                data.append(d)
        x = response["data"]
        for item in x:
            for thing in data:
                if item["ticket_id"] == thing["ticket_id"]:
                    for keys in thing:
                        if thing[keys] is not None:
                            assert thing[keys] == item[keys]

#FlaggedPost get request

def test_get_flaggedPost_wrong_role():
    header={"secret_authtoken":token_login_support_agent(), "Content-Type":"application/json"}
    request=requests.get(url = url_flaggedPosts, headers=header)
    response = request.json()
    assert request.status_code == 404
    assert response["message"] == "You are not authorized to access this feature."

def test_get_flaggedPost():
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.get(url = url_flaggedPosts, headers=header)
    response = request.json()
    assert request.status_code == 200
    flagged_posts = list(Flagged_Post.query.filter_by().all())
    d = response["data"]
    assert len(flagged_posts) == len(d)
    for item in flagged_posts:
        for thing in d:
            if item.ticket_id == thing["ticket_id"]:
                assert item.flagger_id == thing["flagger_id"]
                assert item.creator_id == thing["creator_id"]

def test_get_flaggedPost_unauthenticated():
    request=requests.get(url_flaggedPosts)
    response=request.json()
    assert request.status_code==200
    assert response['status']=='unsuccessful, missing the authtoken'

#FlaggedPost post request

def test_post_flaggedPost_wrong_role():
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    input_dict = { "ticket_id": 1,"flagger_id": 2, "creator_id": 1}
    data = json.dumps(input_dict)
    request=requests.post(url = url_flaggedPosts, headers=header, data = data)
    response = request.json()
    assert request.status_code == 404
    assert response["message"] == "You are not authorized to access this feature."

def test_post_flaggedPost_unauthenticated():
    request=requests.post(url_flaggedPosts)
    response=request.json()
    assert request.status_code==200
    assert response['status']=='unsuccessful, missing the authtoken'

def test_post_flaggedPost_missing_flagger_id():
    header={"secret_authtoken":token_login_support_agent(), "Content-Type":"application/json"}
    input_dict = { "ticket_id": 1, "creator_id": 1}
    data = json.dumps(input_dict)
    request=requests.post(url = url_flaggedPosts, headers=header, data = data)
    response = request.json()
    assert request.status_code == 403
    assert response["message"] == "Please pass the flagger ID."

def test_post_flaggedPost_missing_creator_id():
    header={"secret_authtoken":token_login_support_agent(), "Content-Type":"application/json"}
    input_dict = { "ticket_id": 1,"flagger_id": 2 }
    data = json.dumps(input_dict)
    request=requests.post(url = url_flaggedPosts, headers=header, data = data)
    response = request.json()
    assert request.status_code == 403
    assert response["message"] == "Please pass the creator ID."

def test_post_flaggedPost_missing_ticket_id():
    header={"secret_authtoken":token_login_support_agent(), "Content-Type":"application/json"}
    input_dict = { "creator_id": 1,"flagger_id": 2 }
    data = json.dumps(input_dict)
    request=requests.post(url = url_flaggedPosts, headers=header, data = data)
    response = request.json()
    assert request.status_code == 403
    assert response["message"] == "Please pass the Ticket ID."

def test_post_flaggedPost_wrong_flagger_id():
    header={"secret_authtoken":token_login_support_agent(), "Content-Type":"application/json"}
    input_dict = { "ticket_id": 1, "creator_id": 1,"flagger_id": 100 }
    data = json.dumps(input_dict)
    request=requests.post(url = url_flaggedPosts, headers=header, data = data)
    response = request.json()
    assert request.status_code == 403
    assert response["message"] == "The person who flagged must be a support agent."


def test_post_flaggedPost_wrong_creator_id():
    header={"secret_authtoken":token_login_support_agent(), "Content-Type":"application/json"}
    input_dict = { "ticket_id": 1, "creator_id": 100,"flagger_id": 2 }
    data = json.dumps(input_dict)
    request=requests.post(url = url_flaggedPosts, headers=header, data = data)
    response = request.json()
    assert request.status_code == 403
    assert response["message"] == "The person who created the post must be a student."


def test_post_flaggedPost_wrong_ticket_id():
    header={"secret_authtoken":token_login_support_agent(), "Content-Type":"application/json"}
    input_dict = { "ticket_id": 1000, "creator_id": 1,"flagger_id": 2 }
    data = json.dumps(input_dict)
    request=requests.post(url = url_flaggedPosts, headers=header, data = data)
    response = request.json()
    assert request.status_code == 403
    assert response["message"] == "The referenced ticket is not created by the referenced person/ the ticket doesn't exist in the first place."
"""
def test_post_flaggedPost():
    header={"secret_authtoken":token_login_support_agent(), "Content-Type":"application/json"}
    input_dict = { "ticket_id": 1, "creator_id": 1,"flagger_id": 2 }
    data = json.dumps(input_dict)
    request=requests.post(url = url_flaggedPosts, headers=header, data = data)
    response = request.json()
    assert request.status_code == 200
    assert response["status"] == "success"
    header2 = {"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request2 = requests.get(url = url_flaggedPosts, headers=header2)
    response2 = request2.json()
    for item in response2["data"]:
        if item["ticket_id"] == input_dict["ticket_id"]:
            assert item["creator_id"] == input_dict["creator_id"]
            assert item["flagger_id"] == input_dict["flagger_id"]
"""
#post request for ResponseAPI_by_response_id

def test_post_ResponseAPI_by_response_id_unauthenticated():
    request=requests.post(url_respResp)
    response=request.json()
    assert request.status_code==200
    assert response['status']=='unsuccessful, missing the authtoken'

def test_post_ResponseAPI_by_response_id_missing_response_id():
    header={"secret_authtoken":token_login_support_agent(), "Content-Type":"application/json"}
    input_dict = { }
    data = json.dumps(input_dict)
    request=requests.post(url = url_respResp, headers=header, data = data)
    response = request.json()
    assert request.status_code == 403
    assert response["message"] == "Please provide a response ID."
    
def test_post_ResponseAPI_by_response_id_wrong_response_id():
    header={"secret_authtoken":token_login_support_agent(), "Content-Type":"application/json"}
    input_dict = {"response_id": 1000 }
    data = json.dumps(input_dict)
    request=requests.post(url = url_respResp, headers=header, data = data)
    response = request.json()
    assert request.status_code == 200
    assert response["status"] == "succcess"
    assert response["data"] == []

def test_post_ResponseAPI_by_response_id():
    #Checks all values except timestamp
    header={"secret_authtoken":token_login_support_agent(), "Content-Type":"application/json"}
    input_dict = {"response_id": 1 }
    data = json.dumps(input_dict)
    request=requests.post(url = url_respResp, headers=header, data = data)
    response = request.json()
    assert request.status_code == 200
    response_table = Response.query.filter_by(response_id = input_dict["response_id"]).first()
    assert response["data"]["response_id"] == input_dict["response_id"]
    assert response["data"]["ticket_id"] == response_table.ticket_id
    assert response["data"]["response"] == response_table.response
    assert response["data"]["responder_id"] == response_table.responder_id

#post request for responseAPI by user

def test_post_ResponseAPI_by_user_unauthenticated():
    request=requests.post(url_respUser)
    response=request.json()
    assert request.status_code==200
    assert response['status']=='unsuccessful, missing the authtoken'

def test_post_ResponseAPI_by_user_wrong_role():
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    input_dict = { "responder_id": 2}
    data = json.dumps(input_dict)
    request=requests.post(url = url_respUser, headers=header, data = data)
    response = request.json()
    assert request.status_code == 404
    assert response["message"] == "Sorry, you don't have access to this feature!"

def test_post_ResponseAPI_by_user_missing_responder_id():
    header={"secret_authtoken":token_login_manager(), "Content-Type":"application/json"}
    input_dict = { }
    data = json.dumps(input_dict)
    request=requests.post(url = url_respUser, headers=header, data = data)
    response = request.json()
    assert request.status_code == 403
    assert response["message"] == "Please provide a responder ID for which you need the responses."

def test_post_ResponseAPI_by_user():
    #Checks everything apart from timestamp
    header={"secret_authtoken":token_login_manager(), "Content-Type":"application/json"}
    input_dict = { "responder_id": 2}
    data = json.dumps(input_dict)
    request=requests.post(url = url_respUser, headers=header, data = data)
    response = request.json()
    assert request.status_code == 200
    data = response["data"]
    responses = list(Response.query.filter_by(responder_id = input_dict["responder_id"]).all())
    assert len(data) == len(responses)
    for item in data:
        for thing in responses:
            if thing.response_id == item["response_id"]:
                assert thing.ticket_id == item["ticket_id"]
                assert thing.response == item["response"]
                assert thing.responder_id == item["responder_id"]
    
# post request for getResponseAPI_by_ticket

def test_post_getResponseAPI_by_ticket_unauthenticated():
    request=requests.post(url_getRespTicket)
    response=request.json()
    assert request.status_code==200
    assert response['status']=='unsuccessful, missing the authtoken'

def test_post_getResponseAPI_by_ticket_wrong_ticket_id():
    header={"secret_authtoken":token_login_manager(), "Content-Type":"application/json"}
    input_dict = { "ticket_id": 1000}
    data = json.dumps(input_dict)
    request=requests.post(url = url_getRespTicket, headers=header, data = data)
    response = request.json()
    assert request.status_code == 200
    assert response["data"] == []
    assert response["status"] == "success"

def test_post_getResponseAPI_by_ticket():
    #Checks everything except timestamps
    header={"secret_authtoken":token_login_manager(), "Content-Type":"application/json"}
    input_dict = { "ticket_id": 1}
    data = json.dumps(input_dict)
    request=requests.post(url = url_getRespTicket, headers=header, data = data)
    response = request.json()
    assert request.status_code == 200
    data = response["data"]
    responses = list(Response.query.filter_by(ticket_id = input_dict["ticket_id"]).all())
    assert len(responses) == len(data)
    for thing in responses:
        for item in data:
            if (thing.ticket_id == item["ticket_id"]) and (thing.response_id == item["response_id"]):
                assert thing.response == item["response"]
                assert thing.responder_id == item["responder_id"]
    assert response["status"] == "success"

#patch request for ResponseAPI_by_ticket

def test_patch_ResponseAPI_by_ticket_unauthorized():
    request = requests.patch(url_RespTicket)
    response=request.json()
    assert request.status_code==200
    assert response['status']=='unsuccessful, missing the authtoken'

def test_patch_ResponseAPI_by_ticket_wrong_role():
    header={"secret_authtoken":token_login_manager(), "Content-Type":"application/json"}
    input_dict = { "response_id": 1}
    data = json.dumps(input_dict)
    request=requests.patch(url = url_RespTicket, headers=header, data = data)
    response = request.json()
    assert request.status_code == 404
    assert response['message'] == "You are not authorized to update any responses."
    
def test_patch_ResponseAPI_by_ticket_missing_response_id():
    header={"secret_authtoken":token_login_student(), "Content-Type":"application/json"}
    input_dict = { }
    data = json.dumps(input_dict)
    request=requests.patch(url = url_RespTicket, headers=header, data = data)
    response = request.json()
    assert request.status_code == 404
    assert response['message'] == "Please provide the response id"

def test_patch_ResponseAPI_by_ticket_missing_response():
    header={"secret_authtoken":token_login_student(), "Content-Type":"application/json"}
    input_dict = { "response_id": 1}
    data = json.dumps(input_dict)
    request=requests.patch(url = url_RespTicket, headers=header, data = data)
    response = request.json()
    assert request.status_code == 404
    assert response['message'] == "Since your update response was blank, your earlier response hasn't been altered."

def test_patch_ResponseAPI_by_ticket_wrong_response_id_or_response_not_by_account():
    header={"secret_authtoken":token_login_student(), "Content-Type":"application/json"}
    input_dict = { "response_id": 1, "response": "Hello, this was a response change!"}
    data = json.dumps(input_dict)
    request=requests.patch(url = url_RespTicket, headers=header, data = data)
    response = request.json()
    assert request.status_code == 404
    assert response['message'] == "Either your response id is wrong, or this account is not the responder of the particular response."

def test_patch_ResponseAPI_by_ticket():
    #Verifies everything except timestamp
    header={"secret_authtoken":token_login_support_agent(), "Content-Type":"application/json"}
    input_dict = { "response_id": 1, "response": "Hello, this was a response change!"}
    data = json.dumps(input_dict)
    request=requests.patch(url = url_RespTicket, headers=header, data = data)
    response = request.json()
    assert request.status_code == 200
    assert response['status'] == "success"
    input_dict_2 = {"response_id": input_dict["response_id"]}
    data2 = json.dumps(input_dict_2)
    request2 = requests.post(url = url_respResp, data = data2, headers=header)
    response_request2 = request2.json()
    assert request2.status_code == 200
    assert response_request2["status"] == "success"
    assert response_request2["data"]["response_id"] == input_dict["response_id"]
    assert response_request2["data"]["response"] == input_dict["response"]

#delete request for ResponseAPI_by_responseID_delete
"""
def test_delete_ResponseAPI_by_response_id_delete():
    header={"secret_authtoken":token_login_support_agent(), "Content-Type":"application/json"}
    request=requests.delete(url = url_RespDelete, headers=header)
    response = request.json()
    assert request.status_code == 200
    assert response['status'] == "success"
    input_dict_2 = {"response_id": 8}
    data2 = json.dumps(input_dict_2)
    request2 = requests.post(url = url_respResp, data = data2, headers=header)
    response_request2 = request2.json()
    assert request2.status_code == 200
    assert response_request2["status"] == "succcess"
    assert len(response_request2["data"]) == 0
    assert response_request2["data"] == []
"""
def test_delete_ResponseAPI_by_response_id_wrong_role():
    header={"secret_authtoken":token_login_manager(), "Content-Type":"application/json"}
    request=requests.delete(url = url_RespDelete, headers=header)
    response = request.json()
    assert response["message"] == "You are not authorized to delete responses."
    assert request.status_code == 404
"""
def test_delete_ResponseAPI_by_response_id_admin():
    header={"secret_authtoken":token_login_admin(), "Content-Type":"application/json"}
    request=requests.delete(url = url_RespDelete2, headers=header)
    response = request.json()
    assert request.status_code == 200
    assert response['status'] == "success"
    input_dict_2 = {"response_id": 13}
    data2 = json.dumps(input_dict_2)
    request2 = requests.post(url = url_respResp, data = data2, headers=header)
    response_request2 = request2.json()
    assert request2.status_code == 200
    assert response_request2["status"] == "succcess"
    assert len(response_request2["data"]) == 0
    assert response_request2["data"] == []
"""

def test_delete_ResponseAPI_by_response_id_wrong_response_id():
    header={"secret_authtoken":token_login_support_agent(), "Content-Type":"application/json"}
    request=requests.delete(url = url_RespDelete, headers=header)
    response = request.json()
    assert request.status_code == 404
    assert response["message"] == "Either the response you are trying to delete is not yours, or the response doesn't exist in the first place."
    

