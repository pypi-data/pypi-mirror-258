#a) POS Tagging

# Start by importing spaCy
import spacy

# The spacy.load command initializes the nlp pipeline.
nlp = spacy.load("en_core_web_sm")

# Provide the nlp pipeline with input text.
doc = nlp("On Friday board members meet with senior managers " +
          "to discuss future development of the company.")

# Print the output in a tabular format and add a header to the printout for clarity.
rows = []
rows.append(["Word", "Position", "Lowercase", "Lemma", "POS", "Alphanumeric", "Stopword"])
for token in doc:
    rows.append([token.text, str(token.i), token.lower_, token.lemma_,
                 token.pos_, str(token.is_alpha), str(token.is_stop)])

# Python’s zip function allows you to reformat input from row-wise
# representation to column-wise
columns = zip(*rows)

# Calculate the maximum length of strings in each column to allow
# enough space in the printout.
column_widths = [max(len(item) for item in col) for col in columns]

# Use the format functionality to adjust the width of each column in each row
# while printing out the results.
for row in rows:
    print(''.join(' {:{width}} '.format(row[i], width=column_widths[i])
                  for i in range(0, len(row))))

#b) Named Entity Recognition

import spacy
NER = spacy.load("en_core_web_sm")
raw_text="The Indian Space Research Organisation or is the national space agency of India, headquartered in Bengaluru. It operates under Department of Space which is directly overseen by the Prime Minister of India while Chairman of ISRO acts as executive of DOS as well."
text1= NER(raw_text)
for word in text1.ents:
    print(word.text,word.label_)
