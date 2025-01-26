from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models.sentiment_access import get_sentiment
from models.issue_escalation import should_escalate
from models.response_automation_with_gemini_and_pinecone import automate_response
import requests
import logging
from app.db import TicketResponse

# Initialize the FastAPI app
app = FastAPI()

ZAPIER_WEBHOOK_URL = "Use_your_own_WebhookURL"

class Ticket(BaseModel):
    subject: str
    body: str
    customer_email: str

logging.basicConfig(level=logging.DEBUG)

@app.post("/process-ticket/")
async def process_ticket(ticket: Ticket):
    try:
        # Sentiment analysis
        sentiment_result = get_sentiment(ticket.subject, ticket.body)

        # Handle the case where the result is a string (just the sentiment)
        if isinstance(sentiment_result, str):
            sentiment = sentiment_result
            thought = ""  
        elif isinstance(sentiment_result, dict) and "sentiment" in sentiment_result:
            sentiment = sentiment_result["sentiment"]
            thought = sentiment_result.get("thought", "")  # Get thought, default to empty if missing
        else:
            raise ValueError("Invalid response from sentiment analysis model")

        # Set priority based on sentiment (this is a simplified logic, you can expand it)
        priority = "high" if sentiment == "frustrated" else "low"

        # Prepare incoming issue for escalation
        # Here we simulate tags (you can adjust based on how tags are derived from ticket content)
        incoming_issue = {
            "priority": priority,
            "tag_1": ticket.subject,
            "tag_2": ticket.body,
            "tag_3": ""
        }

        # Determine if issue escalation is required
        escalation_required = should_escalate(incoming_issue) 

        # Set priority based on escalation
        priority = "high" if escalation_required else "low"

        auto_response = automate_response(ticket.subject, ticket.body)

        # Construct response payload
        response = {
            "customer_email": ticket.customer_email,
            "customer_ticket" : ticket.body,
            "sentiment": sentiment,
            "thought": thought,
            "escalation_required": escalation_required,
            "priority": priority,
            "response" : auto_response
        }

        ticket_response = TicketResponse(**response)
        ticket_response.save()
        
        zapier_payload = {
            "To": ticket.customer_email,
            "Subject": f"Issue Report: {ticket.subject}",
            "Body": 
                f"{auto_response}"
                f"Thank you for bringing this to our attention."
                f"Regards, Support Team"
        }

        # Send data to Zapier webhook
        zapier_response = requests.post(ZAPIER_WEBHOOK_URL, json=zapier_payload)
        zapier_response.raise_for_status()

        # Return the constructed response to the client
        return zapier_payload

    except requests.RequestException as req_err:
        logging.error("Error sending data to Zapier: %s", str(req_err))
        raise HTTPException(status_code=500, detail=f"Failed to send data to Zapier: {str(req_err)}")
    except ValueError as val_err:
        logging.error("Value error: %s", str(val_err))
        raise HTTPException(status_code=400, detail=f"Processing error: {str(val_err)}")
    except Exception as e:
        logging.error("Unexpected error: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@app.get("/")
def root():
    return {"message": "Ticket Processing API is running. Use POST /process-ticket/ to process a ticket."}
