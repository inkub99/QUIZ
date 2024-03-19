import streamlit as st
import os

from src.quiz.get_quiz_questions import load_quiz
from src.utils import config
import PyPDF2


def replace_text_in_pdf(pdf_path, old_text, new_text):

    reader = PyPDF2.PdfReader(pdf_path)
    writer = PyPDF2.PdfWriter()

    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text = page.extract_text()
        if old_text in text:
            text = text.replace(old_text, new_text)
            page.merge_page(PyPDF2.pdf.PageObject.create_text_object(text))
        writer.add_page(page)
    with open(pdf_path, "wb") as f:
        writer.write(f)


def display_question():
    # Pierwsze pytanie
    if len(st.session_state.questions) == 0:
        quiz = load_quiz()
        first_question = quiz[0]
        st.session_state.questions.append(first_question)

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

        def download_report():
            file_name = "PBC_certyfikat_wzor.pdf"
            #replace_text_in_pdf(file_name, "Jan Kowalski", st.session_state.name)
            if str(st.session_state.name).split(' ')[0][-1] == 'a' or str(st.session_state.name).split(' ')[0][-1] == 'A':
                #replace_text_in_pdf(file_name, "Ukończył", "Ukończyła")

            with open(file_name, "rb") as f:
                pdf_bytes = f.read()

            return pdf_bytes

        if st.session_state.right_answers > 3:
            st.download_button(
                label="Pobierz dyplom",
                data=download_report(),
                file_name="PBC_certyfikat.pdf",
                mime="application/pdf"
            )



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


def next_question():
    st.session_state.current_question += 1
    quiz = load_quiz()
    if st.session_state.current_question > len(st.session_state.questions) - 1:
        try:
            next_question = quiz[st.session_state.current_question]
            st.session_state.questions.append(next_question)
        except:
            pass
    


# Define a function to go to the previous question
def prev_question():
    if st.session_state.current_question > 0:
        st.session_state.current_question -= 1
        st.session_state.explanation = None
