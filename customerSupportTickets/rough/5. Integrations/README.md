# Customer Support Ticket Analysis using FastAPI, Gemini, and Pinecone

This project integrates **FastAPI**, **Gemini AI**, **Pinecone**, and **MongoDB** to automate customer support ticket responses with sentiment analysis and response automation. It handles ticket escalation and stores processed data in a database for further review.

---
## API Endpoints

### 1. `POST /process-ticket/`
- **Description:** Processes incoming support tickets.
- **Request Body:**
  ```json
  {
    "subject": "Product not working",
    "body": "My device is not turning on.",
    "customer_email": "user@example.com"
  }

## Steps Involved:
-  Perform sentiment analysis using get_sentiment(subject, body).
-  Determine if escalation is required using should_escalate().
-  Automate response using automate_response().
-  Save ticket details in MongoDB.
-  Trigger Zapier webhook to send email responses.

**Response**
```json
{
  "To": "user@example.com",
  "Subject": "Issue Report: Product not working",
  "Body": "Suggested solution based on previous tickets."
}
```

### 2. `Get /`
- **Description:** Returns a welcome message to confirm API availability.
**Response**
```json
{
  "message": "Ticket Processing API is running. Use POST /process-ticket/ to process a ticket."
}
```
---
## Environment Setup
- fastapi
- pydantic
- requests
- mongoengine
- openai
- pinecone-client
- logging

---

## Environment Setup
**1. Create a Virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/MacOS
.venv\Scripts\activate     # Windows
```
**2. Install Dependencies**
**3. Set up API Keys (Gemini, Pinecone, etc.):**
- Ensure you have your API keys configured in environment variables or in code files securely.

---
# Workflow Explanation

## Subject Extraction & Vectorization:

- The **subject** column from `gsheet_data.csv` is analyzed to extract **noun (product)** and **issue** using the **Gemini API**.
- The entire dataset (English) is vectorized using `text-embedding-004` to convert text into numerical representations.
- A **similarity search** is performed using **Pinecone** to find the top 3 matching issues.

## Automated Response Generation:

If similar issues are found, a personalized response is created using the Gemini AI model, combining:

- The top 3 retrieved responses.
- The current user's subject and body.

The generated response is then returned to the user.

## Issue Escalation:

If the issue is deemed **critical** (based on sentiment and predefined conditions), it is escalated for **manual agent review**, bypassing automation.

## Database Storage (MongoDB):

Ticket data is saved in MongoDB via `db.py`, which defines the schema using `mongoengine`.

### Sample schema:
```python
class TicketResponse(Document):
    customer_email = StringField(required=True)
    customer_ticket = StringField(required=True)
    sentiment = StringField(required=True)
    thought = StringField(required=True)
    escalation_required = BooleanField(required=True)
    priority = StringField(required=True)
    response = DictField(required=True)
```
---
## Zapier Integration

- **Zapier Webhook:** Used to send automated email responses to customers.

## How it Works:
1. Construct email payload with subject, body, and recipient.
2. Trigger the Zapier webhook with the payload.
3. Zapier sends the response email to the customer.

## Example Payload Sent to Zapier:
```json
{
  "To": "user@example.com",
  "Subject": "Issue Report: Product not working",
  "Body": "Suggested solution. Thank you for reaching out."
}
```
---
# Running the Project

## Activate virtual environment:
```bash
source .venv/bin/activate  # Linux/MacOS
.venv\Scripts\activate     # Windows
```
## Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
---
## Access the API Documentation:

Open in browser: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

# Future Improvements

- Enhancing sentiment analysis models for higher accuracy.
- Optimizing Pinecone vector search performance.
- Adding a dashboard for manual ticket review.











