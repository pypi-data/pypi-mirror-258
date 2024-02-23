!pip install scikit-learn
!pip install nltk

#a) Support Vector Classifier

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('indiannamesgenders.csv')
df.head()

df=df.dropna()

# Assume 'Name' is the column containing the names, 'Gender' is the target variable
X = df['name']
y = df['gender']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Convert names into numerical features using CountVectorizer
vectorizer = CountVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Train an SVM model
svm_model = SVC(kernel='linear')
svm_model.fit(X_train_vectorized, y_train)

# Make predictions on the test set
predictions = svm_model.predict(X_test_vectorized)

# Evaluate the model
accuracy = accuracy_score(y_test, predictions)
report = classification_report(y_test, predictions)

print(f'Accuracy: {accuracy}')
print('Classification Report:\n', report)


# Input a name for gender prediction
input_name = input("Enter a name for gender prediction: ")

# Preprocess the input name (similar to the preprocessing done during training)
input_name = input_name.lower()  # Convert to lowercase

# Vectorize the input name using the same CountVectorizer
input_name_vectorized = vectorizer.transform([input_name])

# Make a prediction using the trained SVM model
predicted_gender = svm_model.predict(input_name_vectorized)[0]

print(f'The predicted gender for the name "{input_name}" is: {predicted_gender}')

#b) LSTM

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense
from sklearn.metrics import accuracy_score, classification_report

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('indiannamesgenders.csv')

# Drop rows with null values in 'Name' or 'Gender' columns
df = df.dropna(subset=['name', 'gender'])

# Assume 'name' is the column containing the names, 'gender' is the target variable
X = df['name']
y = df['gender']

# Encode gender labels using LabelEncoder
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Tokenize the names
max_words = 1000
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(X_train)

# Convert names to sequences
X_train_sequences = tokenizer.texts_to_sequences(X_train)
X_test_sequences = tokenizer.texts_to_sequences(X_test)

# Pad sequences to ensure uniform length
max_sequence_length = max(len(seq) for seq in X_train_sequences)
X_train_padded = pad_sequences(X_train_sequences, maxlen=max_sequence_length)
X_test_padded = pad_sequences(X_test_sequences, maxlen=max_sequence_length)

# Build LSTM model
embedding_dim = 50
lstm_units = 100

model = Sequential()
model.add(Embedding(input_dim=max_words, output_dim=embedding_dim, input_length=max_sequence_length))
model.add(LSTM(units=lstm_units))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train_padded, y_train, epochs=5, batch_size=32, validation_split=0.1)

# Evaluate the model
y_pred_proba = model.predict(X_test_padded)
y_pred = (y_pred_proba > 0.5).astype(int)

accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f'Accuracy: {accuracy}')
print('Classification Report:\n', report)


# Input a name for gender prediction
input_name = input("Enter a name for gender prediction: ")

# Tokenize and pad the input name
input_name_sequence = tokenizer.texts_to_sequences([input_name])
input_name_padded = pad_sequences(input_name_sequence, maxlen=max_sequence_length)

# Make a prediction using the trained LSTM model
predicted_proba = model.predict(input_name_padded)
predicted_label = (predicted_proba > 0.5).astype(int)[0][0]

# Map the predicted label back to the original gender
predicted_gender = label_encoder.inverse_transform([predicted_label])[0]

print(f'The predicted gender for the name "{input_name}" is: {predicted_gender}')
