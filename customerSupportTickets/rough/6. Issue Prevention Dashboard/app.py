from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import json
from sentiment_analysis import analyze_sentiment_gemini
from issue_escalation import issue_escalation, required_issue_escalation
from response_automation import preprocess_text, get_product_subject, get_product_body

# Initialize the FastAPI app
app = FastAPI()

class Ticket(BaseModel):
    subject: str
    body: str
    customer_email: str

@app.post("/process-ticket/")
async def process_ticket(ticket: Ticket):
    try:
        # Preprocess ticket data
        processed_subject = preprocess_text(ticket.subject)
        processed_body = preprocess_text(ticket.body)

        # Sentiment analysis
        sentiment_result = analyze_sentiment_gemini(processed_body)
        if "error" in sentiment_result:
            raise HTTPException(status_code=500, detail=sentiment_result["error"])

        # Issue escalation
        priority = issue_escalation(processed_body)
        escalation_required = required_issue_escalation(priority)

        # Extract product information
        product_subject = get_product_subject(processed_subject)
        product_body = get_product_body(processed_body)

        # Generate response
        response = {
            "customer_email": ticket.customer_email,
            "sentiment": sentiment_result["sentiment"],
            "escalation_required": escalation_required,
            "priority": priority,
            "product_details": {
                "from_subject": product_subject,
                "from_body": product_body
            }
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Ticket Processing API is running. Use POST /process-ticket/ to process a ticket."}
