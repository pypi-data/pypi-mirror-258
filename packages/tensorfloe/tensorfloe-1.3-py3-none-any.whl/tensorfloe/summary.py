#a) Spacy

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_text(text):
    # Tokenize and preprocess the text
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(tokens)

def generate_summary(text, num_sentences=5):
    # Preprocess the text
    preprocessed_text = preprocess_text(text)

    # Create a document-term matrix using CountVectorizer
    vectorizer = CountVectorizer()
    matrix = vectorizer.fit_transform([preprocessed_text, text])

    # Calculate cosine similarity between sentences
    similarity_matrix = cosine_similarity(matrix, matrix)

    # Get the sentence scores based on similarity
    sentence_scores = similarity_matrix[0]

    # Rank sentences based on scores
    ranked_sentences = sorted(((score, index) for index, score in enumerate(sentence_scores)), reverse=True)

    # Extract top sentences for summary
    summary_sentences = [text.split('.')[i] for _, i in ranked_sentences[:num_sentences]]
    summary = '. '.join(summary_sentences)
    return summary

# Example usage
input_text = """
Natural Language Processing (NLP) is a subfield of artificial intelligence that focuses on the interaction between computers and humans using natural language. It involves the development of algorithms and models that enable computers to understand, interpret, and generate human-like text. Text summarization is one of the applications of NLP, where the goal is to generate a concise and coherent summary of a given document or piece of text.

There are two main approaches to text summarization: extractive and abstractive. Extractive summarization involves selecting and combining important sentences or phrases from the original text to create a summary. Abstractive summarization, on the other hand, involves generating new sentences that capture the key information from the original text.

In this example, we will focus on extractive summarization using spaCy, a popular NLP library in Python. We will use a simple algorithm that calculates the cosine similarity between sentences to identify the most important ones for the summary.

Let's try generating a summary for this sample text using our program.
"""

summary = generate_summary(input_text)
print(summary)


#b) NLTK

import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np

nltk.download('punkt')
nltk.download('stopwords')

def read_article(text):
    # Split the text into sentences
    sentences = nltk.sent_tokenize(text)
    return sentences

def sentence_similarity(sent1, sent2, stop_words):
    # Tokenize sentences
    words1 = nltk.word_tokenize(sent1)
    words2 = nltk.word_tokenize(sent2)

    # Remove stop words
    words1 = [word.lower() for word in words1 if word.isalnum() and word.lower() not in stop_words]
    words2 = [word.lower() for word in words2 if word.isalnum() and word.lower() not in stop_words]

    # Create a set of unique words in both sentences
    all_words = list(set(words1 + words2))

    # Create vectors representing sentence words
    vector1 = [1 if word in words1 else 0 for word in all_words]
    vector2 = [1 if word in words2 else 0 for word in all_words]

    # Calculate cosine similarity between the vectors
    return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences, stop_words):
    # Initialize a matrix with zeros
    similarity_matrix = np.zeros((len(sentences), len(sentences)))

    # Fill the matrix with sentence similarities
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                similarity_matrix[i][j] = sentence_similarity(sentences[i], sentences[j], stop_words)

    return similarity_matrix

def generate_summary(text, num_sentences=5):
    stop_words = set(stopwords.words("english"))

    # Read the article
    sentences = read_article(text)

    # Build the similarity matrix
    similarity_matrix = build_similarity_matrix(sentences, stop_words)

    # Rank sentences based on similarity
    sentence_scores = np.array(similarity_matrix.sum(axis=1))

    # Get the indices of top sentences for summary
    ranked_sentences = np.argsort(-sentence_scores)

    # Extract top sentences for summary
    summary_sentences = [sentences[i] for i in ranked_sentences[:num_sentences]]
    summary = ' '.join(summary_sentences)

    return summary

# Example usage
input_text = """
Natural Language Processing (NLP) is a subfield of artificial intelligence that focuses on the interaction between computers and humans using natural language. It involves the development of algorithms and models that enable computers to understand, interpret, and generate human-like text. Text summarization is one of the applications of NLP, where the goal is to generate a concise and coherent summary of a given document or piece of text.

There are two main approaches to text summarization: extractive and abstractive. Extractive summarization involves selecting and combining important sentences or phrases from the original text to create a summary. Abstractive summarization, on the other hand, involves generating new sentences that capture the key information from the original text.

In this example, we will focus on extractive summarization using NLTK, a popular NLP library in Python. We will use a simple algorithm that calculates the cosine similarity between sentences to identify the most important ones for the summary.

Let's try generating a summary for this sample text using our program.
"""

summary = generate_summary(input_text)
print(summary)
