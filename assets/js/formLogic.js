/* assets/js/formLogic.js */

// Procesa preguntas de opción única
function processSingleChoice(question) {
    const totalQuestions = document.querySelectorAll('.question').length;
    const weight = 10 / totalQuestions;

    // Respuesta correcta (oculta en input hidden)
    const correctInput = question.querySelector('input[type="hidden"][name^="correct_"]');
    const correctAnswer = correctInput ? correctInput.value.trim() : "";

    // Opción seleccionada
    const selected = question.querySelector('input[type="radio"]:checked');
    const isCorrect = (selected && selected.value.trim() === correctAnswer);

    // Muestra la respuesta correcta y color verde/rojo
    let answerDisplay = question.querySelector('.correct-answer');
    if (answerDisplay) {
        answerDisplay.style.display = "block";
        answerDisplay.style.color = isCorrect ? "green" : "red";
    }

    // Retorna la puntuación parcial de esta pregunta
    return isCorrect ? weight : 0;
}

// Procesa preguntas de opción múltiple
function processMultipleChoice(question) {
    const totalQuestions = document.querySelectorAll('.question').length;
    const weight = 10 / totalQuestions;

    // Respuestas correctas en hidden, p.ej. "A, B"
    const correctInput = question.querySelector('input[type="hidden"][name^="correct_"]');
    const correctAnswerStr = correctInput ? correctInput.value.trim() : "";
    const correctAnswers = correctAnswerStr.split(",").map(s => s.trim()).filter(s => s);

    // Respuestas marcadas
    const selectedInputs = question.querySelectorAll('input[type="checkbox"]:checked');
    const selectedAnswers = Array.from(selectedInputs).map(input => input.value.trim());

    // Compara ambas listas (ordenadas)
    correctAnswers.sort();
    selectedAnswers.sort();
    const isCorrect = (
        correctAnswers.length === selectedAnswers.length &&
        correctAnswers.every((val, index) => val === selectedAnswers[index])
    );

    // Muestra la respuesta correcta
    let answerDisplay = question.querySelector('.correct-answer');
    if (answerDisplay) {
        answerDisplay.style.display = "block";
        answerDisplay.style.color = isCorrect ? "green" : "red";
    }

    return isCorrect ? weight : 0;
}

// Función principal para manejar el envío
function submitForm() {
    // Desactiva el botón de envío
    const form = document.getElementById("testForm");
    form.elements["submitButton"].disabled = true;

    let totalScore = 0;
    let correctCount = 0;
    let incorrectCount = 0;

    // Recorre todas las preguntas
    const questions = document.querySelectorAll(".question");
    questions.forEach((question) => {
        let questionScore = 0;

        // Detecta si es singleChoice o multipleChoice
        if (question.classList.contains("singleChoice")) {
            questionScore = processSingleChoice(question);
        } else if (question.classList.contains("multipleChoice")) {
            questionScore = processMultipleChoice(question);
        }

        // Acumula puntuación
        totalScore += questionScore;

        // Contabiliza aciertos/fallos
        if (questionScore > 0) {
            correctCount++;
        } else {
            incorrectCount++;
        }
    });

    // Bloquea las casillas (radio y checkbox) para no poder cambiar después
    questions.forEach((question) => {
        let inputs = question.querySelectorAll('input[type="radio"], input[type="checkbox"]');
        inputs.forEach((inp) => {
            inp.disabled = true;
        });
    });

    // Muestra resultado final
    const scoreDisplay = document.getElementById("scoreDisplay");
    scoreDisplay.innerHTML = 
        "Preguntas acertadas: " + correctCount + "<br>" +
        "Preguntas falladas: " + incorrectCount + "<br>" +
        "Puntuación total: " + totalScore.toFixed(2) + "/10";

    // Evita recarga/submit normal
    return false;
}
