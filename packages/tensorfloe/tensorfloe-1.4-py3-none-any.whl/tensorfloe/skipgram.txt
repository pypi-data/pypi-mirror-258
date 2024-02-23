pip install gensim

import nltk
nltk.download('punkt')

from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize

# Sample sentences
sentences = [
    "Data is everywhere",
    "There are forms of data",
    "Data could be text, image, numbers, audio, video etc"
]

# Tokenize sentences
tokenized_sentences = [word_tokenize(sentence.lower()) for sentence in sentences]

# Define and train Word2Vec model using Skip-gram approach (sg=1 for Skip-gram approach)
model = Word2Vec(sentences=tokenized_sentences, vector_size=100, window=5, sg=1, min_count=1, workers=4)

# Get Word2Vec representation for a word
word = "data"
word_vector = model.wv[word]

print("Word:", word)
print("Word2Vec representation using Skip-gram:", word_vector)
