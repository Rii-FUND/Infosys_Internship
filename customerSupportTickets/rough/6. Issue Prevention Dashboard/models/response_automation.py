import pickle
from transformers import pipeline

# Load the pretrained NER model
ner_pipeline = pipeline("ner", model="dslim/bert-large-NER", tokenizer="dslim/bert-large-NER")

# Load the saved models
with open('data/kmeans_model.pkl', 'rb') as file:
    kmeans_model = pickle.load(file)

with open('data/vectorizer.pkl', 'rb') as file:
    vectorizer = pickle.load(file)

with open('data/pca_model.pkl', 'rb') as file:
    pca_model = pickle.load(file)

def preprocess_text(text: str) -> str:
    """Preprocess text: tokenization, stopword removal, and lemmatization."""
    import nltk
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('punkt', quiet=True)
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer

    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    tokens = [
        lemmatizer.lemmatize(word) 
        for word in nltk.word_tokenize(text.lower()) 
        if word not in stop_words
    ]
    return " ".join(tokens)

def get_product_subject(subject: str) -> str:
    """Extract product information from email subject."""
    tokens = ner_pipeline(subject)
    return " ".join([t["word"] for t in tokens]).replace(" ##", "")

def get_product_body(body: str) -> str:
    """Extract product information from email body."""
    tokens = ner_pipeline(body)
    return " ".join([t["word"] for t in tokens]).replace(" ##", "")
