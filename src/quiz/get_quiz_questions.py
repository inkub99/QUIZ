from __future__ import annotations

import json

import openai

from src.utils import constants

prompt = (
    "Witamy w quizie PBC"
)

topic = (
    "Quiz składa sie z 6 pytań"
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
    with open(json_path, encoding="utf-8") as file:
        quiz = json.load(file)
        print(f"Response:\n{quiz}")
        return quiz
