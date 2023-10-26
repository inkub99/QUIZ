from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

from src.utils import config
from src.utils import constants

st.set_page_config(
    page_title=config.config()["app"]["page_title"],
    page_icon=config.config()["app"]["page_icon"],
)
st.title(config.config()["app"]["project"]["title"])


def read_markdown_file(markdown_file: str) -> str:
    return Path(markdown_file).read_text()


project_markdown = read_markdown_file(
    os.path.join(
        constants.ASSETS_FOLDER,
        "project.md",
    ),
)
st.markdown(project_markdown, unsafe_allow_html=True)
