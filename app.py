from __future__ import annotations
import streamlit as st
from src.streamlit import widgets
from src.utils import config

# Inicjalizacja zmiennych
if "current_question" not in st.session_state:
    st.session_state.answers = {}
    st.session_state.current_question = 0
    st.session_state.questions = []
    st.session_state.right_answers = 0
    st.session_state.wrong_answers = 0

# Tytuł
title = config.config()["app"]["title"]
st.markdown(f"<h1 style='margin-top: -70px; text-align: center;'>{title}</h1>", unsafe_allow_html=True)
st.markdown("\n\n".join(config.config()["app"]["onboarding"]))
#st.divider()

# Pytanie o imie
if "name" not in st.session_state:
    name = st.text_input("Podaj imię i nazwisko (na potrzeby przygotowania dyplomu)")
    if name:
        st.session_state.name = name

# 3 kolumny
col1, col2, col3 = st.columns([1, 6, 1])

# Poprzednie pytanie
with col1:
    if col1.button(config.config()["app"]["quiz"]["prev"]):
        widgets.prev_question()


# Nastepne pytanie
with col3:
    if col3.button(config.config()["app"]["quiz"]["next"]):
        widgets.next_question()

# Wyswietlanie pytania
with col2:
    widgets.display_question()