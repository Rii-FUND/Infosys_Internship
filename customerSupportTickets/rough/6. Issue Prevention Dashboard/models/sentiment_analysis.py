import re
import google.generativeai as genai

# Configure the Gemini API key
genai.configure(api_key="YOUR_GEMINI_API_KEY")

def clean_text(text: str) -> str:
    """Clean input text by removing special characters and extra spaces."""
    text = text.lower()
    text = text.replace('\n', ' ')
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = ' '.join(text.split())
    return text

def analyze_sentiment_gemini(text: str) -> dict:
    """
    Analyze sentiment using the Gemini API.
    
    Args:
        text: Input text to analyze.

    Returns:
        A dictionary with sentiment analysis results.
    """
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Analyze the sentiment: {text}")
        return {
            "sentiment": response["sentiment"],
            "explanation": response["explanation"],
        }
    except Exception as e:
        return {"error": str(e)}
