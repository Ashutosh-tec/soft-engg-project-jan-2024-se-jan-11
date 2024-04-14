from sqlalchemy import func
from application.workers import celery
from flask import current_app as app
from application.models import db, User, Ticket, Response
import requests
from datetime import datetime, timedelta
from celery.schedules import crontab

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=11, minute=30), unanswered_ticket_notification.s(), name='Daily Unanswered Ticket Reminder')
    sender.add_periodic_task(crontab(minute=30, hour=4, day=1), poor_resolution_time.s(), name='Monthly Agent Resolution Time Report')


@celery.task()
def poor_resolution_time():
    thirty_days_ago = datetime.now() - timedelta(days=30)
    agents = db.session.query(User).filter(User.role_id==2).all()
    all_agents_avg_resolution_time = []
    subject = 'This months agent resolution time report'
    eid = db.session.query(User).filter(User.role_id==4).first().email_id

    for agent in agents:
        tickets_responded_by_agent = set(t.ticket_id for t in db.session.query(Response).filter(Response.responder_id == agent.user_id).all())
        ticket_counter = 0
        total_resolution_time = 0
        open_tickets = 0
        for ticket in tickets_responded_by_agent:
            subqry = db.session.query(func.max(Response.response_id)).filter(Response.responder_id == agent.user_id, Response.ticket_id==ticket)
            qry = db.session.query(Response).filter(Response.responder_id == agent.user_id, Response.ticket_id==ticket, Response.response_id == subqry).first()
            tk = db.session.query(Ticket).filter(Ticket.ticket_id==ticket).first()
            if tk.creation_date > thirty_days_ago :
                if not tk.is_open:
                    created_at = tk.creation_date
                    resolved_at = qry.response_timestamp
                    total_resolution_time += (resolved_at - created_at).total_seconds()/3600
                    ticket_counter += 1
                else:
                    open_tickets +=1
        if total_resolution_time > 0 and ticket_counter > 0:
            avg_resolution_time = total_resolution_time/ticket_counter
            if avg_resolution_time > 48:
                all_agents_avg_resolution_time.append((agent.user_name, avg_resolution_time, open_tickets))  
    if all_agents_avg_resolution_time:
        html = '''
            <html> 
            <head> The following agents have a poor resolution time </head>
            <body>
            <ol>
        '''
        for tup in all_agents_avg_resolution_time:
            html += f'<li> {tup[0]} has an average resolution time of {tup[1]} hours and has {tup[2]} unresolved tickets </li>'
        html+= '</ol> </body> </html>'
        send_email.s((html, eid, subject)).apply_async()

        return "Email sent with details of agents with poor resolution time"
    else:
        return "All Agents have have a resolution time less than 48 hours in the past 30 days"

@celery.task()
def unanswered_ticket_notification():
    now = datetime.now()
    three_day_old_timestamp = now - timedelta(hours=72)
    unresolved_tickets = db.session.query(Ticket).filter(Ticket.is_open==1, Ticket.creation_date < three_day_old_timestamp).all()
    agents_user_ids = [a.user_id for a in db.session.query(User.user_id).filter(User.role_id==2).all() ]
    unanswered_tickets = []
    if unresolved_tickets:
        for ticket in unresolved_tickets:
            responses = ticket.responses
            flag = True
            for response in responses:
                if response.responder_id in agents_user_ids:
                    flag = False
                    break
            if flag:
                unanswered_tickets.append(ticket)
    else:
        return "No Unresolved Tickets"
    
    if unanswered_tickets:
        html = '''
            <html>
            <head> The following tickets were created over 72 hours ago and still haven't been answered </head> 
            <body>
            <ol>
        '''
        for ticket in unanswered_tickets:
            html += f'<li> {ticket.title} created on {ticket.creation_date.strftime("%Y-%m-%d")} is still unanswered </li>'
        html+= '</ol> </body> </html>'

        eid = db.session.query(User).filter(User.role_id==4).first().email_id
        subject = f'{len(unanswered_tickets)} ticket(s) older than 72 hours are yet to be answered'
        send_email.s((html, eid, subject)).apply_async()
        return "Notification Sent"
    else:
        return "All Tickets Answered"
                            
@celery.task()
def response_notification(ticket_obj, response_obj):
    # # ticket_obj = db.session.query(Ticket).filter(Ticket.ticket_id==tid).first()
    # # response_obj = db.session.query(Response).filter(Response.response_id==rid).first()
    # creator_obj = db.session.query(User).filter(User.user_id==ticket_obj.creator_id).first()
    # responder_obj = db.session.query(User).filter(User.user_id==response_obj.responder_id).first()
    subject = f'There is a new response to your ticket {ticket_obj["title"]}'
    eid = ticket_obj["creator_email"]
    html = f'''
        <html> 
            <head>
                {response_obj["responder_uname"]} has posted a respone to your ticket {ticket_obj["title"]}
            </head>
            <body>
                <blockquote>
                {response_obj["response"]}
                </blockquote>
            </body>
        </html>
    '''
    return (html, eid, subject)

@celery.task()
def send_email(email):
    html, eid, subject = email
    api_key = app.config['MAILGUN_API_KEY']
    api_url = 'https://api.mailgun.net/v3/iitm.venkatesh.xyz/messages'
    a = requests.post(
        api_url,
        auth=('api', api_key),
        data={
            'from': 'mailgun@iitm.venkatesh.xyz',
            'to': eid,
            'subject': subject,
            'html': html,
        }
    )
    return a.status_code
