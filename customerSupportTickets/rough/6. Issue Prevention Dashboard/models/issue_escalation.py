def required_issue_escalation(priority_level):
    if priority_level in ["high", "critical"]:
        return True
    return False

def issue_escalation(text):
    escalation_keywords = {"urgent": "high", "immediate": "critical", "asap": "high"}
    for keyword, priority in escalation_keywords.items():
        if keyword in text.lower():
            return priority
    return "low"

if __name__ == "__main__":
    sample_text = "This issue needs to be resolved ASAP."
    priority = issue_escalation(sample_text)
    print(f"Issue Priority: {priority}")
    print(f"Escalation Required: {required_issue_escalation(priority)}")
