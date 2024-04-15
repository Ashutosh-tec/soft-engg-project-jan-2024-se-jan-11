from application import app
from flask import request, jsonify
from .models import *
import requests

@app.route("/")
def home():
    return 'hi'

@app.route("/users", methods=["GET"])
@token_required
def get_users(current_user):
    print(current_user)
    users = User.query.all()
    results = [
        {
            "user_id": user.user_id,
            "user_name": user.user_name,
            "name": user.name,
            "email_id": user.email_id,
            "role_id": user.role_id
        } for user in users]

    return jsonify(results)

def send_notification(ticket_title, ticket_description, webhook_url):
    """
    Send a notification to a webhook URL about a new high priority/urgent ticket.
    """
    message = {
        "text": f"New high priority/urgent ticket:\nTitle: {ticket_title}\nDescription: {ticket_description}"
    }
    response = requests.post(webhook_url, json=message)
    if response.status_code == 200:
        print("Notification sent successfully")
    else:
        print("Failed to send notification")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    ticket_title = data.get('title')
    ticket_description = data.get('description')
    priority = data.get('priority')
    if priority == 'high' or priority == 'urgent':
        webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAAVFgvcso/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=bJsKuUQVHQFNOLmgEWN_eop63P8Esx3uDGWPr8ll_A0'
        send_notification(ticket_title, ticket_description, webhook_url)
    return '', 200

# from application.workers import celery
# from application.tasks import send_email
# @app.route("/email", methods=["POST"])
# def post_email():
#     html = request.get_json()['html']
#     email = request.get_json()['email']
#     subject = request.get_json()['subject']
#     send_email.s(eid=email, html=html, subject=subject).apply_async()
#     return jsonify({'message': 'success'})

# from application.workers import celery
# from application.tasks import unanswered_ticket_notification
# @app.route("/notification")
# def get_notif():
#     unanswered_ticket_notification.s().apply_async()
#     return "OK"