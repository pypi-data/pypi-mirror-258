# tensorfloe/__init__.py

import os

# Get the directory path where this __init__.py file is located
dir_path = os.path.dirname(os.path.realpath(__file__))

# Define functions to print the code from .txt files
def spam():
    with open(os.path.join(dir_path, 'spam.txt'), 'r') as file:
        code = file.read()
        print("Code in spam.txt:")
        print(code)

def sentiment():
    with open(os.path.join(dir_path, 'sentiment.txt'), 'r') as file:
        code = file.read()
        print("Code in sentiment.txt:")
        print(code)

def gender():
    with open(os.path.join(dir_path, 'gender.txt'), 'r') as file:
        code = file.read()
        print("Code in gender.txt:")
        print(code)

def pos():
    with open(os.path.join(dir_path, 'pos.txt'), 'r') as file:
        code = file.read()
        print("Code in pos.txt:")
        print(code)

def word2vec():
    with open(os.path.join(dir_path, 'word2vec.txt'), 'r') as file:
        code = file.read()
        print("Code in word2vec.txt:")
        print(code)

def skipgram():
    with open(os.path.join(dir_path, 'skipgram.txt'), 'r') as file:
        code = file.read()
        print("Code in skipgram.txt:")
        print(code)

def chatbot():
    with open(os.path.join(dir_path, 'chatbot.txt'), 'r') as file:
        code = file.read()
        print("Code in chatbot.txt:")
        print(code)

def summary():
    with open(os.path.join(dir_path, 'summary.txt'), 'r') as file:
        code = file.read()
        print("Code in summary.txt:")
        print(code)

def transformer():
    with open(os.path.join(dir_path, 'transformer.txt'), 'r') as file:
        code = file.read()
        print("Code in transformer.txt:")
        print(code)

def latent():
    with open(os.path.join(dir_path, 'latent.txt'), 'r') as file:
        code = file.read()
        print("Code in latent.txt:")
        print(code)

