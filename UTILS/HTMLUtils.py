# UTILS/HTMLUtils.py
import os
from jinja2 import Environment, FileSystemLoader
from UTILS import questionTypes

env = Environment(loader=FileSystemLoader("assets/templates"))


def prepare_options(question):
    options = []
    if question["questionType"] == "singleChoice":
        question = questionTypes.randomizeSingleChoice(question)
        for idx, option in enumerate(question["options"]):
            options.append({"letter": chr(ord("A") + idx), "text": option})
        question["correct_letter"] = chr(ord("A") + question["correct_option"])
    elif question["questionType"] == "multipleChoice":
        question = questionTypes.randomizeMultipleChoice(question)
        for idx, option in enumerate(question["options"]):
            options.append({"letter": chr(ord("A") + idx), "text": option})
        correct_letters = sorted(
            [chr(ord("A") + i) for i in question["correct_options"]]
        )
        question["correct_letter"] = ", ".join(correct_letters)
    return options, question


def examWriter(questions, fileOutName, style):
    base_template = env.get_template("base.html")
    question_blocks = []
    # Mapeo para traducir el valor de questionType a nombre de plantilla
    TEMPLATE_MAP = {
        "singleChoice": "question_single.html",
        "multipleChoice": "question_multiple.html",
    }
    for idx, question in enumerate(questions):
        options, question = prepare_options(question)
        q_template_name = TEMPLATE_MAP.get(
            question["questionType"], f"question_{question['questionType']}.html"
        )
        q_template = env.get_template(q_template_name)
        question_html = q_template.render(
            question_number=idx + 1,
            question_text=question["question"],
            options=options,
            correct_letter=question.get("correct_letter", "A"),
            folder=question.get("folder", ""),
        )
        question_blocks.append(question_html)

    output = base_template.render(
        questions_html="\n".join(question_blocks), style=style
    )
    with open(fileOutName, "w", encoding="utf-8") as f:
        f.write(output)