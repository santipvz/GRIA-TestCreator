# UTILS/questions.py
import random
import json
import copy
import glob
import os
import re


def questionGenerator(
    folderPath: str, numOfQuestions: int = 10, questionsOfEachUnit: dict = None
) -> list:
    """
    Genera una lista de preguntas a partir de los archivos en folderPath.
    """
    questions = []
    questionsByFileDict = questionsByFileInFolder(folderPath)
    maxQuestions = sum(questionsByFileDict.values())
    if numOfQuestions > maxQuestions:
        print(
            "There are not enough questions to generate. Some questions will be repeated."
        )

    if questionsOfEachUnit is None:
        questionsOfEachUnit = {key: 0 for key in questionsByFileDict.keys()}
        while sum(questionsOfEachUnit.values()) < numOfQuestions:
            x = random.choice(list(questionsOfEachUnit.keys()))
            if (
                questionsOfEachUnit[x] < questionsByFileDict[x]
                or numOfQuestions > maxQuestions
            ):
                questionsOfEachUnit[x] += 1

    for f in questionsOfEachUnit.keys():
        if questionsOfEachUnit[f] >= questionsByFileDict[f]:
            print(f"The file {os.path.basename(f)} has no more questions.")

    for filePath in questionsOfEachUnit.keys():
        with open(filePath, "r", encoding="utf-8") as file:
            questionsData = json.load(file)
        numOfQuestionsInUnit = len(questionsData["questions"])
        if questionsOfEachUnit[filePath] < numOfQuestionsInUnit:
            choosenQuestions = random.sample(
                questionsData["questions"], questionsOfEachUnit[filePath]
            )
        else:
            choosenQuestions = [
                copy.deepcopy(item)
                for item in random.choices(
                    questionsData["questions"], k=questionsOfEachUnit[filePath]
                )
            ]
        for q in choosenQuestions:
            q["folder"] = folderPath
            q["question"] = (
                q["question"] + " [Tema " + os.path.basename(filePath)[4:-5] + "]"
            )
        questions.extend(choosenQuestions)
    return questions


def findPatternFiles(pattern="Unit*.json", folderPath=".") -> list:
    files = glob.glob(os.path.join(folderPath, pattern), recursive=True)
    pattern_re = re.compile(pattern.replace("*", "(.*?)"))
    matchingFiles = [os.path.abspath(file) for file in files if pattern_re.search(file)]
    return matchingFiles


def questionsByFileInFolder(folderPath: str) -> dict:
    questions = {x: 0 for x in findPatternFiles(folderPath=folderPath)}
    for f in questions.keys():
        with open(f, "r", encoding="utf-8") as file:
            questionsData = json.load(file)
            questions[f] = len(questionsData["questions"])
    questions = {k: v for k, v in questions.items() if v > 0}
    return questions


def validFolders() -> dict:
    filePath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    folders = {
        f: questionsByFileInFolder(f) for f in os.listdir(filePath) if os.path.isdir(f)
    }
    folders = {k: v for k, v in folders.items() if v}
    return folders


def showNumberOfQuestions() -> None:
    data = validFolders()
    data = dict(sorted(data.items(), key=lambda x: x[0]))
    data = {k: dict(sorted(v.items(), key=lambda x: x[0])) for k, v in data.items()}
    for folder, files in data.items():
        print(f"{folder}: {sum(files.values())}")
        for file, questions in files.items():
            print(f"\t{os.path.basename(file)}: {questions}")


if __name__ == "__main__":
    showNumberOfQuestions()
