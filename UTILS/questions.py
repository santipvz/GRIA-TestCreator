from random import randint, choice
import json
import copy
import glob
import os
import re


def questionGenerator(folderPath, numOfQuestions=10, questionsOfEachUnit=None):
    questions = []
    namesOfUnits = findPatternFiles("Unit*.json", folderPath)

    if questionsOfEachUnit == None:
        questionsOfEachUnit = {key: 0 for key in namesOfUnits}

        for i in range(numOfQuestions):
            x = choice(list(questionsOfEachUnit.keys()))
            questionsOfEachUnit[x] += 1

    for unit in questionsOfEachUnit.keys():
        with open(
            os.path.join(folderPath, "Unit" + str(unit) + ".json"),
            "r",
            encoding="utf-8",
        ) as file:
            questionsData = json.load(file)
        numOfQuestionsInUnit = len(questionsData["questions"])

        enoughQuestions = questionsOfEachUnit[unit] <= numOfQuestionsInUnit

        while questionsOfEachUnit[unit] > 0:
            x = randint(0, numOfQuestionsInUnit - 1)
            questionAdded = copy.deepcopy(questionsData)
            questionAdded = questionAdded["questions"][x]
            questionAdded["folder"] = folderPath
            questionAdded["question"] = (
                questionAdded["question"] + " [Tema " + str(unit) + "]"
            )

            if enoughQuestions and questionAdded not in questions:
                questions.append(questionAdded)
                questionsOfEachUnit[unit] -= 1

            elif not enoughQuestions:
                questions.append(questionAdded)
                questionsOfEachUnit[unit] -= 1

    return questions


def findPatternFiles(pattern, folderPath):
    files = glob.glob(os.path.join(folderPath, pattern), recursive=True)
    pattern_re = re.compile(pattern.replace("*", "(.*?)"))
    matching_parts = [pattern_re.search(file).group(1) for file in files]
    return matching_parts
