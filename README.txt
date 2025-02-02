# Creador de tests

## Resumen

Esto es un programa que crea exámenes tipo tests eligiendo las preguntas y poniendo el orden de las respuestas de manera aleatoria. Una vez generado el html se puede responder al examen y se autocorrige y da la nota que se ha sacado.

## Uso

Para generar exámenes hay que ejecutar el fichero llamado [Test.py](/Test.py). Ahora mismo el número de exámenes, el número de preguntas y la asignatura está codificado como variables en el código. Si las cambias no subas esos cambios al github.

## Contribuir

La manera fácil de contribuir es añadiendo más preguntas. Esto se hace modificando o añadiendo ficheros .json que hay en cada carpeta de asignatura. Ahora mismo para que identifique el archivo, este tiene que empezar por Unit y acabar por .json. Cada archivo es un diccionario cuya única clave es `questions` y su valor es una lista de diccionarios. Para escribir una pregunta tipo test hay que poner la pregunta en la clave `question`, las opciones en la clave `options` (será una lista de strings), la respuesta en la clave `correct_option` (será un entero del índice de la lista de opciones; empieza en 0) y el tipo de pregunta con la clave `questionType` que tendrá como valor `multipleChoice`. Antes de subir una pregunta nueva asegúrate de que está bien escrita, la respuesta es la correcta y que el programa sigue funcionando.

Para hacer esto haz un fork con el nombre de la asignatura a la que quieres añadir preguntas y añade las preguntas. Luego haz un pull request y si todo está bien se añadirá al programa.

Si quieres cambiar el código para mejorarlo o refactorizarlo, abre un issue y hablamos si los cambios que propones son útiles para este proyecto.
