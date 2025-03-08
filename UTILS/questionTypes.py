from random import shuffle
import os


def randomizeSingleChoice(question: dict) -> dict:
    """
    Randomize the order of the options in a single choice question

    Args:
        - question (dict): The question data. It requires the following keys:
            - question (str): The question text
            - options (list): A list with the possible answers
            - correct_option (int): The index of the correct answer

    Returns:
        - dict: The question data with the options randomized
    """
    correct = question["options"][question["correct_option"]]
    shuffle(question["options"])
    question["correct_option"] = question["options"].index(correct)
    return question


def randomizeMultipleChoice(question: dict) -> dict:
    """
    Randomize the order of the options in a multiple choice question

    Args:
        - question (dict): The question data. It requires the following keys:
            - question (str): The question text
            - options (list): A list with the possible answers
            - correct_options (list): A list with the indexes of the correct answers

    Returns:
        - dict: The question data with the options randomized
    """
    correct = [question["options"][i] for i in question["correct_options"]]
    shuffle(question["options"])
    question["correct_options"] = [question["options"].index(c) for c in correct]
    return question


def singleChoiceWriter(question: dict, nQuestion=int) -> str:
    """
    Generate the HTML for a single choice question

    Args:
        - question (dict): The question data. It requires the following keys:
            - question (str): The question text
            - options (list): A list with the possible answers
            - correct_option (int): The index of the correct answer
            - questionType (str): The type of question
            It also can have the following optional keys:
            - folder (str): The folder where the images are located
            - images (list): A list with the names of the images
        - nQuestion (int): The question number. It needs to be in base 0

    Returns:
        - str: The HTML code for the question
    """
    # First we randomize the order of the options
    question = randomizeSingleChoice(question)

    question_text = question["question"]
    options = question["options"]
    correct_option = question["correct_option"]
    option_html = ""

    # Generate the HTML for the options
    for j, option in enumerate(options):
        option_letter = chr(ord("A") + j)  ## Convertir el índice en una letra
        option_html += f'<li><input type="radio" name="question_{nQuestion}" value="{option_letter}"> {option_letter}) {option}</li>'

    # Add the images to the question
    images = ""
    if "images" in question:
        for im in question["images"]:
            location = os.path.join(question["folder"], im)
            images += f'<img src="{location}" alt="imagen">'

    correct_html = f'<p class="correct-answer">Respuesta correcta: {chr(ord("A") + correct_option)}</p>'
    correct_hidden_input = f'<input type="hidden" name="correct_{nQuestion}" value="{chr(ord("A") + correct_option)}">'

    return f"""
            <div class="{question['questionType']} question">
                <p>{nQuestion + 1}: {question_text}</p>  <!-- Mostrar el número de pregunta -->
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
    Generate the HTML for a multiple choice question

    Args:
        - question (dict): The question data. It requires the following keys:
            - question (str): The question text
            - options (list): A list with the possible answers
            - correct_options (list): A list with the indexes of the correct answers
            - questionType (str): The type of question
            It also can have the following optional keys:
            - folder (str): The folder where the images are located
            - images (list): A list with the names of the images
        - nQuestion (int): The question number. It needs to be in base 0

    Returns:
        - str: The HTML code for the question
    """
    # First we randomize the order of the options
    question = randomizeMultipleChoice(question)

    question_text = question["question"]
    options = question["options"]
    correct_options = question["correct_options"]
    option_html = ""

    # Generate the HTML for the options
    for j, option in enumerate(options):
        option_letter = chr(ord("A") + j)  ## Convertir el índice en una letra
        option_html += f'<li><input type="checkbox" name="question_{nQuestion}" value="{option_letter}"> {option_letter}) {option}</li>'

    # Add the images to the question
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
                <p>{nQuestion + 1}: {question_text}</p>  <!-- Mostrar el número de pregunta -->
                {images}
                <ul>
                    {option_html}
                </ul>
                {correct_html}
                {correct_hidden_input}
            </div>
            """
