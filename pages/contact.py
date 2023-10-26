from __future__ import annotations

import os
import webbrowser
from pathlib import Path

import streamlit as st
from PIL import Image

from src.utils import config
from src.utils import constants

st.set_page_config(
    page_title=config.config()["app"]["page_title"],
    page_icon=config.config()["app"]["page_icon"],
)
st.title(config.config()["app"]["contact"]["title"])


CSS_FILE_PATH = Path(
    os.path.join(
        constants.STYLES_FOLDER,
        "main.css",
    ),
)
CV_FILE_PATH = Path(
    os.path.join(
        constants.ASSETS_FOLDER,
        "Kevin_Knights_CV.pdf",
    ),
)
PROFILE_PIC_PATH = Path(
    os.path.join(
        constants.ASSETS_FOLDER,
        "professional_cropped.jpeg",
    ),
)


# --- GENERAL SETTINGS ---
NAME = config.config()["app"]["contact"]["name"]
DESCRIPTION = config.config()["app"]["contact"]["description"]
EMAIL = config.config()["app"]["contact"]["email"]
SOCIAL_MEDIA = {
    "YouTube": config.config()["app"]["contact"]["youtube"],
    "LinkedIn": config.config()["app"]["contact"]["linkedin"],
    "GitHub": config.config()["app"]["contact"]["github"],
    "Twitter": config.config()["app"]["contact"]["twitter"],
}


# --- LOAD CSS, PDF & PROFIL PIC ---
with open(CSS_FILE_PATH) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
with open(CV_FILE_PATH, "rb") as pdf_file:
    pdf_byte = pdf_file.read()
profile_pic = Image.open(PROFILE_PIC_PATH)


# --- HERO SECTION ---
def open_webpage():
    url = config.config()["app"]["contact"]["linkedin"]
    webbrowser.open(url)


col1, col2 = st.columns(2, gap="small")
with col1:
    st.image(profile_pic, width=230)

with col2:
    st.title(NAME)
    st.write(DESCRIPTION)
    st.button(
        label=config.config()["app"]["contact"]["connect_label"],
        on_click=open_webpage,
    )
    st.write("📫", EMAIL)


# --- SOCIAL LINKS ---
st.write("\n")
cols = st.columns(len(SOCIAL_MEDIA))
for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    cols[index].write(f"[{platform}]({link})")
