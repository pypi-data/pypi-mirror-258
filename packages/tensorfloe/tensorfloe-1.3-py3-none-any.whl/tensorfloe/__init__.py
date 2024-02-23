import os

# Get the directory path where the .txt files are located
txt_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tensorfloe')

def spam():
    with open(os.path.join(txt_dir_path, 'spam.txt'), 'r') as file:
        code = file.read()
        print("Code in spam.txt:")
        print(code)

def sentiment():
    with open(os.path.join(txt_dir_path, 'sentiment.txt'), 'r') as file:
        code = file.read()
        print("Code in sentiment.txt:")
        print(code)

def gender():
    with open(os.path.join(txt_dir_path, 'gender.txt'), 'r') as file:
        code = file.read()
        print("Code in gender.txt:")
        print(code)

def pos():
    with open(os.path.join(txt_dir_path, 'pos.txt'), 'r') as file:
        code = file.read()
        print("Code in pos.txt:")
        print(code)

def word2vec():
    with open(os.path.join(txt_dir_path, 'word2vec.txt'), 'r') as file:
        code = file.read()
        print("Code in word2vec.txt:")
        print(code)

def skipgram():
    with open(os.path.join(txt_dir_path, 'skipgram.txt'), 'r') as file:
        code = file.read()
        print("Code in skipgram.txt:")
        print(code)

def chatbot():
    with open(os.path.join(txt_dir_path, 'chatbot.txt'), 'r') as file:
        code = file.read()
        print("Code in chatbot.txt:")
        print(code)

def summary():
    with open(os.path.join(txt_dir_path, 'summary.txt'), 'r') as file:
        code = file.read()
        print("Code in summary.txt:")
        print(code)

def transformer():
    with open(os.path.join(txt_dir_path, 'transformer.txt'), 'r') as file:
        code = file.read()
        print("Code in transformer.txt:")
        print(code)

def latent():
    with open(os.path.join(txt_dir_path, 'latent.txt'), 'r') as file:
        code = file.read()
        print("Code in latent.txt:")
        print(code)
