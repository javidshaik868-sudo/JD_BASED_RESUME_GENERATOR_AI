# utils/preprocessor.py

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# -----------------------------------
# ✅ Safe NLTK setup (runs once)
# -----------------------------------
def setup_nltk():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)

    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)


setup_nltk()

STOP_WORDS = set(stopwords.words('english'))


# -----------------------------------
# 🔹 Clean Text (basic)
# -----------------------------------
def clean_text(text):
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r'\n', ' ', text)            # remove newlines
    text = re.sub(r'\t', ' ', text)            # remove tabs
    text = re.sub(r'[^\w\s]', '', text)        # remove punctuation
    text = re.sub(r'\d+', '', text)            # remove numbers
    text = re.sub(r'\s+', ' ', text).strip()   # remove extra spaces

    return text


# -----------------------------------
# 🔹 Tokenization
# -----------------------------------
def tokenize_text(text):
    if not text:
        return []

    return word_tokenize(text)


# -----------------------------------
# 🔹 Remove Stopwords
# -----------------------------------
def remove_stopwords(tokens):
    return [word for word in tokens if word not in STOP_WORDS]


# -----------------------------------
# 🔹 Full Preprocessing Pipeline
# -----------------------------------
def preprocess_text(text):
    """
    Complete preprocessing:
    - Clean text
    - Tokenize
    - Remove stopwords
    - Return cleaned string
    """

    cleaned = clean_text(text)
    tokens = tokenize_text(cleaned)
    filtered_tokens = remove_stopwords(tokens)

    return " ".join(filtered_tokens)


# -----------------------------------
# 🔹 Optional: Extract Important Words
# -----------------------------------
def get_keywords(text, top_n=10):
    processed = preprocess_text(text)
    words = processed.split()

    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1

    # Sort by frequency
    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    return [word for word, count in sorted_words[:top_n]]
