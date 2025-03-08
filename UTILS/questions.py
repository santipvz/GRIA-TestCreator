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

    for filePath in questionsOfEachUnit.keys():
        with open(
            filePath,
            "r",
            encoding="utf-8",
        ) as file:
            questionsData = json.load(file)
        numOfQuestionsInUnit = len(questionsData["questions"])

        enoughQuestions = questionsOfEachUnit[filePath] <= numOfQuestionsInUnit

        while questionsOfEachUnit[filePath] > 0:
            x = randint(0, numOfQuestionsInUnit - 1)
            questionAdded = copy.deepcopy(questionsData)
            questionAdded = questionAdded["questions"][x]
            questionAdded["folder"] = folderPath
            questionAdded["question"] = (
                questionAdded["question"]
                + " [Tema "
                + os.path.basename(filePath)[4:-5]
                + "]"
            )

            if enoughQuestions and questionAdded not in questions:
                questions.append(questionAdded)
                questionsOfEachUnit[filePath] -= 1

            elif not enoughQuestions:
                questions.append(questionAdded)
                questionsOfEachUnit[filePath] -= 1

    return questions


def findPatternFiles(pattern="Unit*.json", folderPath=".") -> list:
    """
    Returns a list of files that match the pattern
    in the given folderPath. The files are returned
    with their absolute path.

    Args:
        - pattern (str): The pattern to search for
        - folderPath (str): The folder to search in

    Returns:
        - list: The list of files that match the pattern
    """
    files = glob.glob(os.path.join(folderPath, pattern), recursive=True)
    pattern_re = re.compile(pattern.replace("*", "(.*?)"))

    matchingFiles = [os.path.abspath(file) for file in files if pattern_re.search(file)]

    return matchingFiles


def questionsByFile(filePath: str) -> dict:
    """
    Returns a dictionary with the questions of a file

    Args:
        - filePath (str): The path of the file to read

    Returns:
        - dict: A dictionary with the questions of the file
            The keys are the names of the files and the values
            the number of questions of each file
    """
    questions = {x: 0 for x in findPatternFiles(folderPath=filePath)}

    # We go file by file
    for f in questions.keys():
        with open(f, "r", encoding="utf-8") as file:
            questionsData = json.load(file)
            questions[f] = len(questionsData["questions"])

    # Eliminate the files that have no questions
    questions = {k: v for k, v in questions.items() if v > 0}

    return questions
