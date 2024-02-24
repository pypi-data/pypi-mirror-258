import re
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

def word_count(text):
    """
    Count the number of words in the text.
    """
    words = word_tokenize(text)
    return len(words)

def char_count(text):
    """
    Count the number of characters in the text.
    """
    return len(text)

def avg_word_length(text):
    """
    Calculate the average word length in the text.
    """
    words = word_tokenize(text)
    total_length = sum(len(word) for word in words)
    return total_length / len(words) if len(words) > 0 else 0

def most_common_words(text, n=5):
    """
    Find the most common words in the text.
    """
    words = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_words = [word.lower() for word in words if word.lower() not in stop_words and re.match(r'^\w+$', word)]
    word_freq = Counter(filtered_words)
    return word_freq.most_common(n)
