/* assets/js/formLogic.js */
function submitForm() {
    var form = document.getElementById("testForm");
    form.elements["submitButton"].disabled = true;

    var totalScore = 0;
    var questions = document.querySelectorAll(".question");

    questions.forEach((question) => {
        if (question.classList.contains("singleChoice")) {
            totalScore += processSingleChoice(question);
        } else if (question.classList.contains("multipleChoice")) {
            totalScore += processMultipleChoice(question);
        }
    });

    // Se asume que la puntuación se normaliza sobre 10 (se puede ajustar)
    document.getElementById("scoreDisplay").innerHTML = "Puntuación total: " + totalScore.toFixed(2) + "/10";
    return false;
}
