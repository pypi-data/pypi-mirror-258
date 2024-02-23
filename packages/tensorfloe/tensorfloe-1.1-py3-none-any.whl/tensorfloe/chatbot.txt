import nltk
import numpy as np
import random
import string

# NLTK download if not already downloaded
nltk.download('punkt')
nltk.download('wordnet')

# Importing libraries for tokenization and stemming
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Sample corpus for the chatbot
corpus = [
    'Hello, how are you?',
    'Hi there!',
    'What can I do for you?',
    'How can I help you?',
    'Good day!',
    'Bye bye!',
    'See you later.',
    'Nice talking to you.',
    'What is your name?',
    'How old are you?',
    'Tell me about yourself.',
    'What are your hobbies?',
    'Do you like sports?',
    'Can you recommend a book?',
    'What is the weather like today?',
    'How do I get to the nearest pharmacy?',
    'Where can I find a good restaurant?',
    'What is the capital of France?',
    'Who is the president of the United States?',
    'Tell me a joke.',
    'Can you sing?',
    'Tell me about AI.',
    'What is your favorite color?'
]

# Preprocessing the corpus
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    text = text.lower()
    text = word_tokenize(text)
    text = [lemmatizer.lemmatize(token) for token in text if token not in string.punctuation]
    return ' '.join(text)

corpus = [preprocess_text(sentence) for sentence in corpus]

# Creating TF-IDF vectors
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus)

# Function to generate a response to user input
def generate_response(user_input):
    user_input = preprocess_text(user_input)
    tfidf_user_input = vectorizer.transform([user_input])
    similarity = cosine_similarity(tfidf_user_input, tfidf_matrix)
    max_similarity_index = np.argmax(similarity)
    return corpus[max_similarity_index]

# Chatting with the user
print("Chatbot: Hello! How can I assist you today?")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'bye':
        print("Chatbot: Goodbye! Have a great day!")
        break
    else:
        response = generate_response(user_input)
        print("Chatbot:", response)


