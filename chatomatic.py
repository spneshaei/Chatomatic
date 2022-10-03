# Case is not important in the questions

from qa_database import *
import random
from rank_bm25 import *
import numpy as np

class Chatomatic:
    random_generator = random.Random()
    cache = {}
    qa_databases = {}

    def load_from_dataset(self, file_path, qa_database):
        if file_path.endswith('.yml') or file_path.endswith('.yaml'):
            qa_database.load_from_yaml(file_path)
        elif file_path.endswith('.json'):
            qa_database.load_from_json(file_path)


    def __init__(self, file_path, language = "en"):
        self.qa_databases[language] = QADatabase()
        self.load_from_dataset(file_path, self.qa_databases[language])
    
    def add_dataset(self, file_path, language = "en"):
        if not language in self.qa_databases:
            self.qa_databases[language] = QADatabase()
        self.load_from_dataset(file_path, self.qa_databases[language])

    def find_answer_to_question(self, question, language = "en"):
        qa_database = self.qa_databases[language]
        for qa in qa_database.questions:
            if qa.title == question:
                # select a random answer
                return self.random_generator.choice(qa.answers)
        return None

    def find_most_similar_question(self, question, language = "en"): # From https://www.analyticsvidhya.com/blog/2021/05/build-your-own-nlp-based-search-engine-using-bm25/
        if not language in self.cache:
            self.cache[language] = {}
        if question in self.cache[language]:
            return self.cache[language][question]
        qa_database = self.qa_databases[language]
        tokenized_corpus = [doc.title.split(" ") for doc in qa_database.questions]
        bm25 = BM25Okapi(tokenized_corpus)
        tokenized_query = question.split(" ")
        doc_scores = bm25.get_scores(tokenized_query)
        doc_scores = list(doc_scores)
        result = qa_database.questions[doc_scores.index(max(doc_scores))]
        self.cache[language][question] = result
        return result

    def answer(self, question, language = "en"):
        question = question.lower()
        answer = self.find_answer_to_question(question, language)
        if answer is None:
            answer = self.random_generator.choice(self.find_most_similar_question(question, language).answers) # TODO: GAN
        return answer


chatomatic = Chatomatic("test.yml")
print(chatomatic.answer("great, thanks"))
chatomatic.add_dataset("test.json", language="fr")
print(chatomatic.answer("great, thanks", language="fr"))