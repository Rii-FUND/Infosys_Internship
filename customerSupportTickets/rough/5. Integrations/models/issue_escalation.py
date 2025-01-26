import re

def should_escalate(incoming_issue):
    # Initialize an empty list for the tags
    tags_combined = ""
    
    # Loop over expected tags and add them if they exist
    for i in range(9):
        tag_key = f"tag_{i+1}"
        if tag_key in incoming_issue:
            tags_combined += incoming_issue[tag_key] + " "

    # Remove trailing whitespace from the combined tags
    tags_combined = tags_combined.strip()

    # Keywords that trigger escalation
    keywords = ["urgent", "issue", "refund", "Failure", "Outage", "Crash", "Breach", "Critical"]

    # Check if any keyword matches in the combined tags using regular expressions for whole word matching
    for key in keywords:
        if re.search(r'\b' + re.escape(key.lower()) + r'\b', tags_combined.lower()):
            return True

    return False
