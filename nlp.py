import spacy

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

def analyze_text(text):
    """
    Analyze the input text using spaCy and return entities and tokens.
    """
    doc = nlp(text)
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
    tokens = [{"text": token.text, "pos": token.pos_} for token in doc]
    return {
        "entities": entities,
        "tokens": tokens
    }
