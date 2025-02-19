from random import randint, shuffle, choice
import json
import copy
import glob
import os
import re
from typing import List


def combineFunctions(functions: List[str]) -> str:
    # Join the list of functions into a single string
    combinedFunctions = "\n".join(functions)

    # Wrap the combined functions in a <script> tag
    combinedScript = f"<script>\n{combinedFunctions}\n</script>"

    return combinedScript


def findPatternFiles(pattern, folderPath):
    files = glob.glob(os.path.join(folderPath, pattern), recursive=True)
    pattern_re = re.compile(pattern.replace("*", "(.*?)"))
    matching_parts = [pattern_re.search(file).group(1) for file in files]
    return matching_parts


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


def testRandomizer(listOfQuestions):
    shuffle(listOfQuestions)
    for question in listOfQuestions:
        if question["questionType"] == "singleChoice":
            correct = question["options"][question["correct_option"]]
            shuffle(question["options"])
            question["correct_option"] = question["options"].index(correct)
    return listOfQuestions


def examWriter(questions, fileOutName):
    submitFormFunction = """function submitForm() {
        var form = document.getElementById("testForm");
        form.elements["submitButton"].disabled = true;

        var correctGlobal = 0;
        var incorrectGlobal = 0;
        var unanswered = 0;
        var totalScore = 0;

        var questions = document.getElementsByClassName("singleChoice");

        for (var question of questions) {
            var score = singleChoice(question);
            if (score === 1) {
                correctGlobal++;
                totalScore += score;
            } else if (isNaN(score)) {
                unanswered++;
            } else {
                incorrectGlobal++;
                totalScore += score;
            }
        }

        // We calculate the score out of 10
        totalScore = ((totalScore / questions.length) * 10).toFixed(2);

        var scoreDisplay = document.getElementById("scoreDisplay");
        scoreDisplay.innerHTML = "Preguntas acertadas: " + correctGlobal + "<br>Preguntas falladas: " + incorrectGlobal + "<br>Puntuación total: " + totalScore + "/10";

        return false;
    }
"""

    singleChoiceFunction = """function singleChoice(question) {
        var selectedInput = question.querySelector("input:checked");
        var correctAnswer = question.querySelector(".correct-answer");
        correctAnswer.style.display = "block";
        // We only count the ones with radio buttons
        var numOptions = question.querySelectorAll("input[type=radio]").length;

        if (selectedInput && selectedInput.value === correctAnswer.innerHTML.split(":")[1].trim()) {
            correctAnswer.classList.add("correct");
        } else {
            correctAnswer.classList.add("incorrect");
        }

        // If it is correct we return 1
        if (selectedInput && selectedInput.value === correctAnswer.innerHTML.split(":")[1].trim()) {
            return 1;
        } //If there is no answer we return NaN
        else if (selectedInput === null) {
            return NaN;
        } //If it is incorrect we return the penalty for random guessing
        else {
            return -1 / (numOptions - 1);
        }
    }
"""

    html_head = """
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Examen</title>
        <style>
            body {font-family: Arial, sans-serif; 
                }
                .correct {
                    color: green;
                }
                .incorrect {
                    color: red;
                }
                .question {
                    margin-bottom: 19px;
                }
                .question p {
                    font-weight: bold;
                    font-size: 19px;
                }
                .question span {
                    font-size: 17px;
                    font-style: italic;
                }
                .question li {
                    font-size: 18px;
                    list-style-type: none;
                }
                .correct-answer {
                    display: none;
                    font-weight: bold;
                    font-size: 16px;
                }
                .answered {
                    pointer-events: none;
                }
            
        </style>
    </head>
    <body>
        <form id="testForm" onsubmit="return submitForm()">
    """

    html_tail = """
            <input id="submitButton" type="submit" value="Enviar respuestas">
        </form>
        <p id="scoreDisplay"></p>
    </body>
    </html>
    """

    fileOut = open(fileOutName, "w", encoding="utf-8")
    fileOut.write(html_head)

    for i, question in enumerate(questions[:numOfQuestions]):
        """
        ##########################################################
        Here is where we would check the question type and generate the HTML accordingly.
        ##########################################################
        """

        question_number = i + 1  ## Incrementar el número de pregunta

        question_text = question["question"]
        options = question["options"]
        correct_option = question["correct_option"]
        option_html = ""
        for j, option in enumerate(options):
            option_letter = chr(ord("A") + j)  ## Convertir el índice en una letra
            option_html += f'<li><input type="radio" name="question_{i}" value="{option_letter}"> {option_letter}) {option}</li>'

        images = ""
        if "images" in question:
            for im in question["images"]:
                location = os.path.join(question["folder"], im)
                images += f'<img src="{location}" alt="imagen">'

        correct_html = f'<p class="correct-answer">Respuesta correcta: {chr(ord("A") + correct_option)}</p>'
        correct_hidden_input = f'<input type="hidden" name="correct_{i}" value="{chr(ord("A") + correct_option)}">'

        fileOut.write(
            f"""
        <div class="{question['questionType']} question">
            <p>{question_number}: {question_text}</p>  <!-- Mostrar el número de pregunta -->
            {images}
            <ul>
                {option_html}
            </ul>
            {correct_html}
            {correct_hidden_input}
        </div>
        """
        )

    fileOut.write(html_tail)
    fileOut.write(combineFunctions([submitFormFunction, singleChoiceFunction]))
    fileOut.close()


def examGenerator(
    folderPath, numberOfExams=1, numberOfQuestions=30, questionsPerTopic=None
):
    output = "./ExamenTest.html"
    for exam in range(numberOfExams):
        questions = questionGenerator(folderPath, numberOfQuestions, questionsPerTopic)
        questions = testRandomizer(questions)
        examWriter(questions, "./ExamenTest" + str(exam + 1) + ".html")


numExams = 2
numOfQuestions = 10
folder = "PIC"


examGenerator(folder, numExams, numOfQuestions)
