import os

import streamlit as st

# And the root-level secrets are also accessible as environment variables:
TWELVE_USERNAME = st.secrets["TWELVE_USERNAME"]
TWELVE_PASSWORD = st.secrets["TWELVE_PASSWORD"]
TWELVE_API = st.secrets["TWELVE_API"]
TWELVE_BLOB = st.secrets["TWELVE_BLOB"]


# Root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

HOME_TEAM_COLOR = '#59B877'
AWAY_TEAM_COLOR  = '#FF4B4B'


def create_default_configs():
    st.set_page_config(
        page_title="Twelve Community Page",
        page_icon="data/img/light-logo-small.png",
        layout="wide",
        initial_sidebar_state="auto",

    )

    H1_CUSTOM_STYLE = """
            <style>
                #hammarby-analytics-hub {
                    font-family: "Montserrat", sans-serif;
                    color: #1F1F1F;
                    font-size: 36px;
                    font-weight: 600;
                }
            </style>
        """

    st.markdown(H1_CUSTOM_STYLE, unsafe_allow_html=True)

    HIDE_STREAMLIT_STYLE = """
            <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
            </style>
        """

    st.markdown(HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)

    DISABLE_TOOLBAR = """
            <style>
                div[data-testid="stToolbar"] { 
                    display: none;
                }
            </style>
        """

    st.markdown(DISABLE_TOOLBAR, unsafe_allow_html=True)

    st.markdown(
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600&display=swap');
    
            .css-vl8c1e {
                z-index:0
            }
        </style>
    """,
        unsafe_allow_html=True,
    )
