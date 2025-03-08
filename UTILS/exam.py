from random import shuffle


from UTILS import HTMLUtils
from UTILS import questions as qUtils


def examGenerator(
    folderPath, numberOfExams=1, numberOfQuestions=30, questionsPerTopic=None
):
    output = "./ExamenTest.html"
    for exam in range(numberOfExams):
        questions = qUtils.questionGenerator(
            folderPath, numberOfQuestions, questionsPerTopic
        )
        # Randomize the order of the questions
        shuffle(questions)
        HTMLUtils.examWriter(questions, "./ExamenTest" + str(exam + 1) + ".html")
