from __future__ import annotations

import json

import openai

from src.utils import constants

prompt = (
    "Hola ChatGPT, necesito que te comportes como un educador con experiencia en técnicas didácticas para facilitar "
    "el aprendizaje.\n"
    "Tu objetivo es generar una quiz de 5 preguntas de selección multiple de 3 opciones por pregunta, basados "
    "en el tema brindado.\n"
    "Esto con la intención de que el usuario pueda reforzar su conocimiento de forma positiva y divertida.\n"
    "Las preguntas no deben exceder 3 lineas y las opciones de respuestas deben ser todas de una sola linea.\n"
    "Desarrolla las preguntas con un nivel de dificultad bajo o fácil.\n"
    "Diversifica las opciones verdaderas, no permitas que todas las respuestas sean la opción a, b, o c.\n"
    "Asegurate de que las preguntas y posibles respuestas hagan sentido y sean fáciles de interpretar.\n"
    "El formato del quiz debe ser el siguiente: ```\n"
    "[\n"
    "    {\n"
    '        "question": "What is the difference between Docker and Kubernetes?",\n'
    '        "options": [\n'
    '            "Docker is a containerization platform whereas Kubernetes is a container orchestration platform",\n'
    '            "Kubernetes is a containerization platform whereas Docker is a container orchestration platform",\n'
    '            "Both are containerization platforms",\n'
    '            "Neither are containerization platforms"\n'
    "        ],\n"
    '        "answer": "Docker is a containerization platform whereas Kubernetes is a container orchestration '
    'platform",\n'
    '        "explanation": "Docker helps you create, deploy, and run applications within containers, while Kubernetes '
    'helps you manage collections of containers, automating their deployment, scaling, and more."\n'
    "    },\n"
    "]\n"
    "```\n"
    "Puedes observar que cada pregunta es un diccionario dentro de una lista, y esta lista debe tener en total"
    " las 5 preguntas.\n"
    "Valida las preguntas desarrolladas.\n"
    "No compartas información falsa.\n"
)

topic = (
    "Tema para el desarrollo de quiz: ```\n"
    "La inteligencia artificial (AI) es la capacidad de una máquina para realizar las funciones cognitivas que "
    "asociamos con la mente humana, como percibir, razonar, aprender, interactuar con un entorno, resolver problemas e "
    "incluso ejercitar la creatividad.\n"
    '"La inteligencia artificial es la nueva electricidad." - Dr. Andrew Ng.\n'
    "Machine Learning (ML) se basa en algoritmos que pueden aprender de los datos sin depender de una programación "
    "basada en reglas.\n"
    "Deep Learning (DL) es un tipo de ML que puede procesar una gama más amplia de recursos de datos "
    "(imágenes, por ejemplo, además de texto), requiere incluso menos intervención humana y, a menudo, "
    "puede producir resultados más precisos que el aprendizaje automático tradicional.\n"
    "Generative AI (GenAI) describe algoritmos (como ChatGPT) que se pueden utilizar para crear contenido nuevo, "
    "incluido audio, código, imágenes, texto, simulaciones y videos.\n"
    "```"
)


def get_quiz(api_key: str, prompt: str = prompt, topic: str = topic) -> dict[str, str]:
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": topic},
        ],
    )
    quiz = response["choices"][0]["message"]["content"]
    print(f"Response:\n{quiz}")
    return json.loads(quiz)


def load_quiz(json_path=f"{constants.DATA_DIR}/questions.json"):
    with open(json_path) as file:
        quiz = json.load(file)
        print(f"Response:\n{quiz}")
        return quiz
