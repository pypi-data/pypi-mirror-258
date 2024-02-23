!pip install transformers

from transformers import pipeline, set_seed
import warnings
warnings.filterwarnings("ignore")

#a) Text generation

generator = pipeline('text-generation', model='gpt2')
set_seed(42)

# Example 1
generator("Hello, I like to play cricket,", max_length=60, num_return_sequences=7)

# Example 2
generator("Natural Language Processing is evolving technology", max_length=10, num_return_sequences=5)


#b) Question Answering

# Allocate a pipeline for question-answering
question_answerer = pipeline('question-answering')

# Example 1
question_answerer({
    'question': 'What is the Newtons third law of motion?',
    'context': 'Newton’s third law of motion states that, "For every action there is equal and opposite reaction"'})

# Example 2
nlp = pipeline("question-answering")

context = r"""
Micorsoft was founded by Bill gates and Paul allen in the year 1975.
The property of being prime (or not) is called primality.
A simple but slow method of verifying the primality of a given number n is known as trial division.
It consists of testing whether n is a multiple of any integer between 2 and itself.
Algorithms much more efficient than trial division have been devised to test the primality of large numbers.
These include the Miller–Rabin primality test, which is fast but has a small probability of error, and the AKS primality test, which always produces the correct answer in polynomial time but is too slow to be practical.
Particularly fast methods are available for numbers of special forms, such as Mersenne numbers.
As of January 2016, the largest known prime number has 22,338,618 decimal digits.
"""

#Question 1
result = nlp(question="What is a simple method to verify primality?", context=context)

print(f"Answer 1: '{result['answer']}'")

#Question 2
result = nlp(question="When did Bill gates founded Microsoft?", context=context)

print(f"Answer 2: '{result['answer']}'")

#c) Machine Translation

# Example 1
# English to German
translator_ger = pipeline("translation_en_to_de")
print("German: ",translator_ger("Joe Biden became the 46th president of U.S.A.", max_length=40)[0]['translation_text'])

# Example 2
# English to French
translator_fr = pipeline('translation_en_to_fr')
print("French: ",translator_fr("Joe Biden became the 46th president of U.S.A",  max_length=40)[0]['translation_text'])
