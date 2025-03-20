# UTILS/questionTypes.py
from random import shuffle
import os


def randomizeSingleChoice(question: dict) -> dict:
    """
    Randomiza las opciones de una pregunta de opción simple.
    """
    correct = question["options"][question["correct_option"]]
    shuffle(question["options"])
    question["correct_option"] = question["options"].index(correct)
    return question


def randomizeMultipleChoice(question: dict) -> dict:
    """
    Randomiza las opciones de una pregunta de opción múltiple.
    """
    correct = [question["options"][i] for i in question["correct_options"]]
    shuffle(question["options"])
    question["correct_options"] = [question["options"].index(c) for c in correct]
    return question


def singleChoiceWriter(question: dict, nQuestion=int) -> str:
    """
    Genera el HTML para una pregunta de opción simple (método heredado).
    """
    question = randomizeSingleChoice(question)
    question_text = question["question"]
    options = question["options"]
    correct_option = question["correct_option"]
    option_html = ""
    for j, option in enumerate(options):
        option_letter = chr(ord("A") + j)
        option_html += f'<li><input type="radio" name="question_{nQuestion}" value="{option_letter}"> {option_letter}) {option}</li>'
    images = ""
    if "images" in question:
        for im in question["images"]:
            location = os.path.join(question["folder"], im)
            images += f'<img src="{location}" alt="imagen">'
    correct_html = f'<p class="correct-answer">Respuesta correcta: {chr(ord("A") + correct_option)}</p>'
    correct_hidden_input = f'<input type="hidden" name="correct_{nQuestion}" value="{chr(ord("A") + correct_option)}">'
    return f"""
            <div class="{question['questionType']} question">
                <p>{nQuestion + 1}: {question_text}</p>
                {images}
                <ul>
                    {option_html}
                </ul>
                {correct_html}
                {correct_hidden_input}
            </div>
            """


def multipleChoiceWriter(question: dict, nQuestion=int) -> str:
    """
    Genera el HTML para una pregunta de opción múltiple (método heredado).
    """
    question = randomizeMultipleChoice(question)
    question_text = question["question"]
    options = question["options"]
    correct_options = question["correct_options"]
    option_html = ""
    for j, option in enumerate(options):
        option_letter = chr(ord("A") + j)
        option_html += f'<li><input type="checkbox" name="question_{nQuestion}" value="{option_letter}"> {option_letter}) {option}</li>'
    images = ""
    if "images" in question:
        for im in question["images"]:
            location = os.path.join(question["folder"], im)
            images += f'<img src="{location}" alt="imagen">'
    correct_options_str = ", ".join(
        sorted([chr(ord("A") + i) for i in correct_options])
    )
    correct_html = (
        f'<p class="correct-answer">Respuestas correctas: {correct_options_str}</p>'
    )
    correct_hidden_input = f'<input type="hidden" name="correct_{nQuestion}" value="{correct_options_str}">'
    return f"""
            <div class="{question['questionType']} question">
                <p>{nQuestion + 1}: {question_text}</p>
                {images}
                <ul>
                    {option_html}
                </ul>
                {correct_html}
                {correct_hidden_input}
            </div>
            """
