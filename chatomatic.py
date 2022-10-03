# Case is not important in the questions

from qa_database import *
import random
from rank_bm25 import *
import numpy as np

class Chatomatic:
    random_generator = random.Random()

    def __init__(self, file_path):
        self.qa_database = QADatabase()
        if file_path.endswith('.yml') or file_path.endswith('.yaml'):
            self.qa_database.load_from_yaml(file_path)
        elif file_path.endswith('.json'):
            self.qa_database.load_from_json(file_path)

    def find_answer_to_question(self, question):
        for qa in self.qa_database.questions:
            if qa.title == question:
                # select a random answer
                return self.random_generator.choice(qa.answers)
        return None

    def find_most_similar_question(self, question): # From https://www.analyticsvidhya.com/blog/2021/05/build-your-own-nlp-based-search-engine-using-bm25/
        tokenized_corpus = [doc.title.split(" ") for doc in self.qa_database.questions]
        bm25 = BM25Okapi(tokenized_corpus)
        tokenized_query = question.split(" ")
        doc_scores = bm25.get_scores(tokenized_query)
        doc_scores = list(doc_scores)
        return self.qa_database.questions[doc_scores.index(max(doc_scores))]

    def answer(self, question):
        question = question.lower()
        answer = self.find_answer_to_question(question)
        if answer is None:
            answer = self.random_generator.choice(self.find_most_similar_question(question).answers) # TODO: GAN
        return answer


chatomatic = Chatomatic("test.json")
print(chatomatic.answer("great, thanks"))
print(chatomatic.answer("Great thakss"))