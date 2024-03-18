from __future__ import annotations

import openai
import streamlit as st

from src.quiz.get_quiz_questions import get_quiz
from src.quiz.get_quiz_questions import load_quiz
from src.utils import config

from docx import Document
from docx.shared import Pt

def replace_text_in_runs(runs, old_text, new_text):
    for run in runs:
        if old_text in run.text:
            run.text = run.text.replace(old_text, new_text)
            # Zachowanie formatowania tekstu
            new_run = run._element
            for elem in new_run:
                if elem.tag.endswith('rPr'):
                    new_run.insert(0, elem)

def replace_text_in_docx(doc, old_text, new_text):
    for paragraph in doc.paragraphs:
        replace_text_in_runs(paragraph.runs, old_text, new_text)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                replace_text_in_runs(cell.paragraphs[0].runs, old_text, new_text)

def display_question():
    """
    Display a quiz question and handle user interactions with the question.

    The function takes no parameters.

    Returns:s
        None

    Raises:
        openai.error.AuthenticationError: If the OpenAI API key is invalid or missing.

    """

    # Handle first case
    if len(st.session_state.questions) == 0:
        try:

            first_question = get_quiz(
                "ai",
                st.secrets.openai.api_key,
            )
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
    submit_button = st.button(
        config.config()["app"]["quiz"]["submit"],
        disabled=submit_button_disabled,
    )

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
        with st.expander(config.config()["app"]["quiz"]["explanation"]):
            st.write(question["explanation"])

    # Display the current score
    st.write(
        f"{config.config()['app']['quiz']['counter_right']}{st.session_state.right_answers}",
    )
    st.write(
        f"{config.config()['app']['quiz']['counter_wrong']}{st.session_state.wrong_answers}",
    )


def display_question_v2():
    """
    Display a quiz question and handle user interactions with the question.

    The function takes no parameters.

    Returns:
        None

    Raises:
        FileNotFoundError: If the json file in the data dir is invalid or missing.

    """
    # Handle first case
    if len(st.session_state.questions) == 0:
        try:
            quiz = load_quiz()
            first_question = quiz[0]
        except FileNotFoundError:
            st.error(
                "The file containing the pre-generated questions could not be loaded. "
                "Please check your data folder...",
            )
            return
        st.session_state.questions.append(first_question)

    # Disable the submit button if the user has already answered this question
    submit_button_disabled = (
        st.session_state.current_question in st.session_state.answers
    )

    # Get the current question from the questions list
    try:
        question = st.session_state.questions[st.session_state.current_question]
    except IndexError:
        st.markdown(config.config()["app"]["quiz"]["over_message"])
        st.markdown(config.config()["app"]["quiz"]["score_message"])
        # Display the current score
        st.write(
            f"{config.config()['app']['quiz']['counter_right']}{st.session_state.right_answers}",
        )
        st.write(
            f"{config.config()['app']['quiz']['counter_wrong']}{st.session_state.wrong_answers}",
        )
        file_path = "PBC_certyfikat_wzor.docx"
        
        def download_report():
            doc = Document(file_path)
            replace_text_in_docx(doc, "Jan Kowalski", st.session_state.name)
            if st.session_state.name[-1] == 'a' or st.session_state.name[-1] == 'A':
                replace_text_in_docx(doc, "ukończył", "ukończyła")
            doc.save("PBC_certyfikat.docx")
            with open("PBC_certyfikat.docx", "rb") as f:
                doc_bytes = f.read()
            return doc_bytes

        st.download_button(
        label="Pobierz dyplom",
        data=download_report(),
        file_name="PBC_certyfikat.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

        return

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
    submit_button = st.button(
        config.config()["app"]["quiz"]["submit"],
        disabled=submit_button_disabled,
    )

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
        with st.expander(config.config()["app"]["quiz"]["explanation"]):
            st.write(question["explanation"])

    # Display the current score
    st.write(
        f"{config.config()['app']['quiz']['counter_right']}{st.session_state.right_answers}",
    )
    st.write(
        f"{config.config()['app']['quiz']['counter_wrong']}{st.session_state.wrong_answers}",
    )


# Define a function to go to the next question
def next_question():
    """
    Move to the next question in the questions list and get a new question if necessary.

    The function takes no parameters.

    Returns:
        None

    Raises:
        openai.error.AuthenticationError: If the OpenAI API key is invalid or missing.

    """
    # Move to the next question in the questions list
    st.session_state.current_question += 1

    # If we've reached the end of the questions list, get a new question
    if st.session_state.current_question > len(st.session_state.questions) - 1:
        try:
            next_question = get_quiz(
                "ai",
                st.secrets.openai.api_key,
            )
        except openai.error.AuthenticationError:
            st.session_state.current_question -= 1
            return
        st.session_state.questions.append(next_question)


def next_question_v2():
    # Move to the next question in the questions list
    st.session_state.current_question += 1

    try:
        quiz = load_quiz()
    except FileNotFoundError:
        st.error(
            "The file containing the pre-generated questions could not be loaded. "
            "Please check your data folder...",
        )
        return

    # If we've reached the end of the questions list, get a new question
    if st.session_state.current_question > len(st.session_state.questions) - 1:
        try:
            next_question = quiz[st.session_state.current_question]
            st.session_state.questions.append(next_question)
        except IndexError:
            return


# Define a function to go to the previous question
def prev_question():
    # Move to the previous question in the questions list
    if st.session_state.current_question > 0:
        st.session_state.current_question -= 1
        st.session_state.explanation = None
