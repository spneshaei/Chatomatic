class Question:
    def __init__(self, title, answers = []):
        self.title = title
        self.answers = answers

class QADatabase:
    def __init__(self, questions = []):
        self.questions = questions

    def load_from_yaml(self, file_name):
        import yaml
        with open(file_name, 'r') as f:
            conversations = yaml.safe_load(f)['conversations']
            new_questions = []
            for conversation in conversations:
                answers = []
                for i in range(1, len(conversation), 2):
                    answers.append(conversation[i])
                new_questions.append(Question(conversation[0], answers))
            self.questions = new_questions

# Test

qa = QADatabase()
qa.load_from_yaml('test.yml')
print(qa.questions[13].title)
print(qa.questions[13].answers)