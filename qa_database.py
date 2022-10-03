import yaml
import json

class Question:
    def __init__(self, title, answers = []):
        self.title = title
        self.answers = answers

class QADatabase:
    def __init__(self, questions = []):
        self.questions = questions

    def load_from_yaml(self, file_name):
        with open(file_name, 'r') as f:
            conversations = yaml.safe_load(f)['conversations']
            new_questions = []
            for conversation in conversations:
                answers = []
                for i in range(1, len(conversation), 2):
                    answers.append(conversation[i])
                new_questions.append(Question(conversation[0].lower(), answers))
            self.questions = new_questions

    def load_from_json(self, file_name):
        with open(file_name, 'r') as f:
            conversations = json.load(f)['conversations']
            new_questions = []
            for conversation in conversations:
                all_answers = []
                for answer in conversation['answers']:
                    all_answers.append(answer)
                new_questions.append(Question(conversation['question'].lower(), all_answers))
            self.questions = new_questions