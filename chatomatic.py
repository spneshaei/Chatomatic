# Case is not important in the questions

from qa_database import *
import random

class Chatomatic:
    random_generator = random.Random()

    def __init__(self, file_path):
        self.qa_database = QADatabase()
        if file_path.endswith('.yml') or file_path.endswith('.yaml'):
            self.qa_database.load_from_yaml(file_path)

    def find_answer_to_question(self, question):
        for qa in self.qa_database.questions:
            if qa.title == question:
                # select a random answer
                return self.random_generator.choice(qa.answers)
        return None

    def answer(self, question):
        question = question.lower()
        answer = self.find_answer_to_question(question)
        if answer is None:
            return "I don't know" # TODO: Use similarity to find the best answer
        return answer


chatomatic = Chatomatic("test.yml")
print(chatomatic.answer("great, thanks"))
print(chatomatic.answer("greaT, thanks"))
print(chatomatic.answer("Great, thanks"))