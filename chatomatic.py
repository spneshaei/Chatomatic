# Case is not important in the questions

from qa_database import *
import random
from rank_bm25 import *
import numpy as np
from sentence_transformers import SentenceTransformer, util
from transformers import AutoTokenizer, AutoModel
import torch

sent_sim_model = SentenceTransformer('sentence-transformers/msmarco-distilbert-base-tas-b')

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

    def find_most_similar_question_transformers(self, question, language = "en"):
        qa_database = self.qa_databases[language]
        corpus = [doc.title for doc in qa_database.questions]
        corpus_embeddings = sent_sim_model.encode(corpus, convert_to_tensor=True)
        sentence_embedding = sent_sim_model.encode(question, convert_to_tensor=True)
        cos_scores = util.pytorch_cos_sim(sentence_embedding, corpus_embeddings)[0]
        print(cos_scores)
        top_result = np.argpartition(-cos_scores, range(1))[0]
        return qa_database.questions[top_result]

    def find_most_similar_question_bm25(self, question, language = "en"):
        qa_database = self.qa_databases[language]
        tokenized_corpus = [doc.title.split(" ") for doc in qa_database.questions]
        bm25 = BM25Okapi(tokenized_corpus)
        tokenized_query = question.split(" ")
        doc_scores = bm25.get_scores(tokenized_query)
        print(doc_scores)
        doc_scores = list(doc_scores)
        return qa_database.questions[doc_scores.index(max(doc_scores))]

    def find_most_similar_question(self, question, language = "en", method = "bm25"): # bm25 / transformers
        # From https://www.analyticsvidhya.com/blog/2021/05/build-your-own-nlp-based-search-engine-using-bm25/
        if not language in self.cache:
            self.cache[language] = {}
        if question in self.cache[language]:
            return self.cache[language][question]
        result = ""
        if method == "bm25":
            result = self.find_most_similar_question_bm25(question, language)
        elif method == "transformers":
            result = self.find_most_similar_question_transformers(question, language)
        self.cache[language][question] = result
        return result

    def answer(self, question, language = "en", method_for_similarity = "bm25"):
        question = question.lower()
        answer = self.find_answer_to_question(question, language)
        if answer is None:
            answer = self.random_generator.choice(self.find_most_similar_question(question, language, method_for_similarity).answers) # TODO: GAN
        return answer


chatomatic = Chatomatic("test.yml")
# print(chatomatic.answer("great, thanks"))
# print(chatomatic.answer("wow, thank you", method_for_similarity="transformers"))
print(chatomatic.answer("nice, tnxx", method_for_similarity="transformers"))
# all return "You're welcome!"