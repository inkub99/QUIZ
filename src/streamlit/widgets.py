from __future__ import annotations

import openai
import streamlit as st

from src.quiz.get_quiz import get_quiz_from_topic
from src.utils import config


def display_question():
    # Handle first case
    if len(st.session_state.questions) == 0:
        try:
            first_question = get_quiz_from_topic("ai", st.secrets.openai.api_key)
        except openai.error.AuthenticationError:
            st.error(
                "Please enter a valid OpenAI API key in the left sidebar to proceed. "
                "To know how to obtain the key checkout readme for this project here: "
                "https://github.com/Dibakarroy1997/QuizWhizAI/blob/main/README.md",
            )
            return
        st.session_state.questions.append(first_question)

    # Disable the submit button if the user has already answered this question
    submit_button_disabled = (
        st.session_state.current_question in st.session_state.answers
    )

    # Get the current question from the questions list
    question = st.session_state.questions[st.session_state.current_question]

    # Display the question prompt
    st.write(f"{st.session_state.current_question + 1}. {question['question']}")

    # Use an empty placeholder to display the radio button options
    options = st.empty()

    # Display the radio button options and wait for the user to select an answer
    user_answer = options.radio(
        config.config()["app"]["quiz"]["choice"],
        question["options"],
        key=st.session_state.current_question,
    )

    # Display the submit button and disable it if necessary
    submit_button = st.button("Submit", disabled=submit_button_disabled)

    # If the user has already answered this question, display their previous answer
    if st.session_state.current_question in st.session_state.answers:
        index = st.session_state.answers[st.session_state.current_question]
        options.radio(
            config.config()["app"]["quiz"]["choice"],
            question["options"],
            key=float(st.session_state.current_question),
            index=index,
        )

    # If the user clicks the submit button, check their answer and show the explanation
    if submit_button:
        # Record the user's answer in the session state
        st.session_state.answers[st.session_state.current_question] = question[
            "options"
        ].index(user_answer)

        # Check if the user's answer is correct and update the score
        if user_answer == question["answer"]:
            st.write(config.config()["app"]["quiz"]["correct"])
            st.session_state.right_answers += 1
        else:
            st.write(f"{config.config()['app']['quiz']['wrong']}{question['answer']}.")
            st.session_state.wrong_answers += 1

        # Show an expander with the explanation of the correct answer
        with st.expander():
            st.write(question[config.config()["app"]["quiz"]["explanation"]])

    # Display the current score
    st.write(
        f"{config.config()['app']['quiz']['counter_right']}{st.session_state.right_answers}",
    )
    st.write(
        f"{config.config()['app']['quiz']['counter_wrong']}{st.session_state.wrong_answers}",
    )


# Define a function to go to the next question
def next_question():
    # Move to the next question in the questions list
    st.session_state.current_question += 1

    # If we've reached the end of the questions list, get a new question
    if st.session_state.current_question > len(st.session_state.questions) - 1:
        try:
            next_question = get_quiz_from_topic("ai", st.secrets.openai.api_key)
        except openai.error.AuthenticationError:
            st.session_state.current_question -= 1
            return
        st.session_state.questions.append(next_question)


# Define a function to go to the previous question
def prev_question():
    # Move to the previous question in the questions list
    if st.session_state.current_question > 0:
        st.session_state.current_question -= 1
        st.session_state.explanation = None


# # Add download buttons to sidebar which download current questions
# download_button = st.sidebar.download_button(
#     "Download Quiz Data",
#     data=json.dumps(st.session_state.questions, indent=4),
#     file_name="quiz_session.json",
#     mime="application/json",
# )
