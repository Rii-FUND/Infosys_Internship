from mongoengine import Document, StringField, BooleanField, DictField, connect

connect(
    db="ticket_info",  
    host="Use_your_own_host_url",
    alias="default"  
)

class TicketResponse(Document):
    customer_email = StringField(required=True)  
    customer_ticket = StringField(required=True)
    sentiment = StringField(required=True)       
    thought = StringField(required=True)                      
    escalation_required = BooleanField(required=True) 
    priority = StringField(required=True)       
    response = DictField(required=True)
   