from application.models import db, Ticket, Response
from application import client, index

tickets = db.session.query(Ticket).all()
objects = []
for tk in tickets:
    tk_object = {
                'objectID': tk.ticket_id,
                'ticket_id': tk.ticket_id,
                'title': tk.title,
                'description': tk.description,
                'creation_date': tk.creation_date,
                'creator_id': tk.creator_id,
                'number_of_upvotes': tk.number_of_upvotes,
                'is_read': tk.is_read,
                'is_offensive': tk.is_offensive,
                'is_FAQ': tk.is_FAQ,
                'rating': tk.rating,
                'responses': [response.response for response in tk.responses]
                }
    # responses = tk.responses 
    # for response in tk.responses:
    #     tk_object['responses'].append(response.response)
    #     # resp_obj = {
    #     #     'response_id': response.response_id,
    #     #     'response': response.response
    #     # }
    #     # tk_object['responses'].append(resp_obj)
    objects.append(tk_object)

index.save_objects(objects=objects)
